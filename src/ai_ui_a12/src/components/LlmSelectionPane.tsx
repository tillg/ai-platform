import React from 'react';

const defaultLlms = [
    { name: 'GPT-3', description: 'Autoregressive language model that uses deep learning to produce human-like text.' },
    { name: 'BERT', description: 'Pre-training of deep bidirectional transformers for language understanding.' },
    // Add more demo LLMs here
];

const LlmSelectionPane = ({
    llms
}: {
        llms?: { name: string; description: string }[];
}) => {
    const effectiveLlms = llms && llms.length > 0 ? llms : defaultLlms;    const handleSelection = (selectedLLMName: string) => {
        console.log(`Selected LLM: ${selectedLLMName}`);
        // Additional logic for handling selection
    };

    return (
        <div>
            <h2>Select a Language Model</h2>
            <ul>
                {effectiveLlms.map((llm) => (
                    <li key={llm.name} onClick={() => handleSelection(llm.name)}>
                        <strong>{llm.name}</strong> - {llm.description}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default LlmSelectionPane;