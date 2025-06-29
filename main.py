import os
import asyncio
from typing import Annotated, Literal, Optional, List

from dotenv import load_dotenv, find_dotenv

from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

load_dotenv(find_dotenv())

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)


class MessageClassifier(BaseModel):
    message_type: Literal["emotional", "logical"] = Field(
        ...,
        description="Classify if the message requires an emotional (therapist) or logical response."
    )

class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str | None
    path: List[str]
    tool_calls: List[dict]  # Track tool calls

def classify_message(state: State):
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)

    result = classifier_llm.invoke([
        {
            "role": "system",
            "content": """Classify the user message as either:
            - 'emotional': if it asks for emotional support, therapy, deals with feelings, or personal problems
            - 'logical': if it asks for facts, information, logical analysis, or practical solutions
            """
        },
        {"role": "user", "content": last_message.content}
    ])

    new_path = state.get("path", []) + ["classifier"]

    return {
        "message_type": result.message_type,
        "path": new_path,
        "tool_calls": state.get("tool_calls", []),
    }

def router(state: State):
    message_type = state.get("message_type", "logical")
    new_path = state.get("path", []) + ["router"]
    return_value = {
        "path": new_path,
        "tool_calls": state.get("tool_calls", []),
    }
    if message_type == "emotional":
        return_value["next"] = "therapist"
    else:
        return_value["next"] = "logical"
    return return_value

def therapist_agent(state: State):
    last_message = state["messages"][-1]
    messages = [
        {"role": "system",
         "content": """You are a compassionate therapist. Focus on the emotional aspects of the user's message.
                        Show empathy, validate their feelings, and help them process their emotions.
                        Ask thoughtful questions to help them explore their feelings more deeply.
                        Avoid giving logical solutions unless explicitly asked."""
         },
        {"role": "user", "content": last_message.content}
    ]
    reply = llm.invoke(messages)
    new_path = state.get("path", []) + ["therapist"]
    return {
        "messages": [{"role": "assistant", "content": reply.content}],
        "path": new_path,
        "tool_calls": state.get("tool_calls", []),
    }

async def logical_agent(state: State):
    client = MultiServerMCPClient(
        {
            "calculator": {
                "url": "http://localhost:8050/mcp",
                "transport": "streamable_http",
            }
        }
    )

    tools = await client.get_tools()
    agent_runnable = create_react_agent(llm, tools)

    # The react agent expects a dictionary with a "messages" key.
    response = await agent_runnable.ainvoke({"messages": state["messages"]})

    new_messages = response["messages"][len(state["messages"]):]

    tool_calls = []
    for message in new_messages:
        if hasattr(message, 'tool_calls') and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_calls.append(f"Tool Called: {tool_call['name']}; Args: {tool_call['args']}")

    new_path = state.get("path", []) + ["logical"]

    return {
        "messages": new_messages,
        "path": new_path,
        "tool_calls": state.get("tool_calls", []) + tool_calls,
    }

graph_builder = StateGraph(State)   
graph_builder.add_node("classifier", classify_message)
graph_builder.add_node("router", router)
graph_builder.add_node("therapist", therapist_agent)
graph_builder.add_node("logical", logical_agent)
graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("classifier", "router")
graph_builder.add_conditional_edges(
    "router",
    lambda state: state.get("next"),
    {"therapist": "therapist", "logical": "logical"}
)
graph_builder.add_edge("therapist", END)
graph_builder.add_edge("logical", END)
graph = graph_builder.compile()

async def run_chatbot():
    state = {"messages": [], "message_type": None, "tool_calls": []}
    while True:
        user_input = await asyncio.to_thread(input, "Message: ")
        if user_input == "exit":
            print("Bye")
            break
        state["path"] = []
        state["tool_calls"] = []
        state["messages"] = state.get("messages", []) + [
            {"role": "user", "content": user_input}
        ]
        state = await graph.ainvoke(state)
        print(f"\n[Agent Path] {' → '.join(state['path'])}")
        if state.get("tool_calls"):
            for call in state["tool_calls"]:
                print(f"[MCP Tool Used] {call}")
        if state.get("messages") and len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            print(f"Assistant: {last_message.content}")

if __name__ == "__main__":
    asyncio.run(run_chatbot())
