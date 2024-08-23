import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";

import { useContext } from "react";
import { Tag } from "@com.mgmtp.a12.widgets/widgets-core/lib/tag";
import { ThemeContext } from 'styled-components';

interface Props {
    innerWorking: { [key: string]: any };
}
const useCustomTheme = () => {
    return useContext(ThemeContext);
};

const TagComponent = ({ keyName, value }: { keyName: string, value: any }) => {
    const theme = useCustomTheme();
    const tagColor = theme.colors.primary;

    // Function to render value based on its type
    const renderValue = (value: any) => {
        if (typeof value === 'string') {
            // Handle boolean type
            return value
        }
        if (typeof value === 'object' && value !== null) {
            // Handle object type
            return (
                <div>
                    {Object.entries(value).map(([subKey, subValue]) => (
                        <div key={subKey}>
                            <TagComponent key={subKey} keyName={subKey} value={subValue} />
                        </div>
                    ))}
                </div>
            );
        } else {
            let value_str: string;
            try {
                value_str = value.toString();
            } catch (error) {
                console.error("Error converting value to string:", error);
                value_str = "Invalid value";
            }
            return value_str;
        }
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
    return (
        <Tag color={tagColor}>  {keyName}: {renderValue(value)}</Tag>
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