from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv


# Carregar variáveis de ambiente
load_dotenv()

class TalkAgent:
    
    def __init__(self):
        # Configuração da chave de API
        self.agent = None
        self.task = None
        self.crew = None
        
        self.llm = "gpt-4o-mini"
        self._setup_crew()
    
    def _setup_crew(self):
        """
        Inicializa a configuração do agente de transcrição.
        
        :param api_key: Chave da API OpenAI.
        :param verbose: Define se o agente deve ser detalhista nos logs.
        :param memory: Define se o agente deve ter memória ativa.
        """
        
        processor_agent = Agent(
            role="Processador de transcrições",
            goal="Receber uma transcrição de áudio como texto e produzir uma resposta relevante e coerente.",
            backstory="Especialista em compreender contextos e responder com clareza.",
            memory=True,
            verbose=True,
            llm=self.llm
        )

        processor_task = Task(
            description=(
                "Analise o seguinte texto de transcrição e forneça uma resposta com base nas informações apresentadas: "
                "{transcription_text}. A resposta deve ser clara e objetiva. Responda sempre com 'Oi chefe' ou 'Fala professor' ou 'Oi professor' ou 'Aqui está chefe'"
            ),
            expected_output="Um texto com uma resposta coerente e relevante.",
            agent=processor_agent
        )

        self.crew = Crew(
            agents=[processor_agent],
            tasks=[processor_task],
            process=Process.sequential  # Processo sequencial
        )

    def kickoff(self, transcription):
        """
        Processa o texto da transcrição e retorna a resposta.
        
        :param transcription_text: O texto da transcrição de áudio.
        :return: Resposta gerada pelo agente.
        """
        result = self.crew.kickoff(inputs={"transcription_text":transcription})
        return result.raw


