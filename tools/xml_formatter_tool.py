from crewai_tools import tool

@tool("xml_formatter_tool")
def xml_formatter_tool(objeto: str) -> str:
    xml_template = f"""
<ABAP_OBJECT>
  <TYPE>Program</TYPE>
  <CONTENT><![CDATA[
{objeto}
  ]]></CONTENT>
</ABAP_OBJECT>
"""
    try:
    from crewai_tools import tool
except ImportError:
    def tool(name=None):
        def wrapper(func):
            return func
        return wrapper

    return xml_template.strip()

