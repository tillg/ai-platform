import {  useState } from "react";
import { IconButton } from '@fluentui/react/lib/Button';
import { UserChatMessage } from "../UserChatMessage";
import styled from 'styled-components';


import { SearchResult } from "../../api";
import { ChunkViewer } from "./ChunkViewer";

interface Props {
    searchResult: SearchResult;
    setThisSearchResult: () => void;
}


const StyledAnswerContainer = styled.div`
    padding: 20px;
    background: rgb(249, 249, 249);
    border-radius: 8px;
    box-shadow:
        0px 2px 4px rgba(0, 0, 0, 0.14),
        0px 0px 2px rgba(0, 0, 0, 0.12);
    outline: transparent solid 1px;
}
`;


export const SearchResultViewer = ({
    searchResult, setThisSearchResult
}: Props) => {
    console.log("SearchResultViewer: ", searchResult)
    const searchTerm = searchResult?.search_term ?? 'No search term.';
    const [isChunksVisible, setIsChunksVisible] = useState(true); // State to manage chunks visibility

    // Toggle function for chunks visibility
    const toggleChunksVisibility = () => {
        setIsChunksVisible(!isChunksVisible);
    };

    return (
        <StyledAnswerContainer>
                <UserChatMessage>
                    {searchTerm}
                    <IconButton
                        style={{ color: "black" }}
                        iconProps={{ iconName: "Lightbulb" }}
                        title="Show inner workings"
                        ariaLabel="Show inner workings"
                        onClick={() => { setThisSearchResult() }}
                        disabled={!searchResult.inner_working}
                    />
                    <IconButton
                        style={{
                            color: "black",
                            border: '1px solid #ccc', // Add a border
                        }}
                        iconProps={{ iconName: isChunksVisible ? 'ChevronUp' : 'ChevronDown' }}
                        title="Open/close list of chunks"
                        ariaLabel="Open/close list of chunks"
                        onClick={() => { toggleChunksVisibility() }}
                    />

                </UserChatMessage>

                {/* Iterate over the chunks array and display each chunk */}
                {isChunksVisible && searchResult.result?.chunks?.map((chunk, index) => (
                    <div key={index} > 
                        <ChunkViewer chunk={chunk} />
                    </div>))}

                {/* Existing content */}
        </StyledAnswerContainer>
    )
}
