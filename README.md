# LibTO
LibTO is a civic intelligence app designed to transform [Toronto Public Library (TPL)](https://tpl.ca/about-the-library/open-data/) open data into actionable operational insights.
By leveraging Toronto Open Data and DigitalOcean Gradient AI, libTO allows denizens to understand library branch health and can discover programs & events.

## Key Features
### Overview
A high-level overview of the Toronto Public Library System
- Library Agent for asking questions about high level information about the TPL network

### Branch Intelligence
Library Operations: Ask questions about library operations + understand how library branches have changed overtime
- Library Branch Agent: Can ask questions about library information or use it to search for certain amenities the library has
- Library Branch Forecaster: A tool to forecast visits, card registrations, workstation usage, circulations
- Library Pulse Agent: A real-time simulation engine to forecast the impact of operational changes 

### Library Programs & Events
Libeary Events: Leverages open data to show events happening at the different branches
- Event Concierge Agent: Discover branch programs and events filtered by AI to match specific user needs


## Tech Stack
- Front-end: Streamlit 
- Data Processing: Pandas 
- Visualizations: Plotly
- AI Intelligence: DigitalOcean Gradient AI

## Getting Started
1. Environment Configuration
Create a .env file in the root directory with your DigitalOcean credentials:

Bash
```
GRADIENT_ACCESS_TOKEN=your_token_here
GRADIENT_WORKSPACE_ID=your_workspace_id_here
```

2. Installation

Bash
```
pip install streamlit python-dotenv pandas
```

3. Running the App

Bash
```
streamlit run streamlit_app.py
```


