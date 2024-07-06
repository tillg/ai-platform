import { useRef, useState, useEffect } from "react";
import { Panel, DefaultButton, TextField, SpinButton, Slider, Checkbox } from "@fluentui/react";
import { BrainIcon

 } from "../../components/Icons/BrainIcon";
import styles from "./Search.module.css";

import {
    searchApi,
    SearchRequest,
    SearchResult
} from "../../api";
import { QuestionInput } from "../../components/QuestionInput";
import { SearchAnalysisPanel } from "../../components/SearchAnalysisPanel";
import { SettingsButton } from "../../components/SettingsButton";
import { SearchResultList } from "../../components/SearchResult"

const Search = () => {
    const [isConfigPanelOpen, setIsConfigPanelOpen] = useState(false);
    const [isSearchAnalysisOpen, setIsSearchAnalysisOpen] = useState(false);
    const [retrieveCount, setRetrieveCount] = useState<number>(3);

    const lastQuestionRef = useRef<string>("");

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<unknown>();


    const [selectedSearchResult, _setSelectedSearchResult] = useState<number>(0);
    // Wrapper function
    const setSelectedSearchResult = (value: number) => {
        console.log(`setSelectedSearchResult called with value: ${value}`);
        _setSelectedSearchResult(value);
        setIsSearchAnalysisOpen(true);
    };

    const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

    const makeSearchApiRequest = async (question: string) => {
        lastQuestionRef.current = question;

        error && setError(undefined);
        setIsLoading(true);

        try {

            const request: SearchRequest = {
                search_term: question
            };
            const response = await searchApi(request);
            if (!response.body) {
                throw Error("No response body");
            }
            const newSearchResult: SearchResult = await response.json();
            if (response.status > 299 || !response.ok) {
                throw Error("Unknown error");
            }
            setSearchResults([...searchResults, newSearchResult]);
        } catch (e) {
            setError(e);
        } finally {
            setIsLoading(false);
        }
    };


    const onRetrieveCountChange = (_ev?: React.SyntheticEvent<HTMLElement, Event>, newValue?: string) => {
        setRetrieveCount(parseInt(newValue || "3"));
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
                            <BrainIcon fontSize={"120px"}  />
                            <h1 className={styles.chatEmptyStateTitle}>Search your Brain</h1>
                            <h2 className={styles.chatEmptyStateSubtitle}>Ask anything and see what I find...</h2>
                        </div>
                    ) : (
                            <div style={{ display: 'flex', width: '100%' }}>
                                <div style={{ flex: isSearchAnalysisOpen ? 1 : 'auto', width: isSearchAnalysisOpen ? undefined : '100%' }}>
                                    <div className={styles.chatMessageStream}>
                                        <SearchResultList searchResults={searchResults} selectSearchResult={setSelectedSearchResult} />
                                    </div>
                                </div>
                                {isSearchAnalysisOpen && (
                                    <div style={{ flex: 1 }} className={styles.chatAnalysisPanel}>
                                        <SearchAnalysisPanel searchResult={searchResults[selectedSearchResult]} closePanel={function (): void {
                                            setIsSearchAnalysisOpen(false);
                                        } } />
                                    </div>
                                )}
                            </div>
                    )}

                    <div className={styles.chatInput}>
                        <QuestionInput
                            clearOnSend
                            placeholder="Give me something to search for..."
                            disabled={isLoading}
                            onSend={question => makeSearchApiRequest(question)}
                        />
                    </div>
                </div>

                <Panel
                    headerText="Configure search settings"
                    isOpen={isConfigPanelOpen}
                    isBlocking={false}
                    onDismiss={() => setIsConfigPanelOpen(false)}
                    closeButtonAriaLabel="Close"
                    onRenderFooterContent={() => <DefaultButton onClick={() => setIsConfigPanelOpen(false)}>Close</DefaultButton>}
                    isFooterAtBottom={true}
                >
                    <h3>Search Server Settings</h3>
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
                        defaultValue="Huhu"
                        label="Override prompt template"
                        multiline
                        autoAdjustHeight
                    />

                    <Slider
                        className={styles.chatSettingsSeparator}
                        label="Temperature"
                        min={0}
                        max={1}
                        step={0.1}
                        showValue
                        snapToStep
                    />

                </Panel>
            </div>
        </div>
    );
};

export default Search;
