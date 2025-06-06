
# Social Worker Chatbot 
# 🧑‍⚕️ Social Worker Chatbot

Our **LLM-based agent framework** integrates three key components:  
1. Personal Information Database  
2. Tool-Use Module  
3. Conversation Flow Controller  

---

## 📘 1. Personal Information Database

This module allows the agent to:

- Track the patient’s medical history  
- Store personalized profiles  
- Maintain a contextual understanding of health status and care needs  

---

## 🛠️ 2. Tool-Use Module

Agents can access core system functions, including:

- Saving user preferences and medical history  
- Creating and syncing reminders or events to a calendar  
- Managing reminders and calendar entries  
- Providing notifications for tasks or appointments  
- Recording and sharing memos with care teams  
- Contacting emergency services or healthcare professionals  
- Retrieving stored medical history or user preferences  
- Accessing real-time information (e.g., weather, search results)  
- Performing web searches at the patient’s request  

> These tools extend the agent’s capabilities beyond conversation into real-world support tasks.

---

## 💬 3. Conversation Flow Controller

This module allows the agent to classify and transition between conversational topics such as:

- **Patient Information: Medical & Functional**  
- **Patient Information: Exercise & Therapy**  
- **Greetings and Social Interaction**  
- **Reminders and Notifications**  
- **Answering Patient Questions**  
- **Daily Check-Ins**  
- **Medication Support**  

The conversation flow is dynamically driven by the patient’s input.  
The agent can invoke tools, take contextual actions, and generate personalized responses by referencing the personal database.
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


