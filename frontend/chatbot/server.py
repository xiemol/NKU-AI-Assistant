"""Example of a simple chatbot that just passes current conversation
state back and forth between server and client.
"""
from typing import List, Union

from fastapi import FastAPI
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)


# Declare a chain
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful, professional assistant named Cob."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


# 2. Create model
# sparkllm
import os
os.environ["IFLYTEK_SPARK_APP_ID"] = "1a2c0e22"
os.environ["IFLYTEK_SPARK_API_KEY"] = "91ac602cffda5c10bbb78fc314f8525d"
os.environ["IFLYTEK_SPARK_API_SECRET"] = "ODYyMWEzMDViNGVjMWZjYWQyMmE5YWJi"

# 此处参考：https://www.xfyun.cn/doc/spark/Web.html
os.environ["IFLYTEK_SPARK_API_URL"] = "wss://spark-api.xf-yun.com/v3.1/chat"
os.environ["IFLYTEK_SPARK_llm_DOMAIN"] = "generalv3"
from langchain_community.chat_models import ChatSparkLLM
model = ChatSparkLLM()


chain = prompt | model


class InputChat(BaseModel):
    """Input for the chat endpoint."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )


add_routes(
    app,
    chain.with_types(input_type=InputChat),
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type="chat",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)