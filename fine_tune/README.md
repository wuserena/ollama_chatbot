# Deepseek Fine Tune Model

You can get the model [here](https://huggingface.co/SerenaWU/unsloth_deepseek.Q8_0.gguf).\
The model is trained using data from **Healthcare NLP: LLMs, Transformers, Datasets** available on [Kaggle](https://www.kaggle.com/datasets/jpmiller/layoutlm/data).

The code is retrieved from [here](https://github.com/unslothai/unsloth?tab=readme-ov-file)

## System Environment

- **Operating System**: WSL Ubuntu 24.04.1 LTS
- **GPU**: NVIDIA Geforce RTX 4090 Laptop

## Requirements

Install them using:

```sh
pip install -r requirements.txt
```
If you run on Windows, need to install:

```sh
pip install -U triton-windows
```


## Usage

To run the model with Ollama, use the following command:

```sh
ollama run hf.co/SerenaWU/unsloth_deepseek.Q8_0.gguf
