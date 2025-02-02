from flask import Flask, request, jsonify
from rag_pipline import rag_pipeline, preprocess_text, chunk_text, add_to_vector_db
import mysql.connector
from mysql.connector import Error

# Corpus to be updated dynamically
corpus = """
Artificial intelligence (AI) refers to the simulation of human intelligence in machines.
These machines can perform tasks such as problem-solving, decision-making, and language understanding.
AI is widely used in applications like virtual assistants, recommendation systems, and autonomous vehicles.
The theory of relativity, proposed by Albert Einstein, revolutionized our understanding of space and time.
It consists of two parts: special relativity and general relativity.
Special relativity deals with objects moving at constant speeds, while general relativity explains the force of gravity as the curvature of spacetime caused by mass.
"""


def get_db_connection():
    try:
        # Replace with your MySQL credentials
        connection = mysql.connector.connect(
            host='localhost',
            database='chat_history',  # Your database name
            user='root',  # Your MySQL username
            password='2450242'  # Your MySQL password
        )
        if connection.is_connected():
            print('Connected to MySQL server')
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


# Function to save chat history to MySQL
def save_chat_history(role, content):
    print('in')
    connection = get_db_connection()
    print('5')
    if connection:
        print('7')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO messages (role, content) VALUES (%s, %s)", (role, content))
        connection.commit()
        cursor.close()
        connection.close()

# Initialize Flask app
app = Flask(__name__)

# Function to update the corpus, preprocess, chunk, and add to the vector database
def update_corpus(corpus_text):
    # Preprocess and chunk the corpus
    processed_text = preprocess_text(corpus_text)
    chunks = chunk_text(processed_text)

    # Add chunks to the vector database
    add_to_vector_db(chunks)

# Flask API Route to update corpus dynamically
@app.route('/update_corpus', methods=['POST'])
def update_corpus_route():
    data = request.json
    new_corpus = data.get("corpus")

    if not new_corpus:
        return jsonify({"error": "Missing corpus text"}), 400
    
    # Update the global corpus, preprocess, chunk, and add to the vector database
    global corpus
    corpus = new_corpus
    update_corpus(corpus)
    
    return jsonify({"message": "Corpus updated successfully"}), 200

# Flask API Route for chat query
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get("query")
    
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    
    # Assuming rag_pipeline is a function that processes the query and uses the vector database
    answer = rag_pipeline(query)

    # Save user query and system response to the database
    #print('1')
    save_chat_history(role='user', content=query)
    print('2')
    save_chat_history(role='system', content=answer)
    print('3')
    
    return jsonify({"answer": answer})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
