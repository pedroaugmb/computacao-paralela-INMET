from src.monitoring.monitor import monitorar
from src.parallel.llm_sequencial import executar_llm_sequencial
from src.parallel.llm_threads import executar_llm_threads


def main():
    print("=== LLM SEQUENCIAL ===")

    resultado_sequencial = monitorar(executar_llm_sequencial)

    print(f"Tempo: {resultado_sequencial['tempo']:.2f} segundos")
    print(f"CPU máxima: {resultado_sequencial['cpu']:.2f}%")

    print("\n=== LLM THREADS ===")

    resultado_threads = monitorar(executar_llm_threads)

    print(f"Tempo: {resultado_threads['tempo']:.2f} segundos")
    print(f"CPU máxima: {resultado_threads['cpu']:.2f}%")


if __name__ == "__main__":
    main()