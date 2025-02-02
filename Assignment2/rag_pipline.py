from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import T5ForConditionalGeneration, T5Tokenizer
import random
import re

# Step 1: Load a pre-trained embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 2: Create a FAISS index for the vector database
dimension = 384  # Dimension of the embeddings
index = faiss.IndexFlatL2(dimension)

# Step 3: Load a pre-trained T5 model for answer generation
model_name = "t5-small"  # You can use "t5-base" for better performance
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Step 4: Define a function to preprocess and chunk the corpus
def preprocess_text(text):
    # Remove extra whitespaces and normalize text
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Step 5: Add documents to the vector database
def add_to_vector_db(chunks):
    embeddings = embedding_model.encode(chunks)
    index.add(np.array(embeddings))
    return chunks

# Step 6: Retrieve top-k relevant chunks
def retrieve_top_k_chunks(query, k=3):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]

# Step 7: Generate a human-like answer using T5
POLITE_PHRASES = [
    "Sure, let me explain that! 😊",
    "I think I can help with that! 🤔",
    "Great question! Here's what I found:",
    "Let me break it down for you:",
    "Interesting! Here's what I know:",
]

def generate_answer_with_t5(query, context_chunks):
    # Combine the context chunks into a single string
    context = " ".join(context_chunks)
    
    # Create the input text in T5's format: "question: <query> context: <context>"
    input_text = f"question: {query} context: {context}"
    
    # Tokenize the input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    
    # Generate the answer using the model
    output = model.generate(
        input_ids,
        max_length=100,  # Limit the length of the generated answer
        num_beams=4,  # Use beam search for better results
        early_stopping=True,  # Stop generation early if appropriate
    )
    
    # Decode the generated output to text
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Add a polite phrase to the answer
    polite_phrase = random.choice(POLITE_PHRASES)
    human_like_answer = f"{polite_phrase}\n\n{answer}"
    
    return human_like_answer

# Step 8: Full RAG pipeline
def rag_pipeline(query, k=3):
    # Step 1: Convert query to embedding
    query_embedding = embedding_model.encode([query])
    
    # Step 2: Retrieve top-k relevant chunks
    top_chunks = retrieve_top_k_chunks(query, k)
    
    # Step 3: Concatenate the retrieved chunks
    context = " ".join(top_chunks)
    
    # Step 4: Generate the final answer
    answer = generate_answer_with_t5(query, top_chunks)
    
    return answer

# Step 9: Example usage
# Prepare the corpus
corpus = """
Artificial intelligence (AI) refers to the simulation of human intelligence in machines.
These machines can perform tasks such as problem-solving, decision-making, and language understanding.
AI is widely used in applications like virtual assistants, recommendation systems, and autonomous vehicles.
The theory of relativity, proposed by Albert Einstein, revolutionized our understanding of space and time.
It consists of two parts: special relativity and general relativity.
Special relativity deals with objects moving at constant speeds, while general relativity explains the force of gravity as the curvature of spacetime caused by mass.
"""

# Preprocess and chunk the corpus
chunks = chunk_text(preprocess_text(corpus))

# Add chunks to the vector database
add_to_vector_db(chunks)

# Query the RAG pipeline
query = "What is artificial intelligence?"
answer = rag_pipeline(query)
#print("Generated Answer:", answer)