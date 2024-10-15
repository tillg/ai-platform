from prompt_lib.prompt_templates import PROMPT_TEMPLATE_LIST


def get_prompt_template(prompt_id: str) -> str:
    if prompt_id not in PROMPT_TEMPLATE_LIST:
        raise ValueError(f"Prompt ID {prompt_id} not found in prompt list")
    return PROMPT_TEMPLATE_LIST[prompt_id]


def get_prompt(prompt_template_id: str, **kwargs) -> str:
    prompt_template = get_prompt_template(prompt_template_id)
    prompt = prompt_template.format(**kwargs)
    return prompt
