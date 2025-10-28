import sqlite3

# Conectar ao banco
conn = sqlite3.connect("receitas.db")
cursor = conn.cursor()

# Criar tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS receitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    ingredientes TEXT NOT NULL,
    modo_preparo TEXT NOT NULL
)
""")

# Receitas 
receitas = [
    ("Sushi de Salmão", "Arroz para sushi, Salmão, Alga nori, Vinagre", "Enrole o arroz com salmão na alga e corte."),
    ("Tempurá de Legumes", "Legumes, Farinha, Água gelada, Óleo", "Passe os legumes na massa e frite."),
    ("Gnocchi de Batata", "Batata, Farinha de trigo, Ovo, Molho de tomate", "Misture batata com farinha, modele nhoques e cozinhe."),
    ("Rocambole de Carne", "Carne moída, Queijo, Presunto, Molho de tomate", "Modele a carne em formato de rocambole com recheio e asse."),
    ("Empanada", "Massa de empanada, Carne, Ovo, Azeitona", "Recheie a massa, dobre e asse ou frite."),
    ("Panetone", "Farinha de trigo, Frutas cristalizadas, Fermento, Açúcar", "Faça a massa, deixe crescer, adicione frutas e asse.")
]

# Inserir receitas
cursor.executemany("""
INSERT INTO receitas (nome, ingredientes, modo_preparo)
VALUES (?, ?, ?)
""", receitas)

# Remover receitas
#cursor.execute("DELETE FROM receitas WHERE nome = ?", ("Strogonoff de Frango",))

conn.commit()
conn.close()