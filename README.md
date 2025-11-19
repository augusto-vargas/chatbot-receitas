# 🍳 Chatbot de Receitas

Um aplicativo web completo para gerenciamento de receitas com autenticação de usuário, chatbot interativo e receitas personalizadas.

## ✨ Funcionalidades

- 🔐 **Autenticação Segura**: Registro e login com senhas criptografadas
- 💬 **Chatbot**: Busca interativa de receitas por ingredientes
- 📝 **Receitas Públicas**: Biblioteca de receitas compartilhadas
- 👤 **Receitas Personalizadas**: Cada usuário pode criar suas próprias receitas
- 🔍 **Busca e Paginação**: Encontre receitas facilmente
- 🗑️ **Gerenciamento**: Edite e delete suas receitas

## 🚀 Instalação

### Pré-requisitos

- Python 3.7+
- pip

### Passos

1. Clone ou baixe o projeto:

```bash
cd chatbot-receitas
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o banco de dados:

```bash
python setup.py
```

4. Inicie a aplicação:

```bash
python app.py
```

5. Acesse no navegador:

```
http://127.0.0.1:5000
```

## 📖 Uso

### Primeiro Acesso

1. Clique em **"Registre-se aqui"** para criar uma conta
2. Preencha os dados (usuário com mínimo 3 caracteres, senha com mínimo 6)
3. Faça login com suas credenciais

### Chatbot

- Navegue para a página inicial
- Digite um ingrediente ou nome de receita no chat
- O bot buscará e exibirá receitas correspondentes

### Minhas Receitas

- Clique em **"Minhas Receitas"** (botão verde)
- Preencha o formulário para criar uma nova receita
- Suas receitas aparecem na lista abaixo
- Clique no lixo (🗑️) para deletar

### Lista de Receitas

- Acesse **"Lista de Ingredientes"** para ver todas as receitas públicas
- Use a barra de busca para filtrar
- Navegue entre páginas com os botões de paginação

## 🏗️ Estrutura do Projeto

```
chatbot-receitas/
├── app.py                          # Aplicação Flask principal
├── setup.py                        # Script para criar tabelas e seeds
├── requirements.txt                # Dependências Python
├── receitas.db                     # Banco de dados SQLite
├── README.md                       # Este arquivo
├── static/
│   ├── style.css                   # Estilos globais
│   └── script.js                   # JavaScript do cliente
└── templates/
    ├── index.html                  # Página do chatbot
    ├── login.html                  # Página de login
    ├── register.html               # Página de registro
    ├── lista.html                  # Lista de receitas públicas
    └── minhas_receitas.html        # Receitas personalizadas
```

## 🔒 Segurança

- Senhas são criptografadas com Werkzeug
- Autenticação via sessão Flask
- Proteção de rotas com decorator `@login_required`
- Isolamento de dados por usuário no banco de dados

## 🎨 Interface

- Design moderno com tema escuro
- Responsivo e intuitivo
- Ícones Font Awesome
- Animações e transições suaves

## 🐛 Troubleshooting

### Flask não encontrado

```bash
pip install flask werkzeug
```

### Porta 5000 ocupada

```bash
# Modifique a última linha de app.py:
app.run(debug=True, port=5001)
```

## 📚 Tecnologias

- **Backend**: Flask, SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Segurança**: Werkzeug (hashing de senhas)
- **Banco de Dados**: SQLite

## 📄 Licença

Este projeto é de uso livre para fins educacionais.
