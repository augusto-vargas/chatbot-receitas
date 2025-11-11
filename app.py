from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"


def get_db_connection():
    """Estabelece conexão com o banco de dados SQLite."""
    conn = sqlite3.connect("receitas.db")
    conn.row_factory = sqlite3.Row
    return conn


def validar_login(username, password):
    """Valida credenciais do usuário."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE username = ?", (username,))
    resultado = cursor.fetchone()
    conn.close()
    
    return check_password_hash(resultado[0], password) if resultado else False


def obter_user_id(username):
    """Obtém o ID do usuário pelo username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


def buscar_receitas(termo):
    """Busca receitas por nome."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nome, ingredientes, modo_preparo FROM receitas WHERE nome LIKE ?",
        (f"%{termo}%",)
    )
    receitas = cursor.fetchall()
    conn.close()
    return receitas


def login_required(f):
    """Decorator que protege rotas que exigem autenticação."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/")
@login_required
def index():
    username = session.get("user")
    return render_template("index.html", username=username)


@app.route("/chat", methods=["POST"])
@login_required
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


@app.route("/lista", methods=["GET", "POST"])
@login_required
def lista():
    conn = get_db_connection()
    cursor = conn.cursor()

    page = int(request.args.get("page", 1))
    search = request.args.get("search", "").strip()
    per_page, offset = 10, (page - 1) * 10

    if request.method == "POST":
        cursor.execute(
            "INSERT INTO receitas (nome, ingredientes, modo_preparo) VALUES (?, ?, ?)",
            (request.form["nome"], request.form["ingredientes"], request.form["modo_preparo"])
        )
        conn.commit()
        return redirect(url_for("lista"))

    if search:
        cursor.execute("SELECT COUNT(*) FROM receitas WHERE nome LIKE ?", (f"%{search}%",))
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
    return render_template("lista.html", receitas=receitas, page=page, total_pages=total_pages)


@app.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get("next") or request.form.get("next") or url_for("index")
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if validar_login(username, password):
            session["user"] = username
            return redirect(next_page)
        
        return render_template("login.html", error="Usuário ou senha incorretos", next=next_page)

    return render_template("login.html", next=next_page)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        password_confirm = request.form.get("password_confirm", "").strip()

        if not username or len(username) < 3:
            return render_template("register.html", error="Usuário deve ter pelo menos 3 caracteres")

        if not password or len(password) < 6:
            return render_template("register.html", error="Senha deve ter pelo menos 6 caracteres")

        if password != password_confirm:
            return render_template("register.html", error="As senhas não coincidem")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            conn.close()
            return render_template("register.html", success="✓ Conta criada com sucesso! Faça login para continuar.")
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Este usuário já existe. Tente outro nome.")
        except Exception as e:
            conn.close()
            return render_template("register.html", error=f"Erro ao registrar: {str(e)}")

    return render_template("register.html")


@app.route("/minhas-receitas", methods=["GET", "POST"])
@login_required
def minhas_receitas():
    username = session.get("user")
    user_id = obter_user_id(username)
    
    if not user_id:
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    erro = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        ingredientes = request.form.get("ingredientes", "").strip()
        modo_preparo = request.form.get("modo_preparo", "").strip()
        
        if not nome or not ingredientes or not modo_preparo:
            erro = "Todos os campos são obrigatórios"
        else:
            try:
                cursor.execute(
                    "INSERT INTO receitas_personalizadas (user_id, nome, ingredientes, modo_preparo) VALUES (?, ?, ?, ?)",
                    (user_id, nome, ingredientes, modo_preparo)
                )
                conn.commit()
            except Exception as e:
                erro = f"Erro ao salvar receita: {str(e)}"
    
    cursor.execute(
        "SELECT id, nome, ingredientes, modo_preparo, criado_em FROM receitas_personalizadas WHERE user_id = ? ORDER BY criado_em DESC",
        (user_id,)
    )
    minhas_receitas_list = cursor.fetchall()
    conn.close()
    
    return render_template("minhas_receitas.html", receitas=minhas_receitas_list, erro=erro)


@app.route("/deletar-receita/<int:receita_id>", methods=["POST"])
@login_required
def deletar_receita(receita_id):
    username = session.get("user")
    user_id = obter_user_id(username)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id FROM receitas_personalizadas WHERE id = ? AND user_id = ?",
        (receita_id, user_id)
    )
    
    if cursor.fetchone():
        cursor.execute("DELETE FROM receitas_personalizadas WHERE id = ?", (receita_id,))
        conn.commit()
    
    conn.close()
    return redirect(url_for("minhas_receitas"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)