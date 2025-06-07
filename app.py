from flask import Flask, render_template, request, redirect, url_for, flash
from core.servico import ServicoDeTransacoes
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'chave-secreta'
servico = ServicoDeTransacoes()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/abrir_conta', methods=['GET', 'POST'])
def abrir_conta():
    if request.method == 'POST':
        try:
            id_conta = request.form['id_conta']
            agencia = request.form['agencia']
            numero = request.form['numero']
            moeda = request.form['moeda']
            saldo = float(request.form['saldo'])
            servico.abrir_conta(id_conta, agencia, numero, moeda, saldo)
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Erro: {e}', 'danger')
    return render_template('abrir_conta.html')

@app.route('/consultar_saldo', methods=['GET', 'POST'])
def consultar_saldo():
    saldo = None
    moeda = None
    if request.method == 'POST':
        try:
            id_conta = request.form['id_conta']
            saldo, moeda = servico.consultar_saldo(id_conta)
        except Exception as e:
            flash(f'Erro: {e}', 'danger')
    return render_template('consultar_saldo.html', saldo=saldo, moeda=moeda)

@app.route('/historico', methods=['GET', 'POST'])
def historico():
    transacoes = []
    if request.method == 'POST':
        try:
            id_conta = request.form['id_conta']
            transacoes = servico.listar_historico(id_conta)
        except Exception as e:
            flash(f'Erro: {e}', 'danger')
    return render_template('historico.html', transacoes=transacoes)

if __name__ == '__main__':
    app.run(debug=True)
