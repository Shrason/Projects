from flask import Flask, request, render_template
import sqlite3
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

app = Flask(__name__)

# Initialize the "all-MiniLM-L6-v2" model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get the absolute path to the database file
    db_path = os.path.abspath('chromadb.db')
    print("Database path:", db_path)
    
    query = request.form['query']
    top_results = retrieve_similar_subtitles(query, db_path)
    return render_template('results.html', query=query, results=top_results)

def retrieve_similar_subtitles(query, db_path, top_n=10):
    # Connect to SQLite database using the absolute path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create embeddings for the query
    query_embedding = model.encode([query], convert_to_tensor=True).numpy()
    query_embedding = np.array([query_embedding.flatten()])
    
    # Retrieve all subtitles and their embeddings from the database
    c.execute('SELECT name, content, embedding FROM subtitles')
    results = c.fetchall()
    
    # Calculate cosine similarity between query and each subtitle embedding
    similarities = []
    for name, content, stored_embedding in results:
        stored_embedding = np.array([pickle.loads(stored_embedding).flatten()])
        similarity = cosine_similarity(query_embedding, stored_embedding)
        similarities.append((name, content, similarity[0][0]))
    
    # Sort by similarity score in descending order
    similarities.sort(key=lambda x: x[2], reverse=True)
    
    # Get the top N results
    top_results = similarities[:top_n]
    
    # Close the database connection
    conn.close()
    
    return top_results

if __name__ == '__main__':
    app.run(debug=True)
