import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain.agents import initialize_agent, AgentType
from .tools_registry import tools

load_dotenv()
model_name = os.getenv("LLM_MODEL")

llm = ChatOllama(model=model_name)

agent = create_react_agent(
    tools = tools,
    model = llm,
    prompt ="You are a helpful assistant. Show me your chain of thoughts."
            "If the user request is missing any required information to call a tool, "
            "ask the user for the missing information before proceeding."
)
