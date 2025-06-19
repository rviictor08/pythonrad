from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User, Perfil


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha, senha):
            if not user.liberacao:
                flash("Usuário ainda não autorizado. Aguarde a liberação.")
                return redirect(url_for("login"))

            login_user(user)

            if user.mudaSenha:
                flash("Por favor, altere sua senha.")
                return redirect(url_for("nova_senha"))

            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("home")
            return redirect(next_page)
        else:
            flash("Email ou senha inválidos")
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        # Verifica se o usuário já existe
        user_existente = User.query.filter_by(email=email).first()
        if user_existente:
            flash("Email já cadastrado")
        else:
            hashed_senha = generate_password_hash(senha)
            novo_usuario = User(email=email, senha=hashed_senha)
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Cadastro realizado com sucesso")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    profile = current_user.perfil
    if request.method == "POST":
        nome = request.form["nome"]
        contato = request.form["contato"]
        if profile:
            profile.nome = nome
            profile.contato = contato
        else:
            profile = Perfil(userID=current_user.id, nome=nome, contato=contato)
            db.session.add(profile)
        db.session.commit()
        flash("Perfil atualizado")
    return render_template("perfil.html", profile=profile)


@app.route("/nova_senha", methods=["GET", "POST"])
@login_required
def nova_senha():
    if request.method == "POST":
        nova_senha = request.form["nova_senha"]
        current_user.senha = generate_password_hash(nova_senha)
        current_user.mudaSenha = False
        db.session.commit()
        flash("Senha atualizada com sucesso")
        return redirect(url_for("home"))
    return render_template("nova_senha.html")
