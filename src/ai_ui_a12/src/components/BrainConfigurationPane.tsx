import React from 'react';
import { Select } from "@com.mgmtp.a12.widgets/widgets-core/lib/input/select";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";
import { Slider } from "@com.mgmtp.a12.widgets/widgets-core/lib/experimental/input/slider/main/slider.view";
import { Model } from "../api/apiModelsChat";

const BrainConfigurationPane = ({
    brains,
    brainConfiguration,
    setConfiguration
}: {
    brains: string[];
    brainConfiguration: Record<string, any>;
    setConfiguration: (config: Record<string, any>) => void;
}) => {

    const originalBrain = brainConfiguration?.brain;

    // Brains
    const [selectedBrain, setSelectedBrain] = React.useState<undefined | string>(undefined);


    return (
        <div>
            <Select
                id="select-simple"
                placeholder="Please choose..."
                label="Brain"
                labelGraphic={<Icon>psychology</Icon>}
                items={brains?.map(brain => ({ value: brain, label: brain })) ?? []}
                onValueChanged={setSelectedBrain}
                value={selectedBrain || originalBrain}            />
            <br />
            <br />
            <Button label="Save" primary id={generateUid()} icon={<Icon>save</Icon>} onClick={() => {
                    setConfiguration({ brain: selectedBrain })
            }} />
        </div>
    );
};

export default BrainConfigurationPane;