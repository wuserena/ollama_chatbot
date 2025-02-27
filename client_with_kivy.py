import requests
import threading
import queue
from camera_app import start_kivy_app
from speech_to_text import recognize_speech

response_queue = queue.Queue()
prompt_queue = queue.Queue()
chat_history = [{"role": "user", "content": "keep the answer under 100 words"}]
chat_history_lock = threading.Lock()  # Lock for thread-safe access to chat history

def chat_with_server():
    """Function to send user prompts to the server and get responses."""
    while True:
        prompt = prompt_queue.get()  # Wait for user input
        if prompt.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        url = "http://10.108.34.196:5000/chat"
        headers = {"Content-Type": "application/json"}

        with chat_history_lock:
            chat_history.append({"role": "user", "content": prompt})  # Add user message to history
            data = {"prompt": chat_history}  # Send the whole chat history correctly

        try:
            response = requests.post(url, json=data, stream=True)
            if response.status_code == 200:
                response_text = response.text.strip()
                response_queue.put(response_text)  # Send response to Kivy

                with chat_history_lock:
                    chat_history.append({"role": "assistant", "content": response_text})  # Store bot response

                print("Bot:", response_text)  # Print response
            else:
                print("Error:", response.json())
        except Exception as e:
            print(f"Request failed: {e}")

def start_chat():
    """Function to get user input and send it to the server."""
    while True:
        user_input = input("You: ")
        #user_input = recognize_speech()  # This should block until speech is recognized
        if user_input:  # Ensure there's valid input
            prompt_queue.put(user_input)

# Start threads for chat and Kivy
if __name__ == "__main__":
    # Start server communication thread
    server_thread = threading.Thread(target=chat_with_server, daemon=True)
    server_thread.start()

    # Start user input thread
    chat_thread = threading.Thread(target=start_chat, daemon=True)
    chat_thread.start()

    # Start Kivy app in the main thread
    start_kivy_app(response_queue)
