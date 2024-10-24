# AI_Platform
A platform to tinker around with Vector Databases, Prompts and Chats.

In order to play with it we have stuff:
* Vector DBs packaged in **Brains** that you can search
* **LLM**'s all over the place
* **Prompts** that we can modify ant test
* **Chains** that combines it all - Brains, prompts and chats...

This is how the different bits are interacting:

<div style="text-align: center;">
  <img src="/content/ai_platform_overview_simple.png" alt="Overview" width="90%"/>
</div>

</br>

| Component           | API                                                                                                    | Comments                                              |
|-------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| AI Chains | <a href="{{AI_ORCHESTRATION_URL}}/docs" target="_blank">OpenAPI Docs for AI Orchestration & Chains</a> | Currently only 3 chain types: *Default* (a mock chain), *Naked LLM* and *Simple RAG* |
| AI Brains         | <a href="{{AI_BRAIN_URL}}/docs" target="_blank">OpenAPI Docs for Brains & Search</a>                   |                                                                    |
| LLM Wrapper      | <a href="{{LLM_WRAPPER_URL}}/docs" target="_blank">OpenAPI Docs LLM Wrapper Docs</a>                   |                                                                    |

</br>
For the entire code base go see the <a href="https://github.com/tillg/ai-platform" target="_blank">Github repo</a>.

## Chains

Chain are functions that get a `ChatRequest` and produce a `Message`. A typical chain could do things like
1. Query a `Brain` to get some information that can help answering the user question.
2. Create a prompt that contains the user question as well as context (i.e. the documents or chunks it got from the brain)
3. Send this prompt to an LLM (using the `LlmWrapper`)
4. Return the answer to the user.


