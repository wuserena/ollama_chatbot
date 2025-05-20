import json
import os

session_id = 0
formatted_dataset = []

# Loop through all chat_history files
while os.path.exists(f'C:/Users/tut44419/research/ollama/occupational therapy/chat_history{session_id}.json'):
    with open(f'C:/Users/tut44419/research/ollama/occupational therapy/chat_history{session_id}.json', 'r') as f:
        chat_history = json.load(f)

    i = 0
    # Slide forward one turn at a time
    while i < len(chat_history) - 2:
        if (chat_history[i]["role"] == "assistant" and
            chat_history[i+1]["role"] == "user"):

            # Build input from: assistant → user
            input_text = (
                f"Assistant: {chat_history[i]['content'].strip()}\n"
                f"User: {chat_history[i+1]['content'].strip()}"
            )

            # Output is NEXT assistant reply if it exists
            if i+2 < len(chat_history) and chat_history[i+2]["role"] == "assistant":
                output_text = chat_history[i+2]["content"].strip()

                formatted_dataset.append({
                    "Instruction": "Gather occupational therapy patient information through a structured conversation.",
                    "input": input_text,
                    "output": output_text
                })

        i += 1

    print(f"✅ Processed session {session_id}")
    session_id += 1

# Save the final dataset
with open("./structured_dataset_occupational.json", "w") as f:
    json.dump(formatted_dataset, f, indent=2)

print(f"✅ Done! Created {len(formatted_dataset)} samples.")
