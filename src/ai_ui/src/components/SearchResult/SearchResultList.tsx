import { useMemo } from "react";
import { Stack, IconButton } from "@fluentui/react";
import DOMPurify from "dompurify";

import styles from "./Answer.module.css";

import { SearchResult } from "../../api";
import { parseSearchResultToHtml } from "./SearchResultParser";
import { SearchResultIcon } from "./SearchResultIcon";

interface Props {
    searchResults: SearchResult[];
}

export const SearchResultList = ({
    searchResults,
}: Props) => {

    return (
        <Stack>
            {searchResults.map((searchResult, index) => (
                <Stack.Item key={index}> 
                    {"Hello World"} 
                </Stack.Item>
            ))}
        </Stack>
    );
};
