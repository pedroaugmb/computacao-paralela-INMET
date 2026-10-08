from multiprocessing import Pool
from pathlib import Path
from src.tasks.imagens import processar_imagem

def executar_multiprocessing():
    arquivos = list(Path("data/raw/imagens").rglob("*.jpg"))

    with Pool() as pool:
        return pool.map(processar_imagem, arquivos)