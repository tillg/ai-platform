

import { SearchRequest, SearchResult, BrainModel } from "./apiModelsSearch";
import { AI_BRAIN_URL } from "../constants";

export async function searchApi(searchRequest: SearchRequest): Promise<SearchResult> {
    console.log("searchApi searchRequest: ", searchRequest)
    const httpResponse = await fetch(`${AI_BRAIN_URL}/search`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(searchRequest)
    });
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

export async function getBrainList(): Promise<BrainModel[]> {
    const httpResponse = await fetch(`${AI_BRAIN_URL}/list`);
    if (httpResponse.ok) {
        const jsonResponse = await httpResponse.json();
        if (jsonResponse) {
            const brainList = jsonResponse.map((brain: any) => new BrainModel(brain.id, brain.name, brain.description, brain.path, brain.importer));
            return brainList
        }
    }
    throw new Error(`Failed to fetch getBrainList: ${httpResponse.status} ${httpResponse.statusText}`);
}