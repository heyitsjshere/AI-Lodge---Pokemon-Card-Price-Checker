# Pokemon Card Price Checker - Backend

Python FastAPI microservice for identifying Pokemon cards and fetching price information.

## Features

- 🎴 **AI-Powered Card Identification**: Uses OpenAI GPT-4 Vision to identify Pokemon cards from images
- 💰 **Multi-Source Price Aggregation**: Fetches prices from TCGPlayer, eBay, and Cardmarket
- 🔍 **Pokemon TCG API Integration**: Retrieves official card data and details
- ⚡ **Fast & Async**: Built with FastAPI for high performance
- 📊 **Market Analysis**: Provides market price averages and price trends

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- OpenAI API key (for GPT-4 Vision)

### 2. Installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
PORT=8000
DEBUG=True
```

### 4. Get API Keys

#### OpenAI API Key (Required)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

**Pricing**: ~$0.01-0.03 per image analysis

#### Pokemon TCG API Key (Optional)
- Free tier available at [Pokemon TCG API](https://dev.pokemontcg.io/)
- Higher rate limits with API key
- Not required for basic usage

#### TCGPlayer API Key (Optional)
- Requires application approval at [TCGPlayer](https://www.tcgplayer.com/)
- Used for official price data
- Falls back to mock data if not available

### 5. Run the Server

```bash
# Make sure you're in the backend directory
cd backend

# Run with uvicorn
python app.py

# OR
uvicorn app:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```bash
GET /
```

### Identify Card Only
```bash
POST /api/identify-card
Content-Type: multipart/form-data

file: [image file]
```

### Full Price Check (Identify + Prices)
```bash
POST /api/check-price
Content-Type: multipart/form-data

file: [image file]
```

### Get Prices by Card ID
```bash
GET /api/card/{card_id}/prices
```

## Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/

# Upload a Pokemon card image
curl -X POST http://localhost:8000/api/check-price \
  -F "file=@path/to/pokemon-card.jpg"
```

### Using Python

```python
import requests

url = "http://localhost:8000/api/check-price"
files = {"file": open("pokemon_card.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Interactive API Docs

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints directly in your browser.

## Project Structure

```
backend/
├── app.py                    # Main FastAPI application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── models/
│   └── schemas.py           # Pydantic models for request/response
└── services/
    ├── vision_service.py    # OpenAI GPT-4 Vision integration
    ├── card_service.py      # Pokemon TCG API integration
    └── price_service.py     # Price aggregation from multiple sources
```

## Response Examples

### Card Identification Response
```json
{
  "card_name": "Charizard",
  "set_name": "Base Set",
  "card_number": "4/102",
  "rarity": "Holo Rare",
  "card_id": "base1-4",
  "image_url": "https://images.pokemontcg.io/base1/4_hires.png",
  "confidence": "high"
}
```

### Price Check Response
```json
{
  "card_name": "Charizard",
  "set_name": "Base Set",
  "card_number": "4/102",
  "rarity": "Holo Rare",
  "card_id": "base1-4",
  "image_url": "https://images.pokemontcg.io/base1/4_hires.png",
  "prices": [
    {
      "source": "TCGPlayer",
      "price": 450.00,
      "currency": "USD",
      "condition": "Near Mint",
      "url": "https://www.tcgplayer.com/...",
      "in_stock": true,
      "seller": "TCGPlayer Market"
    }
  ],
  "market_price": 425.50,
  "price_trend": "rising",
  "last_updated": "2025-10-06T10:30:00"
}
```

## Notes

- The price service currently uses mock data for demonstration. Implement actual API integrations for production use.
- Rate limiting: Be mindful of API rate limits, especially for Pokemon TCG API (free tier)
- Image size: Keep uploaded images under 10MB
- Supported formats: JPG, PNG, JPEG, WEBP

## Next Steps

1. Test the API with sample Pokemon card images
2. Implement frontend integration
3. Add database for historical price tracking
4. Implement actual price scraping/API integration
5. Add user authentication (optional)
6. Deploy to production (AWS, Google Cloud, etc.)

## Troubleshooting

**Issue**: `OPENAI_API_KEY not found`
- Solution: Make sure `.env` file exists and contains valid API key

**Issue**: `429 Too Many Requests`
- Solution: You've hit rate limits. Wait or upgrade API tier

**Issue**: `Card not found`
- Solution: Image quality might be poor, or card is too new/obscure

## Support

For issues or questions, please open an issue on GitHub.
