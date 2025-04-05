import os
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def get_info_tavily(topic: str):
    """Searches for information."""
    search = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)
    res = search.run(f"{topic}")
    return res

def lookup(topic: str, my_llm) -> str:
    
    tools = [
        Tool(
            name="Web search",
            func=get_info_tavily,
            description="useful for when you need to get information",
        ),
    ]
    
    template = """
       given the topic {topic} I want you to  investigate about it, I need you to 
       find updated information on the web and give me a summary.
       Your Final is extracted from: https://www.google.com/"""

    prompt_template = PromptTemplate(
        input_variables=["topic"], template=template
    )

    react_prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(
        llm = my_llm, 
        tools = tools, 
        prompt = react_prompt
    )
    agent_executor = AgentExecutor(
        agent = agent, 
        tools = tools, 
        verbose = True
    )

    result = agent_executor.invoke(
        input={"input": topic}
    )

    return result["output"]
