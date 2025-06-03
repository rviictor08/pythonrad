# 🐍 Projeto PythonRAD  
### Desenvolvimento Rápido de Aplicações em Python - ARA0095

Este projeto foi desenvolvido como parte da disciplina **ARA0095 - Desenvolvimento Rápido de Aplicações em Python**, utilizando as tecnologias **Python 3.13+**, **Flask** e **SQLite**.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.13+**
- **Flask** (framework web)
- **SQLite** (banco de dados local via REST API)
- **HTML/CSS** (com foco em responsividade e visual moderno)

---

## 🧩 Funcionalidades Implementadas

### 🔐 Controle de Acesso (Login)

- Cadastro de novos usuários
- Login com verificação de e-mail e senha
- Perfil de usuário com:
  - Nome completo
  - Telefone de contato (WhatsApp)
  - Upload de foto
- Logout
- Mensagens de erro e sucesso com `Flask Flash`

### 📋 CRUD com Banco de Dados

- Tabelas utilizadas:

#### 📄 Tabela `usuarios`
| Campo       | Tipo               | Descrição                      |
|-------------|--------------------|-------------------------------|
| id          | INTEGER (PK)       | Identificador único            |
| tipoUsuario | BOOLEAN            | `0` para usuário, `1` para admin |
| email       | VARCHAR(50)        | E-mail do usuário              |
| senha       | VARCHAR(30)        | Senha do usuário               |
| mudaSenha   | BOOLEAN            | Se `1`, usuário deve alterar senha no login |
| liberacao   | BOOLEAN            | `1` para usuário ativo         |

#### 👤 Tabela `perfil`
| Campo   | Tipo         | Descrição                            |
|---------|--------------|---------------------------------------|
| id      | INTEGER (PK) | Identificador do perfil               |
| userID  | INTEGER (FK) | ID do usuário (chave estrangeira)     |
| nome    | VARCHAR(50)  | Nome completo                         |
| contato | VARCHAR(11)  | DDD + número (WhatsApp)               |
| foto    | TEXT         | Caminho da imagem no servidor         |

---

## 📦 Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/rviictor08/pythonrad
   cd pythonrad
