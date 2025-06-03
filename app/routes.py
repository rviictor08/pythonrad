from flask import Flask, render_template, request, redirect, url_for, flash, session

import os
import sqlite3

# Configuração do app Flask
app = Flask(__name__)
app.secret_key = "chave_secreta"
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def conectar_banco():
    return sqlite3.connect('database.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))  # corrigido
        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
                session['user_id'] = usuario[0]  # salva o ID do usuário na sessão
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for('dashboard'))
        else:
            flash("E-mail ou senha incorretos.", "danger")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Você precisa estar logado para acessar o dashboard.", "danger")
        return redirect(url_for('login'))

    user_id = session['user_id']

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome FROM perfil WHERE userID = ?", (user_id,))
    resultado = cursor.fetchone()
    conexao.close()

    nome_completo = resultado[0] if resultado else "Usuário"

    return render_template('dashboard.html', nome_completo=nome_completo)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Você saiu da conta com sucesso.", "success")
    return redirect(url_for('login'))


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        nome = request.form['nome']
        contato = request.form['contato']
        foto = request.files['foto']
        user_id = 1  # Simulação

        caminho_foto = None
        if foto:
            caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
            foto.save(caminho_foto)

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE perfil
            SET nome = ?, contato = ?, foto = ?
            WHERE userID = ?
        """, (nome, contato, caminho_foto, user_id))  # corrigido
        conexao.commit()
        conexao.close()

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('dashboard'))

    user_id = 1  # Simulação
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, contato, foto FROM perfil WHERE userID = ?", (user_id,))  # corrigido
    perfil = cursor.fetchone()
    conexao.close()

    if perfil is None:
        flash("Perfil não encontrado. Verifique se o usuário está cadastrado.", "danger")
        return redirect(url_for('dashboard'))

    return render_template('perfil.html', nome=perfil[0], contato=perfil[1], foto=perfil[2])

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        tipo_usuario = 0
        liberacao = 1

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO usuarios (email, senha, tipoUsuario, liberacao)
            VALUES (?, ?, ?, ?)
        """, (email, senha, tipo_usuario, liberacao))  # corrigido
        conexao.commit()
        conexao.close()

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
