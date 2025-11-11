import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("receitas.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

try:
    hashed_password = generate_password_hash("senha")
    cursor.execute(
        "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
        ("admin", hashed_password)
    )
    conn.commit()
    print("✓ Tabela de usuários criada com sucesso!")
    print("✓ Usuário admin adicionado (senha: senha)")
except sqlite3.IntegrityError:
    print("⚠ Usuário admin já existe no banco de dados")

conn.close()
