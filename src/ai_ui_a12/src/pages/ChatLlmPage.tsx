
import * as React from "react";

import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { useRef, useState, useEffect } from "react";
import { chatApi, getModels } from "../api";
import { ActionContentbox, ContentBoxElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/contentbox";
import LlmConfigurationPane from "../components/LlmConfigurationPane";
import { ModalOverlay } from "@com.mgmtp.a12.widgets/widgets-core/lib/modal-overlay";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { Model } from "../api/apiModelsChat";

export const ChatLlmPage = () => {
    const [error, setError] = useState<unknown>();

    //Models
    const [availableModels, setAvailableModels] = useState<Model[]>([]);
    const [selectedModelName, setSelectedModelName] = useState<string>();
    const fetchModels = async () => {
        try {
            const models = await getModels(); // This returns an array of Models
            setAvailableModels(models);
        } catch (error) {
            console.error("Failed to fetch model names:", error);
            setError(error); // Assuming there's a setError function to handle errors
        }
    };
    useEffect(() => {
        fetchModels();
    }, []); // Empty dependency array means this effect runs once after the initial render

    // Temperature
    const [selectedTemp, setSelectedTemp] = useState<number>(0);

    // Config Pane
    const [isConfigurationOpen, setConfigurationOpen] = React.useState<boolean>(false);
    const showConfiguration = (): void => setConfigurationOpen(true);
    const closeConfiguration = (): void => setConfigurationOpen(false);

    const setConfiguration = (config: Record<string, any>) => {
        console.log("Setting configuration to ", config)
        if (config.model && config.model !== undefined) {
            console.log("Setting model to ", config.model)
            setSelectedModelName(config.model);
        }
        if (config.temperature && config.temperature !== undefined) {
            console.log("Setting temperature to ", config.temperature)
            setSelectedTemp(config.temperature);
        }
    };
    const handleSetConfiguration = (config: Record<string, any>) => {
        setConfiguration(config);
        closeConfiguration();
    };


    return (
        <div>
            <Button label="Settings" id={generateUid()} onClick={showConfiguration} icon={<Icon>settings</Icon>} />
            {isConfigurationOpen && (
                < ModalOverlay closeOnOutsideClick={false} onClose={closeConfiguration}>
                    <ActionContentbox
                        headingElements={<ContentBoxElements.Title ariaLevel={1} text="Settings" />}
                        headingButtons={<ContentBoxElements.CloseButton onClick={closeConfiguration} />}
                    >
                        <LlmConfigurationPane llmModels={availableModels} llmConfiguration={{ model: selectedModelName, temperature: selectedTemp }} setConfiguration={handleSetConfiguration}/>                    
                    </ActionContentbox>
                </ModalOverlay >
            )
            }

            <p>Here goes the chat</p>

        </div>)
}


