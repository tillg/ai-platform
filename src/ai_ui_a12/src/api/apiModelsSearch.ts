

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