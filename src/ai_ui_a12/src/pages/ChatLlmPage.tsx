
import * as React from "react";

import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { useRef, useState, useEffect } from "react";
import { chatApi, getModels } from "../api";
import { SplitView } from "@com.mgmtp.a12.widgets/widgets-core/lib/layout/split-view";
import { ActionContentbox, ContentBoxElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/contentbox";
import  LlmSelectionPane  from "../components/LlmSelectionPane";

export const ChatLlmPage = () => {
    const [error, setError] = useState<unknown>();

    const [availableModels, setAvailableModels] = useState<string[]>([]);
    const [selectedModel, setSelectedModel] = useState<string>("");
    const fetchModelNames = async () => {
        try {
            const models = await getModels();
            // Assuming the response is an array of strings
            setAvailableModels(models);
        } catch (error) {
            console.error("Failed to fetch model names:", error);
            setError(error);
        }
    };
    const [openConfigArea, setOpenConfigArea] = React.useState(true);
    const toggleContentArea = React.useCallback(() => {
        setOpenConfigArea((prevState) => !prevState);

    }, []);

    return (
        <div>
            <SplitView>
                <SplitView.Area>
                    <p>Here goes the chat</p>
                </SplitView.Area>
                {openConfigArea && (
                    <SplitView.Area>
                        <ActionContentbox
                            headingElements={<ContentBoxElements.Title ariaLevel={2} text="Config" />}
                            headingButtons={
                                <ContentBoxElements.HeadingActionButton
                                    icon={<Icon>close</Icon>}
                                    onClick={toggleContentArea}
                                    title="Close Config"
                                />
                            }>
                        </ActionContentbox>
                        <LlmSelectionPane/>.
                    </SplitView.Area>
                )}
            </SplitView>
        </div>)
}


