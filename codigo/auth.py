from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        senha_hash = generate_password_hash(senha)
        with database.conectar() as conexao:
            email_cad = conexao.execute("select email from usuarios where email = ?", (email,)).fetchone()
            if email_cad:
                return redirect(url_for('auth.registro'))
        database.criar_usuario(nome=nome, email=email, senha_hash=senha_hash)

        flash("Complete o cadastro usando database.py e generate_password_hash.")
        return redirect(url_for("auth.registro"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')

        with database.conectar() as conexao:
            senha_hash = conexao.execute("select senha_hash from usuarios where email = ?", (email,)).fetchone()
            usuario_id = conexao.execute('select id from usuarios where email = ?', (email,)).fetchone()
            usuario_nome = conexao.execute('select nome from usuarios where email = ?', (email,)).fetchone()
            email_cad = conexao.execute('select email from usuarios where email = ?', (email,)).fetchone()

        if email == email_cad and check_password_hash(senha_hash, senha):
            session['usuario_id'] = usuario_id
            session['usuario_nome'] = usuario_nome
        
        flash("Complete o login usando check_password_hash e session.")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    flash("Complete o logout removendo os dados da session.")
    return redirect(url_for("auth.login"))
