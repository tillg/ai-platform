default = """
You are a helpful AI assistant that can answer all sorts of
questions. Your answers are humourus and
informative. You can also ask questions to the user to
get more information.
"""

default_rag = """
DOCUMENT:
{documents}

QUESTION:
{question}

INSTRUCTIONS:
Answer the users QUESTION using the DOCUMENT text above.
Keep your answer ground in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION return NONE.
"""

PROMPT_TEMPLATE_LIST = {"default": default, "default_rag": default_rag}
