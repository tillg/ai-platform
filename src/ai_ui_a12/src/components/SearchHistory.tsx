import { Chat, ChatProps } from "@com.mgmtp.a12.widgets/widgets-core";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { Message, hasInnerWorking } from "../api/apiModelsChat";
import { CollapsiblePanel } from "@com.mgmtp.a12.widgets/widgets-core/lib/collapsible-panel";
import { useState, useCallback } from "react";
import { InnerWorkingPane } from "./InnerWorkingPane";
import { SplitView } from "@com.mgmtp.a12.widgets/widgets-core/lib/layout/split-view";
import Slider from '@mui/material/Slider';
import styled from 'styled-components';
import { AssistantChatMessageGroup } from "./AssistantChatMessageGroup";
import { SearchRequest, SearchResult, SearchHistoryItem } from "../api";
import { SearchResultMessageGroup } from "./SearchResultMessageGroup";

interface Props {
    searchHistory: SearchHistoryItem[];
}

function searchRequestPane(searchRequest: SearchRequest) {
    return (
        <Chat.MessageGroup 
            position={'right'}>
            <Chat.UserInfo userName={"User"} />
            <Chat.Message>
                {searchRequest.search_term}
            </Chat.Message>
        </Chat.MessageGroup>
    )
}

export const SearchHistory = ({ searchHistory }: Props) => {
    return (
        <Chat.Container>
            {searchHistory.map((searchHistoryEntry, index) => (
                <div key={index}>
                    {(searchHistoryEntry instanceof SearchRequest)
                        ? searchRequestPane(searchHistoryEntry)
                        : <SearchResultMessageGroup searchResult={searchHistoryEntry} />}
                </div>
            ))}
        </Chat.Container>
    )
}