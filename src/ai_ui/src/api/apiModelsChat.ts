

export type Message = {
    content: string;
    role: string;
};

export type ChatRequest = {
    messages: Message[];
    context?: { [key: string]: string };
};


export type ChatResponse = {
    content: string;
};



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



