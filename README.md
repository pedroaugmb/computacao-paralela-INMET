# Computação Paralela em Python: Análise de Desempenho

Trabalho acadêmico desenvolvido para a disciplina de **Computação Paralela**. O projeto implementa e avalia o desempenho de diferentes modelos de execução em Python — **Sequencial**, **Multithreading** (`concurrent.futures.ThreadPoolExecutor`) e **Multiprocessing** (`multiprocessing.Pool`) — aplicados a quatro cenários com diferentes características de carga de trabalho (I/O-bound e CPU-bound).

---

## 1. Tecnologias Utilizadas

* **Linguagem:** Python 3.14
* **Bibliotecas Principais:**
  * `pandas`: Leitura, tratamento e agregação tabular de dados meteorológicos.
  * `numpy`: Operações matriciais e álgebra linear.
  * `pillow`: Manipulação, redimensionamento e filtragem de imagens.
  * `groq`: Cliente oficial para requisições à API de inferência de LLMs da Groq.
  * `psutil`: Telemetria de processos do sistema operacional e medição agregada de CPU.
  * `requests` e `beautifulsoup4`: Scraping e download automatizado da série histórica do INMET.
  * `kagglehub`: Download automatizado do dataset de imagens via Kaggle.
* **Módulos Nativos:** `multiprocessing`, `concurrent.futures`, `threading`, `time`, `pathlib`, `os`, `sys`.

---

## 2. Estrutura do Projeto

```text
computacao-paralela-INMET/
├── data/                               # Dados brutos e processados (ignorado no Git)
│   ├── raw/
│   │   ├── inmet/                      # Arquivos ZIP anuais do INMET (2000 a 2026)
│   │   └── imagens/                    # Imagens do dataset de flores (Kaggle)
│   └── processed/                      # CSVs descompactados organizados por ano
├── results/                            # Saídas geradas pelos experimentos
│   ├── graphs/                         # Diretório para gráficos comparativos
│   ├── analise_temperatura.csv
│   ├── analise_temperatura_threads.csv
│   └── analise_temperatura_multiprocessing.csv
├── src/
│   ├── monitoring/                     # Módulo de monitoramento e testes
│   │   ├── monitor.py                  # Coletor de tempo e pico agregado de CPU
│   │   ├── teste_monitor.py            # Execução comparativa da tarefa do INMET
│   │   ├── teste_llm.py                # Execução comparativa da tarefa de LLM
│   │   ├── teste_calculo.py            # Execução comparativa da tarefa de cálculos
│   │   └── teste_imagens.py            # Execução comparativa da tarefa de imagens
│   ├── parallel/                       # Implementações sequenciais e paralelas
│   │   ├── threads.py                  # INMET via ThreadPoolExecutor
│   │   ├── multiprocessos.py           # INMET via multiprocessing.Pool
│   │   ├── llm_sequencial.py           # Chamadas à LLM em modo sequencial
│   │   ├── llm_threads.py              # Chamadas à LLM via ThreadPoolExecutor
│   │   ├── calculos_sequencial.py      # Multiplicação matricial sequencial
│   │   ├── calculos_multiprocessing.py # Multiplicação matricial via multiprocessing.Pool
│   │   ├── imagens_sequencial.py       # Pipeline de imagens sequencial
│   │   └── imagens_multiprocessing.py  # Pipeline de imagens via multiprocessing.Pool
│   ├── scraping/                       # Scripts de coleta de dados
│   │   ├── inmet.py                    # Download dos dados históricos do INMET
│   │   ├── extrair_zip.py              # Extração dos arquivos compactados
│   │   └── dataset_download.py         # Download do dataset de flores via kagglehub
│   └── tasks/                          # Lógica de negócio e processamento base
│       ├── dados.py                    # Leitura e parsing dos CSVs do INMET
│       ├── calculos.py                 # Estatísticas de temperatura do INMET
│       ├── llm.py                      # Integração com API Groq e prompts
│       ├── calculos_matematicos.py     # Multiplicação matricial com NumPy
│       └── imagens.py                  # Pipeline de imagem (resize, cinza, blur)
├── .env                                # Variáveis de ambiente locais (não versionado)
├── .gitignore                          # Regras de exclusão do repositório
├── main.py                             # Menu interativo principal para demonstração
├── README.md                           # Documentação do projeto
└── requirements.txt                    # Dependências externas do projeto
```

---

## 3. Descrição das 4 Tarefas

### Tarefa 1: Processamento de Dados Meteorológicos (INMET)
* **Objetivo:** Processar o histórico climático da rede de estações meteorológicas automáticas do INMET.
* **Carga:** Processamento de **6.474 arquivos CSV** (filtrando anos consolidados de 2020 a 2026).
* **Operações:** Leitura de arquivos com cabeçalhos duplos, normalização de datas/horas, limpeza de valores nulos/sentinela (`-9999`) e cálculo de média, mediana, desvio padrão, percentil 95 e contagem de eventos extremos de temperatura.
* **Comparação:** Sequencial $\times$ Threads (`ThreadPoolExecutor`) $\times$ Multiprocessing (`Pool`).

### Tarefa 2: Consultas a LLM (API Groq)
* **Objetivo:** Enviar textos descritivos meteorológicos para classificação de intensidade térmica (`normal`, `quente`, `extremo`) utilizando um Modelo de Linguagem de Grande Porte.
* **Perfil:** **I/O-bound** (tempo dominado por latência de rede e espera da resposta HTTP).
* **Modelo Utilizado:** `openai/gpt-oss-20b` via API da Groq.
* **Comparação:** Sequencial $\times$ Threads (`ThreadPoolExecutor`). Devido aos limites de taxa (*rate limit*) da API gratuita, o experimento padrão avalia 5 requisições controladas.

### Tarefa 3: Cálculos Matemáticos Intensivos
* **Objetivo:** Avaliar o comportamento de operações numéricas densas exclusivamente orientadas a processador.
* **Perfil:** **CPU-bound puro**.
* **Operação:** Geração e multiplicação de 10 pares de matrizes densas de dimensão $1.000 \times 1.000$ geradas aleatoriamente (`np.random.rand`), seguida de agregação por soma dos elementos resultantes.
* **Comparação:** Sequencial $\times$ Multiprocessing (`Pool`).

### Tarefa 4: Processamento em Lote de Imagens
* **Objetivo:** Executar um pipeline completo de visão computacional básica sobre um lote de imagens reais.
* **Perfil:** **CPU-bound / I/O misto**.
* **Dataset:** Imagens do conjunto *Flowers Recognition* do Kaggle (`alxmamaev/flowers-recognition`), armazenadas em `data/raw/imagens`.
* **Pipeline Aplicado a Cada Imagem:**
  1. Carregamento do arquivo via Pillow (`Image.open`);
  2. Redimensionamento para resolução padronizada de $800 \times 600$ pixels;
  3. Conversão para escala de cinza (`convert("L")`);
  4. Aplicação de filtro de desfoque gaussiano com raio 2 (`ImageFilter.GaussianBlur(2)`);
  5. Forçamento do processamento completo em memória (`imagem.load()`).
* **Comparação:** Sequencial $\times$ Multiprocessing (`Pool`).

---

## 4. Metodologia de Coleta de Métricas (Tempo e CPU)

Todas as medições são coordenadas pela função `monitorar` em [`src/monitoring/monitor.py`](src/monitoring/monitor.py):

* **Tempo Total de Execução:** Calculado através de `time.perf_counter()` entre o instante imediatamente anterior ao início da tarefa e o momento de sua conclusão.
* **CPU Máxima Agregada:** O monitoramento é executado por uma thread em segundo plano (`threading.Thread`) que consulta periodicamente o processo principal e todos os processos filhos gerados (`processo.children(recursive=True)`). Para cada processo ativo, lê-se `cpu_percent(interval=0.1)`. A soma do consumo instantâneo de todos os processos é comparada a cada iteração, registrando o valor de pico.
* **Interpretação da Escala de CPU:** Em sistemas operacionais modernos, cada núcleo físico ou lógico a 100% de utilização contribui com 100 pontos percentuais. Em uma CPU com 12 núcleos lógicos, o consumo agregado total pode alcançar até **1.200%**.

---

## 5. Resultados Registrados

Os testes consolidados obtiveram os seguintes desempenhos:

| Tarefa | Modo de Execução | Tempo Total | CPU Máxima Agregada | Observações / Speedup |
| :--- | :--- | :---: | :---: | :--- |
| **1. INMET** (6.474 arquivos) | Sequencial | 114,16 s | 124,80% | Baseline em 1 núcleo |
| | Threads | 96,61 s | 513,40% | Redução marginal limitada pelo GIL |
| | **Multiprocessing** | **50,77 s** | **1.095,30%** | **Speedup de ~2,25x** (uso de ~11 núcleos) |
| **2. LLM** (API Groq) | Sequencial | 8,80 s | 109,00% | Requisições síncronas bloqueantes |
| | **Threads** | **1,49 s** | **93,20%** | **Speedup de ~5,90x** (concorrência I/O) |
| **3. Imagens** (Dataset Flores) | Sequencial | 65,96 s | — | Baseline de processamento em lote |
| | **Multiprocessing** | **37,82 s** | — | **Speedup de ~1,74x** |
| **4. Cálculos Matemáticos** | Sequencial $\times$ Multi | *Aferir localmente* | *Aferir localmente* | Execute `teste_calculo.py` para medir no hardware local |

### Interpretação dos Resultados:
1. **Tarefas I/O-bound (LLM):** Apresentam o maior ganho com **Threads** (~5,9x). Enquanto uma thread aguarda o retorno da rede do provedor Groq, outras disparam requisições sem que o GIL represente gargalo, consumindo pouca CPU global.
2. **Tarefas CPU-bound (INMET, Imagens, Matrizes):** Em processamento massivo de arquivos e transformações de dados em Python, as Threads sofrem interferência do GIL (*Global Interpreter Lock*). O **Multiprocessing** contorna essa limitação criando processos independentes com instâncias próprias do interpretador Python, escalando o uso de CPU para perto do teto de hardware (~1.100%) e reduzindo o tempo à metade ou menos.

---

## 6. Instalação e Configuração

### Pré-requisitos
* Python 3.10 ou superior (testado no Python 3.14).
* Chave de acesso à API da Groq ([console.groq.com](https://console.groq.com)).

### 1. Clonar o repositório e criar o ambiente virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar ambiente virtual (Linux / macOS)
source venv/bin/activate
```

### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar a Chave da API (`GROQ_API_KEY`)
A tarefa de LLM necessita da variável de ambiente `GROQ_API_KEY`. **Nunca commite sua chave no código ou no GitHub.**

* **Opção 1 (Via terminal - Windows PowerShell):**
  ```powershell
  $env:GROQ_API_KEY="gsk_suachaveaqui"
  ```
* **Opção 2 (Via terminal - Linux/macOS):**
  ```bash
  export GROQ_API_KEY="gsk_suachaveaqui"
  ```
* **Opção 3 (Arquivo `.env` na raiz):**
  Crie um arquivo `.env` na raiz do projeto (já configurado no `.gitignore`):
  ```env
  GROQ_API_KEY=gsk_suachaveaqui
  ```

### 4. Obtenção dos Datasets (Opcional se já presentes)
* **Dados INMET:** Podem ser obtidos executando `python -m src.scraping.inmet` e extraídos com `python -m src.scraping.extrair_zip`.
* **Dataset de Imagens:** Pode ser baixado automaticamente com `python -m src.scraping.dataset_download` (requer conta no Kaggle para autenticação do `kagglehub`).

---

## 7. Como Executar

### Demonstração Interativa Principal (`main.py`)
Para apresentar os experimentos de forma centralizada:

```bash
python main.py
```

O programa exibirá um menu no terminal:
```text
=== COMPUTAÇÃO PARALELA ===
1 - Processamento de dados INMET
2 - Consultas a LLM
3 - Cálculos matemáticos
4 - Processamento de imagens
0 - Sair
```

### Execução Individual de Cada Tarefa
Cada teste comparativo pode ser disparado de forma isolada diretamente pelo módulo de monitoramento correspondente:

* **INMET (Permite escolher o modo via argumento):**
  ```bash
  # Executa modo sequencial
  python -m src.monitoring.teste_monitor sequencial

  # Executa com threads (padrão)
  python -m src.monitoring.teste_monitor threads

  # Executa com multiprocessing
  python -m src.monitoring.teste_monitor multiprocessing
  ```

* **LLM (Compara Sequencial e Threads):**
  ```bash
  python -m src.monitoring.teste_llm
  ```

* **Cálculos Matemáticos (Compara Sequencial e Multiprocessing):**
  ```bash
  python -m src.monitoring.teste_calculo
  ```

* **Processamento de Imagens (Compara Sequencial e Multiprocessing):**
  ```bash
  python -m src.monitoring.teste_imagens
  ```

