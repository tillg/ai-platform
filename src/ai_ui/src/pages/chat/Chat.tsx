import { useRef, useState, useEffect } from "react";
import { Panel, DefaultButton, TextField, SpinButton, Slider, Checkbox, Dropdown } from "@fluentui/react";
import styles from "./Chat.module.css";
import EmptyChat from "./EmptyChat"

import { chatApi, getModels } from "../../api";
import {
    ChatRequest,
    ChatResponse,
    Message, messageOrChatResponseToMessage, MessageOrChatResponse, isChatResponse
} from "../../api/apiModelsChat";
import { ChatResponseViewer, ChatResponseError, ChatResponseLoading } from "../../components/ChatResponseViewer";
import { QuestionInput } from "../../components/QuestionInput";
import { UserChatMessage } from "../../components/UserChatMessage";
import { ChatAnalysisPanel, AnalysisPanelTabs } from "../../components/ChatAnalysisPanel";
import { SettingsButton } from "../../components/SettingsButton";
import { ClearChatButton } from "../../components/ClearChatButton";

const Chat = () => {
    const [isConfigPanelOpen, setIsConfigPanelOpen] = useState(false);
    const [promptTemplate, setPromptTemplate] = useState<string>("");
    const [temperature, setTemperature] = useState<number>(0.3);
    const [retrieveCount, setRetrieveCount] = useState<number>(3);
    const [useAdvancedFlow, setUseAdvancedFlow] = useState<boolean>(true);

    const lastQuestionRef = useRef<string>("");

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<unknown>();

    const messagesEndRef = useRef<HTMLDivElement>(null);

    const [activeCitation, setActiveCitation] = useState<string>();
    const [activeAnalysisPanelTab, setActiveAnalysisPanelTab] = useState<AnalysisPanelTabs | undefined>(undefined);

    const [selectedAnswer, setSelectedAnswer] = useState<number>(0);

    const [selectedModel, setSelectedModel] = useState<string>("");
    const [availableModels, setAvailableModels] = useState<string[]>([]);
    const fetchModelNames = async () => {
        try {
            const models = await getModels();
            // Assuming the response is an array of strings
            setAvailableModels(models);
        } catch (error) {
            console.error("Failed to fetch model names:", error);
            setError(error);
        }
    };

    // Use useEffect to call the async function after component mounts
    useEffect(() => {
        fetchModelNames();
    }, []); // Empty dependency array means this effect runs once after the initial render


    // Keep track of our dialogue
    const [messageOrChatResponses, setMessageOrChatResponses] = useState<MessageOrChatResponse[]>([]);

    const makeApiRequest = async (question: string) => {
        lastQuestionRef.current = question;

        error && setError(undefined);
        setIsLoading(true);
        setActiveCitation(undefined);
        setActiveAnalysisPanelTab(undefined);

        // Add the new question to our chat history
        const newMessageOrChatResponses = [...messageOrChatResponses, { content: question, role: 'user' } as Message];
        setMessageOrChatResponses(newMessageOrChatResponses);
        console.log("Chat history after adding", newMessageOrChatResponses);

        const messages: Message[] = newMessageOrChatResponses.map(item => {
            return messageOrChatResponseToMessage(item);
        });


        try {
            const request: ChatRequest = {
                messages: messages,
                model: selectedModel,
            };
            const response = await chatApi(request);
            setMessageOrChatResponses(prevMessages => [
                ...prevMessages,
                response as ChatResponse
            ]);

        } catch (e) {
            setError(e);
        } finally {
            setIsLoading(false);
        }
    };

    const clearChat = () => {
        lastQuestionRef.current = "";
        error && setError(undefined);
        setActiveCitation(undefined);
        setActiveAnalysisPanelTab(undefined);
        setMessageOrChatResponses([]);
        setIsLoading(false);
    };


    const onPromptTemplateChange = (_ev?: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
        setPromptTemplate(newValue || "");
    };

    const onSelectedModelChange = (_ev?: React.FormEvent<HTMLInputElement>, newValue?: any) => {
        console.log("Selected model", newValue);
        console.log("Type of newValue:", typeof newValue);
        setSelectedModel(newValue.key || "");
    };

    const onTemperatureChange = (
        newValue: number,
        range?: [number, number],
        event?: React.MouseEvent | React.TouchEvent | MouseEvent | TouchEvent | React.KeyboardEvent
    ) => {
        setTemperature(newValue);
    };


    const onExampleClicked = (example: string) => {
        makeApiRequest(example);
    };


    const onToggleTab = (tab: AnalysisPanelTabs, index: number) => {
        if (activeAnalysisPanelTab === tab && selectedAnswer === index) {
            setActiveAnalysisPanelTab(undefined);
        } else {
            setActiveAnalysisPanelTab(tab);
        }

        setSelectedAnswer(index);
    };

    // Scroll to the bottom of the list whenever the messages update
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messageOrChatResponses]);

    return (
        <div className={styles.container}>
            <div className={styles.commandsContainer}>
                <ClearChatButton className={styles.commandButton} onClick={clearChat} disabled={!lastQuestionRef.current || isLoading} />
                <SettingsButton className={styles.commandButton} onClick={() => setIsConfigPanelOpen(!isConfigPanelOpen)} />
            </div>
            <div className={styles.chatRoot}>
                <div className={styles.chatContainer}>
                    {!lastQuestionRef.current ? (
                        <EmptyChat onClick={onExampleClicked} />
                    ) : (
                        <div className={styles.chatMessageStream}>
                            {messageOrChatResponses.map((messageOrChatResponse, index) => (
                                <div key={index}>
                                    {!isChatResponse(messageOrChatResponse) ? (
                                        <UserChatMessage>{messageOrChatResponse.content}</UserChatMessage>
                                    ) : (
                                        <div className={styles.chatMessageGpt}>
                                            <ChatResponseViewer
                                                isStreaming={false}
                                                key={index}
                                                answer={messageOrChatResponse.content}
                                                isSelected={selectedAnswer === index && activeAnalysisPanelTab !== undefined}
                                                onThoughtProcessClicked={() => onToggleTab(AnalysisPanelTabs.ThoughtProcessTab, index)}
                                                onSupportingContentClicked={() => onToggleTab(AnalysisPanelTabs.SupportingContentTab, index)}
                                                onFollowupQuestionClicked={q => makeApiRequest(q)}
                                            />
                                        </div>
                                    )}
                                </div>
                            ))}
                            {isLoading && (
                                <>
                                    <div className={styles.chatMessageGptMinWidth}>
                                        <ChatResponseLoading />
                                    </div>
                                </>
                            )}
                            {error ? (
                                <div className={styles.chatMessageGptMinWidth}>
                                    <ChatResponseError error={error.toString()} onRetry={() => makeApiRequest(lastQuestionRef.current)} />
                                </div>
                            ) : null}
                            <div ref={messagesEndRef} />
                        </div>

                    )}

                    <div className={styles.chatInput}>
                        <QuestionInput
                            clearOnSend
                            placeholder="Type a new question"
                            disabled={isLoading}
                            onSend={question => makeApiRequest(question)}
                        />
                    </div>
                </div>

                {messageOrChatResponses.length > 0 && activeAnalysisPanelTab && (
                    <ChatAnalysisPanel
                        className={styles.chatAnalysisPanel}
                        activeCitation={activeCitation}
                        onActiveTabChanged={x => onToggleTab(x, selectedAnswer)}
                        citationHeight="810px"
                        answer={messageOrChatResponses[selectedAnswer]}
                        activeTab={activeAnalysisPanelTab}
                    />
                )}

                <Panel
                    headerText="Configure answer generation"
                    isOpen={isConfigPanelOpen}
                    isBlocking={false}
                    onDismiss={() => setIsConfigPanelOpen(false)}
                    closeButtonAriaLabel="Close"
                    onRenderFooterContent={() => <DefaultButton onClick={() => setIsConfigPanelOpen(false)}>Close</DefaultButton>}
                    isFooterAtBottom={true}
                >
                    <Dropdown
                        label="Select a model"
                        placeholder="Choose a model"
                        options={availableModels.map(model => ({ key: model, text: model }))}
                        onChange={onSelectedModelChange}

                    />

                    <Checkbox
                        className={styles.chatSettingsSeparator}
                        checked={useAdvancedFlow}
                        label="Use advanced flow with query rewriting and filter formulation. Not compatible with Ollama models."
                    />

                    <h3>Settings for database search:</h3>

                    <SpinButton
                        className={styles.chatSettingsSeparator}
                        label="Retrieve this many matching rows:"
                        min={1}
                        max={50}
                        defaultValue={retrieveCount.toString()}
                    />


                    <h3>Settings for final chat completion:</h3>

                    <TextField
                        className={styles.chatSettingsSeparator}
                        defaultValue={promptTemplate}
                        label="Override prompt template"
                        multiline
                        autoAdjustHeight
                        onChange={onPromptTemplateChange}
                    />

                    <Slider
                        className={styles.chatSettingsSeparator}
                        label="Temperature"
                        min={0}
                        max={1}
                        step={0.1}
                        defaultValue={temperature}
                        onChange={onTemperatureChange}
                        showValue
                        snapToStep
                    />

                </Panel>
            </div>
        </div>
    );
};

export default Chat;
