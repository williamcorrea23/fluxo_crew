import streamlit as st
import time
from audio_agents.fluxo_audio import FluxoAudio

st.title("Fluxo de vendas ou trivialidades")
st.write("Depois será implementado com whatsapp")

texto = st.text_input("Sobre o que quer falar?")

if st.button("Enviar"):
    
    st.info("Acessando os agentes")
    
    with st.spinner('Gerando texto...'):
        # Simula uma resposta gerada
                
        fluxo = FluxoAudio()
        resposta = fluxo.kickoff(inputs={"text":texto})
        
        
        st.success("Tudo pronto!")
        
        descricao = st.text_area(
            label="Descreva o produto",
            value=resposta,
            height=200,
            max_chars=500
        )
        
        
        
