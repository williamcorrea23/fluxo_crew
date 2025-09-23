from crewai import Crew, Process
from crewai.loaders import AgentLoader, TaskLoader

from tools.abap_validator_tool import abap_validator_tool
from tools.xml_formatter_tool import xml_formatter_tool

agents = AgentLoader.from_yaml("config/agents.yaml")
tasks = TaskLoader.from_yaml("config/tasks.yaml")

agents["programador"].tools = [xml_formatter_tool]
agents["tester"].tools = [abap_validator_tool]

crew = Crew(
    agents=agents.values(),
    tasks=tasks.values(),
    process=Process.sequential,
    storage=None  # 🔥 desabilita Chroma/Knowledge
)
