import { Stack, IconButton } from "@fluentui/react";


import { SearchResult } from "../../api";
import {SearchResultViewer} from "./SearchResultViewer";

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
