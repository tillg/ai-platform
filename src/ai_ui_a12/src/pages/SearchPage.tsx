import * as React from "react";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { SplitView } from "@com.mgmtp.a12.widgets/widgets-core/lib/layout/split-view";
import { ActionContentbox, ContentBoxElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/contentbox";
import styled from "styled-components";
import { useRef, useState, useEffect } from "react";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";
import { Tag, TagGroup } from "@com.mgmtp.a12.widgets/widgets-core/lib/tag";
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { ModalOverlay } from "@com.mgmtp.a12.widgets/widgets-core/lib/modal-overlay";
import BrainConfigurationPane from "../components/BrainConfigurationPane";
import { SearchRequest, SearchResult, SearchHistoryItem } from "../api";
import { searchApi } from "../api/searchApi";
import { UserInput } from "../components/UserInput";
import { SearchHistory } from "../components/SearchHistory";

// Styled components
const PageContainer = styled.div`
    display: flex;
    flex-direction: column;
    height: 100vh;
`;
const Header = styled.div`
    display: flex;
    align-items: center;
    gap: 10px;
    position: sticky;
    top: 0;
    background-color: #e2e6e9;
    z-index: 1;
    padding: 5px;
`;
const StickyInput = styled.div`
    position: sticky;
    bottom: 0;
    background-color: white;
    padding: 10px;
    z-index: 1;
`;

export const SearchPage = () => {
    const userInputRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        if (userInputRef.current) {
            userInputRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, []);

    const [error, setError] = useState<unknown>();

    //Brains
    const [availableBrains, setAvailableBrains] = useState<string[]>([]);
    const [selectedBrainName, setSelectedBrainName] = useState<string>();
    const fetchBrains = async () => {
        return ["Berlin"]
    };
    useEffect(() => {
        fetchBrains();
    }, []);
    const initiateSelectedBrain = async () => {
        if (selectedBrainName === undefined) {
            const defaultBrain = "Berlin"
            console.log("Default Brain: ", defaultBrain)
            if (defaultBrain) {
                setSelectedBrainName(defaultBrain);
            } else {
                console.error("Failed to fetch default Brain.");
            }
        }
    }
    useEffect(() => {
        initiateSelectedBrain();
    }, []);


    // Config Pane
    const [isConfigurationOpen, setConfigurationOpen] = React.useState<boolean>(false);
    const showConfiguration = (): void => setConfigurationOpen(true);
    const closeConfiguration = (): void => setConfigurationOpen(false);

    const setConfiguration = (config: Record<string, any>) => {
        if (config.brain && config.brain !== undefined) {
            setSelectedBrainName(config.brain);
        }
    };
    const handleSetConfiguration = (config: Record<string, any>) => {
        setConfiguration(config);
        closeConfiguration();
    };

    // Search history
    const [searchHistory, setSearchHistory] = useState<SearchHistoryItem[]>([]);

    // User Questions
    async function sendQuestion(question: string) {
        const searchRequest = new SearchRequest(question);
        const newSearchHistory = [...searchHistory, searchRequest]
        console.log("newSearchHistory: ", newSearchHistory)
        setSearchHistory(newSearchHistory);
        const searchResult = await searchApi(searchRequest)
        console.log("Got searchResult: ", searchResult)
        setSearchHistory([...newSearchHistory, searchResult]);
    }

    return (
        <PageContainer>
            <Header>
                <Button label="Settings" id={generateUid()} onClick={showConfiguration} icon={<Icon>settings</Icon>} />
                <Tag icon={<Icon>psychology</Icon>}> Brain: {selectedBrainName}</Tag>
            </Header>
            {isConfigurationOpen && (
                <ModalOverlay closeOnOutsideClick={false} onClose={closeConfiguration}>
                    <ActionContentbox
                        headingElements={<ContentBoxElements.Title ariaLevel={1} text="Settings" />}
                        headingButtons={<ContentBoxElements.CloseButton onClick={closeConfiguration} />}
                    >
                        <BrainConfigurationPane brains={availableBrains} brainConfiguration={{ brain: selectedBrainName }} setConfiguration={handleSetConfiguration} />
                    </ActionContentbox>
                </ModalOverlay>
            )}
            <SearchHistory searchHistory={searchHistory} />

            <StickyInput ref={userInputRef}>
                <UserInput onSend={sendQuestion} disabled={false} clearOnSend={true} placeholder="What can I visit in Berlin?" />
            </StickyInput>
        </PageContainer>)
}


