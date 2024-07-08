

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
        <div>
            {searchResults.map((searchResult, index) => (
                <div key={index}> 
                    <SearchResultViewer searchResult={searchResult} setThisSearchResult={()=>selectSearchResult(index)}/>
                </div>
            ))}
        </div>
    );
};
