from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from webscrap.webscrap_single import get_chat_model
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
        llm=get_chat_model(),
    )
    return chain


trans1=chToEn()
trans2=get_chat_model()


