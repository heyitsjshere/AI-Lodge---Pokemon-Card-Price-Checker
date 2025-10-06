"""
Card Service - Interacts with Pokemon TCG API to get card details
"""
import httpx
import os
import logging
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
        Get card details from Pokemon TCG API
        
        Args:
            card_name: Name of the Pokemon
            set_name: Set name (optional, helps narrow down results)
            card_number: Card number within set (optional)
            
        Returns:
            Dictionary with card details
        """
        try:
            async with httpx.AsyncClient() as client:
                # Build search query
                query_parts = [f'name:"{card_name}"']
                
                if set_name:
                    query_parts.append(f'set.name:"{set_name}"')
                
                if card_number:
                    # Extract just the number before the slash
                    num = card_number.split("/")[0].strip()
                    query_parts.append(f'number:{num}')
                
                query = " ".join(query_parts)
                
                logger.info(f"Searching Pokemon TCG API with query: {query}")
                
                # Make API request with longer timeout
                response = await client.get(
                    f"{self.BASE_URL}/cards",
                    params={"q": query},
                    headers=self.headers,
                    timeout=30.0  # Increased timeout to 30 seconds
                )
                
                response.raise_for_status()
                data = response.json()
                
                if not data.get("data"):
                    logger.warning(f"No cards found for query: {query}")
                    # Try a broader search with just the name
                    response = await client.get(
                        f"{self.BASE_URL}/cards",
                        params={"q": f'name:"{card_name}"'},
                        headers=self.headers,
                        timeout=30.0  # Increased timeout
                    )
                    data = response.json()
                
                if data.get("data"):
                    # Get the first (most relevant) result
                    card = data["data"][0]
                    
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
                        "cardmarket_url": card.get("cardmarket", {}).get("url")
                    }
                
                return None
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching card details: {str(e)}", exc_info=True)
            # Return None instead of raising to allow app to handle gracefully
            return None
        except Exception as e:
            logger.error(f"Error fetching card details: {str(e)}", exc_info=True)
            # Return None instead of raising to allow app to handle gracefully
            return None
    
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
