from typing import Annotated, Literal, Optional

from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def chatbot(state: State):
    return {
        "messages": [llm.invoke(state["messages"])],
    }

graph_builder.add_node(
    "chatbot",
    chatbot,
)
graph_builder.add_edge(
    START, 
    "chatbot"
)
graph_builder.add_edge(
    "chatbot", 
    END,
)

graph = graph_builder.compile()
user_input = input("Enter a message: ")

state = graph.invoke({"messages": [{"role": "user", "content": user_input}]})

print(state["messages"][-1].content)