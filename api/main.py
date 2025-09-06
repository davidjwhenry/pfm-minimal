"""Ultra-minimal FastAPI app for Vercel deployment."""

import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="PFM Minimal", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# API Key validation
def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify API key from Authorization header."""
    api_key = os.getenv("PFM_API_KEY", "pfm-dev-key-12345")  # Default for development
    
    if credentials.credentials != api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

class ChatRequest(BaseModel):
    message: str
    team_mode: Optional[str] = "coordinate"

class ChatResponse(BaseModel):
    response: str
    team_used: str = "PFM Team"
    status: str = "success"

def get_advice(message: str) -> str:
    """Simple financial advice."""
    msg = message.lower()
    
    if "budget" in msg:
        return "**Budget Advice:** Use the 50/30/20 rule - 50% needs, 30% wants, 20% savings. Track expenses monthly and automate savings."
    elif "invest" in msg:
        return "**Investment Advice:** Start with index funds (VTI/VXUS), max out 401k match, open Roth IRA. Diversify and invest consistently."
    elif "debt" in msg:
        return "**Debt Strategy:** Use debt avalanche (highest interest first) or snowball (smallest balance first). Pay more than minimums."
    elif "save" in msg:
        return "**Savings Plan:** Build 3-6 month emergency fund first, then 15% to retirement. Use high-yield savings accounts."
    else:
        return "**Financial Planning:** Focus on emergency fund, debt payoff, retirement savings, and diversified investing. What specific area interests you?"

@app.get("/")
async def root():
    return {"message": "PFM Minimal API", "status": "online", "auth": "API key required for protected endpoints"}

@app.get("/health")
async def health():
    return {"status": "healthy", "platform": "vercel"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """Protected endpoint - requires API key."""
    advice = get_advice(request.message)
    return ChatResponse(response=advice, team_used="PFM Team")

# Public endpoint for testing
@app.get("/public/status")
async def public_status():
    return {"status": "online", "message": "Public endpoint - no auth required"}

@app.get("/v1/playground/status")
async def playground_status():
    return {"playground": "available", "teams": True}

@app.get("/v1/playground/agents")
async def playground_agents():
    return [{"name": "PFM Advisor", "type": "agent", "description": "Financial planning specialist"}]
