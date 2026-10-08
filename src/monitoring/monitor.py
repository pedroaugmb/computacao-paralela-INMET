import time
import psutil
import threading


def monitorar(funcao, *args, **kwargs):
    processo = psutil.Process()
    maior_cpu = 0

    executando = True

    def monitorar_cpu():
        nonlocal maior_cpu

        while executando:
            try:
                processos = [processo] + processo.children(recursive=True)
                cpu = 0

                for p in processos:
                    try:
                        cpu += p.cpu_percent(interval=0.1)
                    except psutil.NoSuchProcess:
                        pass

                maior_cpu = max(maior_cpu, cpu)

            except psutil.NoSuchProcess:
                break

    monitor = threading.Thread(target=monitorar_cpu)
    monitor.start()

    inicio = time.perf_counter()

    try:
        resultado = funcao(*args, **kwargs)
    finally:
        executando = False
        monitor.join()

    tempo_total = time.perf_counter() - inicio

    return {
        "resultado": resultado,
        "tempo": tempo_total,
        "cpu": maior_cpu
    }