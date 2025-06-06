
# Social Worker Chatbot 

Our LLM-based agent framework integrates three key components:
a personal information database, a tool-use module, and a conversation flow controller.

1. Personal Information Database
This module enables the agent to track a patient's medical history, store personalized profiles, and maintain an understanding of essential health and support information.

2. Tool-Use Module
The agent can interact with system-level tools to perform real-world support tasks, including:

Saving user preferences and medical history

Creating and syncing calendar events

Managing reminders and appointments

Sending notifications for upcoming tasks or activities

Recording and sharing memos with care teams

Contacting emergency services or healthcare professionals

Retrieving saved medical history or preference data

Accessing real-time information (e.g., weather, news, or web searches)

Performing web searches on the patient’s behalf

These tools enhance the agent's capability beyond dialogue, enabling proactive support in daily care.

3. Conversation Flow Controller
This component allows the agent to recognize and transition between various conversation topics, such as:

Patient Information: Medical & Functional

Patient Information: Exercise & Therapy

Greetings

Reminders

Patient Questions

Daily Check-Ins

Medication Support

The conversation flow is dynamically guided by the patient's responses. The agent can invoke tools, take actions, and generate personalized responses by referencing the personal information database.

## System Environment  

* Running Chatbot  
  - **Operating System**: Windows 11  
  - **GPU**: NVIDIA GeForce RTX 2060

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

## Run Serve
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


