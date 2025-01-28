#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Install required libraries
#get_ipython().system('pip install datasets')

# Import necessary libraries
from datasets import load_dataset
import sqlite3

# Step 1: Download the IMDB dataset
dataset = load_dataset("imdb")

# Step 2: Create SQLite database and table
db_path = "imdb_reviews.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS imdb_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_text TEXT NOT NULL,
    sentiment TEXT NOT NULL
)
''')

conn.commit()

# Step 3: Insert data into the table
def insert_data(split):
    for row in dataset[split]:
        review_text = row['text']
        sentiment = "positive" if row['label'] == 1 else "negative"
        cursor.execute(
            '''
            INSERT INTO imdb_reviews (review_text, sentiment)
            VALUES (?, ?)
            ''', (review_text, sentiment)
        )
    conn.commit()

# Insert train and test data
insert_data("train")
insert_data("test")

# Step 4: Verify data
cursor.execute("SELECT COUNT(*) FROM imdb_reviews")
print(f"Total records in the table: {cursor.fetchone()[0]}")

# Query a few rows to confirm
cursor.execute("SELECT * FROM imdb_reviews LIMIT 5")
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()

