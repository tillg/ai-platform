import React from 'react';
import { Select } from "@com.mgmtp.a12.widgets/widgets-core/lib/input/select";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";
import {BrainModel } from "../api";

const BrainConfigurationPane = ({
    brains,
    brainConfiguration,
    setConfiguration
}: {
    brains: BrainModel[];
    brainConfiguration: Record<string, any>;
    setConfiguration: (config: Record<string, any>) => void;
}) => {
    const originalBrain = brainConfiguration?.brain;

    // Brains
    const [selectedBrainId, setSelectedBrainId] = React.useState<undefined | string>(undefined);

    return (
        <div>
            <Select
                id="select-simple"
                placeholder="Please choose..."
                label="Brain"
                labelGraphic={<Icon>psychology</Icon>}
                items={brains?.map(brain => ({ value: brain.id, label: brain.name + " - " + brain.description })) ?? []}
                onValueChanged={setSelectedBrainId}
                value={selectedBrainId || originalBrain}            />
            <br />
            <Button label="Save" primary id={generateUid()} icon={<Icon>save</Icon>} onClick={() => {
                    setConfiguration({ brainId: selectedBrainId })
            }} />
        </div>
    );
};

export default BrainConfigurationPane;