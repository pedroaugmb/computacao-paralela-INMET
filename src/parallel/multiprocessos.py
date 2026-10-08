from multiprocessing import Pool, cpu_count
from src.tasks.dados import encontrar_arquivos
from src.tasks.calculos import analisar_arquivo
from pathlib import Path
import pandas as pd
import sys

pasta_resultados = Path("results")


def executar_multiprocessing():
    arquivos = encontrar_arquivos()
    processos = cpu_count()

    print(f"Arquivos encontrados: {len(arquivos)}")
    print(f"Processos utilizados: {processos}")

    with Pool(processes=processos) as pool:
        resultados = pool.map(analisar_arquivo, arquivos, chunksize=50)

    resultados = [resultado for resultado in resultados if resultado]

    df = pd.DataFrame(resultados)

    pasta_resultados.mkdir(parents=True, exist_ok=True)
    caminho_saida = pasta_resultados / "analise_temperatura_multiprocessing.csv"
    df.to_csv(caminho_saida, index=False, encoding="utf-8-sig")

    print(f"\nAnálise concluída.")
    print(f"Arquivos analisados: {len(df)}")
    print(f"Resultado salvo em: {caminho_saida}")

    return df


if __name__ == "__main__":
    executar_multiprocessing()