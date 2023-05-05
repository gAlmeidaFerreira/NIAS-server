from flask import Flask, render_template, url_for
from flask.helpers import flash, redirect
from forms import Resgistrationform, LogInform

app = Flask(__name__)

app.config['SECRET_KEY'] = '8ec624b940a6696b13c8f50c8bab331b'

#Pagina home
@app.route("/")
def homepage():
    return render_template("homepage.html")

#Pagina de contatos
@app.route("/contatos")
def contatos():
    return render_template("contatos.html", title="contatos")

#pagina de usuarios
@app.route("/usuarios/<nome_do_usuario>")
def usuarios(nome_do_usuario):
    return render_template("usuarios.html", nome_do_usuario=nome_do_usuario)

#Paginas de registro e login
@app.route("/register", methods=['GET','POST'])
def register():
    form = Resgistrationform()
    if form.validate_on_submit():
        flash(f'Conta criada com sucesso para {form.username.data}!', 'success')
        return redirect(url_for('homepage'))
    return render_template("register.html", title = "Register", form=form)

@app.route("/login")
def login():
    form = LogInform()
    return render_template("login.html", title = "LogIn", form=form)


#Colocar site no ar
if __name__ == "__main__":
    app.run(debug=True)