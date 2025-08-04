# AI Odds Builder 🚀

An intelligent API for predicting Serie A football match odds using machine learning. This application leverages neural networks with team embeddings to predict various betting outcomes including match results (3way 1x2), over/under goals, and both teams to score scenarios.

## 📋 Overview

The AI Odds Builder is a FastAPI-based web service that:
- Predicts odds for Serie A football matches using a trained neural network
- Fetches live Serie A fixtures from TheSportsDB API
- Provides both individual match predictions and league-wide odds
- Uses team embeddings to capture team characteristics and relationships

## 🎯 What the Application Does

### Core Functionality
- **Match Odds Prediction**: Predicts 7 different betting outcomes for any Serie A match
- **Live Serie A Data**: Fetches current season fixtures and generates predictions for all upcoming matches
- **RESTful API**: Provides easy-to-use endpoints for odds retrieval
- **Machine Learning**: Uses a neural network with team embeddings trained on historical match data

### Predicted Outcomes
The model predicts odds for:
- `outcome1`: Home team win
- `outcomeX`: Draw
- `outcome2`: Away team win
- `outcomeOver`: Over 2.5 goals
- `outcomeUnder`: Under 2.5 goals
- `outcomeGG`: Both teams to score (Goal/Goal)
- `outcomeNG`: Not both teams to score (No Goal)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pipenv (for dependency management)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-odds-builder
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   ```

3. **Activate the virtual environment**
   ```bash
   pipenv shell
   ```

4. **Train the model** (if not already done)
   ```bash
   python services/train.py
   ```

5. **Start the API server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The API will be available at `http://localhost:8000`

### Environment Variables
- `DEBUG`: Set to "true" for debug mode (default: "false")
- `PORT`: Server port (default: "8000")

## 🤖 Machine Learning Training

### Training Process

The training pipeline (`services/train.py`) performs the following steps:

1. **Data Loading**: Loads historical match data from `csv/passiveEvents.csv`
2. **Team Mapping**: Creates numerical IDs for all teams using embedding techniques
3. **Feature Engineering**: 
   - Maps team names to numerical IDs
   - Prepares home/away team features
4. **Target Preparation**: Normalizes 7 different betting outcomes using MinMaxScaler
5. **Model Architecture**:
   - **Input**: Home team ID and Away team ID
   - **Embeddings**: 16-dimensional embeddings for each team
   - **Neural Network**: 2 hidden layers (64 neurons each) with ReLU activation
   - **Output**: 7 betting outcomes with linear activation
6. **Training**: 20 epochs with validation split (80/20)
7. **Model Persistence**: Saves trained model, scaler, and team mappings to `assets/`

### Model Architecture
```
Input (Home Team ID) → Embedding (16D) → Flatten
Input (Away Team ID) → Embedding (16D) → Flatten
                                    ↓
                              Concatenate
                                    ↓
                            Dense (64, ReLU)
                                    ↓
                            Dense (64, ReLU)
                                    ↓
                            Dense (7, Linear)
```

### Required Training Data
- Historical match data with team names and betting outcomes
- File: `csv/passiveEvents.csv`
- Must contain columns: `homeName`, `awayName`, and all 7 outcome columns

## 🔗 API Endpoints

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints

#### 1. Get Match Odds
**POST** `/api/odds/match`

Predict odds for a specific match between two teams.

**Request Body:**
```json
{
  "homeName": "AC Milan",
  "awayName": "Inter"
}
```

**Response:**
```json
{
  "outcome1": 2.45,
  "outcomeX": 3.20,
  "outcome2": 2.80,
  "outcomeOver": 1.85,
  "outcomeUnder": 1.95,
  "outcomeGG": 1.75,
  "outcomeNG": 2.05
}
```

#### 2. Get All Serie A Odds
**GET** `/api/odds`

Retrieve predicted odds for all upcoming Serie A matches.

**Response:**
```json
{
  "events": [
    {
      "id": "AC Milan_Inter_2024-12-15T15:00:00Z",
      "sport_key": "serie_a",
      "matchId": "generated_match_id",
      "teams": ["AC Milan", "Inter"],
      "start": "2024-12-15T15:00:00Z",
      "odds": {
        "home": 2.45,
        "away": 2.80,
        "draw": 3.20,
        "over": 1.85,
        "under": 1.95,
        "gg": 1.75,
        "ng": 2.05
      }
    }
  ]
}
```

## 📁 Project Structure

```
ai-odds-builder/
├── main.py                    # FastAPI application entry point
├── Pipfile                   # Python dependencies
├── assets/                   # Trained model artifacts
│   ├── odds_embed_model.keras
│   ├── odds_scaler.joblib
│   └── team_id_map.joblib
├── csv/                      # Training and processed data
│   ├── passiveEvents.csv
│   └── dataset_with_ids.csv
├── models/                   # Pydantic data models
│   ├── prediction_payload.py
│   ├── prediction_output.py
│   └── league_output.py
├── routes/                   # API route handlers
│   └── get_odds.py
├── services/                 # Business logic
│   ├── train.py             # ML training pipeline
│   ├── predict_odds.py      # Prediction service
│   └── fetch_matches.py     # External API integration
└── utils/                   # Utility functions
    ├── logger.py
    └── get_match_id.py
```

## 🛠️ Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **TensorFlow/Keras**: Deep learning framework for the neural network
- **Scikit-learn**: Machine learning utilities and preprocessing
- **Pandas**: Data manipulation and analysis
- **Pydantic**: Data validation and serialization
- **Joblib**: Model persistence
- **TheSportsDB API**: External data source for Serie A fixtures

## 📊 Model Performance

The model uses Mean Absolute Error (MAE) as the primary metric during training. Performance is evaluated on a 20% test split of the historical data.

## 🔮 Future Enhancements

- Support for multiple leagues beyond Serie A
- Real-time model updates with new match results
- Enhanced feature engineering (team form, injuries, etc.)
- A/B testing for different model architectures
- Confidence intervals for predictions

## 📝 Logging

The application includes comprehensive logging for:
- API requests and responses
- Model predictions
- Error handling and debugging
- Training progress

Logs are written to `app.log` and console output.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
