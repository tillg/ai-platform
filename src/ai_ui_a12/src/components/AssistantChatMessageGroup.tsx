import { Chat, ChatProps } from "@com.mgmtp.a12.widgets/widgets-core";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { Message, hasInnerWorking } from "../api/apiModelsChat";
import { CollapsiblePanel } from "@com.mgmtp.a12.widgets/widgets-core/lib/collapsible-panel";
import { useState, useCallback, useEffect } from "react";
import { InnerWorkingPane } from "./InnerWorkingPane";
import { SplitView } from "@com.mgmtp.a12.widgets/widgets-core/lib/layout/split-view";
import Slider from '@mui/material/Slider';
import styled, { css } from 'styled-components';
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";

const IconContainer = styled.div<{ open: boolean }>`
    position: absolute;
    top: -20px;
    right: 0;
    cursor: pointer;
    z-index: 10;
    svg {
        font-size: 50px; /* Increase the size of the icon */
        transition: box-shadow 0.3s ease;
        ${({ open }) => open && css`
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* Add shadow when toggled */
        `}
    }
`;
const StyledChatMessage = styled(Chat.Message)`
    position: relative;
`;
const StyledSlider = styled(Slider)`
    position: relative;
    top: -15px; 
`;

interface AssistantChatMessageGroupProps {
    message: Message;
}
export const AssistantChatMessageGroup: React.FC<AssistantChatMessageGroupProps> = ({ message }) => {
    const [open, setOpen] = useState(false);
    const toggleInnerWorkingPanel = useCallback(() => setOpen(!open), [open]);
    const [leftPanePercentage, setLeftPanePercentage] = useState<number>(50);
   
    function handleLeftPanePercentageChange(event: any, newValue: number | number[]) {
        console.log("ChatHistory: handleLeftPanePercentageChange: newValue: ", newValue);
        setLeftPanePercentage(newValue as number);
    }
    console.log("AssistantChatMessageGroup: open: ", open);

    return (
        <Chat.MessageGroup
            position={'left'}
        >
            <Chat.UserInfo userName={'Assistant'} />
            <StyledChatMessage>
                {message.inner_working && !open && (
                    <IconContainer open={open} onClick={toggleInnerWorkingPanel}>
                        <Icon style={{ color: '#D0D021' }}>tips_and_updates</Icon>
                    </IconContainer>)}
                {message.inner_working && open && (
                    <IconContainer open={open} onClick={toggleInnerWorkingPanel}>
                        <Icon style={{ color: 'black' }}>lightbulb</Icon>
                    </IconContainer>)}
                {open && (
                    <StyledSlider value={leftPanePercentage} onChange={handleLeftPanePercentageChange} />
                )}
                <SplitView >
                    <SplitView.Area width={open ? leftPanePercentage + "%" : "100%"}>{message.content}</SplitView.Area>

                    {message.inner_working && open && (
                        <SplitView.Area width={(100 - leftPanePercentage) + "%"}>
                            <InnerWorkingPane innerWorking={message.inner_working} />
                        </SplitView.Area>
                    )}
                </SplitView>
            </StyledChatMessage>
        </Chat.MessageGroup>
    )
}