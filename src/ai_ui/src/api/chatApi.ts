// const VITE_CHAT_BACKEND_URL = import.meta.env.VITE_CHAT_BACKEND_URL;

import { ChatRequest, ChatResponse } from "./apiModelsChat";
import { LLM_WRAPPER_URL } from "../constants";

async function chatApiHttp(request: ChatRequest): Promise<Response> {
    console.log("chatApiHttp request", request);
    return await fetch(`${LLM_WRAPPER_URL}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
    });
    
}

export async function chatApi(request: ChatRequest): Promise<ChatResponse> {
    const httpResponse = await chatApiHttp(request);
    if (httpResponse.ok) {
        const jsonResponse = await httpResponse.json();
        if (jsonResponse.content) {
            const chatResponse: ChatResponse = {
                content: jsonResponse.content, 
                inner_working: {
                    detail: "It worked 😉"
                }
            };
            return chatResponse; 
        } else {
            throw new Error("Content field is missing in the response");
        }
    }
    throw new Error(`Failed to fetch chatApi: ${httpResponse.status} ${httpResponse.statusText}`);
}