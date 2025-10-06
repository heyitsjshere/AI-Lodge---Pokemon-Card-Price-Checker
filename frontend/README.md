# Pokemon Card Price Checker - Frontend

Beautiful, responsive web interface for the Pokemon Card Price Checker.

## Features

- 🎨 Modern, responsive design
- 📸 Drag & drop image upload
- 🔍 Real-time card identification
- 💰 Price comparison from multiple sources
- 📱 Mobile-friendly interface

## Setup

### Quick Start

1. **Start the backend server** (if not already running):
   ```bash
   cd ../backend
   source venv/bin/activate
   python3 app.py
   ```

2. **Open the frontend**:
   - Simply open `index.html` in your web browser
   - Or use a local server (recommended):
     ```bash
     # Using Python
     python3 -m http.server 3000
     
     # Or using Node.js (if you have it)
     npx http-server -p 3000
     ```

3. **Access the app**:
   - Direct: Open `index.html` in your browser
   - With server: http://localhost:3000

## Usage

1. **Upload**: Click or drag & drop a Pokemon card image
2. **Preview**: Review your image and click "Analyze Card"
3. **Results**: View card details, market price, and buy links

## Configuration

The frontend connects to the backend at `http://localhost:8000` by default.

To change this, edit `app.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Browser Compatibility

- Chrome/Edge: ✅ Fully supported
- Firefox: ✅ Fully supported
- Safari: ✅ Fully supported
- Mobile browsers: ✅ Responsive design

## File Structure

```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # CSS styling
├── app.js             # JavaScript logic & API calls
└── README.md          # This file
```

## Troubleshooting

**Issue**: "Cannot connect to the server"
- **Solution**: Make sure the backend is running at http://localhost:8000

**Issue**: CORS errors
- **Solution**: The backend already has CORS enabled. Make sure you're accessing from the same domain or using a local server.

**Issue**: Images not uploading
- **Solution**: Check file size (max 10MB) and format (JPG, PNG, JPEG only)

## Next Steps

- Deploy frontend to Netlify/Vercel
- Add authentication
- Implement card history
- Add price alerts
- Create mobile app version

## Technologies Used

- HTML5
- CSS3 (Grid, Flexbox, Animations)
- Vanilla JavaScript (ES6+)
- Fetch API for backend communication
