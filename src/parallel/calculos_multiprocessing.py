from multiprocessing import Pool, cpu_count
from src.tasks.calculos_matematicos import calcular_matriz

def executar_multiprocessing():
    with Pool(cpu_count()) as pool:
        return pool.map(calcular_matriz, [1000] * 10)