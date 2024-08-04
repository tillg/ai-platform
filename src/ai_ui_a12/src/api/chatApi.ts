import { ChatRequest, Message, Model } from "./apiModelsChat";
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

export async function chatApi(request: ChatRequest): Promise<Message> {
    console.log("chatApi request", request);
    const httpResponse = await chatApiHttp(request);
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
 

export async function getModels(): Promise<Model[]> {
    const httpResponse = await fetch(`${LLM_WRAPPER_URL}/models`);
    if (!httpResponse.ok) {
        throw new Error(`Failed to fetch getModels: ${httpResponse.status} ${httpResponse.statusText}`);
    }
    const jsonResponse = await httpResponse.json();
    const models: Model[] = jsonResponse.map((item: any) => {
        return {
            name: item.name,
            description: item.description,
            details: item.details,
            state: item.state ?? "unknown",
            default: item.default ?? false
        };
    });
    return models;
}
export async function getDefaultModel(): Promise<Model | undefined> {
    const models = await getModels();
    return models.find(model => model.default);
}