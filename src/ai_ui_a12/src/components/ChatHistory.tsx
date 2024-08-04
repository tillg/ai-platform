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

interface Props {
    chatHistory: Message[];
}

function userChatMessageGroup(message: Message) {
    return (
        <Chat.MessageGroup 
            position={'right'}>
            <Chat.UserInfo userName={"User"} />
            <Chat.Message>
                {message.content}
            </Chat.Message>
        </Chat.MessageGroup>
    )
}

export const ChatHistory = ({ chatHistory }: Props) => {
    return (
        <Chat.Container>
            {chatHistory.map((message, index) => (
                <div key={index}>
                {(message.role == 'user')
                    ? userChatMessageGroup(message)
                        : <AssistantChatMessageGroup message={message} />}
                </div>
            ))}
        </Chat.Container>
    )
}