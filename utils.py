
# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import os, os.path
import warnings
import random
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import datetime
from datetime import datetime
import time
import matplotlib
import statistics
import scipy
from scipy.stats import linregress
import sklearn
from sklearn.linear_model import LinearRegression
import pmdarima as pm
from pmdarima import auto_arima
import google.generativeai as genai
from dotenv import load_dotenv, dotenv_values 
from functools import reduce

load_dotenv()

# App Information
APP_NAME = 'LibTO'
ABOUT_HEADER = 'About'
OVERVIEW_HEADER = 'TPL Overview'
BRANCH_INTELLIGENCE_HEADER = "TPL Branch Intelligence"
BRANCH_PROGRAM_EVENT_HEADER = 'Branch Program & Events'

warnings.simplefilter(action='ignore', category=FutureWarning)
st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)

