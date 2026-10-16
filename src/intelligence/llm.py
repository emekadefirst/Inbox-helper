from langchain_anthropic import ChatAnthropic
from src.configs.anthropic import ANTHROPIC_API_KEY, ANTHROPIC_MODEL


model = ChatAnthropic(
    model=ANTHROPIC_MODEL,
    anthropic_api_key=ANTHROPIC_API_KEY,
    streaming=False,
)



