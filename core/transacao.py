from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transacao:
    tipo: str
    valor: float
    moeda: str
    data_hora: datetime
    descricao: str
    categoria: str = ""

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "valor": self.valor,
            "moeda": self.moeda,
            "data_hora": self.data_hora.isoformat(),
            "descricao": self.descricao,
            "categoria": self.categoria,
        }

    @staticmethod
    def from_dict(d):
        return Transacao(
            d["tipo"],
            d["valor"],
            d["moeda"],
            datetime.fromisoformat(d["data_hora"]),
            d["descricao"],
            d.get("categoria", "")
        )
