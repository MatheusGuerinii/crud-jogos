from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="10032008gue",
        database="crud_jogos"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/games", methods=["GET"])
def listar():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM games")
    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify(dados)

@app.route("/games", methods=["POST"])
def criar():
    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO games (nome, plataforma, status, nota) VALUES (%s,%s,%s,%s)",
        (dados["name"], dados["platform"], dados["status"], dados["rating"])
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"msg": "Criado com sucesso"})

@app.route("/games/<int:id>", methods=["PUT"])
def atualizar(id):
    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE games SET nome=%s, plataforma=%s, status=%s, nota=%s WHERE id=%s",
        (dados["name"], dados["platform"], dados["status"], dados["rating"], id)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"msg": "Atualizado com sucesso"})

@app.route("/games/<int:id>", methods=["DELETE"])
def deletar(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM games WHERE id=%s", (id,))
    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({"msg": "Deletado com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)