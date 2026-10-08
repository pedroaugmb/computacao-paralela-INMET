from src.tasks.llm import consultar_llm, gerar_textos


def executar_llm_sequencial():
    textos = gerar_textos(20)
    resultados = []

    for texto in textos:
        resposta = consultar_llm(texto)

        resultados.append({
            "texto": texto,
            "resposta": resposta
        })

    return resultados