from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "clave-por-mientras-xd"

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/registro", methods=["GET","POST"])
def registro():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        usuario_existente = Usuario.query.filter_by(correo=correo).first()

        if usuario_existente:
            flash("El correo ya está registrado.", "error")
            return redirect(url_for("registro"))  

        password_hash = generate_password_hash(password)

        nuevo_usuario = Usuario(correo=correo, password_hash=password_hash)

        db.session.add(nuevo_usuario)

        db.session.commit()

        flash("Usuario registrado correctamente.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")
##REGISTER FIN

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            session["usuario"] = usuario.correo
            flash("Inicio de sesión correcto.", "success")
            return redirect(url_for("inicio"))
        else:
            flash("Correo o contraseña incorrectos.", "error")
    return render_template("login.html")
##LOGIN FIN

@app.route("/products")
def products():
    return render_template("products.html")
##PRODUCTS FIN

@app.route("/perfil")
def perfil():
    if "usuario" not in session:
        flash("Debes iniciar sesión para acceder a tu perfil.", "error")
        return redirect(url_for("login"))
    return render_template("perfil.html")
#PERFIL FIN

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("inicio"))
#LOGOUT FIN

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)