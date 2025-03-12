# Retrieve from: Kaggle QA with Gemma - KerasNLP Starter
# https://www.kaggle.com/code/awsaf49/kaggle-qa-with-gemma-kerasnlp-starter/notebook#Inference-after-fine-tuning
# Dataset: Healthcare NLP: LLMs, Transformers, Datasets (Models and medical data to promote data science in healthcare)
# https://www.kaggle.com/datasets/jpmiller/layoutlm/data


import os
import keras
import keras_hub
import json
import csv
import os

# Note: `userdata.get` is a Colab API. If you're not using Colab, set the env
# vars as appropriate for your system.
os.environ["KAGGLE_USERNAME"] = "wuyingting"
os.environ["KAGGLE_KEY"] = "e2cd889a77e197d70f2a86824f284604"

class CFG:
    seed = 42
    dataset_path = "./medquad.csv"
    present = "llama2_7b_en" # name of pretrained llama
    sequence_length = 256 # max size of input sequence for training
    learning_rate = 8e-5
    batch_size = 1 # size of the input batch in training, x 2 as two GPUs
    epochs = 1 # number of epochs to train
    weights_path = "./weights" # Path to save model weights

# Set environment variable to use CPU only
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

data = []

# Assuming the CSV file is named 'data.csv', and it contains two columns 'question' and 'answer'
with open(CFG.dataset_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # The 'question' in the CSV file corresponds to 'instruction' in the original JSON
        # The 'answer' in the CSV file corresponds to 'response' in the original JSON
        template = "Question:\n{question}\n\nAnswer:\n{answer}\n\nCategory:\n{focus_area}"
        data.append(template.format(**row))

# Use only the first 1000 training instances
data = data[:1000]

# Create the directory for saving weights if it doesn't exist
os.makedirs(CFG.weights_path, exist_ok=True)

llama_lm = keras_hub.models.LlamaCausalLM.from_preset(CFG.present)
# Enable LoRA for the model and set the LoRA rank to 4.
llama_lm.backbone.enable_lora(rank=4)

llama_lm.summary()

# Limit the input sequence length to 512 (to control memory usage).
llama_lm.preprocessor.sequence_length = CFG.sequence_length

# Compile the model with loss, optimizer, and metric
llama_lm.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.Adam(CFG.learning_rate),
    weighted_metrics=[keras.metrics.SparseCategoricalAccuracy()],
)

# Train the model
llama_lm.fit(data, epochs=CFG.epochs, batch_size=CFG.batch_size)

# Save the trained weights
# gemma_lm.save_weights(os.path.join(CFG.weights_path, "gemma_2b_weights.h5"))
llama_lm.save_to_preset(os.path.join(CFG.weights_path, "llama2_7b_weights.h5"))