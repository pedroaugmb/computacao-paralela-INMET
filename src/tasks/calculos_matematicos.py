import numpy as np

def calcular_matriz(tamanho=500):
    a = np.random.rand(tamanho, tamanho)
    b = np.random.rand(tamanho, tamanho)
    return np.sum(a @ b)