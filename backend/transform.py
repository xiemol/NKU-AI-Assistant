from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from models import *


def chToEn():
    prompt_str = """
    你是一位语言翻译专家，擅长将中文翻译成英文。请将以下文本从中文翻译成英文\n\n
    {text}"""

    prompt = PromptTemplate(
        input_variables=["text"],
        template=prompt_str,
    )

    chain = LLMChain(
        prompt=prompt,
        llm=openai(),
    )
    return chain


