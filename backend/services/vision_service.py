"""
Vision Service - Uses OpenAI GPT-4 Vision to identify Pokemon cards from images
"""
import base64
import os
import logging
from typing import Dict, Optional
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class VisionService:
    """Service for identifying Pokemon cards using AI vision"""
    
    def __init__(self):
        """Initialize the vision service with OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=api_key)
    
    async def identify_card(self, image_data: bytes) -> Optional[Dict]:
        """
        Identify a Pokemon card from image data using GPT-4 Vision
        
        Args:
            image_data: Binary image data
            
        Returns:
            Dictionary containing card identification details
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        try:
            # Encode image to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare the prompt for GPT-4 Vision
            prompt = """
            Analyze this Pokemon card image and extract the following information:
            1. Card Name (the Pokemon's name)
            2. Set Name (the set/series this card belongs to, usually at the bottom)
            3. Card Number (e.g., "25/102" - number out of total in set)
            4. Any special features (holographic, first edition, etc.)
            
            Provide the response in this exact JSON format:
            {
                "card_name": "Pokemon name here",
                "set_name": "Set name here",
                "card_number": "Card number here (e.g., 25/102)",
                "special_features": "Any special features",
                "confidence": "high/medium/low"
            }
            
            Be as accurate as possible. If you cannot clearly read some information, mark confidence as "medium" or "low".
            """
            
            # Call GPT-4 Vision API
            response = await self.client.chat.completions.create(
                model="gpt-4o",  # Updated to use gpt-4o which supports vision
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.2  # Low temperature for more consistent results
            )
            
            # Extract the response
            content = response.choices[0].message.content
            logger.info(f"Vision API Response: {content}")
            
            # Parse the JSON response
            import json
            # Try to extract JSON from the response
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()
            
            result = json.loads(json_str)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in vision service: {str(e)}")
            raise


    async def identify_card_gemini(self, image_data: bytes) -> Optional[Dict]:
        """
        Alternative: Identify Pokemon card using Google Gemini Vision
        (Uncomment and use this if you prefer Gemini over OpenAI)
        
        Args:
            image_data: Binary image data
            
        Returns:
            Dictionary containing card identification details
        """
        # Implementation for Google Gemini Vision
        # Requires: pip install google-generativeai
        # 
        # import google.generativeai as genai
        # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # model = genai.GenerativeModel('gemini-pro-vision')
        # ... implementation here
        
        pass
