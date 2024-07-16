

import { SearchRequest } from "./apiModelsSearch";
import { AI_BRAIN_URL } from "../constants";

export async function searchApi(request: SearchRequest): Promise<Response> {
    return await fetch(`${AI_BRAIN_URL}/search`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
    });
}