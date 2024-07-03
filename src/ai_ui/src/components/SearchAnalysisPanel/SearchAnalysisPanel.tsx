import { Stack, Pivot, PivotItem } from "@fluentui/react";

import styles from "./AnalysisPanel.module.css";

import { SupportingContent } from "../SupportingContent";
import { ChatAppResponse, SearchResult } from "../../api";
import { SearchAnalysisPanelTabs } from "./SearchAnalysisPanelTabs";
import { SearchThoughtProcess } from "./SearchThoughtProcess";
import { MarkdownViewer } from "../MarkdownViewer";
import { useState, useEffect } from "react";

interface Props {
    searchResult: SearchResult;
    closePanel: () => void;
}

export const SearchAnalysisPanel = ({ searchResult, closePanel }: Props) => {
    return (
        <div className={styles.thoughtProcess}>
            <div className={styles.closeButtonContainer}>
                <button onClick={closePanel} className={styles.closeButton}>X</button>
            </div>
            <p>Search Analysis</p>
            <p>Search Term: {searchResult.search_term}</p>
        </div>
    );
};