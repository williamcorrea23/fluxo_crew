
from crewai_tools import BaseTool


class QueryCSV(BaseTool):

    name: str = "Ferramenta de execução de código de consulta a um CSV"
    description: str = (
        """Executa e retorna dados de uma consulta a partir de um CSV"""
    )


    def _run(self, codigo_python: str) -> str:

        contexto = {}
        exec(codigo_python, contexto)

        return contexto['resultado']
