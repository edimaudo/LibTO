# LibTO
LibTO is a civic intelligence app designed to transform [Toronto Public Library (TPL)](https://tpl.ca/about-the-library/open-data/) open data into actionable operational insights.
By leveraging Toronto Open Data, libTO allows denizens to understand library branch health and can discover programs & events.

## Key Features
### Overview
- A high-level overview of the Toronto Public Library Network

### Branch Intelligence
- Shows trends to understand how a library branchhas have changed overtime + Library Branch Forecaster: A tool to forecast visits, card registrations, workstation usage, circulations
- Provides the ability to an ask questions about a particular library using the branch agent

## Tech Stack
- Front-end: Streamlit 
- Data Processing: Pandas 
- Visualizations: Plotly
- AI Intelligence: Google Gemini

## Getting Started
1. Environment Configuration
Create a .env file in the root directory with your AI credentials:

Bash
```
GEMINI_API_KEY=your_gemini_api_key_here
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


