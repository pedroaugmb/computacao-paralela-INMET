import pandas as pd
from src.tasks.dados import processar_arquivo

coluna_temperatura = "TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"


def calcular_estatisticas(dados):
    temperatura = pd.to_numeric(dados[coluna_temperatura], errors="coerce").dropna()

    if temperatura.empty:
        return None

    limite_extremo = temperatura.quantile(0.95)

    return {
        "media": temperatura.mean(),
        "mediana": temperatura.median(),
        "minima": temperatura.min(),
        "maxima": temperatura.max(),
        "desvio_padrao": temperatura.std(),
        "percentil_95": limite_extremo,
        "eventos_extremos": (temperatura > limite_extremo).sum()
    }


def analisar_arquivo(caminho):
    resultado = processar_arquivo(caminho)
    estatisticas = calcular_estatisticas(resultado["dados"])

    if estatisticas is None:
        return None

    return {
        "arquivo": resultado["arquivo"],
        "ano": resultado["ano"],
        **estatisticas
    }