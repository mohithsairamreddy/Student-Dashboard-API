from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import logging
import time
import asyncio

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# Environment variables
REDASH_API_KEY = os.getenv('REDASH_API_KEY', 'pGeiV72zVfRn8ZpUWSNATVl24jDdOybYBBIAKkiS')
REDASH_BASE_URL = 'https://viz-data-dashboard.ei-insights.study'

# Template configuration
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/student-data")
async def get_student_data():
    start_time = time.time()
    
    try:
        query_id = '1283'
        results_url = f'{REDASH_BASE_URL}/api/queries/{query_id}/results.json'
        
        headers = {
            'Authorization': f'Key {REDASH_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Use asyncio to perform HTTP request
        async with asyncio.Timeout(10):  # Optional timeout
            async with requests.Session() as session:
                response = await asyncio.to_thread(session.get, results_url, headers=headers)
        
        end_time = time.time()
        latency = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'query_result' in data and 'data' in data['query_result'] and 'rows' in data['query_result']['data']:
                result = data['query_result']['data']['rows'][0]
                result['_latency'] = latency
                return result
        
        return JSONResponse(content={'error': 'Failed to fetch data', '_latency': latency}, status_code=500)
        
    except Exception as e:
        end_time = time.time()
        latency = end_time - start_time
        return JSONResponse(content={'error': str(e), '_latency': latency}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)