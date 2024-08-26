import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { CssEllipsis } from "@com.mgmtp.a12.widgets/widgets-core/lib/css-ellipsis";
import { useContext } from "react";
import { Tag } from "@com.mgmtp.a12.widgets/widgets-core/lib/tag";
import { ThemeContext } from 'styled-components';


const useCustomTheme = () => {
    return useContext(ThemeContext);
};

export const InnerWorkingTag = ({ keyName, value }: { keyName: string, value: any }) => {
    const theme = useCustomTheme();
    const tagColor = theme.colors.primary;

    // Function to render value based on its type
    const renderValue = (value: any) => {
        if (typeof value === 'string') {
            return value.trim()
        }
        let value_str: string;
        try {
            value_str = value.toString();
        } catch (error) {
            console.error("Error converting value to string:", error);
            value_str = "Invalid value";
        }
        return value_str;

    };
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
    if (keyName.includes("chain")) {
        return (
            <Tag color={tagColor} icon={<Icon>format_list_numbered</Icon>}> {keyName}: {value} </Tag>
        );
    }
    if (keyName.includes("search")) {
        return (
            <Tag color={tagColor} icon={<Icon>search</Icon>}> {keyName}: {value} </Tag>
        );
    }
    if (keyName.includes("prompt")) {
        return (
            <Tag color={tagColor} icon={<Icon>question_answer</Icon>}> {keyName}: 
                <CssEllipsis maxLine={2} useTooltip>
                    {value.trim()}
                </CssEllipsis> 
            </Tag>
        );
    }
    if (keyName.includes("no_of")) {
        return (
            <Tag color={tagColor} icon={<Icon>tag</Icon>}> {keyName}: {value} </Tag>
        );
    }
    return (
        <Tag color={tagColor}>  {keyName}: {renderValue(value)}</Tag>
    );
};
