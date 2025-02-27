import requests
import threading
import pyttsx3
import time

engine = pyttsx3.init()

def speak_text(text):
    """Function to output speech"""
    engine.say(text)
    engine.runAndWait()

def chat_with_server(prompt):
    url = "http://10.108.34.196:5000/chat"
    headers = {"Content-Type": "application/json"}
    chat_history.append({"role": "user", "content": prompt})  # Add user message to history
    data = {"prompt": chat_history}  # Send full chat history
    response = requests.post(url, json=data, stream=True)

    if response.status_code == 200:
        print("Bot:", end=" ")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                print(chunk.decode("utf-8"), end="", flush=True)
        print()
    else:
        print("Error:", response.json())

if __name__ == "__main__":
    chat_history = []  # Initialize chat history

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break
        chat_with_server(user_input)