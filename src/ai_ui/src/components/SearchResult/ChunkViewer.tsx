import { useMemo } from "react";
import styled from 'styled-components';
import React, { useState } from 'react';

import { SearchResult, Chunk } from "../../api";
import { HorizontalStack } from "../Stack";

interface Props {
    chunk: Chunk;
}
const StyledChunkContainer = styled.div`
    border-top: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
`;

const StyledChunkDetails = styled.div`
    line-height: 1
`

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
        <StyledChunkContainer>
            <HorizontalStack >
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
            </HorizontalStack>
            {isDetailsVisible && (
                <StyledChunkDetails >
                    <p>ID: {chunk.id}</p>
                    <p>Original Document ID: {chunk.original_document_id}</p>
                    <p>Distance: {chunk.search_info?.distance ?? 'Not available'}</p>
                </StyledChunkDetails>
            )}
            {isContentVisible && (
                <StyledChunkDetails>
                    <p>{chunk.content}</p>
                </StyledChunkDetails>
            )}
        </StyledChunkContainer>
    );
};