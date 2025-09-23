from flask import Flask, request, jsonify, render_template_string
from crew import crew
from rag_loader import load_apostilas

app = Flask(__name__)

# Carrega apostilas no início
load_apostilas()

@app.route("/")
def home():
    return render_template_string("""
    <h2>SAP CrewAI Hub</h2>
    <ul>
      <li><a href='/gerar'>Gerar Programa</a></li>
      <li><a href='/validar'>Validar Código</a></li>
      <li><a href='/chat'>Chat Assistente</a></li>
    </ul>
    """)

@app.route("/gerar", methods=["GET", "POST"])
def gerar():
    if request.method == "POST":
        descricao = request.form.get("descricao")
        result = crew.kickoff(inputs={"descricao": descricao})
        return jsonify({"result": result})
    return """
    <form method='post'>
      <textarea name='descricao' rows=10 cols=60 placeholder='Descreva o programa'></textarea><br>
      <input type='submit' value='Gerar Programa'>
    </form>
    """

@app.route("/validar", methods=["GET", "POST"])
def validar():
    if request.method == "POST":
        code = request.form.get("code")
        result = crew.kickoff(inputs={"descricao": f"Validar código:\n{code}"})
        return jsonify({"result": result})
    return """
    <form method='post'>
      <textarea name='code' rows=15 cols=80 placeholder='Cole o código ABAP aqui'></textarea><br>
      <input type='submit' value='Validar Código'>
    </form>
    """

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        question = request.form.get("question")
        result = crew.kickoff(inputs={"descricao": f"Responder pergunta: {question}"})
        return jsonify({"user": question, "assistant": result})
    return """
    <form method='post'>
      <input name='question' style='width:400px' placeholder='Pergunte algo sobre ABAP'><br>
      <input type='submit' value='Enviar'>
    </form>
    """

if __name__ == "__main__":
    app.run()
