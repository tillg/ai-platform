import React from 'react';
import { Select } from "@com.mgmtp.a12.widgets/widgets-core/lib/input/select";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";
import { Slider } from "@com.mgmtp.a12.widgets/widgets-core/lib/experimental/input/slider/main/slider.view";
import { Model } from "../api/apiModelsChat";

const LlmConfigurationPane = ({
    llmModels,
    llmConfiguration,
    setConfiguration
}: {
    llmModels: Model[];
    llmConfiguration: Record<string, any>;
    setConfiguration: (config: Record<string, any>) => void;
}) => {

    const originalModel = llmConfiguration?.model;

    // Models
    const [selectedModel, setSelectedModel] = React.useState<undefined | string>(undefined);


    // Temperature
    const TEMP_MARKS = [
        { label: "0", value: "0" },
        { label: "0.5", value: "0.5" },
        { label: "1", value: "1" },
        { label: "1.5", value: "1.5" },
        { label: "2", value: "2" },
    ];
    function findClosestTempValue(number: number) {
        let closestValue = TEMP_MARKS[0].value;
        let smallestDifference = Math.abs(number - parseFloat(TEMP_MARKS[0].value));

        for (const mark of TEMP_MARKS) {
            const difference = Math.abs(number - parseFloat(mark.value));
            if (difference < smallestDifference) {
                closestValue = mark.value;
                smallestDifference = difference;
            }
        }

        return closestValue;
    }
    const originalTemp = llmConfiguration?.temperature ?? 0;
    const originalTempValue = findClosestTempValue(originalTemp);
    const [selectedTempValue, setSelectedTempValue] = React.useState<string>(originalTempValue);

    return (
        <div>
            <Select
                id="select-simple"
                placeholder="Please choose..."
                label="LLM"
                labelGraphic={<Icon>psychology</Icon>}
                items={llmModels?.map(llm => ({ value: llm.name, label: llm.name })) ?? []}
                onValueChanged={setSelectedModel}
                value={selectedModel || originalModel}            />
            <br />
            <Slider
                id="simple-slider"
                marks={TEMP_MARKS}
                value={selectedTempValue}
                onChange={setSelectedTempValue}
                label="Temperature"
                leftLabel="Serious"
                rightLabel="Crazyyy"
            />
            <br />
            <br />
            <Button label="Save" primary id={generateUid()} icon={<Icon>save</Icon>} onClick={() => {
                    setConfiguration({ model: selectedModel ,temperature: parseFloat(selectedTempValue)})
                
            }} />
        </div>
    );
};

export default LlmConfigurationPane;