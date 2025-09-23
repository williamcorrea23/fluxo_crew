import os, re, json, requests, weaviate
from openai import OpenAI
from llama_index import load_index_from_storage, StorageContext
from llama_index.vector_stores.weaviate import WeaviateVectorStore

# Import seguro do CrewAI Tools
try:
    from crewai_tools import tool
except ImportError:
    def tool(name=None):
        def wrapper(func):
            return func
        return wrapper

# Carregar regras ABAP
with open(os.path.join(os.path.dirname(__file__), "abap_rules.json"), "r", encoding="utf-8") as f:
    ABAP_RULES = json.load(f)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# RAG com Weaviate
client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))
)
vector_store = WeaviateVectorStore(weaviate_client=client, index_name="ABAPDocs")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

try:
    index = load_index_from_storage(storage_context)
    retriever = index.as_retriever()
except Exception:
    retriever = None

@tool("abap_validator_tool")
def abap_validator_tool(code: str) -> str:
    """Valida código ABAP em várias camadas."""
    errors = []

    # Camada 1: JSON rules
    if not any(code.strip().upper().startswith(start) for start in ABAP_RULES["rules"]["program_start"]):
        errors.append("❌ Programa deve começar com REPORT, PROGRAM, CLASS, FUNCTION-POOL ou MODULE POOL.")

    for i, line in enumerate(code.splitlines(), start=1):
        line = line.strip()
        if line and not line.startswith("*"):
            if (ABAP_RULES["rules"]["must_end_with_dot"]
                and not line.endswith(".")
                and not any(line.endswith(e) for e in ABAP_RULES["rules"]["block_structures"].values())):
                errors.append(f"❌ Linha {i}: instrução sem ponto final.")

    for bad in ABAP_RULES["best_practices"]["avoid"]:
        if bad in code:
            errors.append(f"⚠️ Má prática detectada: {bad}")

    base_result = "✅ OK - Código ABAP válido." if not errors else "\n".join(errors)

    # Camada 2: RAG
    rag_text = "Nenhuma explicação encontrada."
    if retriever:
        rag_info = retriever.retrieve("ABAP regras de sintaxe")
        rag_text = "\n".join([r.text for r in rag_info[:2]]) if rag_info else rag_text

    # Camada 3: GPT
    gpt_response = ""
    try:
        completion = openai_client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "Você é um revisor ABAP experiente."},
                {"role": "user", "content": f"Analise o código ABAP e sugira melhorias:\n{code}"}
            ]
        )
        gpt_response = completion.choices[0].message.content
    except Exception as e:
        gpt_response = f"(⚠️ GPT não disponível: {str(e)})"

    return f"""
🔎 **Validação ABAP**
{base_result}

📖 **Explicação das Apostilas**
{rag_text}

🤖 **Sugestão GPT-5-Nano**
{gpt_response}
""".strip()
