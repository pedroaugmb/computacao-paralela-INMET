import pandas as pd
from pathlib import Path

pasta_dados = Path("data/processed")
anos = ["2020", "2021", "2022", "2023", "2024", "2026"]


def encontrar_arquivos():
    arquivos = []
    for ano in anos:
        arquivos.extend((pasta_dados / ano).glob("*.CSV"))
        arquivos.extend((pasta_dados / ano).glob("*.csv"))

    arquivos = [arquivo for arquivo in arquivos if not (arquivo.parent.name == "2026" and "31-08-2026" in arquivo.name)]
    return arquivos


def carregar_dados(caminho):
    dados = pd.read_csv(
        caminho,
        sep=";",
        encoding="latin1",
        skiprows=8,
        decimal=",",
        na_values=["-9999", "-9999.0"],
        low_memory=False
    )

    dados.columns = dados.columns.str.strip()
    dados = dados.loc[:, ~dados.columns.str.startswith("Unnamed")]

    return dados


def processar_arquivo(caminho):
    dados = carregar_dados(caminho)

    return {
        "arquivo": caminho.name,
        "ano": caminho.parent.name,
        "linhas": len(dados),
        "dados": dados
    }


if __name__ == "__main__":
    arquivos = encontrar_arquivos()

    print(f"Arquivos encontrados: {len(arquivos)}")

    if arquivos:
        resultado = processar_arquivo(arquivos[0])

        print(f"Arquivo: {resultado['arquivo']}")
        print(f"Ano: {resultado['ano']}")
        print(f"Linhas: {resultado['linhas']}")
        print(resultado["dados"].head())