
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel


from audio_agents.avaliador import TextClassificationCrew
from audio_agents.talk_agent import TalkAgent
from audio_agents.sales import SalesReportCrew


class State(BaseModel):
    tipo_msg: bool = False
    text: str = ""
    language: str = ""

class FluxoAudio(Flow[State]):

    @start()
    def start(self):
                
        avaliador = TextClassificationCrew()
        self.state.tipo_msg = avaliador.kickoff(self.state.text)
    

    @router(start)
    def roteamento(self):
        return self.state.tipo_msg
    

    @listen("vendas")
    def terceiro_metodo(self):
        
        sales = SalesReportCrew()
        resposta = sales.kickoff(self.state.text)
                                 
        
        return resposta
        
        

    @listen("trivialidades")
    def quarto_metodo(self):
        agent = TalkAgent()
        resposta = agent.kickoff(self.state.text)
        
        return resposta



