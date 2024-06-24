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

export const ChunkResultViewer = ({ chunk }: Props) => {
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
//     return (
//         <Stack className={`${styles.answerContainer} ${isSelected && styles.selected}`} verticalAlign="space-between">
//             <Stack.Item>
//                 <Stack horizontal horizontalAlign="space-between">
//                     <SearchResultIcon />
//                     <div>
//                         <IconButton
//                             style={{ color: "black" }}
//                             iconProps={{ iconName: "Lightbulb" }}
//                             title="Show thought process"
//                             ariaLabel="Show thought process"
//                             onClick={() => onThoughtProcessClicked()}
//                             disabled={!searchResult.choices[0].context.thoughts?.length}
//                         />
//                         <IconButton
//                             style={{ color: "black" }}
//                             iconProps={{ iconName: "ClipboardList" }}
//                             title="Show supporting content"
//                             ariaLabel="Show supporting content"
//                             onClick={() => onSupportingContentClicked()}
//                             disabled={!searchResult.choices[0].context.data_points}
//                         />
//                     </div>
//                 </Stack>
//             </Stack.Item>

//             <Stack.Item grow>
//                 <div className={styles.answerText} dangerouslySetInnerHTML={{ __html: sanitizedAnswerHtml }}></div>
//             </Stack.Item>

//             {!!parsedAnswer.citations.length && (
//                 <Stack.Item>
//                     <Stack horizontal wrap tokens={{ childrenGap: 5 }}>
//                         <span className={styles.citationLearnMore}>Citations:</span>
//                         {parsedAnswer.citations.map((x, i) => {
//                             return (
//                                 <a key={i} className={styles.citation} title={x}>
//                                     {`${++i}. ${x}`}
//                                 </a>
//                             );
//                         })}
//                     </Stack>
//                 </Stack.Item>
//             )}

//             {!!followupQuestions?.length && showFollowupQuestions && onFollowupQuestionClicked && (
//                 <Stack.Item>
//                     <Stack horizontal wrap className={`${!!parsedAnswer.citations.length ? styles.followupQuestionsList : ""}`} tokens={{ childrenGap: 6 }}>
//                         <span className={styles.followupQuestionLearnMore}>Follow-up questions:</span>
//                         {followupQuestions.map((x, i) => {
//                             return (
//                                 <a key={i} className={styles.followupQuestion} title={x} onClick={() => onFollowupQuestionClicked(x)}>
//                                     {`${x}`}
//                                 </a>
//                             );
//                         })}
//                     </Stack>
//                 </Stack.Item>
//             )}
//         </Stack>
//     );
};
