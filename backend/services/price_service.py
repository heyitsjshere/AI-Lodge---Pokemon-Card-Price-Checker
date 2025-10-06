"""
Price Service - Aggregates prices from multiple sources
"""
import httpx
import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class PriceService:
    """Service for fetching Pokemon card prices from various sources"""
    
    def __init__(self):
        """Initialize price service"""
        self.tcgplayer_api_key = os.getenv("TCGPLAYER_API_KEY")
    
    async def get_prices(
        self,
        card_name: str,
        card_id: str,
        set_name: str,
        card_details: Optional[Dict] = None
    ) -> Dict:
        """
        Aggregate prices from multiple sources
        
        Args:
            card_name: Name of the card
            card_id: Pokemon TCG API card ID
            set_name: Set name
            card_details: Full card details from Pokemon TCG API (if available)
            
        Returns:
            Dictionary with aggregated price information
        """
        prices = []
        
        # If we have real card data from Pokemon TCG API, extract prices
        if card_details and card_details.get("tcgplayer_url"):
            tcg_prices = self._extract_tcgplayer_prices(card_details)
            prices.extend(tcg_prices)
        
        # If we don't have real data, use mock prices
        if not prices:
            # Get prices from different sources (mock data)
            tcgplayer_prices = await self._get_tcgplayer_prices(card_name, set_name)
            prices.extend(tcgplayer_prices)
            
            ebay_prices = await self._get_ebay_prices(card_name, set_name)
            prices.extend(ebay_prices)
            
            cardmarket_prices = await self._get_cardmarket_prices(card_name, set_name)
            prices.extend(cardmarket_prices)
        
        # Calculate market price (average)
        market_price = None
        if prices:
            total = sum(p["price"] for p in prices)
            market_price = round(total / len(prices), 2)
        
        # Determine trend (this is simplified - in production, you'd track historical data)
        trend = self._determine_trend(prices)
        
        return {
            "prices": prices,
            "market_price": market_price,
            "trend": trend,
            "last_updated": datetime.now().isoformat(),
            "total_sources": len(prices)
        }
    
    def _extract_tcgplayer_prices(self, card_details: Dict) -> List[Dict]:
        """
        Extract real TCGPlayer prices from Pokemon TCG API card data
        
        Args:
            card_details: Card details from Pokemon TCG API
            
        Returns:
            List of price dictionaries
        """
        prices = []
        
        try:
            tcgplayer_data = card_details.get("tcgplayer", {})
            tcg_prices = tcgplayer_data.get("prices", {})
            url = tcgplayer_data.get("url")
            
            # TCGPlayer has different price categories
            if tcg_prices:
                # Normal/Unlimited prices
                if "normal" in tcg_prices:
                    normal = tcg_prices["normal"]
                    if "market" in normal and normal["market"]:
                        prices.append({
                            "source": "TCGPlayer",
                            "price": round(float(normal["market"]), 2),
                            "currency": "USD",
                            "condition": "Near Mint",
                            "url": url or f"https://www.tcgplayer.com",
                            "in_stock": True,
                            "seller": "TCGPlayer Market"
                        })
                
                # Holofoil prices
                if "holofoil" in tcg_prices:
                    holo = tcg_prices["holofoil"]
                    if "market" in holo and holo["market"]:
                        prices.append({
                            "source": "TCGPlayer",
                            "price": round(float(holo["market"]), 2),
                            "currency": "USD",
                            "condition": "Near Mint (Holofoil)",
                            "url": url or f"https://www.tcgplayer.com",
                            "in_stock": True,
                            "seller": "TCGPlayer Market"
                        })
                
                # Reverse Holofoil prices
                if "reverseHolofoil" in tcg_prices:
                    reverse = tcg_prices["reverseHolofoil"]
                    if "market" in reverse and reverse["market"]:
                        prices.append({
                            "source": "TCGPlayer",
                            "price": round(float(reverse["market"]), 2),
                            "currency": "USD",
                            "condition": "Near Mint (Reverse Holo)",
                            "url": url or f"https://www.tcgplayer.com",
                            "in_stock": True,
                            "seller": "TCGPlayer Market"
                        })
                
                # 1st Edition prices
                if "1stEdition" in tcg_prices:
                    first_ed = tcg_prices["1stEdition"]
                    if "market" in first_ed and first_ed["market"]:
                        prices.append({
                            "source": "TCGPlayer",
                            "price": round(float(first_ed["market"]), 2),
                            "currency": "USD",
                            "condition": "Near Mint (1st Edition)",
                            "url": url or f"https://www.tcgplayer.com",
                            "in_stock": True,
                            "seller": "TCGPlayer Market"
                        })
            
            logger.info(f"Extracted {len(prices)} real prices from Pokemon TCG API")
            
        except Exception as e:
            logger.error(f"Error extracting TCGPlayer prices from card data: {str(e)}")
        
        return prices
    
    async def _get_tcgplayer_prices(self, card_name: str, set_name: str) -> List[Dict]:
        """
        Get prices from TCGPlayer
        
        Note: This requires TCGPlayer API access (needs approval)
        For demo purposes, this returns mock data
        """
        try:
            # Mock data for demonstration
            # In production, implement actual TCGPlayer API integration
            base_price = random.uniform(5.0, 50.0)
            
            return [
                {
                    "source": "TCGPlayer",
                    "price": round(base_price, 2),
                    "currency": "USD",
                    "condition": "Near Mint",
                    "url": f"https://www.tcgplayer.com/search/pokemon/product?q={card_name.replace(' ', '+')}",
                    "in_stock": True,
                    "seller": "TCGPlayer Market"
                },
                {
                    "source": "TCGPlayer",
                    "price": round(base_price * 0.85, 2),
                    "currency": "USD",
                    "condition": "Lightly Played",
                    "url": f"https://www.tcgplayer.com/search/pokemon/product?q={card_name.replace(' ', '+')}",
                    "in_stock": True,
                    "seller": "TCGPlayer Market"
                }
            ]
            
        except Exception as e:
            logger.error(f"Error fetching TCGPlayer prices: {str(e)}")
            return []
    
    async def _get_ebay_prices(self, card_name: str, set_name: str) -> List[Dict]:
        """
        Get prices from eBay
        
        Note: This uses eBay's public search (no API key needed for basic search)
        Returns constructed URLs for price checking
        """
        try:
            # Construct eBay search URL
            search_query = f"{card_name} {set_name} Pokemon Card".replace(" ", "+")
            ebay_url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
            
            # Mock prices for demonstration
            # In production, you could scrape eBay or use their API
            base_price = random.uniform(8.0, 55.0)
            
            return [
                {
                    "source": "eBay",
                    "price": round(base_price, 2),
                    "currency": "USD",
                    "condition": "Near Mint",
                    "url": ebay_url,
                    "in_stock": True,
                    "seller": "Various Sellers"
                },
                {
                    "source": "eBay",
                    "price": round(base_price * 1.15, 2),
                    "currency": "USD",
                    "condition": "Mint/PSA Graded",
                    "url": ebay_url + "&LH_PrefLoc=1",  # US Only
                    "in_stock": True,
                    "seller": "Various Sellers"
                }
            ]
            
        except Exception as e:
            logger.error(f"Error fetching eBay prices: {str(e)}")
            return []
    
    async def _get_cardmarket_prices(self, card_name: str, set_name: str) -> List[Dict]:
        """
        Get prices from Cardmarket (European market)
        """
        try:
            # Construct Cardmarket search URL
            search_query = f"{card_name}".replace(" ", "+")
            cardmarket_url = f"https://www.cardmarket.com/en/Pokemon/Products/Search?searchString={search_query}"
            
            # Mock prices for demonstration
            base_price = random.uniform(6.0, 45.0)
            
            return [
                {
                    "source": "Cardmarket",
                    "price": round(base_price, 2),
                    "currency": "USD",
                    "condition": "Near Mint",
                    "url": cardmarket_url,
                    "in_stock": True,
                    "seller": "Cardmarket Sellers"
                }
            ]
            
        except Exception as e:
            logger.error(f"Error fetching Cardmarket prices: {str(e)}")
            return []
    
    def _determine_trend(self, prices: List[Dict]) -> str:
        """
        Determine price trend based on available data
        
        Note: This is simplified. In production, you'd track historical prices
        """
        if not prices:
            return "unknown"
        
        # Simple logic based on price variation
        all_prices = [p["price"] for p in prices]
        avg_price = sum(all_prices) / len(all_prices)
        max_price = max(all_prices)
        min_price = min(all_prices)
        
        variation = (max_price - min_price) / avg_price if avg_price > 0 else 0
        
        if variation > 0.3:
            return "volatile"
        elif max_price == all_prices[-1]:
            return "rising"
        elif min_price == all_prices[-1]:
            return "falling"
        else:
            return "stable"
    
    async def get_historical_prices(self, card_id: str, days: int = 30) -> Dict:
        """
        Get historical price data (placeholder for future implementation)
        
        Args:
            card_id: Card ID
            days: Number of days of historical data
            
        Returns:
            Historical price data
        """
        # This would require a database to store historical prices
        # Placeholder for future implementation
        return {
            "card_id": card_id,
            "data": [],
            "message": "Historical data not yet implemented"
        }
