import sqlite3
from werkzeug.security import generate_password_hash

DB_FILE = "receitas.db"


def setup_database():
    """Cria todas as tabelas e insere dados iniciais."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Tabela de receitas públicas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            modo_preparo TEXT NOT NULL
        )
    """)

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de receitas personalizadas
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
    print("✓ Tabelas criadas com sucesso!")

    # Insere receitas públicas iniciais
    receitas = [
        ("Sushi de Salmão", "Arroz para sushi, Salmão, Alga nori, Vinagre", "Enrole o arroz com salmão na alga e corte."),
        ("Tempurá de Legumes", "Legumes, Farinha, Água gelada, Óleo", "Passe os legumes na massa e frite."),
        ("Gnocchi de Batata", "Batata, Farinha de trigo, Ovo, Molho de tomate", "Misture batata com farinha, modele nhoques e cozinhe."),
        ("Rocambole de Carne", "Carne moída, Queijo, Presunto, Molho de tomate", "Modele a carne em formato de rocambole com recheio e asse."),
        ("Empanada", "Massa de empanada, Carne, Ovo, Azeitona", "Recheie a massa, dobre e asse ou frite."),
        ("Panetone", "Farinha de trigo, Frutas cristalizadas, Fermento, Açúcar", "Faça a massa, deixe crescer, adicione frutas e asse."),
        ("Frango Assado", "Frango, Alho, Limão, Azeite, Sal, Pimenta", "Tempere o frango e asse em forno alto por 1 hora."),
        ("Frango Assado com Batatas", "Frango, Batatas, Alho, Alecrim, Azeite, Sal", "Tempere o frango e batatas, disponha na assadeira e asse por 1h30."),
        ("Lasanha à Bolonhesa", "Massa de lasanha, Carne moída, Molho de tomate, Queijo, Bechamel", "Monte camadas alternadas e asse por 40 minutos."),
        ("Risoto de Funghi", "Arroz arbóreo, Funghi secos, Caldo de legumes, Vinho branco, Queijo parmesão", "Refogue o arroz, adicione caldo aos poucos mexendo sempre até cremoso."),
        ("Strogonoff de Carne", "Carne em tiras, Creme de leite, Molho de tomate, Champignon, Mostarda", "Refogue a carne, adicione molhos e finalize com creme de leite."),
        ("Moqueca de Peixe", "Peixe, Leite de coco, Dendê, Tomate, Pimentão, Coentro", "Cozinhe o peixe com temperos e finalize com leite de coco e dendê."),
        ("Feijoada", "Feijão preto, Carnes de porco, Linguiça, Bacon, Louro, Alho", "Cozinhe o feijão com as carnes até ficarem macias."),
        ("Escondidinho de Carne Seca", "Carne seca, Mandioca, Queijo, Manteiga, Leite", "Faça purê de mandioca, adicione carne desfiada e cubra com queijo para gratinar."),
        ("Pão de Queijo", "Polvilho azedo, Queijo meia cura, Ovos, Leite, Óleo", "Misture todos ingredientes, faça bolinhas e asse até dourar."),
        ("Brigadeiro", "Leite condensado, Chocolate em pó, Manteiga, Granulado", "Cozinhe em fogo baixo mexendo sempre, espere esfriar e enrole."),
        ("Quindim", "Gemas, Açúcar, Coco ralado, Manteiga", "Bata as gemas com açúcar, adicione coco e asse em banho-maria."),
        ("Coxinha", "Frango desfiado, Massa de farinha de trigo, Catupiry, Ovos", "Recheie a massa com frango, modele e frite até dourar."),
        ("Acarajé", "Feijão fradinho, Cebola, Sal, Dendê, Camarão, Vatapá", "Bata o feijão, modele bolinhos e frite no dendê, recheie com vatapá."),
        ("Bobó de Camarão", "Camarão, Mandioca, Leite de coco, Dendê, Tomate, Pimentão", "Cozinhe a mandioca, faça purê e misture com camarão refogado."),
        ("Picanha na Brasa", "Picanha, Sal grosso", "Tempere com sal grosso e asse na brasa virando até o ponto desejado."),
        ("Pavê de Chocolate", "Biscoito maisena, Creme de chocolate, Leite condensado, Creme de leite", "Monte camadas alternadas de biscoito molhado e creme."),
        ("Torta de Limão", "Massa de biscoito, Leite condensado, Suco de limão, Creme de leite", "Faça a base de biscoito, adicione creme de limão e refrigere."),
        ("Bolo de Cenoura", "Cenoura, Ovos, Açúcar, Farinha de trigo, Chocolate em pó", "Bata cenoura com ovos, misture farinha e asse, cubra com chocolate."),
        ("Pudim de Leite", "Leite condensado, Leite, Ovos, Açúcar para calda", "Faça calda de açúcar, bata ingredientes e asse em banho-maria."),
        ("Salada Caesar", "Alface romana, Frango grelhado, Parmesão, Croutons, Molho caesar", "Monte a salada com alface, frango e finalize com molho e queijo."),
        ("Nhoque de Abóbora", "Abóbora, Farinha de trigo, Ovo, Queijo parmesão, Manteiga", "Cozinhe abóbora, faça massa com farinha, modele nhoques e cozinhe."),
        ("Bacalhau à Brás", "Bacalhau desfiado, Batata palha, Ovos, Cebola, Azeitona", "Refogue bacalhau com cebola, adicione ovos mexidos e batata palha."),
        ("Ratatouille", "Berinjela, Abobrinha, Pimentão, Tomate, Azeite, Ervas", "Corte legumes em rodelas finas, disponha em camadas e asse."),
        ("Sopa de Cebola", "Cebola, Caldo de carne, Pão, Queijo gruyere, Manteiga", "Caramelize cebolas, adicione caldo, sirva com pão e queijo gratinado.")
    ]

    cursor.execute("SELECT COUNT(*) FROM receitas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO receitas (nome, ingredientes, modo_preparo) VALUES (?, ?, ?)",
            receitas
        )
        conn.commit()
        print("✓ Receitas públicas inseridas!")
    else:
        print("⚠ Receitas já existem no banco")

    conn.close()
    print("\n✅ Setup concluído!")

if __name__ == "__main__":
    setup_database()
