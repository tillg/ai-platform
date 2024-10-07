
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

// @ts-ignore
import { useDbState, } from 'use-db-state';

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
    justify-content: space-between;
`;

const LeftContainer = styled.div`
  display: flex;
  gap: 10px;
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
    const [selectedChainName, setSelectedChainName] = useDbState('ChatChainPage.selectedChainName', undefined);
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
    }, []);

    // Config Pane
    const [isConfigurationOpen, setConfigurationOpen] = React.useState<boolean>(false);
    const showConfigurationWindow = async (): Promise<void> => {
        await fetchChains();
        setConfigurationOpen(true);
    };
    const closeConfigurationWindow = (): void => setConfigurationOpen(false);

    const setConfiguration = (config: Record<string, any>) => {
        console.log("Setting configuration: ", config);
        if (config.chain && config.chain !== undefined) {
            setSelectedChainName(config.chain);
        }
    };
    const handleSetConfiguration = (config: Record<string, any>) => {
        setConfiguration(config);
        closeConfigurationWindow();
    };

    // Chat history
    const [chatHistory, setChatHistory] = useDbState('ChatChainPage.chatHistory', []); // useState<Message[]>([]);

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

    const resetChatAndConfiguration = (): void => {
        setSelectedChainName(undefined)
        setChatHistory([])
    }

    return (
        <PageContainer>
            <Header>
                <LeftContainer>
                    <Button label="Settings" id={generateUid()} onClick={showConfigurationWindow} icon={<Icon>settings</Icon>} />
                    <Tag icon={<Icon>format_list_numbered</Icon>}> Chain: {selectedChainName}</Tag>
                </LeftContainer>
                <Button label="Reset Config & Chat" id={generateUid()} onClick={resetChatAndConfiguration} icon={<Icon>power_settings_new</Icon>} />
            </Header>
            {isConfigurationOpen && (
                <ModalOverlay closeOnOutsideClick={false} onClose={closeConfigurationWindow}>
                    <ActionContentbox
                        headingElements={<ContentBoxElements.Title ariaLevel={1} text="Settings" />}
                        headingButtons={<ContentBoxElements.CloseButton onClick={closeConfigurationWindow} />}
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


