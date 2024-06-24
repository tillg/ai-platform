import { useRef, useState, useEffect } from "react";
import { Panel, DefaultButton, TextField, SpinButton, Slider, Checkbox } from "@fluentui/react";
import { BrainCircuitFilled, SparkleFilled } from "@fluentui/react-icons";
import {COLORS } from "../../constants";
import styles from "./Search.module.css";

import {
    searchApi,
    SearchRequest,
    SearchAppResponseOrError,
    SearchAppResponse,
    SearchResult
} from "../../api";
import { Answer, AnswerError, AnswerLoading } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";
import { SearchAnalysisPanel, SearchAnalysisPanelTabs } from "../../components/SearchAnalysisPanel";
import { SettingsButton } from "../../components/SettingsButton";
import { SearchResultList } from "../../components/SearchResult"

const Search = () => {
    const [isConfigPanelOpen, setIsConfigPanelOpen] = useState(false);
    const [promptTemplate, setPromptTemplate] = useState<string>("");
    const [temperature, setTemperature] = useState<number>(0.3);
    const [retrieveCount, setRetrieveCount] = useState<number>(3);
    const [useAdvancedFlow, setUseAdvancedFlow] = useState<boolean>(true);

    const lastQuestionRef = useRef<string>("");

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<unknown>();

    const [activeCitation, setActiveCitation] = useState<string>();
    const [activeAnalysisPanelTab, setActiveAnalysisPanelTab] = useState<SearchAnalysisPanelTabs | undefined>(undefined);

    const [selectedAnswer, setSelectedAnswer] = useState<number>(0);
    const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

    const makeSearchApiRequest = async (question: string) => {
        lastQuestionRef.current = question;

        error && setError(undefined);
        setIsLoading(true);
        setActiveCitation(undefined);
        setActiveAnalysisPanelTab(undefined);

        try {

            const request: SearchRequest = {
                search_term: question
            };
            const response = await searchApi(request);
            if (!response.body) {
                throw Error("No response body");
            }
            const parsedResponse: SearchAppResponseOrError = await response.json();
            if (response.status > 299 || !response.ok) {
                throw Error(parsedResponse.error || "Unknown error");
            }
            const newSearchResult: SearchResult = {
                searchTerm: question,
                searchAppResponse: parsedResponse as SearchAppResponse
            }
            setSearchResults([...searchResults, newSearchResult]);
        } catch (e) {
            setError(e);
        } finally {
            setIsLoading(false);
        }
    };


    const onPromptTemplateChange = (_ev?: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
        setPromptTemplate(newValue || "");
    };

    const onTemperatureChange = (
        newValue: number,
        range?: [number, number],
        event?: React.MouseEvent | React.TouchEvent | MouseEvent | TouchEvent | React.KeyboardEvent
    ) => {
        setTemperature(newValue);
    };

    const onRetrieveCountChange = (_ev?: React.SyntheticEvent<HTMLElement, Event>, newValue?: string) => {
        setRetrieveCount(parseInt(newValue || "3"));
    };

    const onUseAdvancedFlowChange = (_ev?: React.FormEvent<HTMLElement | HTMLInputElement>, checked?: boolean) => {
        setUseAdvancedFlow(!!checked);
    }


    const onShowCitation = (citation: string, index: number) => {
        if (activeCitation === citation && activeAnalysisPanelTab === SearchAnalysisPanelTabs.CitationTab && selectedAnswer === index) {
            setActiveAnalysisPanelTab(undefined);
        } else {
            setActiveCitation(citation);
            setActiveAnalysisPanelTab(SearchAnalysisPanelTabs.CitationTab);
        }

        setSelectedAnswer(index);
    };

    const onToggleTab = (tab: SearchAnalysisPanelTabs, index: number) => {
        if (activeAnalysisPanelTab === tab && selectedAnswer === index) {
            setActiveAnalysisPanelTab(undefined);
        } else {
            setActiveAnalysisPanelTab(tab);
        }

        setSelectedAnswer(index);
    };

    return (
        <div className={styles.container}>
            <div className={styles.commandsContainer}>
                <SettingsButton className={styles.commandButton} onClick={() => setIsConfigPanelOpen(!isConfigPanelOpen)} />
            </div>
            <div className={styles.chatRoot}>
                <div className={styles.chatContainer}>
                    {!lastQuestionRef.current ? (
                        <div className={styles.chatEmptyState}>
                            <BrainCircuitFilled fontSize={"120px"} primaryFill={COLORS.brandColor} aria-hidden="true" aria-label="AI logo" />
                            <h1 className={styles.chatEmptyStateTitle}>Search your Brain</h1>
                            <h2 className={styles.chatEmptyStateSubtitle}>Ask anything and see what I find...</h2>
                        </div>
                    ) : (
                        <div className={styles.chatMessageStream}>
                            <SearchResultList searchResults={searchResults} />
                        </div>
                    )}

                    <div className={styles.chatInput}>
                        <QuestionInput
                            clearOnSend
                            placeholder="Type a question and I will search..."
                            disabled={isLoading}
                            onSend={question => makeSearchApiRequest(question)}
                        />
                    </div>
                </div>

                <Panel
                    headerText="Configure answer generation"
                    isOpen={isConfigPanelOpen}
                    isBlocking={false}
                    onDismiss={() => setIsConfigPanelOpen(false)}
                    closeButtonAriaLabel="Close"
                    onRenderFooterContent={() => <DefaultButton onClick={() => setIsConfigPanelOpen(false)}>Close</DefaultButton>}
                    isFooterAtBottom={true}
                >

                    <Checkbox
                        className={styles.chatSettingsSeparator}
                        checked={useAdvancedFlow}
                        label="Use advanced flow with query rewriting and filter formulation. Not compatible with Ollama models."
                        onChange={onUseAdvancedFlowChange}
                    />

                    <h3>Settings for database search:</h3>

                    <SpinButton
                        className={styles.chatSettingsSeparator}
                        label="Retrieve this many matching rows:"
                        min={1}
                        max={50}
                        defaultValue={retrieveCount.toString()}
                        onChange={onRetrieveCountChange}
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

export default Search;
