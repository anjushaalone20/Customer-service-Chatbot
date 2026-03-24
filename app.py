from flask import Flask, render_template, request, jsonify
import json
import pickle
import random
import nltk
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)
lemmatizer = WordNetLemmatizer()

try:
    with open('model.pkl', 'rb') as f:
        model_data = pickle.load(f)
        classifier = model_data['classifier']
        word_features = model_data['word_features']
except FileNotFoundError:
    print("Warning: Model not found. Please run 'python train.py' first.")
    classifier = None
    word_features = []

with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

def generate_features(document_words, word_features):
    document_words_set = set(document_words)
    features = {}
    for word in word_features:
        features[f'contains({word})'] = (word in document_words_set)
    return features

def get_response(user_input):
    if classifier is None:
        return "The backend Machine Learning model is currently unavailable."
        
    tokens = nltk.word_tokenize(user_input.lower())
    lemmatized = [lemmatizer.lemmatize(w) for w in tokens if w.isalnum()]
    
    if not lemmatized:
        return "Please type a valid message!"

    features = generate_features(lemmatized, word_features)
    tag = classifier.classify(features)
    
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
            
    return "I'm still learning! Could you rephrase your question?"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    bot_response = get_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
