from flask import Flask, jsonify, request
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Initialize sentiment analysis model
sentiment_tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
sentiment_model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-emotion")

# Initialize dialogue generation model
tokenizer = AutoTokenizer.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")
model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")

# Last.fm API key
API_KEY = "e554f25da26e93055f2780bbe2b9293b"

# Function to generate response
def generate_response(dialog):
    knowledge = ''
    instruction = f'Instruction: given a dialog context, you need to respond empathically.'
    dialog_text = ' EOS '.join(dialog)
    query = f"{instruction} [CONTEXT] {dialog_text} {knowledge}"

    input_ids = tokenizer.encode(query, return_tensors="pt")
    output = model.generate(input_ids, max_length=16, min_length=2, top_p=0.9, do_sample=True)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Function to perform sentiment analysis
def sentiment_finder(user_dialog):
    input_ids = sentiment_tokenizer.encode(user_dialog + '</s>', return_tensors='pt')
    output = sentiment_model.generate(input_ids=input_ids, max_length=2)
    emotion = [sentiment_tokenizer.decode(ids) for ids in output][0]
    return emotion[6:]

@app.route("/get_response", methods=["POST", "GET"])
def get_response():
    data = request.json
    dialog = data.get('dialog', [])
    generated_text = generate_response(dialog)
    user_dialog = dialog[-1]
    emotion = sentiment_finder(user_dialog)

    # Fetch music recommendations based on emotion
    recommendations_url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={emotion}&api_key={API_KEY}&format=json&limit=4"
    recommendations_response = requests.get(recommendations_url)

    recommendations = []
    if recommendations_response.ok:
        recommendations_data = recommendations_response.json()
        recommendations = recommendations_data["tracks"]["track"]

    response_data = {'generated_response': generated_text, 'recommendations': recommendations}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=8000)
