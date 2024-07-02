export const enum RetrievalMode {
    Hybrid = "hybrid",
    Vectors = "vectors",
    Text = "text"
}

export type ChatAppRequestOverrides = {
    use_advanced_flow?: boolean;
    retrieval_mode?: RetrievalMode;
    top?: number;
    temperature?: number;
    prompt_template?: string;
};

export type ResponseMessage = {
    content: string;
    role: string;
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
    message: ResponseMessage;
    context: ResponseContext;
    session_state: any;
};

export type ChatAppResponseOrError = {
    choices?: ResponseChoice[];
    error?: string;
};

export type ChatAppResponse = {
    choices: ResponseChoice[];
};

export type ChatAppRequestContext = {
    overrides?: ChatAppRequestOverrides;
};

export type ChatAppRequest = {
    messages: ResponseMessage[];
    context?: ChatAppRequestContext;
};

export type SearchRequest = {
    search_term: String
}

type Document = {
    title: string;
    content: string;
    uri: string;
    id?: string | null;
    search_info?: SearchInfo | null;
};

// Extending Document type to create Chunk type
export type Chunk = Document & {
    original_document_id: string;
    search_info?: SearchInfo | null;
};

class SearchResultChunksAndDocuments {
    chunks?: Chunk[] = [];
    documents?: Document[] = [];

    constructor(chunks?: Chunk[], documents?: Document[]) {
        if (chunks) this.chunks = chunks;
        if (documents) this.documents = documents;
    }
}

export type SearchInfo = {
    search_term: string;
    distance: number;
}


export class SearchResult {
    search_term?: string;
    result?: SearchResultChunksAndDocuments;
    inner_working?: { [key: string]: any };

    constructor(result?: SearchResultChunksAndDocuments, inner_working?: { [key: string]: any }) {
        this.result = result;
        this.inner_working = inner_working;
    }
}