from core.conta import Conta
from datetime import datetime, timedelta
import json
import os

class ServicoDeTransacoes:

    def __init__(self):
        self.caminho_arquivo = "contas.json"
        self.contas = self._carregar_contas()

    def _carregar_contas(self):
        if not os.path.exists(self.caminho_arquivo) or os.path.getsize(self.caminho_arquivo) == 0:
            return {}
        with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {id_: Conta.from_dict(c) for id_, c in data.items()}

    def _salvar_contas(self):
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump({id_: conta.to_dict() for id_, conta in self.contas.items()}, f, indent=4)

    def abrir_conta(self, id_conta, agencia, numero, moeda, saldo):
        if id_conta in self.contas:
            raise ValueError("Conta já existe.")
        self.contas[id_conta] = Conta(id_conta, agencia, numero, saldo, moeda)
        self._salvar_contas()

    def consultar_saldo(self, id_conta):
        conta = self._obter_conta(id_conta)
        return conta.saldo, conta.moeda_padrao

    def registrar_credito(self, id_conta, valor, moeda, data_hora, descricao, categoria=""):
        conta = self._obter_conta(id_conta)
        conta.registrar_credito(valor, moeda, data_hora, descricao, categoria)
        self._salvar_contas()

    def registrar_debito(self, id_conta, valor, moeda, data_hora, descricao, categoria=""):
        conta = self._obter_conta(id_conta)
        conta.registrar_debito(valor, moeda, data_hora, descricao, categoria)
        self._salvar_contas()

    def realizar_transferencia(self, origem_id, destino_id, valor, moeda, data_hora, descricao):
        origem = self._obter_conta(origem_id)
        destino = self._obter_conta(destino_id)
        origem.registrar_debito(valor, moeda, data_hora, f"Transferência para {destino_id}: {descricao}")
        destino.registrar_credito(valor, moeda, data_hora, f"Transferência de {origem_id}: {descricao}")
        self._salvar_contas()

    def listar_historico(self, id_conta):
        conta = self._obter_conta(id_conta)
        return conta.historico

    def listar_transacoes_por_tipo(self, id_conta, tipo, data_inicio, data_fim):
        conta = self._obter_conta(id_conta)
        fim_do_dia = datetime.combine(data_fim, datetime.max.time())
        return [t for t in conta.historico if t.tipo == tipo and data_inicio <= t.data_hora <= fim_do_dia]

    def calcular_saldo_em_data(self, id_conta, data_alvo):
        conta = self._obter_conta(id_conta)
        saldo = 0.0
        for t in sorted(conta.historico, key=lambda x: x.data_hora):
            if t.data_hora <= data_alvo:
                if t.tipo == "credito":
                    saldo += t.valor
                elif t.tipo == "debito":
                    saldo -= t.valor
        return saldo

    def encontrar_transacao_mais_valiosa(self, id_conta, tipo, data_inicio, data_fim):
        transacoes = self.listar_transacoes_por_tipo(id_conta, tipo, data_inicio, data_fim)
        if not transacoes:
            return None
        return max(transacoes, key=lambda t: t.valor)

    def _obter_conta(self, id_conta):
        if id_conta not in self.contas:
            raise ValueError("Conta não encontrada.")
        return self.contas[id_conta]
