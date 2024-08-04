import { Chat, ChatProps } from "@com.mgmtp.a12.widgets/widgets-core";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { Message, hasInnerWorking } from "../api/apiModelsChat";
import { CollapsiblePanel } from "@com.mgmtp.a12.widgets/widgets-core/lib/collapsible-panel";
import { useState, useCallback, useContext } from "react";
import { Tag, TagGroup } from "@com.mgmtp.a12.widgets/widgets-core/lib/tag";
import styled, { useTheme, ThemeContext } from 'styled-components';

interface Props {
    innerWorking: { [key: string]: any };
}
const useCustomTheme = () => {
    return useContext(ThemeContext);
};

const TagComponent = ({ keyName, value }: { keyName: string, value: any }) => {
    const theme = useCustomTheme();
    const tagColor = theme.colors.primary;
    if (keyName == "model") {
        return (
            <Tag color={tagColor} icon={<Icon>psychology</Icon>}> LLM: {value}</Tag>
        );
    }
    if (keyName.includes("duration")) {
        return (
            <Tag color={tagColor} icon={<Icon>timer</Icon>}> {keyName}: {new Intl.NumberFormat('en-US', { style: 'decimal', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format((value as number) / 1000000)} ms</Tag>
        );  
    }
    if (keyName.includes("count")) {
        return (
            <Tag color={tagColor} icon={<Icon>tag</Icon>}> {keyName}: {value} </Tag>
        );
    }
    if (keyName == "temperature") {
        return (
            <Tag color={tagColor} icon={<Icon>thermostat</Icon>}> Temperature: {value}</Tag>
        );
    }
    return (
        <Tag color={tagColor}>  {keyName}: {value}</Tag>
    );
};

export const InnerWorkingPane = ({ innerWorking }: Props) => {
    return (
        <div>
            {Object.entries(innerWorking).map(([key, value]) => (
                <TagComponent key={key} keyName={key} value={value} />
            ))}
        </div>
    );
};