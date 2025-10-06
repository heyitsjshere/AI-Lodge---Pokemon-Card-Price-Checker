// API Configuration
// For local development, use: 'http://localhost:8000'
// For production, use your Render backend URL
// Permanently point the frontend to the production Render backend.
// Change this value if you redeploy the backend to a different URL.
const API_BASE_URL = 'https://pokemon-card-backend-0vqc.onrender.com';

// Debug: show configured API base URL in console so we can verify deployment wiring
console.log('Configured API_BASE_URL =', API_BASE_URL);

// State
let selectedFile = null;

// DOM Elements and Event Listeners - wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing...');
    
    // DOM Elements
    const fileInput = document.getElementById('fileInput');
    const selectFileBtn = document.getElementById('selectFileBtn');
    const uploadBox = document.getElementById('uploadBox');
    const uploadSection = document.getElementById('uploadSection');
    const previewSection = document.getElementById('previewSection');
    const previewImage = document.getElementById('previewImage');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const changeImageBtn = document.getElementById('changeImageBtn');
    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    const retryBtn = document.getElementById('retryBtn');
    const newSearchBtn = document.getElementById('newSearchBtn');
    
    console.log('Elements loaded:', {
        fileInput: !!fileInput,
        selectFileBtn: !!selectFileBtn,
        uploadBox: !!uploadBox
    });

    // Event Listeners
    if (selectFileBtn) {
        selectFileBtn.addEventListener('click', (e) => {
            console.log('Select button clicked!');
            e.preventDefault();
            e.stopPropagation();
            if (fileInput) {
                fileInput.click();
            } else {
                console.error('fileInput not found!');
            }
        });
    } else {
        console.error('selectFileBtn not found!');
    }
    
    if (uploadBox) {
        uploadBox.addEventListener('click', () => {
            console.log('Upload box clicked!');
            if (fileInput) fileInput.click();
        });
    }
    
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
    
    if (analyzeBtn) analyzeBtn.addEventListener('click', analyzeCard);
    if (changeImageBtn) changeImageBtn.addEventListener('click', resetToUpload);
    if (retryBtn) retryBtn.addEventListener('click', resetToUpload);
    if (newSearchBtn) newSearchBtn.addEventListener('click', resetToUpload);

    // Drag and Drop
    if (uploadBox) {
        uploadBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadBox.classList.add('dragover');
        });

        uploadBox.addEventListener('dragleave', () => {
            uploadBox.classList.remove('dragover');
        });

        uploadBox.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadBox.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        });
    }

    // Functions
    function handleFileSelect(event) {
        console.log('File select triggered');
        const file = event.target.files[0];
        console.log('Selected file:', file);
        if (file) {
            handleFile(file);
        }
    }

    function handleFile(file) {
        console.log('handleFile called with:', file);
        
        // Validate file type
        if (!file.type.startsWith('image/')) {
            showError('Please select a valid image file (JPG, PNG, JPEG)');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            showError('File size must be less than 10MB');
            return;
        }

        selectedFile = file;
        console.log('File validated, starting FileReader');
        
        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            console.log('FileReader loaded successfully');
            previewImage.src = e.target.result;
            showSection(previewSection);
            hideSection(uploadSection);
        };
        reader.onerror = (e) => {
            console.error('FileReader error:', e);
            showError('Failed to read the image file');
        };
        reader.readAsDataURL(file);
        console.log('FileReader.readAsDataURL called');
    }

    async function analyzeCard() {
        if (!selectedFile) {
            showError('Please select an image first');
            return;
        }

        // Show loading
    showSection(loadingSection);
    hideSection(previewSection);

    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        // Call API with cache-busting
        const response = await fetch(`${API_BASE_URL}/api/check-price?t=${Date.now()}`, {
            method: 'POST',
            body: formData,
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache'
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to analyze card');
        }

        // Show results
        displayResults(data);
        showSection(resultsSection);
        hideSection(loadingSection);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to analyze the card. Please try again.');
        hideSection(loadingSection);
    }
}

function displayResults(data) {
    // Card Info
    document.getElementById('cardName').textContent = data.card_name;
    document.getElementById('cardSet').textContent = data.set_name || 'N/A';
    document.getElementById('cardNumber').textContent = data.card_number || 'N/A';
    document.getElementById('cardRarity').textContent = data.rarity || 'N/A';
    document.getElementById('cardId').textContent = data.card_id || 'N/A';
    
    // Card Image - force reload with cache busting
    const resultCardImage = document.getElementById('resultCardImage');
    if (data.image_url) {
        // Add timestamp to bust cache
        resultCardImage.src = data.image_url + '?t=' + Date.now();
    } else {
        // Use the uploaded preview image
        resultCardImage.src = previewImage.src;
    }

    // Market Price
    const marketPrice = data.market_price || 0;
    document.getElementById('marketPrice').textContent = `$${marketPrice.toFixed(2)}`;

    // Price Trend
    const trendBadge = document.querySelector('.trend-badge');
    const trend = data.price_trend || 'stable';
    trendBadge.textContent = trend;
    trendBadge.className = 'trend-badge';
    
    // Add trend-specific styling
    if (trend === 'rising') {
        trendBadge.style.background = 'rgba(39, 174, 96, 0.3)';
    } else if (trend === 'falling') {
        trendBadge.style.background = 'rgba(231, 76, 60, 0.3)';
    }

    // Price Listings
    const priceList = document.getElementById('priceList');
    priceList.innerHTML = '';

    if (data.prices && data.prices.length > 0) {
        data.prices.forEach(price => {
            const priceItem = document.createElement('div');
            priceItem.className = 'price-item';
            priceItem.innerHTML = `
                <div>
                    <div class="price-source">${price.source}</div>
                    <div class="price-condition">${price.condition}</div>
                </div>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="price-amount">$${price.price.toFixed(2)}</div>
                    <a href="${price.url}" target="_blank" class="buy-link">Buy</a>
                </div>
            `;
            priceList.appendChild(priceItem);
        });
    } else {
        priceList.innerHTML = '<p style="color: var(--text-light);">No price listings available</p>';
    }
}

function showError(message) {
    errorMessage.textContent = message;
    showSection(errorSection);
    hideSection(uploadSection);
    hideSection(previewSection);
    hideSection(loadingSection);
    hideSection(resultsSection);
}

function resetToUpload() {
    selectedFile = null;
    fileInput.value = '';
    showSection(uploadSection);
    hideSection(previewSection);
    hideSection(loadingSection);
    hideSection(resultsSection);
    hideSection(errorSection);
}

    function showSection(section) {
        section.classList.remove('hidden');
    }

    function hideSection(section) {
        section.classList.add('hidden');
    }

    // Check API connectivity on load
    async function checkAPIConnection() {
        try {
            console.log('Checking API connection to', API_BASE_URL + '/');
            const response = await fetch(`${API_BASE_URL}/`);
            console.log('Health check response status:', response.status);
            const bodyText = await response.text();
            console.log('Health check response body:', bodyText);
            if (!response.ok) {
                throw new Error('API not available (status ' + response.status + ')');
            }
            console.log('✅ Connected to Pokemon Card Price Checker API');
        } catch (error) {
            console.error('❌ Failed to connect to API. Make sure the backend is running at', API_BASE_URL, error);
            showError('Cannot connect to the server. Please make sure the backend is running. Check browser console for details.');
        }
    }
    
    // Check connection
    checkAPIConnection();
});
