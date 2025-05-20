from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Read API key and URL from .env
API_KEY = os.getenv("4jXrGTxuSnp2alL49+AB9Q==knASijU4VY3wjEDu")
API_URL = os.getenv("https://api.api-ninjas.com/v1/vinlookup")

app = FastAPI()

@app.get("/vin/{vin}")
async def get_car_details(vin: str):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"vin": vin}
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))