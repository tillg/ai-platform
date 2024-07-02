import { useMemo } from "react";
import { Stack, IconButton } from "@fluentui/react";
import DOMPurify from "dompurify";
import React, { useState } from 'react';

import styles from "./Answer.module.css";

import { SearchResult, Chunk } from "../../api";
import { parseSearchResultToHtml } from "./SearchResultParser";
import { SearchResultIcon } from "./SearchResultIcon";

interface Props {
    chunk: Chunk;
}

export const ChunkViewer = ({ chunk }: Props) => {
    const [isContentVisible, setContentVisible] = useState(false);

    const toggleContentVisibility = () => setContentVisible(!isContentVisible);

    return (
        <div style={{ border: '1px solid #ccc', padding: '20px', margin: '10px', borderRadius: '5px' }}>
            <strong>{chunk.title}</strong>
            <div>
                <p>URI: {chunk.uri}</p>
                <p>ID: {chunk.id}</p>
                <p>Original Document ID: {chunk.original_document_id}</p>
                <p>Search Term: {chunk.search_info.search_term}</p>
                <p>Distance: {chunk.search_info.distance}</p>
            </div>
            <button onClick={toggleContentVisibility}>
                {isContentVisible ? 'Hide Content' : 'Show Content'}
            </button>
            {isContentVisible && (
                <div>
                    <p>{chunk.content}</p>
                </div>
            )}
        </div>
    );
};
