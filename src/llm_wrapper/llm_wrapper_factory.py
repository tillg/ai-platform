class LlmWrapperFactory:

    def create_llm_wrapper(self) -> LlmWrapper:  # noqa
        if self.config["llm_wrapper"] == "llm_wrapper":
            return LlmWrapper(self.config)  # noqa
        elif self.config["llm_wrapper"] == "llm_wrapper_v2":
            return LlmWrapperV2(self.config)  # noqa
        else:
            raise ValueError("Invalid LLM Wrapper")
