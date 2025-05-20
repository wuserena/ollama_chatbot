import requests
import json
import pandas as pd
import os
from data_prepare import dialogues

URL = "http://10.109.12.179:11434/api/generate"
MODEL = "deepseek-v2:16b"   #"llama3:latest"
CHAT_HISTORY_FILE = './chat_history4.json'
patient_history = []
END_KEYWORDS = ["goodbye", "bye", "farewell", "see you", "end the current agent", "start a new conversation", "The conversation is complete", "<end>"]
session_id = 0
'''
with open("C:/Users/tut44419/research/ollama/social worker/tool_definition.json", "r") as file:
    TOOL_DEFINITIONS = json.load(file)'''
TOOL_DEFINITIONS = [{
        "name": "save_preference",
        "description": "Save user preference or summary string",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "A short summary including therapy type, day, time, location, and reminder method."
                }
            },
            "required": ["summary"]
        }
    }]


def is_end_of_conversation(text):
    text = text.lower()
    return any(keyword in text for keyword in END_KEYWORDS)

def get_chat_history_file():
    return f'./chat_history{session_id}.json'

def restart_conversation():
    global patient_history
    global session_id

    chat_history = load_chat_history()
    summary_prompt = (
        f"Please summarize the appointment reminder details from the chat history below:\n\n{chat_history}\n\n"
        f"Then call the following tool: {TOOL_DEFINITIONS}\n\n"
        "Use this exact format:\n"
        "<function_call>[{\"function\": {\"name\": \"save_preference\", \"arguments\": {\"summary\": \"Template\"}}}]</function_call>\n\n"
        "Fill in the `summary` using the following template (keep it under 15 words):\n"
        "  - Time:\n"
        "  - Day(s):\n"
        "  - Location Therapy type: therapy at home independently, at home with a therapist or other provider, or at a therapy clinic?\n"
        "  - Reminder method:"
    )


    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "prompt": summary_prompt,
            "stream": False
        }
    )
    assistant_reply = response.json()['response']

    chat = load_chat_history()

    if chat[-1]["role"] == "assistant":
        chat[-1]["content"] += "\n" + assistant_reply
        with open(get_chat_history_file(), 'w') as f:
            json.dump(chat, f, indent=2)
    else:
        save_chat_history("assistant", assistant_reply)

    session_id += 1  # First, increment session
    patient_history = []

    # Create a new empty file for new session
    with open(get_chat_history_file(), 'w') as f:
        json.dump([], f)

    # Re-run decision tree setup
    DecisionTree = decision_tree()
    start_chat(DecisionTree)
    patient_start_chat()



# Initialize an empty chat history file if not exists
if not os.path.exists((get_chat_history_file())):
    with open(get_chat_history_file(), 'w') as f:
        json.dump([], f)

def load_chat_history():
    with open(get_chat_history_file(), 'r') as f:
        return json.load(f)

def save_chat_history(role, content):
    """Properly append to existing history and save it."""
    history = load_chat_history()  # Load existing chat history (list)
    history.append({
        "role": role,
        "content": content
    })
    with open(get_chat_history_file(), 'w') as f:
        json.dump(history, f, indent=2)

def build_prompt():
    history = load_chat_history()
    return "\n\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])

def add_patient_chat(role, content):
    """Update both file and full running string."""
    patient_history.append({"role": role, "content": content})

'''
def decision_tree():
    create_decision_tree_prompt = (
        "You are a helpful assistant supporting patients in managing their speech therapy schedules.\n"
        "Please ask the following structured questions to gather information that will help better support them and their scheduling needs.\n"
        "Then, based on the information collected, draw a decision tree diagram showing how patients are guided through these questions.\n"
        "Information to collect:\n"
        "1. Are you currently doing any type of speech therapy? (Yes/No)\n"
        "2. If yes, what type of speech therapy are you doing? (Multiple-choice Question:Therapy at home independently, Therapy at home with a physical therapist or other provider, or Therapy at a physical therapy clinic\n"
        "3. Would you like to receive reminders for your appointments? (Yes/No)\n"
        "4. If yes, please share the time, day, and location of your appointments."
    )
'''
def decision_tree():
    all_dialogues = dialogues()
    dialogue_block = "\n".join([f"- {d}" for d in all_dialogues])

    create_decision_tree_prompt = (
        "You are an assistant helping patients manage their speech therapy schedules.\n"
        "Follow these steps:\n"
        "1. Review the example dialogues below. Each dialogue represents one complete interaction (or branch) in the decision tree.\n"
        f"Here are the example dialogues:\n\n{dialogue_block}"
        "2. Classify each assistant message as one of the following types:\n"
        "   - Yes/No Questions (Yes: continue to the next question; No: end the current agent)\n"
        "   - Multiple Choice Questions (Use the selected option to determine the next branch)\n"
        "   - User Information Input (Store the information or use it to call tools)\n"
        "   - Recommendations (Call tools or summarize based on collected input)\n"
        "3. Build a decision tree where each user reply leads to the appropriate next step.\n"
        "4. End each complete path in the decision tree with `<end>`.\n\n"
        "Please use the example dialogues to build a decision tree.\n\n"
    )

    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "prompt": create_decision_tree_prompt,
            "stream": False
        }
    )
    decision_tree = response.json()['response']

    #save_chat_history("user", create_decision_tree_prompt)
    return decision_tree

def start_chat(DecisionTree):
    initial_prompt = (
        "You are a helpful assistant managing a patient's speech therapy schedule.\n\n"
        "Use the decision tree to guide the conversation one step at a time.\n"
        "Ask only one short question at a time, based on the user's previous response.\n\n"
        "Information to collect:\n"
        "  1. Are you currently doing any type of speech therapy? (Yes/No Questions)\n"
        "  2. If yes, what type of speech therapy are you doing?\n"
        "   (Multiple Choice Questions: Therapy at home independently, Therapy at home with a therapist or other provider, or Therapy at a therapy clinic)\n"
        "  3. Would you like to receive reminders for your appointments? (Yes/No Questions)\n"
        "  4. If yes, please share the time, day, and location of your appointments.\n\n"
        f"The tools you can use are: {TOOL_DEFINITIONS}\n"
        "Call a tool when needed.\n"
        "Use this format:\n"
        "  <function_call>[{\"function\": {\"name\": \"tool_name\", \"arguments\": {\"parameters\": \"value\"}}}]</function_call>\n\n"
        "Mark the end of each complete path with `<end>`.\n\n"
        f"Here is the decision tree you should follow:\n\n{DecisionTree}\n"
        "Start by asking the first question."
    )
    save_chat_history("user", initial_prompt)

    full_prompt = build_prompt()

    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "prompt": full_prompt,
            "stream": False
        }
    )
    assistant_reply = response.json()['response']

    save_chat_history("assistant", assistant_reply)

def patient_start_chat():
    guide = load_chat_history()
    question = guide[-1]
    initial_prompt = (
        "Assume you are a patient, and I am a helpful assistant supporting patients in managing their speech therapy schedules.\n"
        "Please respond to my questions in under 10 words, as if you are a real patient."
        f"{question['content']}"
    )
    add_patient_chat("user", initial_prompt)

    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "prompt": initial_prompt,
            "stream": False
        }
    )
    patient_reply = response.json()['response']

    save_chat_history("user", patient_reply)
    add_patient_chat("assistant", patient_reply)

def doctor():
    full_prompt = build_prompt()

    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "prompt": full_prompt,
            "stream": False
        }
    )
    assistant_reply = response.json()['response']

    save_chat_history("assistant", assistant_reply)
    add_patient_chat("user", assistant_reply)
    # ✅ After patient replies, check if conversation should restart
    if is_end_of_conversation(assistant_reply):
        print("\n[System]: End detected. Restarting new conversation!\n")
        restart_conversation()

def patient():
    conversation = "\n\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in patient_history])

    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "prompt": conversation,
            "stream": False
        }
    )
    user_reply = response.json()['response']

    save_chat_history("user", user_reply)
    add_patient_chat("assistant", user_reply)

    # ✅ After patient replies, check if conversation should restart
    if is_end_of_conversation(user_reply):
        print("\n[System]: End detected. Restarting new conversation!\n")
        restart_conversation()

if __name__ == "__main__":

    DecisionTree = decision_tree()
    start_chat(DecisionTree)
    patient_start_chat()
    counter = 0

    for i in range(50):
        doctor()
        patient()

