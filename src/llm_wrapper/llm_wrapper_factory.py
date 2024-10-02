

class LlmWrapperFactory:

    def create_llm_wrapper(self) -> LlmWrapper:
        if self.config["llm_wrapper"] == "llm_wrapper":
            return LlmWrapper(self.config)
        elif self.config["llm_wrapper"] == "llm_wrapper_v2":
            return LlmWrapperV2(self.config)
        else:
            raise ValueError("Invalid LLM Wrapper")