# Assignment1

we have files

1.data_setup.py : dwonload imdb dataset from dataset library and save it in a sql database

2.train_model.ipynb : notebook shows bulding a sentimental model on the above data with logistic regression
ouputs `logreg_model.pkl` file and `tfidf_vectorizer.pkl` file , we are using the logistic regression model.

3.app.py : runs the flask webapp

your database file name is imdb_reviews.db


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x (use `python --version` to check your Python version)
- `pip` (Python package installer)
- packages mentioned in requirment.txt

## Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository

Clone the repository using Git:

```bash
git clone https://github.com/data2450/Assignments.git

#move into the assigment1

cd Assignment1
```
### 2. Set Up a Virtual Environment (Optional but recommended)

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the Application
```bash
python app.py
```
Your Flask app should now be running at http://127.0.0.1:5000/.

### 5. Testing the API
You can test the application by sending a POST request to the /predict endpoint using curl or Postman:
i am using curl
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"review_text\": \"I love this product!\"}"

```
This should return a JSON response with the sentiment prediction.
### Example Response:
```bash
{
  "sentiment_prediction": "positive"
}

```
### 6. Running the model notebook
you can simple go into the train_model.ipynb notebook and check how the model is trained 
## model info
* Model: Logistic Regression
* Feature Extraction: TF-IDF Vectorizer
* Configuration:
  * max_features=5000: Limits the number of features to the top 5000 terms based on their TF-IDF scores.
  * stop_words='english': Excludes common English stop words from the feature set.

## Key Results
Final Accuracy on Test Set: 88%
