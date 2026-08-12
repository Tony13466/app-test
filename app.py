from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "clave-por-mientras-xd"

USUARIO_PRUEBA = "hector@gmail.com"
PASSWORD_PRUEBA = "123456"

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        if correo == USUARIO_PRUEBA and password == PASSWORD_PRUEBA:
            session["usuario"] = correo
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

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)