from flask import Flask, render_template, request

app = Flask(__name__)

# Página inicial
@app.route('/')
def index():
    return "Página Inicial"

# Página de cadastro (exibe o formulário)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')  # mostra o formulário
    elif request.method == 'POST':
        # Aqui você pode processar o cadastro (salvar no banco)
        email = request.form['email']
        senha = request.form['senha']
        # Aqui você pode chamar uma função para salvar os dados
        return "Usuário cadastrado com sucesso!"  # mensagem de confirmação ou redirecionar

if __name__ == '__main__':
    app.run(debug=True)