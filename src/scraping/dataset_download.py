import kagglehub

caminho = kagglehub.dataset_download("alxmamaev/flowers-recognition", output_dir="data/raw/imagens")

print(caminho)