import { useMemo } from "react";
import { Stack, IconButton } from "@fluentui/react";
import DOMPurify from "dompurify";

import styles from "./Answer.module.css";

import { SearchResult } from "../../api";
import {SearchResultViewer} from "./SearchResultViewer";
import { parseSearchResultToHtml } from "./SearchResultParser";
import { SearchResultIcon } from "./SearchResultIcon";

interface Props {
    searchResults: SearchResult[];
    selectSearchResult: (index: number) => void;
}

export const SearchResultList = ({
    searchResults,
    selectSearchResult
}: Props) => {

    console.log("SearchResults: ", searchResults);

    return (
        <Stack>
            {searchResults.map((searchResult, index) => (
                <Stack.Item key={index}> 
                    <SearchResultViewer searchResult={searchResult} setThisSearchResult={()=>selectSearchResult(index)}/>
                </Stack.Item>
            ))}
        </Stack>
    );
};
