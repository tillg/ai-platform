
import * as React from "react";

import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { useRef, useState, useEffect, useCallback } from "react";
import { chainApi, getChains } from "../api";
import { ActionContentbox, ContentBoxElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/contentbox";
import ChainConfigurationPane from "../components/ChainConfigurationPane";
import { ModalOverlay } from "@com.mgmtp.a12.widgets/widgets-core/lib/modal-overlay";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { Message, ChatRequest } from "../api/apiModelsChat";
import { Tag } from "@com.mgmtp.a12.widgets/widgets-core/lib/tag";
import { UserInput } from "../components/UserInput";
import { ChatHistory } from "../components/ChatHistory";
import styled from "styled-components";

// Styled components
const PageContainer = styled.div`
    display: flex;
    flex-direction: column;
    height: 100vh;
`;
const Header = styled.div`
    display: flex;
    align-items: center;
    gap: 10px;
    position: sticky;
    top: 0;
    background-color: #e2e6e9;
    z-index: 1;
    padding: 5px;
`;

const Content = styled.div`
    flex: 1;
    overflow-y: auto;
`;

const StickyInput = styled.div`
    position: sticky;
    bottom: 0;
    background-color: white;
    padding: 10px;
    z-index: 1;
`;

export const ChatChainPage = () => {
    const userInputRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        if (userInputRef.current) {
            userInputRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, []);


    //Chains
    const [availableChains, setAvailableChains] = useState<string[]>([]);
    const [selectedChainName, setSelectedChainName] = useState<string>();
    const fetchChains = async () => {
        try {
            const chains = await getChains(); 
            setAvailableChains(chains);
        } catch (error) {
            console.error("Failed to fetch model names:", error);
        }
    };
    useEffect(() => {
        fetchChains();
    }, []); // Empty dependency array means this effect runs once after the initial render

    const initiateSelectedChain = useCallback(async () => {
        if (selectedChainName === undefined) {
            const defaultChain = "default";
            console.log("Default chain: ", defaultChain)
            setSelectedChainName(defaultChain);
        }
    }, [selectedChainName])
    useEffect(() => {
        initiateSelectedChain();
    }, [initiateSelectedChain]); 

    // Config Pane
    const [isConfigurationOpen, setConfigurationOpen] = React.useState<boolean>(false);
    const showConfiguration = (): void => setConfigurationOpen(true);
    const closeConfiguration = (): void => setConfigurationOpen(false);

    const setConfiguration = (config: Record<string, any>) => {
        if (config.chain && config.chain !== undefined) {
            setSelectedChainName(config.chain);
        }
    };
    const handleSetConfiguration = (config: Record<string, any>) => {
        setConfiguration(config);
        closeConfiguration();
    };

    // Chat history
    const [chatHistory, setChatHistory] = useState<Message[]>([]);

    // User Questions
    const sendQuestion = (question: string) => {
        const newMessage: Message = { content: question, role: "user" };
        const newChatHistory = [...chatHistory, newMessage]
        setChatHistory(newChatHistory);
        const chatRequest: ChatRequest = { messages: newChatHistory, chain: selectedChainName };
        chainApi(chatRequest)
            .then((response) => {
                console.log("Got response: ", response)
                setChatHistory([...newChatHistory, response]);
            })
            .catch((error) => {
                console.error("Failed to send question:", error);
            });
    }

    return (
        <PageContainer>
            <Header>
                <Button label="Settings" id={generateUid()} onClick={showConfiguration} icon={<Icon>settings</Icon>} />
                <Tag icon={<Icon>chain</Icon>}> Chain: {selectedChainName}</Tag>
            </Header>
            {isConfigurationOpen && (
                <ModalOverlay closeOnOutsideClick={false} onClose={closeConfiguration}>
                    <ActionContentbox
                        headingElements={<ContentBoxElements.Title ariaLevel={1} text="Settings" />}
                        headingButtons={<ContentBoxElements.CloseButton onClick={closeConfiguration} />}
                    >
                        <ChainConfigurationPane chains={availableChains} chainConfiguration={{ chain: selectedChainName }} setConfiguration={handleSetConfiguration} />
                    </ActionContentbox>
                </ModalOverlay>
            )}
            <Content>
                <ChatHistory chatHistory={chatHistory} />
            </Content>
            <StickyInput ref={userInputRef}>
                <UserInput onSend={sendQuestion} disabled={false} clearOnSend={true} placeholder="Who was Einstein?" />
            </StickyInput>
        </PageContainer>
    );
}

