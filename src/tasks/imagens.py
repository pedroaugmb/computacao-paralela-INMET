from PIL import Image, ImageFilter

def processar_imagem(caminho):
    imagem = Image.open(caminho)
    imagem = imagem.resize((800, 600))
    imagem = imagem.convert("L")
    imagem = imagem.filter(ImageFilter.GaussianBlur(2))
    imagem.load()
    return imagem