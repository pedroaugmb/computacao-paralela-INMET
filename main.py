from src.monitoring.teste_monitor import main as tarefa_inmet
from src.monitoring.teste_llm import main as tarefa_llm
from src.monitoring.teste_calculo import main as tarefa_calculo
from src.monitoring.teste_imagens import main as tarefa_imagens


def main():
    print("=== COMPUTAÇÃO PARALELA ===")
    print("1 - Processamento de dados INMET")
    print("2 - Consultas a LLM")
    print("3 - Cálculos matemáticos")
    print("4 - Processamento de imagens")
    print("0 - Sair")

    opcao = input("\nEscolha uma tarefa: ")

    if opcao == "1":
        tarefa_inmet()
    elif opcao == "2":
        tarefa_llm()
    elif opcao == "3":
        tarefa_calculo()
    elif opcao == "4":
        tarefa_imagens()
    elif opcao == "0":
        print("Encerrando...")
    else:
        print("Opção inválida.")


if __name__ == "__main__":
    main()