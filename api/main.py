from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from data_processor import DataProcessor
from ai_agents import LibraryAIAgent
import os

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize Logic Classes
dp = DataProcessor()
ai = LibraryAIAgent()

# routes
@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/overview", response_class=HTMLResponse)
async def read_overview(request: Request):
    kpis = dp.get_overview_kpis()
    charts = dp.get_trend_charts()
    heatmap = dp.get_heatmap()
    
    return templates.TemplateResponse("overview.html", {
        "request": request,
        "kpis": kpis,
        "charts": charts,
        "heatmap": heatmap
    })

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)


# Start the server if running locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
