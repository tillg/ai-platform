import { Chat, ChatProps } from "@com.mgmtp.a12.widgets/widgets-core";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { Message, hasInnerWorking } from "../api/apiModelsChat";
import { CollapsiblePanel, CollapsiblePanelElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/collapsible-panel";
import { useState, useCallback, useEffect, useContext } from "react";
import { InnerWorkingPane } from "./InnerWorkingPane";
import { SplitView } from "@com.mgmtp.a12.widgets/widgets-core/lib/layout/split-view";
import Slider from '@mui/material/Slider';
import styled, { css, useTheme, ThemeContext } from 'styled-components';
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { Tooltip } from "@com.mgmtp.a12.widgets/widgets-core/lib/tooltip";
import { Chunk } from "../api";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";

interface ChunkPaneProps {
    chunk: Chunk;
}
export const ChunkPane: React.FC<ChunkPaneProps> = ({ chunk }) => {
    const [open, setOpen] = useState(false);
    const toggleCollapsiblePanel = useCallback(() => setOpen(!open), [open]);
    const isInFlatTheme = true;

    return (
        < CollapsiblePanel
            title={chunk.title}
            onClick={toggleCollapsiblePanel}
            info="Chunk" 
            addons={
                <>
                    <CollapsiblePanelElements.Addon>
                        <Button
                            icon={<Icon>launch</Icon>}
                            title="Open page in new tab"
                            invert={!isInFlatTheme}
                            onClick={() => window.open(chunk.uri, '_blank')}
                        />
                    </CollapsiblePanelElements.Addon>
                </>
            }>
            {open && <p>{chunk.content}</p>}
        </CollapsiblePanel >
    );
}