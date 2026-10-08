from src.monitoring.monitor import monitorar
from src.parallel.imagens_sequencial import executar_sequencial
from src.parallel.imagens_multiprocessing import executar_multiprocessing


def main():
    print("=== IMAGENS SEQUENCIAL ===")
    r = monitorar(executar_sequencial)
    print(f"Tempo: {r['tempo']:.2f}s")
    print(f"CPU máxima: {r['cpu']:.2f}%")

    print("\n=== IMAGENS MULTIPROCESSING ===")
    r = monitorar(executar_multiprocessing)
    print(f"Tempo: {r['tempo']:.2f}s")
    print(f"CPU máxima: {r['cpu']:.2f}%")


if __name__ == "__main__":
    main()