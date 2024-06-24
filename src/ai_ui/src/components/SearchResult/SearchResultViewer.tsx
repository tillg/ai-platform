import { useMemo } from "react";
import { Stack, IconButton } from "@fluentui/react";
import DOMPurify from "dompurify";

import styles from "./Answer.module.css";

import { SearchResult } from "../../api";
import { parseSearchResultToHtml } from "./SearchResultParser";
import { SearchResultIcon } from "./SearchResultIcon";

interface Props {
    searchResult: SearchResult;
}

export const SearchResultViewer = ({
    searchResult,
}: Props) => {
    const searchTerm = searchResult.searchTerm;
    //const parsedAnswer = useMemo(() => parseSearchResultToHtml(messageContent,  onCitationClicked), [searchResult]);

    //const sanitizedAnswerHtml = DOMPurify.sanitize(parsedAnswer.answerHtml);

    return (
        <div>
            <div>
                Search Term: {searchTerm}
            </div>)

            <Stack className={styles.answerContainer} verticalAlign="space-between">
                <Stack.Item>
                    <Stack horizontal horizontalAlign="space-between">
                        <SearchResultIcon />
                        <div>
                            <IconButton
                                style={{ color: "black" }}
                                iconProps={{ iconName: "Lightbulb" }}
                                title="Show thought process"
                                ariaLabel="Show thought process"
                                // onClick={() => onThoughtProcessClicked()}
                                // disabled={!searchResult.choices[0].context.thoughts?.length}
                            />
                            <IconButton
                                style={{ color: "black" }}
                                iconProps={{ iconName: "ClipboardList" }}
                                title="Show supporting content"
                                ariaLabel="Show supporting content"
                                // onClick={() => onSupportingContentClicked()}
                                // disabled={!searchResult.choices[0].context.data_points}
                            />
                        </div>
                    </Stack>
                </Stack.Item>

                {/* <Stack.Item grow>
                    <div className={styles.answerText} dangerouslySetInnerHTML={{ __html: sanitizedAnswerHtml }}></div>
                </Stack.Item>

                {!!parsedAnswer.citations.length && (
                    <Stack.Item>
                        <Stack horizontal wrap tokens={{ childrenGap: 5 }}>
                            <span className={styles.citationLearnMore}>Citations:</span>
                            {parsedAnswer.citations.map((x, i) => {
                                return (
                                    <a key={i} className={styles.citation} title={x}>
                                        {`${++i}. ${x}`}
                                    </a>
                                );
                            })}
                        </Stack>
                    </Stack.Item>
                )}

                {!!followupQuestions?.length && showFollowupQuestions && onFollowupQuestionClicked && (
                    <Stack.Item>
                        <Stack horizontal wrap className={`${!!parsedAnswer.citations.length ? styles.followupQuestionsList : ""}`} tokens={{ childrenGap: 6 }}>
                            <span className={styles.followupQuestionLearnMore}>Follow-up questions:</span>
                            {followupQuestions.map((x, i) => {
                                return (
                                    <a key={i} className={styles.followupQuestion} title={x} onClick={() => onFollowupQuestionClicked(x)}>
                                        {`${x}`}
                                    </a>
                                );
                            })}
                        </Stack>
                    </Stack.Item> */}
                {/* )} */}
            </Stack>
        </div>
    )
}