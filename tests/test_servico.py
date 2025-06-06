import unittest
from datetime import datetime
from core.servico import ServicoDeTransacoes, ContaNaoEncontradaException, SaldoInsuficienteException

class TestServicoDeTransacoes(unittest.TestCase):

    def setUp(self):
        self.servico = ServicoDeTransacoes()
        self.conta1_id = "conta1"
        self.conta2_id = "conta2"
        self.servico.abrir_conta(self.conta1_id, "0001", "123456-7", "BRL", 1000.0)
        self.servico.abrir_conta(self.conta2_id, "0002", "765432-1", "BRL", 500.0)

    def test_abrir_conta_e_consultar_saldo(self):
        saldo = self.servico.consultar_saldo(self.conta1_id)
        self.assertEqual(saldo, 1000.0)

    def test_registrar_credito(self):
        self.servico.registrar_credito(self.conta1_id, 200.0, "BRL", datetime.now(), "Depósito")
        saldo = self.servico.consultar_saldo(self.conta1_id)
        self.assertEqual(saldo, 1200.0)

    def test_registrar_debito(self):
        self.servico.registrar_debito(self.conta1_id, 300.0, "BRL", datetime.now(), "Pagamento")
        saldo = self.servico.consultar_saldo(self.conta1_id)
        self.assertEqual(saldo, 700.0)

    def test_registrar_debito_saldo_insuficiente(self):
        with self.assertRaises(SaldoInsuficienteException):
            self.servico.registrar_debito(self.conta2_id, 600.0, "BRL", datetime.now(), "Pagamento")

    def test_realizar_transferencia(self):
        self.servico.realizar_transferencia(self.conta1_id, self.conta2_id, 400.0, "BRL", datetime.now(), "Transferência")
        saldo_origem = self.servico.consultar_saldo(self.conta1_id)
        saldo_destino = self.servico.consultar_saldo(self.conta2_id)
        self.assertEqual(saldo_origem, 600.0)
        self.assertEqual(saldo_destino, 900.0)

    def test_conta_nao_encontrada(self):
        with self.assertRaises(ContaNaoEncontradaException):
            self.servico.consultar_saldo("conta_inexistente")

    def test_valor_negativo(self):
        with self.assertRaises(ValueError):
            self.servico.registrar_credito(self.conta1_id, -100.0, "BRL", datetime.now(), "Erro")

if __name__ == "__main__":
    unittest.main()
