from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nova-entrada")
def nova_entrada():
    return render_template("nova_entrada.html")


@app.route("/registrar-saida")
def registrar_saida():
    return render_template("registrar_saida.html")


@app.route("/historico")
def historico():
    return render_template("historico.html")


@app.route("/presentes")
def presentes():
    return render_template("presentes.html")


@app.route("/assistente-ia")
def assistente_ia():
    return render_template("assistente_ia.html")


if __name__ == "__main__":
    app.run(debug=True)