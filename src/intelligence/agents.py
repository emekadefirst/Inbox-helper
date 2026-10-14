from src.intelligence.prompts import SYSTEM_PROMPT
from src.intelligence.tools import tools
from langchain.agents import create_agent
from src.intelligence.llm import model



agent = create_agent(model, tools=tools, system_prompt=SYSTEM_PROMPT)
