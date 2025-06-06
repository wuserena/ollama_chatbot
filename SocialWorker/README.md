
# Social Worker Chatbot 

our LLM-based agent framework integrates three key components: a personal information database, a tool-use module, and a conversation flow controller. 

1. Personal Information Database
This module allows agents to track the patient's medical history, store personalized profiles, and maintain an understanding of core health and support concepts.

3. Tool-Use Module
Agents can access core system functions, including:
  1.	Saving user preferences and medical history 
  2.	Save reminder or event (sync calendar) 
  3.	Managing reminders and calendar events 
  4.	Providing notifications for tasks or appointments 
  5.	Recording and sharing memos with care teams 
  6.	Contacting emergency resources or healthcare professionals 
  7.	Pull out information from previously saved medical history or preferences 
  8.	Accessing real-time information (e.g., weather, web searches) 
  9.	Search web at patient’s request.  
These tools extend the agent's utility beyond conversation into real-world support tasks.

3. Conversation Flow Controller
This module enables the agent to classify and transition between different conversational topics, including:
  1.	Patient Information: Medical & Functional 
  2.	Patient Information: Exercise & Therapy 
  3.	Greetings 
  4.	Reminders 
  5.	Patient Questions 
  6.	Daily Check-Ins and  
  7.	Medication Support
     
The conversation flow is dynamically determined based on the patient's responses. The agent can invoke tools, take actions, and generate personalized recommendations and responses by referencing information from the personal database.


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


