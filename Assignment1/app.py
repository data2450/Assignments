# Import necessary libraries
from flask import Flask, request, jsonify
import joblib
import re

# Initialize the Flask app
app = Flask(__name__)

# Load the pre-trained model and vectorizer
model = joblib.load('logreg_model.pkl')  # Replace with your local model path
vectorizer = joblib.load('tfidf_vectorizer.pkl')  # Replace with your local vectorizer path

# Function to clean and preprocess text
def clean_text(text):
    # Lowercase the text
    text = text.lower()
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)
    # Remove punctuation (optional)
    text = re.sub(r"[^\w\s]", "", text)
    return text

# Define the /predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.get_json()
    review_text = data.get("review_text")

    # Ensure that the review_text is provided
    if not review_text:
        return jsonify({"error": "No review_text field provided"}), 400

    # Preprocess the input text
    cleaned_text = clean_text(review_text)
    # Transform the text using the loaded vectorizer
    text_vector = vectorizer.transform([cleaned_text])
    # Predict sentiment using the loaded model
    sentiment = model.predict(text_vector)[0]
    # Map prediction to "positive" or "negative"
    sentiment_label = "positive" if sentiment == 1 else "negative"

    # Return the result in JSON format
    return jsonify({"sentiment_prediction": sentiment_label})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)  # Debug mode is optional
