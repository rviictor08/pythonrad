import sqlite3

# Conecta ou cria o banco
con = sqlite3.connect("database.db")
cursor = con.cursor()

# Cria tabela USUÁRIOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipoUsuario INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    mudaSenha INTEGER DEFAULT 0,
    liberacao INTEGER DEFAULT 1
)
''')

# Cria tabela PERFIL
cursor.execute('''
CREATE TABLE IF NOT EXISTS perfil (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER NOT NULL,
    nome TEXT,
    contato TEXT,
    foto TEXT,
    FOREIGN KEY (userID) REFERENCES usuarios(id)
)
''')

# Confirma e fecha
con.commit()
con.close()

print("Banco de dados criado com as tabelas 'usuarios' e 'perfil'.")
