import requests
import json
#from sample_function import get_current_weather, get_local_time 
chat_history = ""
END_KEYWORDS = ["goodbye", "thank you", "bye", "farewell", "thanks", "see you"]

'''
with open("C:/Users/tut44419/research/ollama/social worker/tool_definition.json", "r") as file:
    TOOL_DEFINITIONS = json.load(file)
'''
def get_current_weather(city):
    return f"The weather in {city} is sunny."

def get_local_time(city):
    return f"The local time in {city} is 3:00 PM."


TOOL_DEFINITIONS = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City to get weather for"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_local_time",
        "description": "Get the current time for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City to get time for"}
            },
            "required": ["city"]
        }
    }
]


def is_end_of_conversation(text):
    text = text.lower()
    return any(keyword in text for keyword in END_KEYWORDS)

def restart_conversation():
    global patient_history
    summary = chat_with_server("Can you summarize my upcoming therapy appointments, including the date, time, and location?")

    patient_history = ""
    start_chat("occupational therapy")

def chat_with_server(prompt):
    global chat_history
    chat_history += f"user: {prompt}\n"

    response = requests.post(
        "http://10.109.12.179:11434/api/generate",  # or http://localhost:5000 if using proxy
        json={
            "model": "deepseek-v2:16b",  #"hf.co/SerenaWU/model_ExerciseTherapy:Q8_0"
            "prompt": chat_history,
            "stream": False,
        }
    )

    chat_history += f"assistant: {response.json()['response']}\n"
    print(response.json()['response'])

    return response.json()['response']


def start_chat(therapy_type):
    initial_prompt = (
 
        #"Assume you are a helpful assistant supporting patients in managing their therapy schedules, and I am a patient. "
        #f"Please ask separately about my participation in {therapy_type}. Start the conversation by asking me questions to gather "
        #"information that will help better support my scheduling needs, asking only one question at a time. "
    
        f"You are an AI agent. If you don't konw the answer, please use the tool. Your available tools are: {TOOL_DEFINITIONS}. "
        "If you decide that you need to call one or more tools to answer, you should pass the tool request as a list in the following format:\n"
        "<function_call>[{\"function\": {\"name\": \"function_name\", \"arguments\": {\"parameter\": \"value\"}}}]</function_call>\n"
        "Example when you need to know the weather in a city:\n"
        "<function_call>[{\"function\": {\"name\": \"get_current_weather\", \"arguments\": {\"city\": \"New York\"}}}]</function_call>"
    )
    chat_with_server(initial_prompt)

def use_tools(tool_calls, tool_functions):
    tool_responses = []
    for tool_call in tool_calls:
        tool_name = tool_call["function"]["name"]
        arguments = tool_call["function"]["arguments"]
        if tool_name in tool_functions:
            result = tool_functions[tool_name](**arguments)
            tool_responses.append(str(result))
        else:
            raise KeyError(f"Function '{tool_name}' not found.")
    return "\n".join(tool_responses)


if __name__ == "__main__":
    functions = {tool["name"]: globals()[tool["name"]]for tool in TOOL_DEFINITIONS}
    start_chat("physical therapy")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break
        
        ans = chat_with_server(user_input)

        if "<function_call>" in ans:
            json_str = ans.split("<function_call>")[1].split("</function_call>")[0]
            tool_calls = json.loads(json_str)
            result = use_tools(tool_calls, functions)
            print(f"[Tool Response]: {result}")

        
        if is_end_of_conversation(user_input):
            print("\n[System]: Restarting new conversation!\n")
            restart_conversation()
