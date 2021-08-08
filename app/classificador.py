import spacy
import string
import re
from flask import Flask, request, render_template


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        query = request.form['query']
        if query:
            sentimento = process_model(query)
            return render_template('index.html', sentimento=sentimento)
    else:
        return render_template('index.html')


def process_model(texto):

    text_previsao = prepocessamento(texto)
    # carregando o modelo
    modelo = spacy.load('modelos')

    # obtendo resultado da previsao
    result_previssao = modelo(text_previsao).cats

    return result_previssao


def prepocessamento(texto):

    pln = spacy.load('pt')

    stop_words = spacy.lang.pt.stop_words.STOP_WORDS

    # letras maiuscula
    texto = texto.lower()

    # remocao do nome usuario
    texto = re.sub(r"@[A-Za-z0-9$-_@.&+]+", ' ', texto)

    # removemndo as urls
    texto = re.sub(r"https?://[A-Za-z0-9./]+", ' ', texto)

    # removendo espacos em branco
    texto = re.sub(r" +", ' ', texto)

    # removendo emoticons
    lista_emocoes = {
        ':)': 'emocaopositiva',
        ':d': 'emocaopositiva',
        ':(': 'emocaonegativa'
        }
    for emocao in lista_emocoes:
        texto = texto.replace(emocao, lista_emocoes[emocao])

    # lematizacao
    documento = pln(texto)
    lista = []

    for token in documento:
        lista.append(token.lemma_)

    # removendo stop_words e pontuacao
    lista = [
        palavra for palavra in lista
        if palavra not in stop_words and palavra not in string.punctuation
    ]
    lista = ' '.join([
        str(elemento) for elemento in lista if not elemento.isdigit()
    ])

    return lista


if __name__ == "__main__":
    app.run(debug=True)
