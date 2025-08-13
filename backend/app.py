import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import numpy as np

DB_PATH = 'reviews.db'
MODEL_PATH = 'model.pkl'
DATA_PATH = 'sample_reviews.csv'

app = Flask(__name__)
CORS(app)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL
    )''')
    conn.commit()
    conn.close()

# --- ML Model Setup ---
def train_model():
    """Train a text classification model on the sample data."""
    df = pd.read_csv(DATA_PATH)
    
    # Clean data - remove any rows with missing values
    df = df.dropna()
    
    # Ensure we have enough data
    if len(df) < 2:
        raise ValueError("Not enough training data")
    
    X = df['review'].astype(str)  # Ensure text data
    y = df['label']
    
    # Basic validation - check for required labels
    if not all(label in ['fake', 'genuine'] for label in y.unique()):
        raise ValueError("Labels must be 'fake' or 'genuine'")
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
        ('clf', LogisticRegression(random_state=42))
    ])
    
    pipeline.fit(X, y)
    return pipeline

model = train_model()
init_db()

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Fake Review Detector API is running'})

# --- API Endpoints ---
@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict if a review is fake or genuine."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        review = data.get('review', '').strip()
        if not review:
            return jsonify({'error': 'Review text is required'}), 400
            
        if len(review) > 1000:  # Reasonable length limit
            return jsonify({'error': 'Review text is too long (max 1000 characters)'}), 400
        
        # Get prediction
        proba = model.predict_proba([review])[0]
        pred_idx = np.argmax(proba)
        pred_label = model.classes_[pred_idx]
        confidence = float(proba[pred_idx])
        
        # Store in DB
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO reviews (review, prediction, confidence) VALUES (?, ?, ?)',
                  (review, pred_label, confidence))
        conn.commit()
        conn.close()
        
        return jsonify({
            'prediction': pred_label, 
            'confidence': round(confidence * 100, 2),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/history', methods=['GET'])
def history():
    """Get recent review predictions from database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT review, prediction, confidence FROM reviews ORDER BY id DESC LIMIT 20')
        rows = c.fetchall()
        conn.close()
        
        history = [
            {
                'review': r[:100] + '...' if len(r) > 100 else r,  # Truncate long reviews
                'prediction': p, 
                'confidence': round(c * 100, 2)
            }
            for r, p, c in rows
        ]
        return jsonify({'history': history, 'status': 'success'})
        
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)