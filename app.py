from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['POST'])
def display_file():
    file = request.files['file']
    if not file:
        return "No file"

    # Tenta ler o arquivo com diferentes codificações
    try:
        df = pd.read_csv(file, delimiter=";")
    except UnicodeDecodeError:
        file.seek(0)  # Reseta o ponteiro do arquivo
        try:
            df = pd.read_csv(file, encoding='latin1', delimiter=";")
        except UnicodeDecodeError:
            file.seek(0)  # Reseta o ponteiro do arquivo
            df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=";")

    # Renderiza o template com os dados do arquivo CSV
    return render_template('display.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

# Rota para simular erro 404 (para teste do Application Insights)
@app.route('/test-404')
def test_404():
    from flask import abort
    abort(404)

if __name__ == '__main__':
    # Para produção no Azure
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)