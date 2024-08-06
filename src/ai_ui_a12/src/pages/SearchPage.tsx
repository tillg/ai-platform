import * as React from "react";
import { Icon } from "@com.mgmtp.a12.widgets/widgets-core/lib/icon";
import { ActionContentbox, ContentBoxElements } from "@com.mgmtp.a12.widgets/widgets-core/lib/contentbox";
import styled from "styled-components";
import { useRef, useState, useEffect } from "react";
import { Button } from "@com.mgmtp.a12.widgets/widgets-core/lib/button";
import { Tag } from "@com.mgmtp.a12.widgets/widgets-core/lib/tag";
import { generateUid } from "@com.mgmtp.a12.widgets/widgets-core/lib/common";
import { ModalOverlay } from "@com.mgmtp.a12.widgets/widgets-core/lib/modal-overlay";
import BrainConfigurationPane from "../components/BrainConfigurationPane";
import { SearchRequest, SearchHistoryItem, BrainModel } from "../api";
import { getBrainList, searchApi } from "../api/searchApi";
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

    //Brains
    const [availableBrainModels, setAvailableBrainModels] = useState<BrainModel[]>([]);
    const [selectedBrainId, setSelectedBrainId] = useState<string>();
    const fetchBrains = async () => {
        try {
            const brains = await getBrainList();
            setAvailableBrainModels(brains);
            if (selectedBrainId === undefined) {
                console.log("Default Brain: ", brains[0].id)
                setSelectedBrainId(brains[0].id);
            }
        }
        catch (error) {
            console.error('SearchPage.fetchBrains: Failed to fetch brain list:', error);
        }
    };
    useEffect(() => {
        fetchBrains();
    }, []);

    // Config Pane
    const [isConfigurationOpen, setConfigurationOpen] = React.useState<boolean>(false);
    const showConfiguration = (): void => setConfigurationOpen(true);
    const closeConfiguration = (): void => setConfigurationOpen(false);

    const setConfiguration = (config: Record<string, any>) => {
        if (config.brainId && config.brainId !== undefined) {
            setSelectedBrainId(config.brainId);
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
        const searchRequest = new SearchRequest(question, selectedBrainId);
        const newSearchHistory = [...searchHistory, searchRequest]
        setSearchHistory(newSearchHistory);
        const searchResult = await searchApi(searchRequest)
        setSearchHistory([...newSearchHistory, searchResult]);
    }

    return (
        <PageContainer>
            <Header>
                <Button label="Settings" id={generateUid()} onClick={showConfiguration} icon={<Icon>settings</Icon>} />
                <Tag icon={<Icon>psychology</Icon>}> Brain: {selectedBrainId}</Tag>
            </Header>
            {isConfigurationOpen && (
                <ModalOverlay closeOnOutsideClick={false} onClose={closeConfiguration}>
                    <ActionContentbox
                        headingElements={<ContentBoxElements.Title ariaLevel={1} text="Settings" />}
                        headingButtons={<ContentBoxElements.CloseButton onClick={closeConfiguration} />}
                    >
                        <BrainConfigurationPane brains={availableBrainModels} brainConfiguration={{ brain: selectedBrainId }} setConfiguration={handleSetConfiguration} />
                    </ActionContentbox>
                </ModalOverlay>
            )}
            <SearchHistory searchHistory={searchHistory} />

            <StickyInput ref={userInputRef}>
                <UserInput onSend={sendQuestion} disabled={false} clearOnSend={true} placeholder="What can I visit in Berlin?" />
            </StickyInput>
        </PageContainer>)
}


