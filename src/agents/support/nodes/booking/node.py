from langchain.agents import create_agent

from agents.support.nodes.booking.tools import tools
from agents.support.nodes.booking.prompt import prompt_template


booking_node = create_agent(
    model="google_genai:gemini-2.5-flash",
    tools=tools,
    system_prompt=prompt_template.format(),
)