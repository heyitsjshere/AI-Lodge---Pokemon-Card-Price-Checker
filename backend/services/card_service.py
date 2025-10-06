"""
Card Service - Interacts with Pokemon TCG API to get card details
"""
import httpx
import os
import logging
import asyncio
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class CardService:
    """Service for fetching Pokemon card details from Pokemon TCG API"""
    
    BASE_URL = "https://api.pokemontcg.io/v2"
    
    def __init__(self):
        """Initialize card service with API configuration"""
        self.api_key = os.getenv("POKEMON_TCG_API_KEY")
        self.headers = {}
        if self.api_key:
            self.headers["X-Api-Key"] = self.api_key
    
    async def get_card_details(
        self,
        card_name: str,
        set_name: Optional[str] = None,
        card_number: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get card details from Pokemon TCG API with fallback to mock data
        
        Args:
            card_name: Name of the Pokemon
            set_name: Set name (optional, helps narrow down results)
            card_number: Card number within set (optional)
            
        Returns:
            Dictionary with card details
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Build search query - try just with name first (simpler, faster)
                query = f'name:"{card_name}"'
                
                logger.info(f"Searching Pokemon TCG API: {query}")
                
                # Make API request
                response = await client.get(
                    f"{self.BASE_URL}/cards",
                    params={"q": query, "pageSize": 10},
                    headers=self.headers
                )
                
                response.raise_for_status()
                data = response.json()
                
                if data.get("data"):
                    # Filter results by set and number if provided
                    cards = data["data"]
                    
                    # Try to find exact match
                    for card in cards:
                        card_set = card.get("set", {}).get("name", "")
                        card_num = card.get("number", "")
                        
                        # Check if set matches (if provided)
                        set_match = not set_name or set_name.lower() in card_set.lower()
                        
                        # Check if number matches (if provided)
                        num_match = True
                        if card_number:
                            query_num = card_number.split("/")[0].strip()
                            num_match = query_num in card_num
                        
                        if set_match and num_match:
                            logger.info(f"Found match: {card.get('name')} - {card_set} #{card_num}")
                            return {
                                "id": card.get("id"),
                                "name": card.get("name"),
                                "set": card_set,
                                "number": card_num,
                                "rarity": card.get("rarity"),
                                "image_url": card.get("images", {}).get("large"),
                                "image_url_small": card.get("images", {}).get("small"),
                                "set_id": card.get("set", {}).get("id"),
                                "set_series": card.get("set", {}).get("series"),
                                "artist": card.get("artist"),
                                "hp": card.get("hp"),
                                "types": card.get("types", []),
                                "tcgplayer_url": card.get("tcgplayer", {}).get("url"),
                                "cardmarket_url": card.get("cardmarket", {}).get("url"),
                                "tcgplayer": card.get("tcgplayer", {})  # Full TCGPlayer data including prices
                            }
                    
                    # If no exact match, return first result
                    logger.warning(f"No exact match, returning first result")
                    card = cards[0]
                    return {
                        "id": card.get("id"),
                        "name": card.get("name"),
                        "set": card.get("set", {}).get("name"),
                        "number": card.get("number"),
                        "rarity": card.get("rarity"),
                        "image_url": card.get("images", {}).get("large"),
                        "image_url_small": card.get("images", {}).get("small"),
                        "set_id": card.get("set", {}).get("id"),
                        "set_series": card.get("set", {}).get("series"),
                        "artist": card.get("artist"),
                        "hp": card.get("hp"),
                        "types": card.get("types", []),
                        "tcgplayer_url": card.get("tcgplayer", {}).get("url"),
                        "cardmarket_url": card.get("cardmarket", {}).get("url"),
                        "tcgplayer": card.get("tcgplayer", {})  # Full TCGPlayer data including prices
                    }
                
                logger.warning(f"No cards found for: {card_name}")
                # Fall through to mock data
                    
        except (httpx.ReadTimeout, httpx.HTTPError) as e:
            logger.warning(f"Pokemon TCG API unavailable: {str(e)}")
            logger.info("Using mock data as fallback...")
        except Exception as e:
            logger.error(f"Error fetching card details: {str(e)}", exc_info=True)
        
        # Fallback: Return mock data when API is unavailable
        logger.info(f"Returning mock data for {card_name}")
        
        # Create a more realistic-looking mock ID
        set_prefix = "unknown"
        if set_name:
            # Convert set name to abbreviated format (e.g., "Base Set" -> "base1")
            set_prefix = set_name.lower().replace(" ", "")[:4]
        
        card_num = card_number.split("/")[0] if card_number else "001"
        mock_id = f"{set_prefix}-{card_num}"
        
        return {
            "id": mock_id,
            "name": card_name,
            "set": set_name or "Unknown Set",
            "number": card_number or "001",
            "rarity": "Common",
            "image_url": None,  # Don't provide image so frontend uses uploaded image
            "image_url_small": None,
            "set_id": set_prefix,
            "set_series": "Mock Series",
            "artist": "Unknown Artist",
            "hp": "50",
            "types": ["Grass"],
            "tcgplayer_url": None,
            "cardmarket_url": None
        }
    
    async def get_card_by_id(self, card_id: str) -> Optional[Dict]:
        """
        Get card details by specific card ID
        
        Args:
            card_id: Pokemon TCG API card ID
            
        Returns:
            Dictionary with card details
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/cards/{card_id}",
                    headers=self.headers,
                    timeout=30.0  # Increased timeout
                )
                
                response.raise_for_status()
                data = response.json()
                
                if data.get("data"):
                    card = data["data"]
                    return {
                        "id": card.get("id"),
                        "name": card.get("name"),
                        "set": card.get("set", {}).get("name"),
                        "number": card.get("number"),
                        "rarity": card.get("rarity"),
                        "image_url": card.get("images", {}).get("large"),
                        "tcgplayer_url": card.get("tcgplayer", {}).get("url"),
                        "cardmarket_url": card.get("cardmarket", {}).get("url")
                    }
                
                return None
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching card by ID: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error fetching card by ID: {str(e)}")
            raise
    
    async def search_cards(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for cards by name or other criteria
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of card dictionaries
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/cards",
                    params={"q": query, "pageSize": limit},
                    headers=self.headers,
                    timeout=30.0  # Increased timeout
                )
                
                response.raise_for_status()
                data = response.json()
                
                cards = []
                for card in data.get("data", []):
                    cards.append({
                        "id": card.get("id"),
                        "name": card.get("name"),
                        "set": card.get("set", {}).get("name"),
                        "number": card.get("number"),
                        "rarity": card.get("rarity"),
                        "image_url": card.get("images", {}).get("small")
                    })
                
                return cards
                
        except Exception as e:
            logger.error(f"Error searching cards: {str(e)}")
            return []
