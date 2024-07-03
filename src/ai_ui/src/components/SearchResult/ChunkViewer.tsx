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
    const [isDetailsVisible, setDetailsVisible] = useState(false);

    const toggleContentVisibility = () => setContentVisible(!isContentVisible);
    const toggleDetailsVisibility = () => setDetailsVisible(!isDetailsVisible);

    // Extract the domain from the URI and construct the favicon URL
    const faviconUrl = useMemo(() => {
        try {
            const url = new URL(chunk.uri);
            return `${url.protocol}//${url.hostname}/favicon.ico`;
        } catch (error) {
            console.error("Error constructing favicon URL:", error);
            return ''; // Return an empty string if the URL is invalid
        }
    }, [chunk.uri]);

    return (
        <div style={{ border: '1px solid #ccc', padding: '20px', margin: '10px', borderRadius: '5px' }}>
            <Stack horizontal tokens={{ childrenGap: 10 }}>
                <a href={chunk.uri} target="_blank" rel="noopener noreferrer">
                    {faviconUrl && <img src={faviconUrl} alt="Favicon" style={{ width: '16px', height: '16px', marginRight: '8px' }} />}
                    <strong>{chunk.title}</strong>
                </a>

                <button onClick={toggleDetailsVisibility}>
                    {isDetailsVisible ? 'Hide Details' : 'Show Details'}
                </button>
                <button onClick={toggleContentVisibility}>
                    {isContentVisible ? 'Hide Content' : 'Show Content'}
                </button>
            </Stack>
            {isDetailsVisible && (
                <div style={{ lineHeight: '0.5' }}>
                    <p>ID: {chunk.id}</p>
                    <p>Original Document ID: {chunk.original_document_id}</p>
                    <p>Distance: {chunk.search_info?.distance ?? 'Not available'}</p>
                </div>
            )}
            {isContentVisible && (
                <div>
                    <p>{chunk.content}</p>
                </div>
            )}
        </div>
    );
};
