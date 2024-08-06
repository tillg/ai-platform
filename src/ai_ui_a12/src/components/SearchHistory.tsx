import { Chat } from "@com.mgmtp.a12.widgets/widgets-core";
import { SearchRequest, SearchHistoryItem } from "../api";
import { SearchResultMessageGroup } from "./SearchResultMessageGroup";

interface Props {
    searchHistory: SearchHistoryItem[];
}

function searchRequestPane(searchRequest: SearchRequest) {
    return (
        <Chat.MessageGroup
            position={'right'}>
            <Chat.UserInfo userName={"User"} />
            <Chat.Message>
                {searchRequest.search_term}
            </Chat.Message>
        </Chat.MessageGroup>
    )
}

export const SearchHistory = ({ searchHistory }: Props) => {
    return (
        <Chat.Container>
            {searchHistory.map((searchHistoryEntry, index) => (
                <div key={index}>
                    {(searchHistoryEntry instanceof SearchRequest)
                        ? searchRequestPane(searchHistoryEntry)
                        : <SearchResultMessageGroup searchResult={searchHistoryEntry} />}
                </div>
            ))}
        </Chat.Container>
    )
}