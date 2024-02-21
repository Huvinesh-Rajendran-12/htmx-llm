from flask import Flask, render_template, request, stream_with_context
import queue
from random import randint
from prompts import AssistantPrompt
import requests
from models import *
import uuid
import os
import json


USERNAME = "Teleme"
AI_NAME = "Teleme AI"
model_path = "TheBloke/medicine-chat-AWQ"
message_queue = queue.Queue()
messages  = [{"role":"system", "content":"You are a friendly healthcare assistant."}]
STREAM = True

AI_CHATBOT_URL = os.getenv("AI_CHATBOT_URL", "http://127.0.0.1:8080/v1/chat/completions")


app:"Flask" = Flask(__name__)


def chat_response(user_input:str, session_id:str):
    #max_new_tokens = 256
    #repetition_penalty = 1.2
    #temperature = .4
    #top_k = 50
    #stop_words = [f"{AI_NAME}:", f"{USERNAME}:", "</s>"]
    message_list = get_session_conversation(session_id=session_id)
    for message in message_list:
        messages.append({'role':'user', 'content': message.user_prompt})
        messages.append({'role':'assistant', 'content': message.llm_response})
    try:
        data = {
                "model": model_path,
                "messages": messages,
                "response_format": {"type": "json_object"},
                "stream": STREAM,
                }
        message_window = 15
        messages_string = messages[-message_window:]
        prompt = AssistantPrompt.format(user_input=user_input, messages=messages_string, ai_name=AI_NAME, username=USERNAME)
        res = requests.post(url=AI_CHATBOT_URL, stream=STREAM, data=json.dumps(data))
        message = ""
        for word in res.iter_content(chunk_size=5000, decode_unicode=True):     
            if word.strip()[6:] != "[DONE]":
                json_response = json.loads(s=word[6:])
                print(json_response)
                if 'content' in json_response['choices'][0]['delta']:
                    content = json_response['choices'][0]['delta']['content']
                    message += content
                    print(content)
                    yield(content)


    except Exception as e:
        response = f"Could not process response.\n\n{e}"
        print("Error: ", e)
        return response

@app.route("/")
def index():
    messages.clear()
    session_id = uuid.uuid4().hex 
    conversations = get_session_conversation(session_id=session_id)
    return render_template("index.html", username=USERNAME, ai_name=AI_NAME, session_id=session_id, conversations=conversations)

@app.route("/admin")
def admin():
    messages.clear()
    return render_template("admin.html", username=USERNAME, ai_name=AI_NAME)

@app.route("/chat_submit/<session_id>", methods=["POST"])
def chat_input(session_id:str):
    user_input = request.form.get("user_input")
    print(session_id)
    if not user_input:
        ai_response = "Error: Please Enter a Valid Input"
        current_response_id = f"gptblock{randint(67, 999999)}"
        return render_template("ai_response.html", ai_name=AI_NAME, ai_response=ai_response, hx_swap=False, current_response_id=current_response_id )
    
    message_queue.put(user_input)
    create_user_input(user_prompt=user_input, session_id=session_id)
    return "Success", 204 

@app.route('/stream/<session_id>')
def stream(session_id:str):
    def message_stream():
        global new_conversation

        while True:
            # If a message is present in the queue, send it to the clients
            if not message_queue.empty():
                user_message = message_queue.get()

                current_response_id = f"gptblock{randint(67, 999999)}"

                hx_swap = False

                message = ""
            
                for word in chat_response(user_message, session_id):
                    try:
                        message += word.replace("\n", "<br>")

                        ai_message = f"<p><strong>{ AI_NAME }</strong> : { message }</p>"

                        res = f"""data: <li class="text-white p-4 m-2 shadow-md rounded bg-gray-800 text-sm" id="{ current_response_id }" {"hx-swap-oob='true'" if hx_swap else ""}>{ai_message}</li>\n\n"""

                        hx_swap = True

                        print(f"{USERNAME}: {user_message}")
                        print(res)

                        yield res
        
                    except Exception as e:
                        print(e)
                        return e
                update_conversation(llm_response=message, session_id=session_id)
                    
    return app.response_class(stream_with_context(message_stream()), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9898)
