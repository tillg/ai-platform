

export type Message = {
    content: string;
    role: string;
};

export type ChatResponse = {
    content: string;
    inner_working?: { [key: string]: any };
};

export type MessageOrChatResponse = Message | ChatResponse;

export type ChatRequest = {
    messages: Message[];
    context?: { [key: string]: string };
    model?: string;
};

export function messageOrChatResponseToMessage(messageOrChatResponse: MessageOrChatResponse): Message {
    if (!isChatResponse(messageOrChatResponse)) {
        return messageOrChatResponse;
    }
    return {
        content: messageOrChatResponse.content,
        role: "assistant"
    };
}

export function isChatResponse(item: MessageOrChatResponse): item is ChatResponse {
    return (item as ChatResponse).inner_working !== undefined;
}

export type Model = {
    name: string;  // Also used as ID
    description?: string;
    details?: { [key: string]: string };
    state?: string;
};