from dataclasses import dataclass, field
from typing import List
from core.transacao import Transacao

@dataclass
class Conta:
    id: str
    agencia: str
    numero: str
    saldo: float
    moeda_padrao: str
    historico: List[Transacao] = field(default_factory=list)

    def registrar_credito(self, valor, moeda, data_hora, descricao, categoria=None):
        self.saldo += valor
        self.historico.append(Transacao("credito", valor, moeda, data_hora, descricao, categoria))

    def registrar_debito(self, valor, moeda, data_hora, descricao, categoria=None):
        if self.saldo < valor:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= valor
        self.historico.append(Transacao("debito", valor, moeda, data_hora, descricao, categoria))

    def to_dict(self):
        return {
            "id": self.id,
            "agencia": self.agencia,
            "numero": self.numero,
            "saldo": self.saldo,
            "moeda_padrao": self.moeda_padrao,
            "historico": [t.to_dict() for t in self.historico],
        }

    @staticmethod
    def from_dict(d):
        conta = Conta(
            d["id"], d["agencia"], d["numero"], d["saldo"], d["moeda_padrao"]
        )
        conta.historico = [Transacao.from_dict(t) for t in d["historico"]]
        return conta
