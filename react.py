import openai
import re
import httpx
import os
from dotenv import load_dotenv(), find_dotenv()

load_dotenv(find_dotenv())

import os
import asyncio
from typing import Annotated, Literal, Optional, List

from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

load_dotenv(find_dotenv())

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)


