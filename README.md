# 🎴 Pokemon Card Price Checker

AI-powered web application that identifies Pokemon cards from images and provides price information from multiple marketplaces.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange)

## Features

- **🤖 AI Card Identification**: Uses OpenAI GPT-4o Vision to accurately identify Pokemon cards from photos
- ** Multi-Source Pricing**: Aggregates prices from TCGPlayer, eBay, and Cardmarket
- ** Market Analysis**: Shows average market price and price trends
- ** Drag & Drop Upload**: User-friendly interface with image preview
- ** Fast & Responsive**: Built with FastAPI for high performance
- ** Beautiful UI**: Pokemon-themed design with custom background

## Quick Start

### Prerequisites

- Python 3.13+ (tested on 3.13.7)
- OpenAI API key
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/heyitsjshere/AI-Lodge---Pokemon-Card-Price-Checker.git
cd AI-Lodge---Pokemon-Card-Price-Checker
```

2. **Set up the backend**
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

3. **Run the backend server**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

4. **Open the frontend**
```bash
# In a new terminal, navigate to frontend
cd ../frontend

# Open in browser
open index.html
```

The app will be available at `http://localhost:8000` (backend) and you can open `frontend/index.html` directly in your browser.

## How It Works

1. **Upload** - Drag and drop or select a Pokemon card image
2. **Identify** - AI analyzes the card using GPT-4o Vision
3. **Price Check** - System fetches prices from multiple sources
4. **Results** - View card details, market price, and buy links

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI GPT-4o** - Vision AI for card identification
- **Pokemon TCG API** - Official card database
- **httpx** - Async HTTP client
- **Pydantic** - Data validation

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **Fetch API** - Modern HTTP requests
- **Responsive CSS** - Works on all devices
- **Custom Pokemon Theme** - Viridian green styling

## 📁 Project Structure

```
AI-Lodge---Pokemon-Card-Price-Checker/
├── backend/
│   ├── app.py                 # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables (create this)
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   └── services/
│       ├── vision_service.py  # OpenAI integration
│       ├── card_service.py    # Pokemon TCG API
│       └── price_service.py   # Price aggregation
│
├── frontend/
│   ├── index.html            # Main HTML page
│   ├── styles.css            # Styling
│   ├── app.js                # JavaScript logic
│   └── assets/
│       └── pokemon-background.png  # Background image
│
└── README.md                 # This file
```

##  API Keys

### OpenAI API (Required)
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and generate an API key
3. Add to `backend/.env`: `OPENAI_API_KEY=sk-...`
4. Cost: ~$0.01-0.03 per image

### TCGPlayer API (Optional - For Real Pricing)
1. Apply at [TCGPlayer Developer Portal](https://www.tcgplayer.com/developer)
2. Approval takes 1-3 business days
3. Currently using mock data as placeholder

## Current Status

**Working:**
- Card identification with GPT-4o (tested with 6+ different cards)
- Full frontend with drag-and-drop upload
- Backend API with all endpoints
- Fallback to mock data when APIs are unavailable
- CORS configuration for local development

**Known Issues:**
- Pokemon TCG API experiencing timeouts (504 errors)
- Price data is mock/placeholder (pending TCGPlayer approval)
- Select image button may require page refresh to work

**Tested Cards:**
- Turtwig (Celebrations)
- Gyarados (Base Set)
- Charizard (Brilliant Stars)
- Eevee VMAX
- Lillie's Determination
- Mega Gardevoir EX

## 📊 API Endpoints

### `GET /`
Health check endpoint

### `POST /api/identify-card`
Identify card from image (no pricing)

### `POST /api/check-price`
Full workflow: identify card + get prices

### `GET /api/card/{card_id}/prices`
Get prices for specific card ID

### Interactive Docs
Visit `http://localhost:8000/docs` for Swagger UI

## Testing

**Test with cURL:**
```bash
curl -X POST http://localhost:8000/api/check-price \
  -F "file=@path/to/pokemon-card.jpg"
```

**Test with Python:**
```python
import requests

url = "http://localhost:8000/api/check-price"
files = {"file": open("pokemon_card.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## Troubleshooting

**Backend won't start:**
- Verify virtual environment is activated
- Check `.env` file has valid OpenAI API key
- Ensure port 8000 is not in use: `lsof -ti:8000 | xargs kill -9`

**Card identification fails:**
- Ensure image is clear and well-lit
- Check image file size (max 10MB)
- Verify OpenAI API key is valid

**Prices not loading:**
- Expected - Pokemon TCG API currently timing out
- App automatically uses mock data as fallback
- Real pricing requires TCGPlayer API approval

**Frontend can't connect:**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Try hard refresh (Cmd+Shift+R)

## 🚀 Deployment

**Ready to deploy? Follow the complete guide:** [DEPLOYMENT.md](./DEPLOYMENT.md)

### Quick Deploy

**Backend (Render):**
1. Push code to GitHub
2. Connect repo to [Render](https://render.com/)
3. Set `OPENAI_API_KEY` environment variable
4. Deploy! Get URL like: `https://your-app.onrender.com`

**Frontend (Vercel):**
1. Install: `npm install -g vercel`
2. Update `API_BASE_URL` in `frontend/app.js` to your backend URL
3. Run: `vercel --prod`
4. Get URL like: `https://your-app.vercel.app`

**Free Tier Available** - Perfect for demos and portfolios!

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- Step-by-step instructions
- Alternative platforms (Railway, Netlify, Heroku)
- Environment configuration
- Custom domains
- Troubleshooting
- Cost breakdown

## 📝 Next Steps

- [ ] Wait for Pokemon TCG API to stabilize
- [ ] Apply for and integrate TCGPlayer API
- [ ] Add database for price history tracking
- [ ] Implement user accounts and favorites
- [ ] Add card collection management
- [ ] Deploy to production
- [ ] Add more card marketplaces

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## License

MIT License - feel free to use this project for learning or commercial purposes.

## Author

Created by [@heyitsjshere](https://github.com/heyitsjshere)

## Acknowledgments

- OpenAI for GPT-4o Vision API
- [Pokemon TCG API](https://pokemontcg.io/) for card data
- Pokemon Company for the amazing cards!

---

**Note**: This is a demonstration project. Price data is currently mock/placeholder. For production use, integrate official marketplace APIs and add proper error handling, rate limiting, and caching.
