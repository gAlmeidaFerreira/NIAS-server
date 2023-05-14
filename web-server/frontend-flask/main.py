from flask import Flask, render_template, url_for
from flask.helpers import flash, redirect
from forms import Resgistrationform, LogInform, UploadFileForm
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '8ec624b940a6696b13c8f50c8bab331b'
app.config['UPLOAD_FOLDER'] = 'static/files'

#Pagina home
@app.route("/")
def homepage():
    return render_template("homepage.html")

#Pagina de contatos
@app.route("/contatos")
def contatos():
    return render_template("contatos.html", title="contatos")

#pagina de upload de arquivos
@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        flash(f'Arquivo {form.file.name} sumetido com sucesso!','success')
        return redirect(url_for('homepage'))
    return render_template("upload.html", title="Upload Files", form = form)

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