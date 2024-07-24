

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


export type Thoughts = {
    title: string;
    description: any; // It can be any output from the api
    props?: { [key: string]: string };
};

export type ResponseContext = {
    data_points: string[];
    followup_questions: string[] | null;
    thoughts: Thoughts[];
};

export type ResponseChoice = {
    index: number;
    message: Message;
    context: ResponseContext;
    session_state: any;
};

export type ChatAppResponseOrError = {
    choices?: ResponseChoice[];
    error?: string;
};



