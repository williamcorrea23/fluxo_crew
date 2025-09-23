from crewai import Crew, Process
from crewai.loaders import AgentLoader, TaskLoader

# Importar tools
from tools.abap_validator_tool import abap_validator_tool
from tools.xml_formatter_tool import xml_formatter_tool

# Carregar agentes e tarefas
agents = AgentLoader.from_yaml("config/agents.yaml")
tasks = TaskLoader.from_yaml("config/tasks.yaml")

# Atribuir ferramentas específicas
agents["programador"].tools = [xml_formatter_tool]  # Programador pode exportar código para XML
agents["tester"].tools = [abap_validator_tool]      # Tester pode validar código ABAP

# Criar Crew
crew = Crew(
    agents=agents.values(),
    tasks=tasks.values(),
    process=Process.sequential  # Executa Programador → Revisor → Tester → Funcional
)
