import { Chat, ChatProps } from "@com.mgmtp.a12.widgets/widgets-core";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { Message, hasInnerWorking } from "../api/apiModelsChat";
import { CollapsiblePanel } from "@com.mgmtp.a12.widgets/widgets-core/lib/collapsible-panel";
import { useState, useCallback } from "react";
import { Tag, TagGroup } from "@com.mgmtp.a12.widgets/widgets-core/lib/tag";

interface Props {
    innerWorking: { [key: string]: any };
}

export const InnerWorkingPane = ({ innerWorking }: Props) => {
    console.log("InnerWorkingPane: innerWorking: ", innerWorking);

    return (
        <div>
            {Object.entries(innerWorking).map(([key, value]) => {
                switch (key) {
                    case "model":
                        return (
                            <Tag icon={<Icon>psychology</Icon>}> LLM: {value}</Tag>
                        );
                    case "total_duration":
                        return (
                            <Tag icon={<Icon>timer</Icon>}> Total duration: {new Intl.NumberFormat('en-US', { style: 'decimal', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format((value as number) / 1000000)} ms</Tag>
                        );
                    default:
                        return (
                            <Tag>  {key}: {value}</Tag>
                        );
                }
            })}
        </div>
    );
};