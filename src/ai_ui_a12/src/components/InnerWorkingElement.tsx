// import { useContext } from "react";
// import { Tag } from "@com.mgmtp.a12.widgets/widgets-core/lib/tag";
// import { ThemeContext } from 'styled-components';
import { InnerWorkingTag } from "./InnerWorkingTag";
import { InnerWorkingSubPane } from "./InnerWorkingSubPane";
import { InnerWorkingSubPaneChunks } from "./InnerWorkingSubPaneChunks";

export const InnerWorkingElement = ({ keyName, value }: { keyName: string, value: any }) => {
    // const tagColor = useContext(ThemeContext).colors.primary;

    if (value === null) {
        return null;// <Tag color={tagColor}> {keyName}: null</Tag>;
    }
    if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
        return <InnerWorkingTag keyName={keyName} value={value} />;
    }
    if (typeof value === 'object') {
        if (keyName==="chunks") {
            return (<InnerWorkingSubPaneChunks title={keyName} subInnerWorking={value} />)
        }
        return (
            <InnerWorkingSubPane title={keyName} subInnerWorking={value}/>
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

