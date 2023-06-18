from flask import Flask, render_template, url_for, request
from flask.helpers import flash, redirect
from forms import Resgistrationform, LogInform, UploadFileForm
import pika
import os
import requests

#Declarando Variáveis
queue_producer_name = os.environ.get('QUEUE_PRODUCER_NAME')
queue_producer_port = os.environ.get('QUEUE_PRODUCER_PORT')
producer_url=f"http://{queue_producer_name}:{queue_producer_port}/product_message"

app = Flask(__name__)

app.config['SECRET_KEY'] = '8ec624b940a6696b13c8f50c8bab331b'
app.config['UPLOAD_FOLDER'] = 'static/files'

producer_url=f"http://{queue_producer_name}:{queue_producer_port}/product_message"

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
        response = requests.post(producer_url, file)
        if response.status_code == 200:
            print(response.json())
            flash(f'Arquivo {file.filename} submetido com sucesso!','success')
            return redirect(url_for('homepage'))
        else:
            print(response.json())
            flash(f'Falha ao enviar arquivo {file.filename}', 'error')
            return redirect(url_for('upload'))
    return render_template("upload.html", title="Upload Files", form = form)
    
#TODO: #2 Criar página para retornar o resultado dos códigos ao usuário

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
    app.run(host="0.0.0.0")