from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco
def get_db_connection():
    conn = sqlite3.connect("receitas.db")
    conn.row_factory = sqlite3.Row
    return conn

def buscar_receitas(termo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome, ingredientes, modo_preparo
        FROM receitas
        WHERE nome LIKE ?
    """, (f"%{termo}%",))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()
    receitas = buscar_receitas(user_message)

    if not receitas:
        return jsonify({"reply": "Não encontrei receitas com esse ingrediente ou nome. Tente outro!"})

    if len(receitas) > 1:
        nomes = ", ".join([r["nome"] for r in receitas])
        return jsonify({"reply": f"Encontrei várias receitas: {nomes}. Qual você quer ver?"})

    receita = receitas[0]
    detalhes = f"🍴 {receita['nome']}\nIngredientes: {receita['ingredientes']}\nModo de preparo: {receita['modo_preparo']}"
    return jsonify({"reply": detalhes})

# -------------------------------
# ROTA PARA LISTA DE RECEITAS
# -------------------------------

@app.route("/lista", methods=["GET", "POST"])
def lista():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Paginação
    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    search = request.args.get("search", "").strip()

    if request.method == "POST":
        nome = request.form["nome"]
        ingredientes = request.form["ingredientes"]
        modo_preparo = request.form["modo_preparo"]

        cursor.execute("""
            INSERT INTO receitas (nome, ingredientes, modo_preparo)
            VALUES (?, ?, ?)
        """, (nome, ingredientes, modo_preparo))
        conn.commit()

        return redirect(url_for("lista"))

    # Contar total de receitas (com ou sem filtro)
    if search:
        cursor.execute(
            "SELECT COUNT(*) FROM receitas WHERE nome LIKE ?",
            (f"%{search}%",)
        )
        total = cursor.fetchone()[0]
        cursor.execute(
            "SELECT * FROM receitas WHERE nome LIKE ? ORDER BY nome ASC LIMIT ? OFFSET ?",
            (f"%{search}%", per_page, offset)
        )
    else:
        cursor.execute("SELECT COUNT(*) FROM receitas")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM receitas ORDER BY nome ASC LIMIT ? OFFSET ?", (per_page, offset))

    receitas = cursor.fetchall()
    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "lista.html",
        receitas=receitas,
        page=page,
        total_pages=total_pages
    )

if __name__ == "__main__":
    app.run(debug=True)