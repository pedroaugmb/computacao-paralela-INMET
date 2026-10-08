from pathlib import Path
from src.tasks.imagens import processar_imagem

def executar_sequencial():
    arquivos = list(Path("data/raw/imagens").rglob("*.jpg"))
    resultados = []

    for arquivo in arquivos:
        resultados.append(processar_imagem(arquivo))

    return resultados