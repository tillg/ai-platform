import { useMemo } from "react";
import { Stack, IconButton } from "@fluentui/react";
import DOMPurify from "dompurify";

import styles from "./Answer.module.css";

import { SearchResult } from "../../api";
import { SearchResultIcon } from "./SearchResultIcon";
import { ChunkViewer } from "./ChunkViewer";

interface Props {
    searchResult: SearchResult;
}

export const SearchResultViewer = ({
    searchResult,
}: Props) => {
    console.log("SearchResultViewer: ", searchResult)
    const searchTerm = searchResult?.search_term ?? 'No search term.';    

    return (
        <div>
            <div>
                Search Term: {searchTerm}
            </div>

            <Stack className={styles.answerContainer} verticalAlign="space-between">
                {/* Existing content */}

                {/* Iterate over the chunks array and display each chunk */}
                {searchResult.result?.chunks?.map((chunk, index) => (
                    <ChunkViewer key={index} chunk={chunk} />
                ))}

                {/* Existing content */}
            </Stack>
        </div>
    )
}