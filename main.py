from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from data_processor import DataProcessor
from ai_agents import LibraryAIAgent

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize Logic Classes
dp = DataProcessor()
ai = LibraryAIAgent()

# --- Exception Handlers ---

@app.exception_handler(404)
async def custom_404_handler(request: Request, __):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """The high-impact entry point."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """The functional 'Library OS' tool."""
    branches = dp.get_branch_list()
    return templates.TemplateResponse("dashboard.html", {"request": request, "branches": branches})

@app.post("/generate-insights")
async def generate_insights(request: Request, branch_name: str = Form(...), persona: str = Form(...)):
    try:
        data = dp.get_branch_data(branch_name)
        insight = await ai.get_persona_insight(persona, data)
        # Placeholder for real-time visualization data
        return {
            "status": "success",
            "branch": branch_name, 
            "insight": insight, 
            "data": data
        }
    except Exception as e:
        # If branch data isn't found, trigger a controlled error
        raise HTTPException(status_code=404, detail="Branch not found")

# Start the server if running locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
