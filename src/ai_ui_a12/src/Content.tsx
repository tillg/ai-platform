import React from "react";
import { ActionContentbox, ContentBoxElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/contentbox";

export interface ContentProps {
    title: string;
    text: string;
}

export function Content(props: ContentProps): React.ReactElement<ContentProps> {
    return (
        <ActionContentbox
            headingElements={<ContentBoxElements.Title text={props.title} />}
        >
            {props.text}
        </ActionContentbox>
    );
}
