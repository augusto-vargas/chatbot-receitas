import sqlite3

conn = sqlite3.connect("receitas.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS receitas_personalizadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        ingredientes TEXT NOT NULL,
        modo_preparo TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES usuarios (id) ON DELETE CASCADE
    )
""")

conn.commit()
print("✓ Tabela receitas_personalizadas criada com sucesso!")
conn.close()
