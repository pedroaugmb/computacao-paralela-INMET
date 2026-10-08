from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pandas as pd
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tasks.dados import encontrar_arquivos
from tasks.calculos import analisar_arquivo

pasta_resultados = Path("results")


def executar_threads():
    arquivos = encontrar_arquivos()
    threads = 10

    print(f"Arquivos encontrados: {len(arquivos)}")
    print(f"Threads utilizadas: {threads}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        resultados = list(executor.map(analisar_arquivo, arquivos))

    resultados = [resultado for resultado in resultados if resultado]

    df = pd.DataFrame(resultados)

    pasta_resultados.mkdir(parents=True, exist_ok=True)
    caminho_saida = pasta_resultados / "analise_temperatura_threads.csv"
    df.to_csv(caminho_saida, index=False, encoding="utf-8-sig")

    print("\nAnálise concluída.")
    print(f"Arquivos analisados: {len(df)}")
    print(f"Resultado salvo em: {caminho_saida}")

    return df


if __name__ == "__main__":
    executar_threads()