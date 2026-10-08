from concurrent.futures import ThreadPoolExecutor
from src.tasks.llm import consultar_llm, gerar_textos


def executar_llm_threads():
    textos = gerar_textos(10)
    threads = 3

    with ThreadPoolExecutor(max_workers=threads) as executor:
        respostas = list(executor.map(consultar_llm, textos))

    return [
        {
            "texto": texto,
            "resposta": resposta
        }
        for texto, resposta in zip(textos, respostas)
    ]