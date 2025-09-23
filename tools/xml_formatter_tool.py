# Import seguro do CrewAI Tools
try:
    from crewai_tools import tool
except ImportError:
    def tool(name=None):
        def wrapper(func):
            return func
        return wrapper

@tool("xml_formatter_tool")
def xml_formatter_tool(objeto: str) -> str:
    """Formata código ABAP em XML padrão."""
    return f"""
<ABAP_OBJECT>
  <TYPE>Program</TYPE>
  <CONTENT><![CDATA[
{objeto}
  ]]></CONTENT>
</ABAP_OBJECT>
""".strip()
