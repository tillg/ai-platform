

import { SearchRequest, SearchResult } from "./apiModelsSearch";
import { AI_BRAIN_URL } from "../constants";

async function searchApiHttp(request: SearchRequest): Promise<Response> {
    return await fetch(`${AI_BRAIN_URL}/search`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
    });
}

export async function searchApi(request: SearchRequest): Promise<SearchResult> {
    const httpResponse = await searchApiHttp(request);
    if (httpResponse.ok) {
        const jsonResponse = await httpResponse.json();
        if (jsonResponse.result) {
            const searchResponse: SearchResult = new SearchResult(jsonResponse.result, jsonResponse.inner_working || {})
            return searchResponse;
        } else {
            throw new Error("Result field is missing in the response");
        }
    }
    throw new Error(`Failed to fetch searchApi: ${httpResponse.status} ${httpResponse.statusText}`);
}