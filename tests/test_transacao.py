from core.transacao import Transacao
from datetime import datetime

def teste_criacao_transacao():
    t1 = Transacao(
        tipo="credito",
        valor=100.0,
        moeda="BRL",
        descricao="Depósito inicial",
        categoria="Depósito"
    )
    print(t1)

    # Teste valor negativo - deve lançar exceção
    try:
        t2 = Transacao(
            tipo="debito",
            valor=-50.0,
            moeda="BRL",
            descricao="Saque",
            categoria="Caixa"
        )
    except ValueError as e:
        print(f"Erro esperado: {e}")

    # Teste tipo inválido - deve lançar exceção
    try:
        t3 = Transacao(
            tipo="tipo_invalido",
            valor=10.0,
            moeda="BRL"
        )
    except ValueError as e:
        print(f"Erro esperado: {e}")

if __name__ == "__main__":
    teste_criacao_transacao()
