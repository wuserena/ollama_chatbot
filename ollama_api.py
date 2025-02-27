# Retriver from: https://github.com/anushkaspatil/llama3-chatbot/blob/master/chat.py

from flask import Flask, render_template, request, Response, stream_with_context
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)
MODEL_NAME = "deepseek-r1"  # Choose between: deepseek-r1, llama3, llama2
 # Set environment variable to enable GPU usage

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Parse incoming JSON request
        data = request.get_json()
        message = data.get("prompt", "")
        if not message:
            return {"error": "No prompt provided"}, 400

        response = ollama.chat(model=MODEL_NAME, messages=message, stream=False)

        return Response(response['message']['content'].split("\n")[-1], content_type='text/plain; charset=utf-8')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
