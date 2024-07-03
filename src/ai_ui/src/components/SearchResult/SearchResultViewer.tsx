import { useMemo, useState } from "react";
import { Stack } from "@fluentui/react";
import { IconButton } from '@fluentui/react/lib/Button';

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
    const [isChunksVisible, setIsChunksVisible] = useState(true); // State to manage chunks visibility

    // Toggle function for chunks visibility
    const toggleChunksVisibility = () => {
        setIsChunksVisible(!isChunksVisible);
    };

    return (
        <div>
            <Stack className={styles.answerContainer} verticalAlign="space-between">
                <div style={{ position: 'relative', marginTop: '20px' }}>
                    <div style={{
                        position: 'absolute',
                        top: '0',
                        left: '20px',
                        background: 'rgb(249, 249, 249)',
                        padding: '0 5px',
                        fontWeight: 'bold'
                    }}>
                        Search Term
                    </div>
                    <div style={{
                        border: '1px solid #ccc',
                        padding: '20px',
                        margin: '10px',
                        borderRadius: '5px',
                        display: 'flex', // Use flexbox to align items
                        justifyContent: 'space-between', // This will push your icon to the right
                        alignItems: 'center' // This will vertically center the items
                    }}>
                        {searchTerm}
                        <div> {/* This div wraps the IconButton and allows for alignment */}
                            <IconButton
                                style={{ color: "black" }}
                                iconProps={{ iconName: "Lightbulb" }}
                                title="Show inner workings"
                                ariaLabel="Show inner workings"
                            // onClick={() => onThoughtProcessClicked()}
                            // disabled={!answer.choices[0].context.thoughts?.length}
                            />
                        </div>
                        {/* Toggle button for showing/hiding chunks */}
                        <IconButton
                            style={{
                                color: "black",
                                position: 'absolute',
                                right: '5px',
                                bottom: '-7px',
                                border: '1px solid #ccc', // Add a border
                                borderRadius: '50%', // Optional: to make it circular
                                padding: '5px', // Optional: to add some space between the icon and the border
                                background: 'rgb(249, 249, 249)',
                            }}
                            iconProps={{ iconName: isChunksVisible ? 'ChevronUp' : 'ChevronDown' }}
                            title="Open/close list of chunks"
                            ariaLabel="Open/close list of chunks"
                            onClick={() => { toggleChunksVisibility() }}
                        />

                    </div>
                </div>

                {/* Iterate over the chunks array and display each chunk */}
                {isChunksVisible && searchResult.result?.chunks?.map((chunk, index) => (
                    <div key={index} style={{ marginLeft: '20px' }}> {/* Add a left margin */}
                        <ChunkViewer chunk={chunk} />
                    </div>))}

                {/* Existing content */}
            </Stack>
        </div>
    )
}