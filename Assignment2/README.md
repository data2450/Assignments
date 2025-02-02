# Assignment2

RAG based chatboat on given text or corpus

1.data_processing.py : shows how the given text corpus is cleaned and divided into small chunks

2.embed_store.py : In this script we are dividing the corpus and creatning embedings using an sentence-transformer model and storing them in a vector database and showing how the the correct related text chunk is retreived from the vector database according to the query

3.rag_pipline: addition to the above 2 process we are using an llm model T5 to generate the answer from the retrived chunks based on the query , complete pipline 

4.app.py : runs the flask webapp , only the chat part is included so u can first run app_new.py


5.app_new.py : flask web app with chat and history endpoints , we add sql in this notebook to save both query and asnwer generated so we can use it later



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

cd Assignment2
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
You can test the application by sending a POST request to the /chat endpoint using curl or Postman:
i am using curl
```bash
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"query\": \"What is artificial intelligence?\"}"


```
This should return a JSON response with the sentiment prediction.
### Example Response:
```bash
{
  "answer": "Great question! Here's what I found:\n\nsimulation of human intelligence"
}

```
### 6.you can test /history endpoint also, 
since i have not included sql feature only in app_new.py script
```bash
python app_new.py
```
to test /chat end point 
i am using curl
```bash
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"query\": \"What is artificial intelligence?\"}"


```
This should return a JSON response for the given query
### Example Response:
```bash
{
  "answer": "Great question! Here's what I found:\n\nsimulation of human intelligence"
}
```
to test /history end point 
```bash
curl -X GET http://127.0.0.1:5000/history

```
This should return a JSON response for history
### Example Response:
ure previous query and its answer generated
```bash
{
    "history": [
        {"role": "user", "content": "What is AI?"},
        {"role": "system", "content": "AI refers to the simulation of human intelligence in machines."}
    ]
}

```
### 7. Database Schema:
create ure database
```bash
CREATE DATABASE chat_history;
USE chat_history;

```
create the table

```bash
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role ENUM('user', 'system') NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
connect ure sql database and the webapp outputs
go inside app_new.py and change the sql credentiols correctly
```bash
        # Replace with your MySQL credentials
        connection = mysql.connector.connect(
            host='localhost',
            database='chat_history',  # Your database name
            user='root',  # Your MySQL username
            password='password'  # Your MySQL password
        )
```