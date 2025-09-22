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
    return xml_template.strip()
