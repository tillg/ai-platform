import { useRef, useState, useEffect } from "react";
import { Panel, DefaultButton, TextField, SpinButton, Slider, Checkbox } from "@fluentui/react";
import styles from "./Search.module.css";
import { PromptsIcon } from "../../components/Icons/PromptsIcon";

import {
    searchApi,
    SearchRequest,
    SearchResult
} from "../../api";

const Prompts = () => {
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

    return (
        <div className={styles.container}>
            <div className={styles.chatRoot}>
                <div className={styles.chatContainer}>
                    <div className={styles.chatEmptyState}>
                        <PromptsIcon fontSize={"120px"} />
                        <h1 className={styles.chatEmptyStateTitle}>Fiddle around with prompts</h1>
                        <h2 className={styles.chatEmptyStateSubtitle}>&gt;_ Write, test, tune...</h2>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Prompts;
