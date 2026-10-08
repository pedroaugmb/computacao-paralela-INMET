import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.monitoring.monitor import monitorar
from src.parallel.threads import executar_threads
from src.parallel.multiprocessos import executar_multiprocessing
from src.tasks.dados import encontrar_arquivos
from src.tasks.calculos import analisar_arquivo


def executar_sequencial():
    arquivos = encontrar_arquivos()
    resultados = []

    print(f"Arquivos encontrados: {len(arquivos)}")

    for arquivo in arquivos:
        resultado = analisar_arquivo(arquivo)

        if resultado:
            resultados.append(resultado)

    return pd.DataFrame(resultados)


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "threads"

    if modo == "sequencial":
        funcao = executar_sequencial
    elif modo == "threads":
        funcao = executar_threads
    elif modo == "multiprocessing":
        funcao = executar_multiprocessing
    else:
        raise ValueError("Use: sequencial, threads ou multiprocessing")

    resultado = monitorar(funcao)

    print(f"\n=== RESULTADO {modo.upper()} ===")
    print(f"Tempo: {resultado['tempo']:.2f} segundos")
    print(f"CPU máxima: {resultado['cpu']:.2f}%")


if __name__ == "__main__":
    main()