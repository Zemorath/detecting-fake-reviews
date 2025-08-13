# Fake Review Detector

A complete full-stack web application that uses machine learning to detect fake product reviews. Built with React frontend, Flask backend, and scikit-learn ML model.

## 🚀 Features
- **Smart Detection**: Uses TF-IDF vectorization and Logistic Regression to classify reviews
- **Real-time Analysis**: Input a review and get instant fake/genuine prediction with confidence score
- **Review History**: Stores and displays past analyses with SQLite database
- **Modern UI**: Clean, responsive React interface with visual feedback
- **Robust Backend**: Flask API with comprehensive error handling and validation

## 🛠 Tech Stack
- **Frontend**: React, HTML/CSS, JavaScript
- **Backend**: Flask (Python), SQLite database
- **Machine Learning**: scikit-learn, pandas, numpy
- **Text Processing**: TF-IDF vectorization with English stop words

## 📁 Project Structure
```
/backend/          # Flask API server
  ├── app.py              # Main Flask application
  ├── requirements.txt    # Python dependencies
  ├── sample_reviews.csv  # Training data (30 labeled reviews)
  └── reviews.db         # SQLite database (auto-created)

/frontend/         # React web application
  ├── src/
  │   ├── App.js         # Main React component
  │   ├── App.css        # Styling
  │   └── index.js       # React entry point
  ├── public/
  │   └── index.html     # HTML template
  └── package.json       # Node.js dependencies
```

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Node.js 14+ and npm installed

### 1. Backend Setup (Flask + ML + SQLite)
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

The backend will run on **http://localhost:5000**

### 2. Frontend Setup (React)
```bash
# In a new terminal window
cd frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

The frontend will run on **http://localhost:3000**

## 🎯 Usage

1. **Start both servers** (backend on :5000, frontend on :3000)
2. **Open your browser** to http://localhost:3000
3. **Enter a product review** in the text area (e.g., "This product is amazing!")
4. **Click "Analyze Review"** to get prediction
5. **View results** with fake/genuine classification and confidence percentage
6. **Check history** to see past analyses stored in the database

### Example Reviews to Test:
- **Genuine**: "Great product, arrived quickly and works as described"
- **Fake**: "URGENT! Buy now! Limited time offer! Click here!"

## 🔍 How It Works

1. **Training**: Model trains on labeled review data using TF-IDF features
2. **Prediction**: New reviews are vectorized and classified by the trained model
3. **Storage**: All predictions are stored in SQLite database for history
4. **API**: RESTful endpoints handle prediction requests and history retrieval

## 🌟 Key Features Implemented

- ✅ **Input validation** (length limits, empty checks)
- ✅ **Error handling** (server errors, network issues)
- ✅ **Loading states** (visual feedback during analysis)
- ✅ **Character counter** (1000 character limit)
- ✅ **Responsive design** (works on mobile and desktop)
- ✅ **Health check endpoint** (/api/health)
- ✅ **Enhanced training data** (30 diverse examples)
- ✅ **Database persistence** (SQLite for review storage)

## 🔧 Development Notes

- **Model Training**: Automatically retrains when server starts
- **Database**: SQLite file created automatically on first run
- **CORS**: Enabled for frontend-backend communication
- **Environment**: Uses virtual environment for Python dependencies

## 📈 Future Enhancements

- Add more sophisticated ML features (sentiment analysis, n-grams)
- Implement model retraining with user feedback
- Add user authentication and personal history
- Deploy to cloud platforms (Heroku, AWS, etc.)
- Add batch review analysis
- Implement A/B testing for different models

---

**Happy Review Detection! 🕵️‍♂️**