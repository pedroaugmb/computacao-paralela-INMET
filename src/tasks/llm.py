import os
import time
from groq import Groq, RateLimitError

modelo = "openai/gpt-oss-20b"


def consultar_llm(texto):
    cliente = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    for tentativa in range(5):
        try:
            resposta = cliente.chat.completions.create(
                model=modelo,
                messages=[
                    {
                        "role": "system",
                        "content": "Classifique o texto meteorológico como normal, quente ou extremo. Responda apenas com uma classificação."
                    },
                    {
                        "role": "user",
                        "content": texto
                    }
                ],
                temperature=0,
                max_completion_tokens=10
            )

            return resposta.choices[0].message.content.strip()

        except RateLimitError:
            time.sleep(3)

    raise RuntimeError("Limite da API atingido após várias tentativas.")


def gerar_textos(quantidade=5):
    textos = []

    for i in range(quantidade):
        temperatura = 25 + (i % 20)

        textos.append(
            f"Estação meteorológica registrou temperatura de {temperatura} °C."
        )

    return textos