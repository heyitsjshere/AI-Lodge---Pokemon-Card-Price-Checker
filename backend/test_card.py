#!/usr/bin/env python3
"""
Simple test script to upload a Pokemon card image to the API
"""
import requests
import sys
import os
from pathlib import Path

def test_card_price_check(image_path):
    """Test the card price check endpoint"""
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found: {image_path}")
        return
    
    # API endpoint
    url = "http://localhost:8000/api/check-price"
    
    print(f"📸 Uploading image: {image_path}")
    print(f"🔗 Sending to: {url}")
    print("⏳ Processing...\n")
    
    try:
        # Open and send the file
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(url, files=files)
        
        # Check response
        if response.status_code == 200:
            print("✅ Success!\n")
            result = response.json()
            
            print("=" * 60)
            print("📋 CARD IDENTIFICATION RESULT")
            print("=" * 60)
            print(f"Card Name:     {result.get('card_name')}")
            print(f"Set:           {result.get('set_name')}")
            print(f"Card Number:   {result.get('card_number')}")
            print(f"Rarity:        {result.get('rarity')}")
            print(f"Card ID:       {result.get('card_id')}")
            print(f"Image URL:     {result.get('image_url')}")
            print()
            
            print("=" * 60)
            print("💰 PRICE INFORMATION")
            print("=" * 60)
            print(f"Market Price:  ${result.get('market_price', 'N/A')}")
            print(f"Price Trend:   {result.get('price_trend', 'N/A')}")
            print()
            
            prices = result.get('prices', [])
            if prices:
                print(f"Found {len(prices)} price listings:")
                print()
                for i, price in enumerate(prices, 1):
                    print(f"  {i}. {price['source']}")
                    print(f"     Price: ${price['price']} {price['currency']}")
                    print(f"     Condition: {price['condition']}")
                    print(f"     URL: {price['url']}")
                    print(f"     In Stock: {'✓' if price['in_stock'] else '✗'}")
                    print()
            
            print("=" * 60)
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def find_pokemon_images():
    """Find Pokemon card images in Downloads folder"""
    downloads = Path.home() / "Downloads"
    
    # Common image extensions
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    
    images = []
    for ext in extensions:
        images.extend(downloads.glob(ext))
    
    return sorted(images)[:10]  # Return first 10


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use provided image path
        image_path = sys.argv[1]
        test_card_price_check(image_path)
    else:
        # Find images in Downloads
        print("🔍 Looking for images in Downloads folder...\n")
        images = find_pokemon_images()
        
        if not images:
            print("❌ No images found in Downloads folder")
            print("\nUsage:")
            print("  python3 test_card.py /path/to/pokemon-card.jpg")
        else:
            print(f"Found {len(images)} image(s):")
            for i, img in enumerate(images, 1):
                print(f"  {i}. {img.name}")
            
            print("\nTo test with an image, run:")
            print(f"  python3 test_card.py ~/Downloads/{images[0].name}")
