import streamlit as st
from crew import crew
from rag_loader import load_apostilas

st.set_page_config(page_title="SAP CrewAI Hub", layout="wide")

# Indexação em background
load_apostilas()

st.sidebar.title("SAP CrewAI Hub")
section = st.sidebar.radio("Navegação", ["Dashboard", "Gerar Programa", "Validar Código", "Chat"])

if section == "Dashboard":
    st.title("📊 Dashboard - SAP CrewAI")
    st.info("Agentes prontos: Programador → Revisor → Tester → Funcional")

elif section == "Gerar Programa":
    st.title("📝 Gerar Programa ABAP")
    descricao = st.text_area("Descreva o que deseja implementar", height=200)

    if st.button("Executar Crew"):
        result = crew.kickoff(inputs={"descricao": descricao})
        st.subheader("📄 Resultado Final")
        st.write(result)

elif section == "Validar Código":
    st.title("✅ Validar Código ABAP")
    code_input = st.text_area("Cole seu código ABAP", height=200)

    if st.button("Validar"):
        result = crew.kickoff(inputs={"descricao": f"Validar código:\n{code_input}"})
        st.subheader("📄 Resultado da Validação")
        st.write(result)

elif section == "Chat":
    st.title("💬 Chat Assistente ABAP")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Digite sua pergunta")
    if st.button("Enviar") and user_input:
        result = crew.kickoff(inputs={"descricao": f"Responder pergunta: {user_input}"})
        st.session_state.messages.append(("🧑 Usuário", user_input))
        st.session_state.messages.append(("🤖 Assistente", result))

    for role, msg in st.session_state.messages:
        st.markdown(f"**{role}:** {msg}")
