from fastapi import FastAPI
from routes import get_odds
import os
from utils.logger import logger

logger.info("Starting Ai Odds Builder API")
app = FastAPI(
    debug=os.getenv("DEBUG", "false").lower() == "true", 
    title="Ai Odds Builder API", 
    description="API for managing odds prediction. It returns predicted Serie A odds", 
    version="1.0.0",
    port=os.getenv("PORT", "8000")
)

# Include the get_odds router
app.include_router(
    get_odds.router, 
    prefix="/api", tags=["Odds Prediction"]
)
logger.info("Ai Odds Builder API started successfully")