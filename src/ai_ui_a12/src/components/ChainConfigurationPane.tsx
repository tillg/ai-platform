import React from 'react';
import { Select } from "@com.mgmtp.a12.widgets/widgets-core/lib/input/select";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";

const LlmConfigurationPane = ({
    chains,
    chainConfiguration,
    setConfiguration
}: {
    chains: string[];
    chainConfiguration: Record<string, any>;
    setConfiguration: (config: Record<string, any>) => void;
}) => {

    console.log("chainConfiguration", chainConfiguration);
    console.log("chains", chains);
    
    const originalChain = chainConfiguration?.chain;

    // Chains
    const [selectedChain, setSelectedChain] = React.useState<undefined | string>(undefined);

    const chainsAsItems = chains.map(chain => ({ value: chain, label: chain }));
    console.log("chainsAsItems", chainsAsItems);

    return (
        <div>
            <Select
                id="select-simple"
                placeholder="Please choose..."
                label="Chain"
                labelGraphic={<Icon>psychology</Icon>}
                items={chainsAsItems}
                onValueChanged={setSelectedChain}
                value={selectedChain || originalChain}            />
            <br />
            <br />
            <br />
            <Button label="Save" primary id={generateUid()} icon={<Icon>save</Icon>} onClick={() => {
                    setConfiguration({ chain: selectedChain })
                
            }} />
        </div>
    );
};

export default LlmConfigurationPane;