import os, sqlite3, streamlit as st
from openai import OpenAI
from tools.abap_validator_tool import abap_validator_tool
from tools.xml_formatter_tool import xml_formatter_tool
from rag_loader import load_apostilas

# ========================
# CONFIGURAÇÃO
# ========================
st.set_page_config(page_title="SAP CrewAI Hub", layout="wide")
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Indexação em background
load_apostilas()

# SQLite para histórico
conn = sqlite3.connect("history.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT, content TEXT
)""")
conn.commit()

def log_action(action, content):
    c.execute("INSERT INTO history (action, content) VALUES (?, ?)", (action, content))
    conn.commit()

# ========================
# INTERFACE
# ========================
st.sidebar.title("SAP CrewAI Hub")
section = st.sidebar.radio("Navegação", ["Dashboard", "Gerar Código", "Validar Código", "Chat"])

# --- Dashboard ---
if section == "Dashboard":
    st.title("📊 Dashboard - SAP CrewAI")
    count_gen = c.execute("SELECT COUNT(*) FROM history WHERE action='generate'").fetchone()[0]
    count_val = c.execute("SELECT COUNT(*) FROM history WHERE action='validate'").fetchone()[0]
    count_chat = c.execute("SELECT COUNT(*) FROM history WHERE action='chat'").fetchone()[0]

    st.metric("Objetos gerados", count_gen)
    st.metric("Validações executadas", count_val)
    st.metric("Consultas ao chat", count_chat)

    st.subheader("Últimas interações")
    rows = c.execute("SELECT action, content FROM history ORDER BY id DESC LIMIT 5").fetchall()
    for r in rows:
        st.write(f"**{r[0]}** → {r[1][:80]}...")

# --- Gerar Código ---
elif section == "Gerar Código":
    st.title("📝 Gerador de Código ABAP")
    object_type = st.selectbox("Tipo de Objeto", ["Program", "Table", "Class", "Function"])
    object_name = st.text_input("Nome do Objeto")
    description = st.text_input("Descrição")
    natural_language = st.text_area("Defina em linguagem natural", height=150)

    if st.button("Gerar Código"):
        # (1) Programador (GPT-5-Nano)
        completion = openai_client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "Você é um programador ABAP experiente."},
                {"role": "user", "content": f"Gerar um objeto ABAP do tipo {object_type}, nome {object_name}, descrição {description}, detalhes: {natural_language}"}
            ]
        )
        raw_code = completion.choices[0].message.content

        # (2) Revisor (GPT-5-Nano)
        review = openai_client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "Você é um revisor ABAP experiente."},
                {"role": "user", "content": f"Revise o seguinte código ABAP e sugira melhorias:\n{raw_code}"}
            ]
        )
        revised = review.choices[0].message.content

        # (3) Mostrar resultados
        st.subheader("📄 Código Gerado (original)")
        st.code(raw_code, language="abap")

        st.subheader("🔎 Revisão do Revisor")
        st.write(revised)

        xml_output = xml_formatter_tool(raw_code)
        st.subheader("📦 Exportação XML")
        st.code(xml_output, language="xml")

        log_action("generate", raw_code)

# --- Validar Código ---
elif section == "Validar Código":
    st.title("✅ Validador ABAP")
    code_input = st.text_area("Cole o código ABAP para validar", height=200)

    if st.button("Validar"):
        validation = abap_validator_tool(code_input)
        st.subheader("Resultado da Validação")
        st.markdown(validation)

        log_action("validate", code_input)

# --- Chat ---
elif section == "Chat":
    st.title("💬 Chat Assistente SAP")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Digite sua mensagem")
    if st.button("Enviar") and user_input:
        # RAG + GPT
        completion = openai_client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "Você é um consultor ABAP experiente que usa apostilas como referência."},
                {"role": "user", "content": user_input}
            ]
        )
        response = completion.choices[0].message.content

        st.session_state.messages.append(("🧑 Usuário", user_input))
        st.session_state.messages.append(("🤖 Assistente", response))
        log_action("chat", user_input)

    for role, msg in st.session_state.messages:
        st.markdown(f"**{role}:** {msg}")
