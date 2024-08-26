
import { InnerWorkingElement } from "./InnerWorkingElement";
import { CollapsiblePanel } from "@com.mgmtp.a12.widgets/widgets-core/lib/collapsible-panel";
import * as React from "react";
import styled from "styled-components";

interface Props {
    title: string;
    subInnerWorking: { [key: string]: any };
}
const IndentedDiv = styled.div`
    padding-left: 20px;
`;

export const sortEntriesByType = (entries: [string, any][]): [string, any][] => {
    return entries.sort(([keyA, valueA], [keyB, valueB]) => {
        const isStringA = typeof valueA === 'string';
        const isStringB = typeof valueB === 'string';
        if (isStringA && !isStringB) return -1;
        if (!isStringA && isStringB) return 1;
        return 0;
    });
};

export const InnerWorkingSubPane = ({ title, subInnerWorking }: Props): React.ReactElement => {
    const [open, setOpen] = React.useState(false);
    const setOpenWithLog = (openOrNot: boolean): void => {
        console.log(`CollapsiblePanel ${title} is now ${openOrNot ? 'open' : 'closed'}`);
        setOpen(openOrNot);
    }
    const toggleCollapsiblePanel = React.useCallback(() => setOpenWithLog(!open), [open]);

    return (
        <CollapsiblePanel title={title} onClick={toggleCollapsiblePanel} >
            {open && (
                <IndentedDiv>
                    {sortEntriesByType(Object.entries(subInnerWorking)).map(([key, value]) => (
                        <InnerWorkingElement key={key} keyName={key} value={value} />
                    ))}
                </IndentedDiv>
            )}
        </CollapsiblePanel>
    );
};