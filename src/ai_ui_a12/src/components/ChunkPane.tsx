import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { CollapsiblePanel, CollapsiblePanelElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/collapsible-panel";
import { useState, useCallback } from "react";
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