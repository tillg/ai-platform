import { Chat } from "@com.mgmtp.a12.widgets/widgets-core";
import { Message } from "../api";
import { AssistantChatMessageGroup } from "./AssistantChatMessageGroup";

interface Props {
    chatHistory: Message[];
}

function userChatMessageGroup(message: Message) {
    return (
        <Chat.MessageGroup 
            position={'right'}>
            <Chat.UserInfo userName={"User"} />
            <Chat.Message>
                {message.content}
            </Chat.Message>
        </Chat.MessageGroup>
    )
}

export const ChatHistory = ({ chatHistory }: Props) => {
    return (
        <Chat.Container>
            {chatHistory.map((message, index) => (
                <div key={index}>
                {(message.role == 'user')
                    ? userChatMessageGroup(message)
                        : <AssistantChatMessageGroup message={message} />}
                </div>
            ))}
        </Chat.Container>
    )
}