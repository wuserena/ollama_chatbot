import pandas as pd
import numpy as np

def dialogues():
    # Load and clean data
    data = pd.read_excel("C:/Users/tut44419/research/ollama/social worker/Conversation Flows.xlsx", header=None)
    cleaned_df = data.fillna(method="ffill")

    # Extract rows 6 to 10 and desired columns
    dataset = cleaned_df[6:11]
    dataset = dataset.iloc[:, 19:]

    # Replace part of row 10 with actual NaN values
    dataset.loc[10, dataset.columns[2:]] = np.nan

    # Prepare output list
    all_dialogues = []

    # Loop through each row (6 to 10)
    for idx in dataset.index:
        row = dataset.loc[idx].dropna().astype(str).tolist()
        dialogue = []
        for i in range(0, len(row), 2):
            assistant = f"Assistant: {row[i]}"
            if i + 1 < len(row):
                user_response = row[i + 1]
                if user_response.strip().startswith("{") and user_response.strip().endswith("}"):
                    user = f"Action: {user_response.strip()}"
                else:
                    user = f"User: {user_response.strip()}"
            else:
                user = ""
            dialogue.extend([assistant, user])
        all_dialogues.append("\t".join(dialogue))

    return all_dialogues
    
'''
if __name__ == '__main__':
    all_dialogues = dialogues()
    print(all_dialogues[0], all_dialogues[-1])
'''
