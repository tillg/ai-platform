import { Chat } from "@com.mgmtp.a12.widgets/widgets-core";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { useState, useCallback } from "react";
import { InnerWorkingPane } from "./InnerWorkingPane";
import { SplitView } from "@com.mgmtp.a12.widgets/widgets-core/lib/layout/split-view";
import Slider from '@mui/material/Slider';
import styled, { css } from 'styled-components';
import { Tooltip } from "@com.mgmtp.a12.widgets/widgets-core/lib/tooltip";
import { Chunk, SearchResult } from "../api/apiModelsSearch";
import { List } from "@com.mgmtp.a12.widgets/widgets-core/lib/list";
import { ChunkPane } from "./ChunkPane";

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

interface SearchResultMessageGroupProps {
    searchResult: SearchResult;
}


function chunksPane(chunks: Chunk[]) {
    return (
        <List border divider>

            {chunks.map((chunk, index) => (
                <List.Item key={index} text={<ChunkPane chunk={chunk} />} />
            ))}
        </List>
    )
}
export const SearchResultMessageGroup: React.FC<SearchResultMessageGroupProps> = ({ searchResult }) => {
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
                {searchResult.inner_working && !open && (
                    <Tooltip text="Expand Inner Working">
                        <IconContainer open={open} onClick={toggleInnerWorkingPanel}>
                            <Icon style={{ color: '#D0D021' }}>tips_and_updates</Icon>
                        </IconContainer>
                    </Tooltip>)}
                {searchResult.inner_working && open && (
                    <Tooltip text="Close Inner Working">
                        <IconContainer open={open} onClick={toggleInnerWorkingPanel}>
                            <Icon style={{ color: 'black' }}>lightbulb</Icon>
                        </IconContainer>
                    </Tooltip>)}
                {open && (
                    <StyledSlider value={leftPanePercentage} onChange={handleLeftPanePercentageChange} />
                )}
                <SplitView >
                    <SplitView.Area width={open ? leftPanePercentage + "%" : "100%"}>{chunksPane(searchResult.result?.chunks ?? [])}</SplitView.Area>

                    {searchResult.inner_working && open && (
                        <SplitView.Area width={(100 - leftPanePercentage) + "%"}>
                            <InnerWorkingPane innerWorking={searchResult.inner_working} />
                        </SplitView.Area>
                    )}
                </SplitView>
            </StyledChatMessage>
        </Chat.MessageGroup>
    )
}