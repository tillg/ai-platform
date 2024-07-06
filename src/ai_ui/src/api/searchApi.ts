
const VITE_SEARCH_BACKEND_URL = import.meta.env.VITE_SEARCH_BACKEND_URL;

import { SearchRequest } from "./apiModelsSearch";

export async function searchApi(request: SearchRequest): Promise<Response> {
    return await fetch(`${VITE_SEARCH_BACKEND_URL}/search`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
    });
}