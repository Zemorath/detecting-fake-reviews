import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [review, setReview] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/history');
      const data = await res.json();
      if (res.ok) {
        setHistory(data.history || []);
      } else {
        console.error('Failed to fetch history:', data.error);
      }
    } catch (err) {
      console.error('Error fetching history:', err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);
    
    if (!review.trim()) {
      setError('Please enter a review.');
      setLoading(false);
      return;
    }
    
    if (review.length > 1000) {
      setError('Review is too long. Please keep it under 1000 characters.');
      setLoading(false);
      return;
    }
    
    try {
      const res = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ review })
      });
      const data = await res.json();
      
      if (res.ok) {
        setResult(data);
        setReview('');
        fetchHistory();
      } else {
        setError(data.error || 'An error occurred.');
      }
    } catch (err) {
      setError('Unable to connect to server. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Fake Review Detector</h1>
      <p className="subtitle">Analyze product reviews to detect if they're genuine or fake</p>
      
      <form onSubmit={handleSubmit}>
        <textarea
          value={review}
          onChange={e => setReview(e.target.value)}
          placeholder="Enter your product review here... (e.g., 'This product is amazing, works perfectly!')"
          rows={4}
          maxLength={1000}
          disabled={loading}
        />
        <div className="char-count">{review.length}/1000 characters</div>
        <button type="submit" disabled={loading || !review.trim()}>
          {loading ? 'Analyzing...' : 'Analyze Review'}
        </button>
      </form>
      
      {error && <div className="error">{error}</div>}
      
      {result && (
        <div className={`result ${result.prediction}`}>
          <div className="prediction">
            <strong>{result.prediction === 'fake' ? '🚫 Fake' : '✅ Genuine'}</strong> Review
          </div>
          <div className="confidence">
            Confidence: {result.confidence}%
          </div>
        </div>
      )}
      
      <div className="history-section">
        <h2>Recent Analyses</h2>
        {history.length === 0 ? (
          <p className="no-history">No analyses yet. Try analyzing a review!</p>
        ) : (
          <ul className="history">
            {history.map((item, idx) => (
              <li key={idx}>
                <span className={`prediction-badge ${item.prediction}`}>
                  {item.prediction === 'fake' ? 'Fake' : 'Genuine'}
                </span>
                <span className="review-text">"{item.review}"</span>
                <span className="confidence">({item.confidence}%)</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
