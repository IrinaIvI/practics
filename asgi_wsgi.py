from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()
API_URL = "https://api.exchangerate-api.com/v4/latest/{}"

@app.get("/{currency}")
async def get_exchange_rate(currency: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL.format(currency))
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
