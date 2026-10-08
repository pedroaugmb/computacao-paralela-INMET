import zipfile
from pathlib import Path


PASTA_RAW = Path("data") / "raw" / "inmet"
PASTA_PROCESSED = Path("data") / "processed"


def extrair_arquivos():

    PASTA_PROCESSED.mkdir(parents=True, exist_ok=True)
    arquivos_zip = list(PASTA_RAW.glob("*.zip"))

    print(f"{len(arquivos_zip)} arquivos ZIP encontrados.")

    for arquivo_zip in arquivos_zip:

        pasta_destino = (PASTA_PROCESSED / arquivo_zip.stem)
        pasta_destino.mkdir(parents=True, exist_ok=True)

        print(f"Extraindo: {arquivo_zip.name}")

        with zipfile.ZipFile(arquivo_zip,"r") as arquivo:
            arquivo.extractall(pasta_destino)

        print(f"Extraído em: {pasta_destino}")


if __name__ == "__main__":
    extrair_arquivos()