
# Social Worker Chatbot 

Our **LLM-based agent framework** integrates three key components:  
1. Personal Information Database  
2. Tool-Use Module  
3. Conversation Flow Controller  

### 1. Personal Information Database

This module allows the agent to:

- Track the patient’s medical history  
- Store personalized profiles  
- Maintain a contextual understanding of health status and care needs  

### 2. Tool-Use Module

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

### 3. Conversation Flow Controller

This module allows the agent to classify and transition between conversational topics such as:

- Patient Information: Medical & Functional
- Patient Information: Exercise & Therapy
- Greetings and Social Interaction
- Reminders and Notifications
- Answering Patient Questions
- Daily Check-Ins
- Medication Support

The conversation flow is dynamically driven by the patient’s input.  
The agent can invoke tools, take contextual actions, and generate personalized responses by referencing the personal database.

## System Environment   
  - **Operating System**: Windows 11  
  - **GPU**: NVIDIA GeForce RTX 2060

## Data Preparing

We simulate a conversation between two roles:

- **Assistant Model**: Acts like a helpful doctor. It uses a decision tree to ask structured, relevant questions based on patient responses.
- **Patient Model**: Plays the role of a real patient, providing diverse and realistic replies.

To train a large language model effectively, we need a substantial amount of dialogue data—especially with **variation in phrasing** for the same intent. To achieve this, we log and store each chat history iteration.

### Step 1: Generate Simulated Chat History
This script creates multiple conversation records between the assistant and patient models.

```sh
python create_dataset.py
```

###  Step 2: Combine All Chat Histories into One Dataset
Merges individual chat history into a single dataset ready for model training or fine-tuning.

```sh
python combine.py
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


