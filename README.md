# AI Chatbot with NLTK and Flask

A simple, interactive chatbot built using Python, NLTK (Natural Language Toolkit), and Flask. The chatbot uses a Naive Bayes Classifier to categorize user input into predefined intents and provides relevant responses.

## 🚀 Features
- **Natural Language Processing**: Uses NLTK for tokenization and lemmatization.
- **Machine Learning**: Trained on custom intents using a Naive Bayes Classifier.
- **Web Interface**: Clean and responsive UI built with HTML/CSS/JS.
- **REST API**: Flask-based backend for seamless message handling.

## 📂 Project Structure
```text
chatbot/
├── app.py              # Flask server and inference logic
├── train.py            # Script to train the ML model
├── intents.json        # Training data (patterns and responses)
├── model.pkl           # Serialized trained model
├── requirements.txt    # Python dependencies
├── static/             # Frontend assets (CSS, JS)
│   ├── script.js
│   └── style.css
└── templates/          # HTML templates
    └── index.html
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd chatbot
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🧠 Training the Model
To train (or retrain) the chatbot with the patterns in `intents.json`, run:
```bash
python train.py
```
This will generate/update the `model.pkl` file used by the application.

## 🏃 Running the Application
Start the Flask server:
```bash
python app.py
```
After running the command, open your browser and navigate to `http://127.0.0.1:5000`.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
