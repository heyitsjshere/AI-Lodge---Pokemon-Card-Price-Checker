# Pokemon Card Price Checker - Backend

Python FastAPI microservice for identifying Pokemon cards and fetching price information.

## Features

- 🎴 **AI-Powered Card Identification**: Uses OpenAI GPT-4o Vision to identify Pokemon cards from images
- 💰 **Multi-Source Price Aggregation**: Fetches prices from TCGPlayer, eBay, and Cardmarket
- 🔍 **Pokemon TCG API Integration**: Retrieves official card data and details (with fallback to mock data)
- ⚡ **Fast & Async**: Built with FastAPI for high performance
- 📊 **Market Analysis**: Provides market price averages and price trends
- 🔄 **Automatic Fallback**: Uses mock data when external APIs are unavailable

## Current Status

✅ **Working**:
- OpenAI GPT-4o Vision card identification (tested with multiple cards)
- FastAPI server with CORS support
- Complete API endpoints (health check, identify, price check)
- Mock price data for demonstration
- Frontend integration with drag-and-drop upload
- Fallback mechanism when Pokemon TCG API is down

⚠️ **Known Issues**:
- Pokemon TCG API experiencing timeout issues (504 Gateway Timeout)
- Price data is currently mock/placeholder (TCGPlayer API requires approval)
- Real-time price extraction needs Pokemon TCG API to be available

## Setup Instructions

### 1. Prerequisites

- Python 3.13.7 or higher (tested on 3.13.7)
- OpenAI API key (for GPT-4o Vision)

### 2. Installation

```bash
# Navigate to backend directory
cd backend

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
OPENAI_API_KEY=your-actual-openai-api-key-here
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

**Model Used**: GPT-4o (`gpt-4o`)
**Pricing**: ~$0.01-0.03 per image analysis

#### Pokemon TCG API Key (Not Required)
- Free tier available at [Pokemon TCG API](https://pokemontcg.io/)
- No API key needed for basic usage
- Currently experiencing server issues (fallback to mock data active)

#### TCGPlayer API Key (Optional - For Real Pricing)
- Requires application approval at [TCGPlayer Developer Portal](https://www.tcgplayer.com/developer)
- Approval time: 1-3 business days
- Used for official price data
- Currently using mock data as placeholder

### 5. Run the Server

```bash
# Make sure you're in the backend directory and virtual environment is activated
cd backend
source venv/bin/activate

# Run with uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://0.0.0.0:8000`

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
├── requirements.txt          # Python dependencies (Python 3.13 compatible)
├── .env                      # Environment variables (create from .env.example)
├── .env.example             # Environment variables template
├── venv/                    # Virtual environment (not in git)
├── models/
│   └── schemas.py           # Pydantic models for request/response
└── services/
    ├── vision_service.py    # OpenAI GPT-4o Vision integration
    ├── card_service.py      # Pokemon TCG API with fallback to mock data
    └── price_service.py     # Price aggregation (currently mock data)
```

## Dependencies (requirements.txt)

Key dependencies:
- `fastapi==0.115.0` - Web framework
- `uvicorn[standard]==0.32.0` - ASGI server
- `openai==1.54.0` - OpenAI API client (GPT-4o)
- `httpx==0.25.1` - Async HTTP client
- `pydantic==2.9.2` - Data validation
- `python-dotenv==1.0.0` - Environment variables
- `Pillow==10.4.0` - Image processing

All dependencies are Python 3.13 compatible.

## Response Examples

### Card Identification Response
```json
{
  "card_name": "Charizard",
  "set_name": "Base Set",
  "card_number": "4/102",
  "rarity": "Common",
  "card_id": "base-4",
  "image_url": null,
  "confidence": "high"
}
```

Note: `image_url` is `null` when using mock data (Pokemon TCG API unavailable).

### Price Check Response
```json
{
  "card_name": "Charizard",
  "set_name": "Base Set",
  "card_number": "4/102",
  "rarity": "Common",
  "card_id": "base-4",
  "image_url": null,
  "prices": [
    {
      "source": "TCGPlayer",
      "price": 23.45,
      "currency": "USD",
      "condition": "Near Mint",
      "url": "https://www.tcgplayer.com/search/pokemon/product?q=Charizard",
      "in_stock": true,
      "seller": "TCGPlayer Market"
    },
    {
      "source": "eBay",
      "price": 25.67,
      "currency": "USD",
      "condition": "Near Mint",
      "url": "https://www.ebay.com/sch/i.html?_nkw=Charizard+Base+Set+Pokemon+Card",
      "in_stock": true,
      "seller": "Various Sellers"
    }
  ],
  "market_price": 24.56,
  "price_trend": "stable",
  "last_updated": "2025-10-06T15:30:00"
}
```

Note: Prices are currently mock/random data for demonstration. Implement real API integrations for production.

## Testing Results

Successfully tested with:
- ✅ Turtwig (Celebrations)
- ✅ Gyarados (Base Set)
- ✅ Charizard (Brilliant Stars)
- ✅ Eevee VMAX (SWSH Black Star Promos)
- ✅ Lillie's Determination
- ✅ Mega Gardevoir EX

All cards were correctly identified by GPT-4o Vision with high confidence.

## Notes

- **Mock Data**: Price service currently uses random mock data since Pokemon TCG API is timing out and TCGPlayer API requires approval
- **Fallback System**: When Pokemon TCG API fails (504 timeout), the system automatically returns mock card data with correct identification from GPT-4o
- **Image Handling**: When mock data is used, the frontend displays the uploaded image instead of a placeholder
- **Rate Limiting**: Be mindful of OpenAI API rate limits
- **Image Size**: Keep uploaded images under 10MB
- **Supported Formats**: JPG, PNG, JPEG, WEBP
- **Timeout Settings**: Pokemon TCG API timeout set to 30 seconds with automatic fallback

## Frontend Integration

The backend is designed to work with the included frontend:
- Location: `../frontend/`
- Features: Drag-and-drop upload, image preview, results display
- Background: Custom Pokemon-themed background image
- Styling: Viridian green gradient header, responsive design

To run the full application:
1. Start backend: `cd backend && uvicorn app:app --host 0.0.0.0 --port 8000 --reload`
2. Open frontend: `open ../frontend/index.html` (or use a local server)

## Next Steps

1. ✅ ~~Test the API with sample Pokemon card images~~ - DONE
2. ✅ ~~Implement frontend integration~~ - DONE
3. ⏳ Wait for Pokemon TCG API to stabilize (currently timing out)
4. ⏳ Apply for TCGPlayer API access for real pricing (1-3 days approval)
5. 🔄 Implement real price extraction when Pokemon TCG API returns data
6. 📊 Add database for historical price tracking
7. 🚀 Deploy to production (AWS, Google Cloud, Vercel, etc.)

## Troubleshooting

**Issue**: `OPENAI_API_KEY not found`
- Solution: Make sure `.env` file exists with valid API key (not the placeholder value)

**Issue**: `No module named 'fastapi'`
- Solution: Activate virtual environment: `source venv/bin/activate`

**Issue**: `429 Too Many Requests` from OpenAI
- Solution: You've hit rate limits. Wait or upgrade API tier

**Issue**: `Pokemon TCG API timeout`
- Solution: This is expected - API is experiencing issues. App uses fallback mock data automatically

**Issue**: `CORS errors` in browser
- Solution: Backend has CORS enabled for localhost. Make sure backend is running on port 8000

**Issue**: Frontend shows old image
- Solution: Browser cache issue. Hard refresh with Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

## Server Logs Example

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:app:Processing image for price check: charizard.jpg
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:services.vision_service:Vision API Response: {"card_name": "Charizard", ...}
INFO:services.card_service:Searching Pokemon TCG API: name:"Charizard"
WARNING:services.card_service:Pokemon TCG API unavailable: 504 Gateway Timeout
INFO:services.card_service:Using mock data as fallback...
INFO:services.card_service:Returning mock data for Charizard
INFO:     127.0.0.1:50123 - "POST /api/check-price HTTP/1.1" 200 OK
```

## Support

For issues or questions:
- Open an issue on GitHub
- Check logs for detailed error messages
- Verify `.env` file has correct API keys
