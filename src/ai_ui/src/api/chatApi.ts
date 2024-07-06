const VITE_CHAT_BACKEND_URL = import.meta.env.VITE_CHAT_BACKEND_URL;

import { ChatRequest } from "./apiModelsChat";

export async function chatApi(request: ChatRequest): Promise<Response> {
    return await fetch(`${VITE_CHAT_BACKEND_URL}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
    });
    
}