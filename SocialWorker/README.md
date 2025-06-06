
# Social Worker Chatbot 

📘 1. Personal Information Database
This module enables the chatbot to:

Track the patient’s medical history

Store personalized user profiles

Maintain awareness of health status and care concepts

It serves as the memory system, allowing the agent to provide contextually accurate and patient-specific responses.

🛠️ 2. Tool-Use Module
The tool-use module allows the chatbot to perform real-world tasks by calling system functions. Key capabilities include:

Saving user preferences and medical history

Scheduling and syncing reminders/events with the calendar

Managing ongoing reminders and notifications

Sending alerts for tasks or appointments

Recording and sharing memos with care teams

Contacting emergency services or healthcare professionals

Retrieving data from stored history or preferences

Accessing real-time information (e.g., weather, search queries)

Performing web searches upon patient request

These tools empower the chatbot to move beyond conversation and into actionable patient support.

💬 3. Conversation Flow Controller
This module classifies the user’s intent and guides the conversation across multiple topics, including:

Medical & functional information

Exercise & therapy routines

Greetings and small talk

Reminder setup and follow-up

Answering patient questions

Daily check-ins

Medication support

The flow controller dynamically selects the next conversational step based on the patient’s response. It coordinates with both the personal information database and the tool-use module to generate personalized, meaningful outputs.
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


