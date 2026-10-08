from src.tasks.calculos_matematicos import calcular_matriz

def executar_sequencial():
    resultados = []
    for _ in range(10):
        resultados.append(calcular_matriz())
    return [calcular_matriz(1000) for _ in range(10)]