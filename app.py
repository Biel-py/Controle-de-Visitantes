from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ia import generate_response

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///visitantes.db"
db = SQLAlchemy(app)


class Visitante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    documento = db.Column(db.String(30), nullable=False)
    pessoa_visitada = db.Column(db.String(120), nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    data_hora_entrada = db.Column(db.DateTime, default=datetime.now)
    data_hora_saida = db.Column(db.DateTime, nullable=True)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    agora = datetime.now()
    inicio_hoje = datetime.combine(agora.date(), datetime.min.time())

    visitantes = Visitante.query.order_by(
        Visitante.data_hora_entrada.desc()
    ).limit(8).all()

    return render_template(
        'index.html',
        visitantes=visitantes,
        total_visitantes=Visitante.query.count(),
        total_presentes=Visitante.query.filter_by(
            data_hora_saida=None
        ).count(),
        total_sairam=Visitante.query.filter(
            Visitante.data_hora_saida.isnot(None)
        ).count(),
        total_hoje=Visitante.query.filter(
            Visitante.data_hora_entrada >= inicio_hoje
        ).count(),
        data_hoje=agora.strftime('%d de %B de %Y'),
        hora_agora=agora.strftime('%H:%M'),
    )


@app.route("/nova-entrada", methods=["GET", "POST"])
def nova_entrada():
    if request.method == "POST":
        nome = request.form.get("nome")
        documento = request.form.get("documento")
        pessoa_visitada = request.form.get("pessoa_visitada")
        motivo = request.form.get("motivo")

        novo_visitante = Visitante(
            nome=nome,
            documento=documento,
            pessoa_visitada=pessoa_visitada,
            motivo=motivo
        )
        db.session.add(novo_visitante)
        db.session.commit()

        return redirect(url_for("presentes"))

    return render_template("nova_entrada.html")


@app.route("/presentes")
def presentes():
    presentes_lista = Visitante.query.filter_by(data_hora_saida=None).all()
    return render_template("presentes.html", visitantes=presentes_lista)


@app.route("/registrar-saida", methods=["GET", "POST"])
def registrar_saida():
    if request.method == "POST":
        visitante_id = request.form.get("visitante_id")
        visitante = Visitante.query.get(visitante_id)
        if visitante:
            visitante.data_hora_saida = datetime.now()
            db.session.commit()
        return redirect(url_for("registrar_saida"))

    presentes_lista = Visitante.query.filter_by(data_hora_saida=None).all()
    return render_template("registrar_saida.html", visitantes=presentes_lista)


@app.route("/historico")
def historico():
    todos = Visitante.query.all()
    return render_template("historico.html", visitantes=todos)


@app.route("/assistente-ia", methods=["GET", "POST"])
def assistente_ia():
    resposta = None
    if request.method == "POST":
        pergunta = request.form.get("pergunta")
        resposta = generate_response(pergunta)
    return render_template("assistente_ia.html", resposta=resposta)


if __name__ == "__main__":
    app.run(debug=True)