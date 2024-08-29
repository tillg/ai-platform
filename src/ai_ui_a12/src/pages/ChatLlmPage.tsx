
import * as React from "react";

import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { useRef, useState, useEffect } from "react";
import { chatApi, getModels, getDefaultModel } from "../api";
import { ActionContentbox, ContentBoxElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/contentbox";
import LlmConfigurationPane from "../components/LlmConfigurationPane";
import { ModalOverlay } from "@com.mgmtp.a12.widgets/widgets-core/lib/modal-overlay";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { Model, Message, ChatRequest } from "../api/apiModelsChat";
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
    justify-content: space-between
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

export const ChatLlmPage = () => {
    const userInputRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        if (userInputRef.current) {
            userInputRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, []);


    //Models
    const [availableModels, setAvailableModels] = useState<Model[]>([]);
    const [selectedModelName, setSelectedModelName] = useDbState("ChatLlmPage.selectedModelName", undefined);
    const fetchModels = async () => {
        try {
            const models = await getModels(); // This returns an array of Models
            setAvailableModels(models);
        } catch (error) {
            console.error("Failed to fetch model names:", error);
        }
    };
    useEffect(() => {
        fetchModels();
    }, []); // Empty dependency array means this effect runs once after the initial render
    const initiateSelectedModel = async () => {
        if (selectedModelName === undefined) {
            const defaultModel = await getDefaultModel();
            console.log("Default model: ", defaultModel)
            if (defaultModel) {
                setSelectedModelName(defaultModel.name);
            } else {
                console.error("Failed to fetch default model.");
            }
        }
    }
    useEffect(() => {
        initiateSelectedModel();
    }, []);

    // Temperature
    const [selectedTemp, setSelectedTemp] = useDbState("ChatLlmPage.setSelectedTemp", undefined);

    // Config Pane
    const [isConfigurationOpen, setConfigurationOpen] = React.useState<boolean>(false);
    const showConfiguration = (): void => setConfigurationOpen(true);
    const closeConfiguration = (): void => setConfigurationOpen(false);

    const setConfiguration = (config: Record<string, any>) => {
        if (config.model && config.model !== undefined) {
            setSelectedModelName(config.model);
        }
        if (config.temperature && config.temperature !== undefined) {
            console.log("Setting temperature to ", config.temperature)
            setSelectedTemp(config.temperature);
        }
    };
    const handleSetConfiguration = (config: Record<string, any>) => {
        setConfiguration(config);
        closeConfiguration();
    };

    // Chat history
    const [chatHistory, setChatHistory] = useDbState("ChatLlmPage.chatHistory", []);

    // User Questions
    const sendQuestion = (question: string) => {
        const newMessage: Message = { content: question, role: "user" };
        const newChatHistory = [...chatHistory, newMessage]
        setChatHistory(newChatHistory);
        const chatRequestOptions = { temperature: selectedTemp };
        const chatRequest: ChatRequest = { messages: newChatHistory, model: selectedModelName, options: chatRequestOptions };
        chatApi(chatRequest)
            .then((response) => {
                console.log("Got response: ", response)
                setChatHistory([...newChatHistory, response]);
            })
            .catch((error) => {
                console.error("Failed to send question:", error);
            });
    }

    const resetChatAndConfiguration = (): void => {
        setSelectedModelName(undefined)
        setSelectedTemp(undefined)
        setChatHistory([])
    }

    return (
        <PageContainer>
            <Header>
                <LeftContainer>
                    <Button label="Settings" id={generateUid()} onClick={showConfiguration} icon={<Icon>settings</Icon>} />
                    <Tag icon={<Icon>psychology</Icon>}> LLM: {selectedModelName}</Tag>
                    <Tag icon={<Icon>thermostat</Icon>}> Temperature: {selectedTemp}</Tag>
                </LeftContainer>
                <Button label="Reset Config & Chat" id={generateUid()} onClick={resetChatAndConfiguration} icon={<Icon>power_settings_new</Icon>} />
            </Header>
            {isConfigurationOpen && (
                <ModalOverlay closeOnOutsideClick={false} onClose={closeConfiguration}>
                    <ActionContentbox
                        headingElements={<ContentBoxElements.Title ariaLevel={1} text="Settings" />}
                        headingButtons={<ContentBoxElements.CloseButton onClick={closeConfiguration} />}
                    >
                        <LlmConfigurationPane llmModels={availableModels} llmConfiguration={{ model: selectedModelName, temperature: selectedTemp }} setConfiguration={handleSetConfiguration} />
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


