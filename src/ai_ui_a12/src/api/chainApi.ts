import { ChatRequest, Message } from "./apiModelsChat";
import { AI_ORCHESTRATION_URL } from "../constants";

async function chainApiHttp(request: ChatRequest): Promise<Response> {
    console.log("chainApiHttp request", request);
    return await fetch(`${AI_ORCHESTRATION_URL}/run_chain`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
    });
}

export async function chainApi(request: ChatRequest): Promise<Message> {
    console.log("chainApi request", request);
    const httpResponse = await chainApiHttp(request);
    if (httpResponse.ok) {
        const jsonResponse = await httpResponse.json();
        if (jsonResponse.content) {
            const chatResponse: Message = {
                content: jsonResponse.content,
                role: jsonResponse.role || "assistant",
                inner_working: jsonResponse.inner_working || {}
            };
            return chatResponse;
        } else {
            throw new Error("Content field is missing in the response");
        }
    }
    throw new Error(`Failed to fetch chatApi: ${httpResponse.status} ${httpResponse.statusText}`);
}
 

export async function getChains(): Promise<string[]> {
    const httpResponse = await fetch(`${AI_ORCHESTRATION_URL}/list`);
    if (!httpResponse.ok) {
        throw new Error(`Failed to fetch list of chains: ${httpResponse.status} ${httpResponse.statusText}`);
    }
    const jsonResponse = await httpResponse.json();
    console.log("jsonResponse", jsonResponse);
    return jsonResponse
}
