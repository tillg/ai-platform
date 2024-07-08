
import styles from "./AnalysisPanel.module.css";

import { SearchResult } from "../../api";

import { AnalysisPanel } from "../AnalysisPanel/AnalysisPanel";
import { Pill } from "../AnalysisPanel/Pill";

interface Props {
    searchResult: SearchResult;
    closePanel: () => void;
}

export const SearchAnalysisPanel = ({ searchResult, closePanel }: Props) => {
    return (
        <AnalysisPanel>
            <div className={styles.closeButtonContainer}>
                <button onClick={closePanel} className={styles.closeButton}>X</button>
            </div>
            <p>Search Analysis</p>
            <p>Search Term: {searchResult.search_term}</p>
            <div >
                {searchResult.inner_working &&
                    (Object.keys(searchResult.inner_working) || []).map((k: any, ind) => (
                        <Pill key={ind}>
                            {k}: {JSON.stringify(searchResult.inner_working?.[k])}
                        </Pill>
                    ))}
            </div>
        </AnalysisPanel>
    );
};