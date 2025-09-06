# PFM Minimal API

Production-ready Personal Finance Management API built with FastAPI and deployed on Vercel.

## 🚀 Live API

**Production URL**: `https://pfm-minimal-pfisku3rw-mal-abc4f885.vercel.app`

## 🔐 Authentication

This API uses Bearer token authentication. Include your API key in the Authorization header:

```bash
curl -X POST https://pfm-minimal-pfisku3rw-mal-abc4f885.vercel.app/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key-here" \
  -d '{"message": "Help me budget $60,000 salary"}'
```

## 📊 Available Endpoints

- **POST `/chat`** - Get financial advice (requires API key)
- **GET `/health`** - Health check
- **GET `/public/status`** - Public status endpoint
- **GET `/v1/playground/status`** - Agno Playground compatibility

## 💡 Financial Advice Categories

- **💰 Budgeting**: 50/30/20 rule, expense tracking, automation
- **📈 Investing**: Index funds, retirement accounts, asset allocation  
- **💳 Debt Management**: Avalanche vs snowball methods, credit optimization
- **💵 Savings**: Emergency funds, goal setting, high-yield accounts
- **📋 General Planning**: Comprehensive financial health advice

## 🔗 Integration Example

```typescript
const PFM_API = 'https://pfm-minimal-pfisku3rw-mal-abc4f885.vercel.app';
const API_KEY = 'your-api-key-here';

const getFinancialAdvice = async (message: string) => {
  const response = await fetch(`${PFM_API}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`
    },
    body: JSON.stringify({ message })
  });
  
  const data = await response.json();
  return data.response;
};
```

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn api.main:app --reload

# Test endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer pfm-dev-key-12345" \
  -d '{"message": "Help with budgeting"}'
```

## 🚀 Deployment

This project is configured for automatic deployment to Vercel when changes are pushed to the `main` branch.

### Environment Variables

Set these in your Vercel project:

- `PFM_API_KEY` - Your production API key

## 📁 Project Structure

```
pfm-minimal/
├── api/
│   └── main.py          # FastAPI application
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel configuration
├── SECURITY.md         # Security documentation
└── README.md           # This file
```

## 🔒 Security

- API key authentication required for protected endpoints
- CORS enabled for web app integration
- Rate limiting ready (can be added as needed)

## 📝 License

MIT License - see LICENSE file for details
