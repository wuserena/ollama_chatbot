# Chatbot with Deepseek-r1 Model  

This project creates a chatbot using MiniPupper to recognize speech and send it to a server, which uses the Deepseek-r1 model to generate responses. The system is also integrated with a camera for face detection, allowing it to track and follow the user by controlling a servo, enhancing interaction.

## System Environment  

* Running Chatbot  
  - **Operating System**: Windows 11  
  - **GPU**: NVIDIA GeForce RTX 2060  
  - **CUDA Version**: 12.7  
  - **Python Version**: 3.12  

* MiniPupper (Raspberry Pi Compute Module 4)  
  - **Screen:**  Displays the chatbot's responses.
  - **Servo:** Enables tracking of the user.
  - **Camera:** Used for face detection to track the user.
  - **Microphone:** (on MiniPupper) Captures speech for recognition.
  - **Speaker:** (on the screen) Outputs the chatbot’s responses for the user to hear.

## Requirements  

Install dependencies using:  

```sh
pip install -r requirements.txt
```

## Environment Setup

Build a virual environment to mangae the project
```sh
python -m venv ollama_env
ollama_env\Scripts\activate
pip install ollama
```

Download deepseek-r1 model on the local system

```sh
ollama pull deepseek-r1
```

## Requirements

Install them using:

```sh
pip install -r requirements.txt
```

##  Usage
1. Start the chatbot server
Run the server to generate responses:

```sh
python ollama_api.py
```

2. Run User interface on MiniPupper
Run this on MiniPupper to start voice recognition and launch the interactive user interface:

```sh
python client_with_kivy.py
```

## Run Sever
1. Setting system environment
 ```sh
set OLLAMA_HOST=http://0.0.0.0:11434
```
```sh
$env:OLLAMA_HOST = "http://0.0.0.0:11434"
```
2. Start running sever
```sh
ollama serve
```


