"""
Pydantic schemas for request/response models
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CardIdentificationResponse(BaseModel):
    """Response model for card identification"""
    card_name: str = Field(..., description="Name of the Pokemon card")
    set_name: str = Field(..., description="Set the card belongs to")
    card_number: str = Field(..., description="Card number within the set")
    rarity: Optional[str] = Field(None, description="Card rarity")
    card_id: str = Field(..., description="Unique card ID from Pokemon TCG API")
    image_url: Optional[str] = Field(None, description="Official card image URL")
    confidence: str = Field(default="high", description="Confidence level of identification")


class PriceInfo(BaseModel):
    """Price information from a specific source"""
    source: str = Field(..., description="Source of the price (e.g., TCGPlayer, eBay)")
    price: float = Field(..., description="Price in USD")
    currency: str = Field(default="USD", description="Currency code")
    condition: str = Field(default="Near Mint", description="Card condition")
    url: str = Field(..., description="URL to purchase")
    in_stock: bool = Field(default=True, description="Availability status")
    seller: Optional[str] = Field(None, description="Seller name if applicable")


class PriceCheckResponse(BaseModel):
    """Complete response with card details and prices"""
    card_name: str = Field(..., description="Name of the Pokemon card")
    set_name: str = Field(..., description="Set the card belongs to")
    card_number: str = Field(..., description="Card number within the set")
    rarity: Optional[str] = Field(None, description="Card rarity")
    card_id: str = Field(..., description="Unique card ID")
    image_url: Optional[str] = Field(None, description="Official card image URL")
    prices: List[PriceInfo] = Field(default_factory=list, description="List of prices from different sources")
    market_price: Optional[float] = Field(None, description="Average market price")
    price_trend: str = Field(default="stable", description="Price trend (up/down/stable)")
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Last update timestamp")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")
