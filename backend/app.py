"""
Pokemon Card Price Checker - Main FastAPI Application
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv
import logging

from services.vision_service import VisionService
from services.card_service import CardService
from services.price_service import PriceService
from models.schemas import CardIdentificationResponse, PriceCheckResponse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Pokemon Card Price Checker API",
    description="AI-powered Pokemon card identification and price checking",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
vision_service = VisionService()
card_service = CardService()
price_service = PriceService()

# Create uploads directory
os.makedirs("uploads", exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Pokemon Card Price Checker",
        "version": "1.0.0"
    }


@app.post("/api/identify-card", response_model=CardIdentificationResponse)
async def identify_card(file: UploadFile = File(...)):
    """
    Identify a Pokemon card from an uploaded image
    
    Args:
        file: Uploaded image file (JPG, PNG)
        
    Returns:
        Card identification details
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        
        logger.info(f"Processing image: {file.filename}")
        
        # Use vision AI to identify the card
        identification = await vision_service.identify_card(image_data)
        
        if not identification:
            raise HTTPException(
                status_code=404,
                detail="Could not identify the Pokemon card from the image"
            )
        
        # Get exact card details from Pokemon TCG API
        card_details = await card_service.get_card_details(
            card_name=identification.get("card_name"),
            set_name=identification.get("set_name"),
            card_number=identification.get("card_number")
        )
        
        return CardIdentificationResponse(
            card_name=card_details.get("name"),
            set_name=card_details.get("set"),
            card_number=card_details.get("number"),
            rarity=card_details.get("rarity"),
            card_id=card_details.get("id"),
            image_url=card_details.get("image_url"),
            confidence=identification.get("confidence", "high")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error identifying card: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/api/check-price", response_model=PriceCheckResponse)
async def check_price(file: UploadFile = File(...)):
    """
    Complete flow: Identify card and get price information
    
    Args:
        file: Uploaded image file (JPG, PNG)
        
    Returns:
        Card details with price information
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await file.read()
        
        logger.info(f"Processing image for price check: {file.filename}")
        
        # Step 1: Identify the card using AI vision
        identification = await vision_service.identify_card(image_data)
        
        if not identification:
            raise HTTPException(
                status_code=404,
                detail="Could not identify the Pokemon card from the image"
            )
        
        # Step 2: Get exact card details from Pokemon TCG API
        card_details = await card_service.get_card_details(
            card_name=identification.get("card_name"),
            set_name=identification.get("set_name"),
            card_number=identification.get("card_number")
        )
        
        if not card_details:
            # Log the identification for debugging
            logger.warning(f"Card not found in Pokemon TCG API. Identification: {identification}")
            raise HTTPException(
                status_code=404,
                detail=f"Card '{identification.get('card_name')}' from '{identification.get('set_name')}' not found in database. The card was identified but may not exist in the Pokemon TCG database yet."
            )
        
        # Step 3: Fetch prices from various sources
        prices = await price_service.get_prices(
            card_name=card_details.get("name"),
            card_id=card_details.get("id"),
            set_name=card_details.get("set")
        )
        
        return PriceCheckResponse(
            card_name=card_details.get("name"),
            set_name=card_details.get("set"),
            card_number=card_details.get("number"),
            rarity=card_details.get("rarity"),
            card_id=card_details.get("id"),
            image_url=card_details.get("image_url"),
            prices=prices.get("prices", []),
            market_price=prices.get("market_price"),
            price_trend=prices.get("trend", "stable"),
            last_updated=prices.get("last_updated")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking price: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/api/card/{card_id}/prices")
async def get_card_prices(card_id: str):
    """
    Get prices for a specific card by ID
    
    Args:
        card_id: Pokemon TCG API card ID
        
    Returns:
        Price information
    """
    try:
        card_details = await card_service.get_card_by_id(card_id)
        
        if not card_details:
            raise HTTPException(status_code=404, detail="Card not found")
        
        prices = await price_service.get_prices(
            card_name=card_details.get("name"),
            card_id=card_id,
            set_name=card_details.get("set")
        )
        
        return prices
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching prices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
