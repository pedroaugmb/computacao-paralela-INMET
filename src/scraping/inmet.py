import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

link = "https://portal.inmet.gov.br/dadoshistoricos"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"}
pasta = Path("data") / "raw" / "inmet"


def obter_links():
    requisicao = requests.get(link, headers=headers, timeout=30)
    requisicao.raise_for_status()
    site = BeautifulSoup(requisicao.text, "html.parser")
    doc = site.find_all("article", class_="post-preview")
    links = []

    for artigo in doc:
        link_tag = artigo.find("a")
        if link_tag:
            url = link_tag.get("href")
            if url:
                links.append(urljoin(link, url))

    return links


def baixar_dados():
    pasta.mkdir(parents=True, exist_ok=True)
    links = obter_links()
    print(f"{len(links)} arquivos encontrados.")

    for url in links:
        nome = url.split("/")[-1]
        caminho = pasta / nome

        if caminho.exists():
            print(f"O arquivo {nome} já existe. Pulando...")
            continue

        print(f"Baixando: {nome}")

        try:
            resposta = requests.get(url, headers=headers, stream=True, timeout=30)
            resposta.raise_for_status()

            with open(caminho, "wb") as f:
                for chunk in resposta.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"Salvo com sucesso em: {caminho}")

        except Exception as e:
            print(f"Erro ao tentar baixar {nome}. Detalhe: {e}")

        print("Aguardando 3 segundos...")
        time.sleep(3)


if __name__ == "__main__":
    baixar_dados()