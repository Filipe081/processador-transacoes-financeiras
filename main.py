
from core.servico import ServicoDeTransacoes
from datetime import datetime
import os

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def exibir_menu():
    print("\n--- MENU ---")
    print("1. Abrir nova conta")
    print("2. Consultar saldo")
    print("3. Registrar crédito")
    print("4. Registrar débito")
    print("5. Realizar transferência")
    print("6. Ver histórico da conta")
    print("7. Listar transações por tipo e período")
    print("8. Calcular saldo em uma data específica")
    print("9. Encontrar transação mais valiosa")
    print("0. Sair")

def main():
    servico = ServicoDeTransacoes()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        try:
            if opcao == "1":
                id_conta = input("ID da conta: ")
                agencia = input("Número da agência: ")
                numero_conta = input("Número da conta: ")
                moeda = input("Moeda padrão (ex: BRL): ")
                saldo_inicial = float(input("Saldo inicial: "))
                servico.abrir_conta(id_conta, agencia, numero_conta, moeda, saldo_inicial)
                print("✅ Conta criada com sucesso!")
                input("Pressione Enter para continuar...")

            elif opcao == "2":
                id_conta = input("ID da conta: ")
                saldo, moeda = servico.consultar_saldo(id_conta)
                print(f"💰 Saldo atual: {saldo} {moeda}")
                input("Pressione Enter para continuar...")

            elif opcao == "3":
                id_conta = input("ID da conta: ")
                valor = float(input("Valor do crédito: "))
                moeda = input("Moeda: ")
                descricao = input("Descrição: ")
                categoria = input("Categoria (opcional): ")
                servico.registrar_credito(id_conta, valor, moeda, datetime.now(), descricao, categoria)
                print("✅ Crédito registrado com sucesso!")
                input("Pressione Enter para continuar...")

            elif opcao == "4":
                id_conta = input("ID da conta: ")
                valor = float(input("Valor do débito: "))
                moeda = input("Moeda: ")
                descricao = input("Descrição: ")
                categoria = input("Categoria (opcional): ")
                servico.registrar_debito(id_conta, valor, moeda, datetime.now(), descricao, categoria)
                print("✅ Débito registrado com sucesso!")
                input("Pressione Enter para continuar...")

            elif opcao == "5":
                origem = input("ID da conta de origem: ")
                destino = input("ID da conta de destino: ")
                valor = float(input("Valor da transferência: "))
                moeda = input("Moeda: ")
                descricao = input("Descrição: ")
                servico.realizar_transferencia(origem, destino, valor, moeda, datetime.now(), descricao)
                print("✅ Transferência realizada com sucesso!")
                input("Pressione Enter para continuar...")

            elif opcao == "6":
                id_conta = input("ID da conta: ")
                historico = servico.listar_historico(id_conta)
                if not historico:
                    print("📭 Nenhuma transação encontrada.")
                else:
                    for t in historico:
                        print(f"{t.data_hora} - {t.tipo} - {t.valor} {t.moeda} - {t.descricao} [{t.categoria}]")
                input("Pressione Enter para continuar...")

            elif opcao == "7":
                id_conta = input("ID da conta: ")
                tipo = input("Tipo de transação (ex: credito, debito, transferencia_enviada, transferencia_recebida): ")
                data_inicio = input("Data início (DD-MM-AAAA): ")
                data_fim = input("Data fim (DD-MM-AAAA): ")

                dt_inicio = datetime.strptime(data_inicio, "%d-%m-%Y")
                dt_fim = datetime.strptime(data_fim, "%d-%m-%Y").replace(hour=23, minute=59, second=59, microsecond=999999)

                transacoes = servico.listar_transacoes_por_tipo(id_conta, tipo, dt_inicio, dt_fim)
                if not transacoes:
                    print("📭 Nenhuma transação encontrada.")
                else:
                    print("\n📋 Transações encontradas:")
                    for t in transacoes:
                        print(f"{t.data_hora} - {t.tipo} - {t.valor} {t.moeda} - {t.descricao} [{t.categoria}]")
                input("Pressione Enter para continuar...")

            elif opcao == "8":
                id_conta = input("ID da conta: ")
                data_str = input("Data (DD-MM-AAAA): ")
                data_alvo = datetime.strptime(data_str, "%d-%m-%Y").replace(hour=23, minute=59, second=59, microsecond=999999)
                saldo = servico.calcular_saldo_em_data(id_conta, data_alvo)
                moeda = servico.contas[id_conta].moeda_padrao
                print(f"💼 Saldo em {data_alvo.date()}: {saldo:.2f} {moeda}")
                input("Pressione Enter para continuar...")

            elif opcao == "9":
                id_conta = input("ID da conta: ")
                tipo = input("Tipo da transação (ex: credito, debito): ")
                data_inicio = input("Data início (DD-MM-AAAA): ")
                data_fim = input("Data fim (DD-MM-AAAA): ")

                dt_inicio = datetime.strptime(data_inicio, "%d-%m-%Y")
                dt_fim = datetime.strptime(data_fim, "%d-%m-%Y").replace(hour=23, minute=59, second=59, microsecond=999999)

                transacao = servico.encontrar_transacao_mais_valiosa(id_conta, tipo, dt_inicio, dt_fim)
                if not transacao:
                    print("📭 Nenhuma transação encontrada.")
                else:
                    print("💎 Transação mais valiosa:")
                    print(f"{transacao.data_hora} - {transacao.tipo} - {transacao.valor} {transacao.moeda} - {transacao.descricao} [{transacao.categoria}]")
                input("Pressione Enter para continuar...")

            elif opcao == "0":
                print("👋 Encerrando o sistema.")
                break

            else:
                print("⚠️ Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

        except Exception as e:
            print(f"❌ Erro: {e}")
            input("Pressione Enter para continuar...")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
