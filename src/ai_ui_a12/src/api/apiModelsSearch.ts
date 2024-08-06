

export class SearchRequest  {
    search_term: String;

    constructor(search_term: String) {
        this.search_term = search_term;
    }
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
};

export class SearchResultChunksAndDocuments {
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

export type SearchHistoryItem = SearchRequest | SearchResult;

export class BrainModel {
    id: string
    name: string;
    description: string;
    path: string;
    importer?: { [key: string]: any };

    constructor(id: string, name: string, description: string, path: string, importer?: { [key: string]: any }) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.path = path;
        this.importer = importer;
    }
}