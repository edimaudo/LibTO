# LibTO
LibTO is a civic intelligence platform and "Library OS" designed to transform [Toronto Public Library (TPL)](https://tpl.ca/about-the-library/open-data/) open data into actionable operational insights.
By leveraging Toronto Open Data and DigitalOcean Gradient AI, libTO allows denizens to understand library branch health and can discover programs & events.

## Key Features
### Overview
Operational Dashboard: A high-level overview of the Toronto Public Library System

### Library Insights
Library Operations: Ask questions about library operations + understand how library branches have changed overtime
- Library Agent: Can ask questions about library information or use it to search for certain amenities the library has
- Library Branch Forecaster: A tool to forecast visits, card registrations, workstation usage, circulations
- Library Pulse Agent: A real-time simulation engine to forecast the impact of operational changes 

### Library Programs & Events
Libeary Events: Leverages open data to show events happening at the different branches
- Event Concierge Agent: Discover branch programs and events filtered by AI to match specific user needs


## Tech Stack
- Backend: FastAPI 
- Data Processing: Pandas 
- Visualizations: Plotly (Interactive charts and maps)
- AI Intelligence: DigitalOcean Gradient AI (Llama-3 RAG Agents)
- Frontend: HTML5, CSS3 , Jinja2 Templates
- Deployment: Vercel

## Project Structure
```
libTO/
├── main.py              # FastAPI routes and server logic
├── data_processor.py    # Pandas logic for data cleaning & Health Index calculations
├── ai_agents.py         # DigitalOcean Gradient AI persona & simulation logic
├── static/
│   ├── css/
│   │   └── style.css    # TPL branding (Blue: #007FA3)
│   └── images/
│       └── logo.png     # TPL Logo
├── templates/
│   └── index.html       
├── requirements.txt     # Pinned dependencies
└── vercel.json          # Vercel deployment configuration
```

## Installation & Local Setup

Bash
```
git clone https://github.com/edimaudo/libTO.git
cd libTO
```

Set up a virtual environment:

Bash
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

Bash
```
pip install -r requirements.txt
Environment Variables: Create a .env file and add your DigitalOcean Gradient credentials:
```

Code snippet
```
GRADIENT_ACCESS_TOKEN=your_token_here
GRADIENT_WORKSPACE_ID=your_workspace_id_here
```

Run the application:

Bash
```
uvicorn main.py:app --reload
```
