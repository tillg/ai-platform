import { Chat, ChatProps } from "@com.mgmtp.a12.widgets/widgets-core";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { Message, hasInnerWorking } from "../api/apiModelsChat";
import { CollapsiblePanel } from "@com.mgmtp.a12.widgets/widgets-core/lib/collapsible-panel";
import { useState, useCallback, useEffect } from "react";
import { InnerWorkingPane } from "./InnerWorkingPane";
import { SplitView } from "@com.mgmtp.a12.widgets/widgets-core/lib/layout/split-view";
import Slider from '@mui/material/Slider';
import styled, { css, useTheme, ThemeContext } from 'styled-components';
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { Tooltip } from "@com.mgmtp.a12.widgets/widgets-core/lib/tooltip";

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
    & .MuiSlider-thumb {
        color: ${({ theme }) => theme.colors.divider.colorDark}; 
  }
  & .MuiSlider-track {
        color: ${({ theme }) => theme.colors.divider.colorDark}; 
    }; 
  }
  & .MuiSlider-rail {
    color: ${({ theme }) => {
        const color = theme.colors.divider.colorDark;
        const r = parseInt(color.slice(1, 3), 16);
        const g = parseInt(color.slice(3, 5), 16);
        const b = parseInt(color.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, 0.5)`;
    }};
  }

  }
`;

interface AssistantChatMessageGroupProps {
    message: Message;
}
export const AssistantChatMessageGroup: React.FC<AssistantChatMessageGroupProps> = ({ message }) => {
    const [open, setOpen] = useState(false);
    const toggleInnerWorkingPanel = useCallback(() => setOpen(!open), [open]);
    const [leftPanePercentage, setLeftPanePercentage] = useState<number>(50);

    function handleLeftPanePercentageChange(event: any, newValue: number | number[]) {
        setLeftPanePercentage(newValue as number);
    }

    return (
        <Chat.MessageGroup
            position={'left'}
        >
            <Chat.UserInfo userName={'Assistant'} />
            <StyledChatMessage>
                {message.inner_working && !open && (
                    <Tooltip text="Expand Inner Working">
                        <IconContainer open={open} onClick={toggleInnerWorkingPanel}>
                            <Icon style={{ color: '#D0D021' }}>tips_and_updates</Icon>
                        </IconContainer>
                    </Tooltip>)}
                {message.inner_working && open && (
                    <Tooltip text="Close Inner Working">
                        <IconContainer open={open} onClick={toggleInnerWorkingPanel}>
                            <Icon style={{ color: 'black' }}>lightbulb</Icon>
                        </IconContainer>
                    </Tooltip>)}
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