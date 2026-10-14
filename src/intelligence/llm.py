from langchain_anthropic import ChatAnthropic
from src.configs import ANTHROPIC_API_KEY


model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    anthropic_api_key=ANTHROPIC_API_KEY,
    streaming=False,
)

