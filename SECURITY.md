# 🔐 PFM API Security Guide

## **Deployment Security Options**

### **✅ Option 1: API Key Authentication (Recommended)**

**Current Implementation**: Your API now uses Bearer token authentication.

**Setup in Vercel:**
1. Go to [vercel.com/mal-abc4f885/pfm-minimal](https://vercel.com/mal-abc4f885/pfm-minimal)
2. Go to **Settings** → **Environment Variables**
3. Add: `PFM_API_KEY` = `your-secure-api-key-here`
4. **Disable Vercel Authentication** in **Settings** → **Deployment Protection**

**Usage in your v0 app:**
```typescript
const PFM_API = 'https://pfm-minimal-oqeqn1keo-mal-abc4f885.vercel.app';
const API_KEY = 'your-secure-api-key-here';

const getFinancialAdvice = async (message: string) => {
  const response = await fetch(`${PFM_API}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`
    },
    body: JSON.stringify({ message })
  });
  
  if (!response.ok) {
    throw new Error('Authentication failed');
  }
  
  const data = await response.json();
  return data.response;
};
```

### **✅ Option 2: Vercel Authentication + Allowlist**

**Setup:**
1. Keep **Vercel Authentication** enabled
2. Go to **Settings** → **Deployment Protection**
3. Add your v0 app domain to **Trusted Origins**
4. Add your IP addresses to **IP Allowlist**

**Pros:** 
- No code changes needed
- Vercel handles authentication
- Good for internal/team use

**Cons:**
- Less flexible for public APIs
- Harder to integrate with external services

### **✅ Option 3: JWT Authentication (Advanced)**

For more sophisticated auth, you could implement JWT tokens:

```python
import jwt
from datetime import datetime, timedelta

def create_jwt_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

## **🎯 Recommended Approach for v0 Integration**

**Use Option 1 (API Key)** because:

✅ **Simple Integration**: Easy to add to your v0 frontend  
✅ **Secure**: Proper authentication without complexity  
✅ **Flexible**: Works with any client application  
✅ **Scalable**: Can add rate limiting, user tracking later  
✅ **Standard**: Industry-standard Bearer token approach  

## **🔒 Security Best Practices**

### **API Key Management:**
```typescript
// In your v0 app - store API key securely
const API_KEY = process.env.NEXT_PUBLIC_PFM_API_KEY; // For client-side
// OR
const API_KEY = process.env.PFM_API_KEY; // For server-side (more secure)
```

### **Error Handling:**
```typescript
const callPFMAPI = async (message: string) => {
  try {
    const response = await fetch(`${PFM_API}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({ message })
    });

    if (response.status === 401) {
      throw new Error('API key invalid or expired');
    }
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('PFM API Error:', error);
    return { response: 'Sorry, financial advice is temporarily unavailable.' };
  }
};
```

### **Rate Limiting (Future Enhancement):**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("10/minute")  # 10 requests per minute
async def chat(request: Request, chat_request: ChatRequest):
    # ... existing code
```

## **🚀 Next Steps**

1. **Set Environment Variable**: Add `PFM_API_KEY` in Vercel
2. **Disable Vercel Auth**: Turn off deployment protection
3. **Test Authentication**: Use the examples above
4. **Integrate with v0**: Add API calls to your frontend
5. **Monitor Usage**: Check Vercel analytics for API usage

## **🧪 Testing Your Secured API**

```bash
# Test without API key (should fail)
curl -X POST https://pfm-minimal-oqeqn1keo-mal-abc4f885.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Help with budgeting"}'

# Test with API key (should work)
curl -X POST https://pfm-minimal-oqeqn1keo-mal-abc4f885.vercel.app/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key-here" \
  -d '{"message": "Help with budgeting"}'

# Test public endpoint (no auth needed)
curl https://pfm-minimal-oqeqn1keo-mal-abc4f885.vercel.app/public/status
```

Your API is now **production-ready** with proper authentication! 🎉
