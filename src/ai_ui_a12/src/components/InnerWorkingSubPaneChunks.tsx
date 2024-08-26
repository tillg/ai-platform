
import { CollapsiblePanel } from "@com.mgmtp.a12.widgets/widgets-core/lib/collapsible-panel";
import * as React from "react";
import { ChunkPane } from "./ChunkPane";
import styled from "styled-components";
import { Chunk } from "../api";

interface Props {
    title: string;
    subInnerWorking: { [key: string]: any };
}


const IndentedDiv = styled.div`
    padding-left: 20px;
`;

const obj2Chunk = (obj: Object): Chunk => {
    return obj as Chunk;
}

export const InnerWorkingSubPaneChunks = ({ title, subInnerWorking }: Props): React.ReactElement => {
    const [open, setOpen] = React.useState(false);
    const setOpenWithLog = (openOrNot: boolean): void => {
        console.log(`CollapsiblePanel ${title} is now ${openOrNot ? 'open' : 'closed'}`);
        setOpen(openOrNot);
    }
    const toggleCollapsiblePanel = React.useCallback(() => setOpenWithLog(!open), [open]);

    const paneTitle = "Chunks "
    return (
        <CollapsiblePanel title={paneTitle} onClick={toggleCollapsiblePanel} >
            {open && (
                <IndentedDiv>
                    {Object.entries(subInnerWorking).map(([key, value]) => (
                        <ChunkPane chunk={obj2Chunk(value)} />
                    ))}
                </IndentedDiv>
            )}
        </CollapsiblePanel>
    );
};