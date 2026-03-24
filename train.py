import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import random

# Download requirement
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

lemmatizer = WordNetLemmatizer()

# Build bag of words from a sentence
def generate_features(document_words, word_features):
    document_words_set = set(document_words)
    features = {}
    for word in word_features:
        features[f'contains({word})'] = (word in document_words_set)
    return features

def train_model():
    print("Loading intents.json...")
    with open('intents.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = []
    all_words = []

    for intent in data['intents']:
        tag = intent['tag']
        for pattern in intent['patterns']:
            tokens = nltk.word_tokenize(pattern.lower())
            lemmatized = [lemmatizer.lemmatize(w) for w in tokens if w.isalnum()]
            documents.append((lemmatized, tag))
            all_words.extend(lemmatized)

    all_words_freq = nltk.FreqDist(all_words)
    # top 2000 words
    word_features = list(all_words_freq.keys())[:2000]

    featuresets = [(generate_features(doc_words, word_features), category) for (doc_words, category) in documents]

    print("Training NLTK NaiveBayes Classifier...")
    classifier = nltk.NaiveBayesClassifier.train(featuresets)

    # Save exactly what we need for inference
    with open('model.pkl', 'wb') as f:
        pickle.dump({
            'classifier': classifier,
            'word_features': word_features
        }, f)
        
    print("Training complete! Model successfully saved to disk.")

if __name__ == "__main__":
    train_model()
