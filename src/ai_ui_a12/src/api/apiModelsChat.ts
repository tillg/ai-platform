

export type Message = {
    content: string;
    role: string;
    inner_working?: { [key: string]: any };
};

export type ChatRequest = {
    messages: Message[];
    context?: { [key: string]: string };
    model?: string;
    options?: { [key: string]: any };
};


export function hasInnerWorking(message: Message): boolean {
    return message.inner_working !== null && message.inner_working !== undefined;
}

export type Model = {
    name: string;  // Also used as ID
    description?: string;
    details?: { [key: string]: string };
    state?: string;
    default?: boolean
};