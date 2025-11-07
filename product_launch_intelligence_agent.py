import streamlit as st
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.firecrawl import FirecrawlTools
from dotenv import load_dotenv
from datetime import datetime
from textwrap import dedent
import os
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import base64

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="🚀 LaunchIQ Intelligence", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Custom CSS for Dark Theme & Animations ----------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Orbitron:wght@500;700;900&display=swap');
    
    /* Main App Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated Gradient Background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Title Animation */
    @keyframes glow {
        0%, 100% {
            text-shadow: 0 0 10px #00fff2, 0 0 20px #00fff2, 0 0 30px #00fff2, 0 0 40px #00fff2;
        }
        50% {
            text-shadow: 0 0 20px #ff00ff, 0 0 30px #ff00ff, 0 0 40px #ff00ff, 0 0 50px #ff00ff;
        }
    }
    
    @keyframes slideInFromTop {
        0% {
            transform: translateY(-50px);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes fadeInUp {
        0% {
            transform: translateY(30px);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes rotateGradient {
        0% {
            filter: hue-rotate(0deg);
        }
        100% {
            filter: hue-rotate(360deg);
        }
    }
    
    /* Animated Title */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00fff2, #ff00ff, #00fff2);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease infinite, slideInFromTop 1s ease-out;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: 2px;
    }
    
    /* Animated Subtitle */
    .main-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        color: #00fff2;
        text-align: center;
        animation: fadeInUp 1.5s ease-out;
        margin-top: 10px;
        letter-spacing: 1px;
    }
    
    /* Card Styling with Glass Effect */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: linear-gradient(135deg, rgba(0, 255, 242, 0.1), rgba(255, 0, 255, 0.1));
        border-radius: 12px;
        color: #00fff2;
        font-weight: 600;
        border: 1px solid rgba(0, 255, 242, 0.3);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, rgba(0, 255, 242, 0.3), rgba(255, 0, 255, 0.3));
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0, 255, 242, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00fff2, #ff00ff) !important;
        color: #000 !important;
        font-weight: 700;
        box-shadow: 0 0 20px rgba(0, 255, 242, 0.6);
    }
    
    /* Button Animations */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
        animation: pulse 1s infinite;
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    /* Primary Button Special Style */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        animation: rotateGradient 3s linear infinite;
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 30px rgba(245, 87, 108, 0.8);
    }
    
    /* Input Fields Styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(0, 255, 242, 0.3);
        border-radius: 12px;
        color: #fff;
        font-size: 1rem;
        padding: 12px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00fff2;
        box-shadow: 0 0 15px rgba(0, 255, 242, 0.5);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(0, 255, 242, 0.3);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #00fff2;
        box-shadow: 0 0 15px rgba(0, 255, 242, 0.3);
    }
    
    /* Slider Styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 242, 0.3);
        border-radius: 12px;
        color: #00fff2;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(0, 255, 242, 0.1);
        box-shadow: 0 0 15px rgba(0, 255, 242, 0.3);
    }
    
    /* Container Cards */
    .element-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(0, 255, 242, 0.3);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0, 255, 242, 0.4);
    }
    
    .stMetric label {
        color: #00fff2 !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #fff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Success/Error/Info Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 255, 127, 0.2), rgba(0, 200, 100, 0.2));
        border-left: 5px solid #00ff7f;
        border-radius: 12px;
        animation: slideInFromTop 0.5s ease-out;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 0, 100, 0.2), rgba(200, 0, 80, 0.2));
        border-left: 5px solid #ff0064;
        border-radius: 12px;
        animation: slideInFromTop 0.5s ease-out;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(0, 191, 255, 0.2), rgba(0, 150, 200, 0.2));
        border-left: 5px solid #00bfff;
        border-radius: 12px;
        animation: slideInFromTop 0.5s ease-out;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.2), rgba(200, 130, 0, 0.2));
        border-left: 5px solid #ffa500;
        border-radius: 12px;
        animation: slideInFromTop 0.5s ease-out;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid rgba(0, 255, 242, 0.3);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #00fff2;
    }
    
    /* Divider with Glow */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00fff2, transparent);
        margin: 30px 0;
        box-shadow: 0 0 10px rgba(0, 255, 242, 0.5);
    }
    
    /* Markdown Content */
    .stMarkdown {
        color: #e0e0e0;
        line-height: 1.6;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #00fff2;
        font-weight: 700;
    }
    
    .stMarkdown h1 {
        border-bottom: 3px solid #00fff2;
        padding-bottom: 10px;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Spinner Animation */
    .stSpinner > div {
        border-color: #00fff2 transparent #ff00ff transparent;
    }
    
    /* Download Button Special */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        animation: float 3s ease-in-out infinite;
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 0 30px rgba(56, 239, 125, 0.8);
    }
    
    /* Status Icons Animation */
    .status-icon {
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00fff2, #ff00ff);
    }
    
    /* Floating Particles Effect */
    @keyframes float-particles {
        0%, 100% {
            transform: translateY(0) translateX(0);
            opacity: 0.3;
        }
        50% {
            transform: translateY(-20px) translateX(10px);
            opacity: 0.6;
        }
    }
    
    /* Code Block Styling */
    code {
        background: rgba(0, 255, 242, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
        color: #00fff2;
        font-family: 'Courier New', monospace;
    }
    
    /* Table Styling */
    table {
        border-collapse: collapse;
        width: 100%;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        overflow: hidden;
    }
    
    thead {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
    
    th {
        color: white;
        font-weight: 700;
        padding: 15px;
    }
    
    td {
        color: #e0e0e0;
        padding: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    tr:hover {
        background: rgba(0, 255, 242, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Environment & Agent ----------------
load_dotenv()

# ---------------- Data Persistence Setup ----------------
DATA_DIR = Path("intelligence_data")
DATA_DIR.mkdir(exist_ok=True)
HISTORY_FILE = DATA_DIR / "analysis_history.json"
ALERTS_FILE = DATA_DIR / "alerts_config.json"

# Initialize history file
if not HISTORY_FILE.exists():
    HISTORY_FILE.write_text(json.dumps([]))

# Initialize alerts file
if not ALERTS_FILE.exists():
    ALERTS_FILE.write_text(json.dumps({}))

# Add animated logo at the top of sidebar
st.sidebar.markdown("""
<style>
    @keyframes logoFloat {
        0%, 100% {
            transform: translateY(0px) rotate(0deg);
        }
        25% {
            transform: translateY(-10px) rotate(5deg);
        }
        75% {
            transform: translateY(-5px) rotate(-5deg);
        }
    }
    
    @keyframes logoGlow {
        0%, 100% {
            filter: drop-shadow(0 0 10px rgba(0, 255, 242, 0.6)) 
                    drop-shadow(0 0 20px rgba(255, 0, 255, 0.4));
        }
        50% {
            filter: drop-shadow(0 0 20px rgba(255, 0, 255, 0.8)) 
                    drop-shadow(0 0 30px rgba(0, 255, 242, 0.6));
        }
    }
    
    @keyframes logoRotate {
        0% {
            transform: rotate(0deg) scale(1);
        }
        50% {
            transform: rotate(180deg) scale(1.1);
        }
        100% {
            transform: rotate(360deg) scale(1);
        }
    }
    
    @keyframes logoPulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(0, 255, 242, 0.5), 0 0 40px rgba(255, 0, 255, 0.3);
        }
        50% {
            box-shadow: 0 0 40px rgba(0, 255, 242, 0.8), 0 0 60px rgba(255, 0, 255, 0.6);
        }
    }
    
    .logo-container {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
        border-radius: 20px;
        border: 3px solid rgba(0, 255, 242, 0.5);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        animation: logoPulse 3s ease-in-out infinite;
    }
    
    .logo-container::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 242, 0.15), transparent);
        animation: logoRotate 4s linear infinite;
    }
    
    .logo-container::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(-45deg, transparent, rgba(255, 0, 255, 0.15), transparent);
        animation: logoRotate 4s linear infinite reverse;
    }
    
    .logo-image {
        position: relative;
        z-index: 1;
        animation: logoFloat 4s ease-in-out infinite, logoGlow 2s ease-in-out infinite;
        border-radius: 50%;
        transition: all 0.5s ease;
        background: rgba(0, 0, 0, 0.3);
        padding: 10px;
    }
    
    .logo-image:hover {
        transform: scale(1.2) rotate(360deg);
        filter: drop-shadow(0 0 40px rgba(0, 255, 242, 1)) 
                drop-shadow(0 0 50px rgba(255, 0, 255, 1))
                drop-shadow(0 0 60px rgba(255, 165, 0, 0.8));
        cursor: pointer;
    }
    
    .logo-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00fff2, #ff00ff, #ffd700, #00fff2);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 4s ease infinite;
        margin-top: 15px;
        letter-spacing: 3px;
        text-shadow: 0 0 20px rgba(0, 255, 242, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .logo-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 0.75rem;
        color: #00fff2;
        margin-top: 5px;
        letter-spacing: 2px;
        opacity: 0.8;
        position: relative;
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)

# Display logo if it exists
logo_path = Path("Logo.png")
if logo_path.exists():
    with open(logo_path, "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()
    st.sidebar.markdown(f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_data}" class="logo-image" width="140">
        <div class="logo-title">LaunchIQ</div>
        <div class="logo-subtitle">INTELLIGENCE AI</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div class="logo-container">
        <div style="font-size: 4rem; animation: logoFloat 4s ease-in-out infinite;">🚀</div>
        <div class="logo-title">LaunchIQ</div>
        <div class="logo-subtitle">INTELLIGENCE AI</div>
    </div>
    """, unsafe_allow_html=True)

# Add API key inputs in sidebar with enhanced design
st.sidebar.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
">
    <h2 style="color: white; margin: 0; font-family: 'Orbitron', sans-serif;">🔑 API Configuration</h2>
</div>
""", unsafe_allow_html=True)

with st.sidebar.container():
    openai_key = st.text_input(
        "🤖 OpenAI API Key", 
        type="password", 
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Required for AI agent functionality"
    )
    firecrawl_key = st.text_input(
        "🔥 Firecrawl API Key", 
        type="password", 
        value=os.getenv("FIRECRAWL_API_KEY", ""),
        help="Required for web search and crawling"
    )

# Set environment variables
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
if firecrawl_key:
    os.environ["FIRECRAWL_API_KEY"] = firecrawl_key

# Initialize team only if both keys are provided
if openai_key and firecrawl_key:
    # Agent 1: Competitor Launch Analyst
    launch_analyst = Agent(
        name="Product Launch Analyst",
        description=dedent("""
            You are a senior Go-To-Market strategist who evaluates competitor product launches with a critical, evidence-driven lens.
            Your objective is to uncover:
            • How the product is positioned in the market
            • Which launch tactics drove success (strengths)
            • Where execution fell short (weaknesses)
            • Actionable learnings competitors can leverage
            Always cite observable signals (messaging, pricing actions, channel mix, timing, engagement metrics). Maintain a crisp, executive tone and focus on strategic value.
            IMPORTANT: Conclude your report with a 'Sources:' section, listing all URLs of websites you crawled or searched for this analysis.
        """),
        model=OpenAIChat(id="gpt-4o-mini", temperature=0.3),
        tools=[FirecrawlTools(enable_search=True, enable_crawl=True, poll_interval=10)],
        markdown=True,
        exponential_backoff=True,
        delay_between_retries=2,
        debug_mode=True,
    )
    
    # Agent 2: Market Sentiment Specialist
    sentiment_analyst = Agent(
        name="Market Sentiment Specialist",
        description=dedent("""
            You are a market research expert specializing in sentiment analysis and consumer perception tracking.
            Your expertise includes:
            • Analyzing social media sentiment and customer feedback
            • Identifying positive and negative sentiment drivers
            • Tracking brand perception trends across platforms
            • Monitoring customer satisfaction and review patterns
            • Providing actionable insights on market reception
            Focus on extracting sentiment signals from social platforms, review sites, forums, and customer feedback channels.
            IMPORTANT: Conclude your report with a 'Sources:' section, listing all URLs of websites you crawled or searched for this analysis.
        """),
        model=OpenAIChat(id="gpt-4o-mini", temperature=0.3),
        tools=[FirecrawlTools(enable_search=True, enable_crawl=True, poll_interval=10)],
        markdown=True,
        exponential_backoff=True,
        delay_between_retries=2,
        debug_mode=True,
    )
    
    # Agent 3: Launch Metrics Specialist
    metrics_analyst = Agent(
        name="Launch Metrics Specialist", 
        description=dedent("""
            You are a product launch performance analyst who specializes in tracking and analyzing launch KPIs.
            Your focus areas include:
            • User adoption and engagement metrics
            • Revenue and business performance indicators
            • Market penetration and growth rates
            • Press coverage and media attention analysis
            • Social media traction and viral coefficient tracking
            • Competitive market share analysis
            Always provide quantitative insights with context and benchmark against industry standards when possible.
            IMPORTANT: Conclude your report with a 'Sources:' section, listing all URLs of websites you crawled or searched for this analysis.
        """),
        model=OpenAIChat(id="gpt-4o-mini", temperature=0.3),
        tools=[FirecrawlTools(enable_search=True, enable_crawl=True, poll_interval=10)],
        markdown=True,
        exponential_backoff=True,
        delay_between_retries=2,
        debug_mode=True,
    )

    # Create the coordinated team
    product_intelligence_team = Team(
        name="Product Intelligence Team",
        model=OpenAIChat(id="gpt-4o-mini", temperature=0.3),
        members=[launch_analyst, sentiment_analyst, metrics_analyst],
        instructions=[
            "Coordinate the analysis based on the user's request type:",
            "1. For competitor analysis: Use the Product Launch Analyst to evaluate positioning, strengths, weaknesses, and strategic insights",
            "2. For market sentiment: Use the Market Sentiment Specialist to analyze social media sentiment, customer feedback, and brand perception",
            "3. For launch metrics: Use the Launch Metrics Specialist to track KPIs, adoption rates, press coverage, and performance indicators",
            "Always provide evidence-based insights with specific examples and data points",
            "Structure responses with clear sections and actionable recommendations",
            "Include sources section with all URLs crawled or searched"
        ],
        markdown=True,
        debug_mode=True,
    )
else:
    product_intelligence_team = None
    st.warning("⚠️ Please enter both API keys in the sidebar to use the application.")

# ---------------- Helper Functions for History & Alerts ----------------
def save_analysis_to_history(company_name, analysis_type, result, sentiment_score=None):
    """Save analysis result to history with timestamp"""
    try:
        history = json.loads(HISTORY_FILE.read_text())
        entry = {
            "timestamp": datetime.now().isoformat(),
            "company": company_name,
            "analysis_type": analysis_type,
            "result": result[:500],  # Store summary
            "sentiment_score": sentiment_score,
            "full_result": result
        }
        history.append(entry)
        # Keep last 100 entries
        history = history[-100:]
        HISTORY_FILE.write_text(json.dumps(history, indent=2))
    except Exception as e:
        st.warning(f"Could not save to history: {e}")

def load_analysis_history(company_name=None):
    """Load analysis history, optionally filtered by company"""
    try:
        history = json.loads(HISTORY_FILE.read_text())
        if company_name:
            history = [h for h in history if h["company"].lower() == company_name.lower()]
        return history
    except:
        return []

def calculate_sentiment_score(sentiment_text):
    """Extract sentiment score from sentiment analysis text"""
    # Simple heuristic: count positive vs negative indicators
    positive_words = ["positive", "success", "growth", "strong", "excellent", "praised", "loved", "popular"]
    negative_words = ["negative", "criticism", "decline", "weak", "poor", "complaint", "issue", "problem"]
    
    text_lower = sentiment_text.lower()
    pos_count = sum(text_lower.count(word) for word in positive_words)
    neg_count = sum(text_lower.count(word) for word in negative_words)
    
    total = pos_count + neg_count
    if total == 0:
        return 0
    
    # Score from -100 to +100
    score = ((pos_count - neg_count) / total) * 100
    return round(score, 1)

def save_alert_config(company_name, alert_type, threshold, email=None):
    """Save alert configuration"""
    try:
        alerts = json.loads(ALERTS_FILE.read_text())
        alert_id = f"{company_name}_{alert_type}"
        alerts[alert_id] = {
            "company": company_name,
            "alert_type": alert_type,
            "threshold": threshold,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_check": None
        }
        ALERTS_FILE.write_text(json.dumps(alerts, indent=2))
        return True
    except Exception as e:
        st.error(f"Could not save alert: {e}")
        return False

def load_alert_configs(company_name=None):
    """Load alert configurations"""
    try:
        alerts = json.loads(ALERTS_FILE.read_text())
        if company_name:
            return {k: v for k, v in alerts.items() if v["company"].lower() == company_name.lower()}
        return alerts
    except:
        return {}

def check_alerts(company_name, current_sentiment_score):
    """Check if any alerts should be triggered"""
    alerts = load_alert_configs(company_name)
    triggered_alerts = []
    
    for alert_id, config in alerts.items():
        if config["alert_type"] == "sentiment_drop":
            history = load_analysis_history(company_name)
            if len(history) >= 2:
                # Compare with previous sentiment
                prev_sentiment = history[-2].get("sentiment_score", 0)
                if prev_sentiment - current_sentiment_score >= config["threshold"]:
                    triggered_alerts.append({
                        "type": "sentiment_drop",
                        "message": f"⚠️ Sentiment dropped by {prev_sentiment - current_sentiment_score:.1f} points!",
                        "company": company_name
                    })
    
    return triggered_alerts

# ---------------- Visualization & Export Functions ----------------
def create_sentiment_gauge(sentiment_score):
    """Create a gauge chart for sentiment score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Sentiment Score", 'font': {'size': 24}},
        delta = {'reference': 0, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [-100, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [-100, -20], 'color': '#ffcccc'},
                {'range': [-20, 20], 'color': '#ffffcc'},
                {'range': [20, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': sentiment_score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def create_competitive_positioning_map(companies_data):
    """Create 2x2 positioning map for companies"""
    # Parse data to extract innovation and market fit scores
    fig = go.Figure()
    
    for company, data in companies_data.items():
        # Simplified: random positioning for demo (would be extracted from actual analysis)
        import random
        innovation = random.randint(40, 100)
        market_fit = random.randint(40, 100)
        
        fig.add_trace(go.Scatter(
            x=[innovation],
            y=[market_fit],
            mode='markers+text',
            name=company,
            text=[company],
            textposition="top center",
            marker=dict(size=20, line=dict(width=2, color='DarkSlateGrey'))
        ))
    
    fig.update_layout(
        title="Competitive Positioning Map",
        xaxis_title="Innovation Score",
        yaxis_title="Market Fit Score",
        xaxis=dict(range=[0, 110], showgrid=True),
        yaxis=dict(range=[0, 110], showgrid=True),
        height=500,
        showlegend=True,
        hovermode='closest'
    )
    
    # Add quadrant lines
    fig.add_hline(y=50, line_dash="dash", line_color="gray")
    fig.add_vline(x=50, line_dash="dash", line_color="gray")
    
    # Add quadrant labels
    fig.add_annotation(x=25, y=75, text="Niche Players", showarrow=False, font=dict(size=12, color="gray"))
    fig.add_annotation(x=75, y=75, text="Leaders", showarrow=False, font=dict(size=12, color="gray"))
    fig.add_annotation(x=25, y=25, text="Laggards", showarrow=False, font=dict(size=12, color="gray"))
    fig.add_annotation(x=75, y=25, text="Challengers", showarrow=False, font=dict(size=12, color="gray"))
    
    return fig

def generate_word_cloud_data(text):
    """Generate word frequency data for word cloud visualization"""
    from collections import Counter
    import re
    
    # Remove common stop words
    stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by'}
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    words = [w for w in words if w not in stop_words]
    
    # Count frequency
    word_freq = Counter(words)
    
    return word_freq.most_common(20)

def create_word_cloud_chart(text):
    """Create a bar chart showing word frequency (pseudo word cloud)"""
    word_data = generate_word_cloud_data(text)
    
    if not word_data:
        return None
    
    words, counts = zip(*word_data)
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(counts),
            y=list(words),
            orientation='h',
            marker=dict(
                color=counts,
                colorscale='Viridis',
                showscale=True
            )
        )
    ])
    
    fig.update_layout(
        title="Top Keywords & Themes",
        xaxis_title="Frequency",
        yaxis_title="Keywords",
        height=500,
        yaxis={'categoryorder':'total ascending'}
    )
    
    return fig

def generate_pdf_report(company_name, analyses):
    """Generate a professional PDF report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph(f"<b>Product Intelligence Report</b><br/>{company_name}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Metadata
    meta_data = [
        ['Report Generated:', datetime.now().strftime("%B %d, %Y at %H:%M")],
        ['Company Analyzed:', company_name],
        ['Analysis Types:', ', '.join(analyses.keys())]
    ]
    
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(meta_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Add each analysis
    for analysis_type, content in analyses.items():
        # Section heading
        heading = Paragraph(f"<b>{analysis_type.upper()} ANALYSIS</b>", heading_style)
        elements.append(heading)
        
        # Content (truncate if too long)
        text_content = content[:2000] + "..." if len(content) > 2000 else content
        para = Paragraph(text_content.replace('\n', '<br/>'), styles['BodyText'])
        elements.append(para)
        elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    elements.append(PageBreak())
    footer = Paragraph(
        "<i>Generated by AI Product Launch Intelligence Agent</i><br/>"
        "<i>Confidential - For Internal Use Only</i>",
        styles['Italic']
    )
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer

def export_to_excel(company_name, analyses, history=None):
    """Export data to Excel with multiple sheets"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = {
            'Company': [company_name],
            'Report Date': [datetime.now().strftime("%Y-%m-%d %H:%M")],
            'Analyses Included': [', '.join(analyses.keys())]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        # Analysis sheets
        for analysis_type, content in analyses.items():
            df = pd.DataFrame({
                'Analysis Type': [analysis_type],
                'Content': [content]
            })
            sheet_name = analysis_type[:31]  # Excel sheet name limit
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # History sheet if available
        if history and len(history) > 0:
            history_df = pd.DataFrame(history)
            history_df.to_excel(writer, sheet_name='Historical Data', index=False)
    
    output.seek(0)
    return output

# ---------------- Strategic Recommendations Generator ----------------
def generate_swot_analysis(company_name, analyses):
    """Generate SWOT analysis from all analyses"""
    if not product_intelligence_team:
        return None
    
    combined_analysis = "\n\n".join([f"{k}: {v}" for k, v in analyses.items()])
    
    prompt = f"""Based on the following analyses for {company_name}, create a comprehensive SWOT analysis.

{combined_analysis}

Generate a structured SWOT analysis with:
- **Strengths**: 4-6 key internal advantages
- **Weaknesses**: 4-6 internal limitations or gaps
- **Opportunities**: 4-6 external market opportunities
- **Threats**: 4-6 external risks or competitive threats

Format as a markdown table with clear bullet points."""
    
    try:
        result = product_intelligence_team.run(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        return f"Error generating SWOT: {e}"

def generate_gtm_playbook(company_name, analyses):
    """Generate Go-to-Market playbook with specific tactics"""
    if not product_intelligence_team:
        return None
    
    combined_analysis = "\n\n".join([f"{k}: {v}" for k, v in analyses.items()])
    
    prompt = f"""Based on the competitive intelligence for {company_name}, create a practical Go-to-Market playbook.

{combined_analysis}

Structure:
## GTM Strategy Playbook for {company_name}

### 1. Positioning Strategy
- Core value proposition
- Target customer segments
- Differentiation vs competitors

### 2. Launch Tactics (Prioritized)
- Tactic 1: [Specific action with rationale]
- Tactic 2: [Specific action with rationale]
- Tactic 3: [Specific action with rationale]

### 3. Channel Mix Recommendations
- Primary channels and why
- Budget allocation suggestions

### 4. Messaging Framework
- Key messages for each segment
- Proof points and evidence

### 5. Competitive Counters
- How to address competitor strengths
- Opportunities to exploit gaps

Keep it actionable and specific."""
    
    try:
        result = product_intelligence_team.run(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        return f"Error generating playbook: {e}"

def generate_risk_assessment(company_name, analyses):
    """Generate risk assessment matrix"""
    if not product_intelligence_team:
        return None
    
    combined_analysis = "\n\n".join([f"{k}: {v}" for k, v in analyses.items()])
    
    prompt = f"""Analyze potential risks for {company_name} based on this intelligence:

{combined_analysis}

Create a Risk Assessment Matrix with:

| Risk Category | Risk Description | Probability (H/M/L) | Impact (H/M/L) | Mitigation Strategy |
|--------------|------------------|---------------------|----------------|---------------------|
| Market Risk | ... | ... | ... | ... |
| Competitive Risk | ... | ... | ... | ... |
| Execution Risk | ... | ... | ... | ... |
| Technology Risk | ... | ... | ... | ... |
| Financial Risk | ... | ... | ... | ... |

Add 4-6 specific risks with concrete mitigation strategies."""
    
    try:
        result = product_intelligence_team.run(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        return f"Error generating risk assessment: {e}"

def generate_opportunity_scoring(company_name, analyses):
    """Generate opportunity scoring and prioritization"""
    if not product_intelligence_team:
        return None
    
    combined_analysis = "\n\n".join([f"{k}: {v}" for k, v in analyses.items()])
    
    prompt = f"""Identify and score market opportunities for {company_name}:

{combined_analysis}

Generate an Opportunity Scoring Matrix:

| Opportunity | Description | Market Size | Competition | Feasibility | Score (0-10) | Priority |
|------------|-------------|-------------|-------------|-------------|--------------|----------|
| Opportunity 1 | ... | High/Med/Low | High/Med/Low | High/Med/Low | X.X | High/Med/Low |

Identify 5-7 specific opportunities with:
- Clear description
- Rationale for scoring
- Recommended next steps for High priority items"""
    
    try:
        result = product_intelligence_team.run(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        return f"Error generating opportunity scoring: {e}"

def generate_action_plan(company_name, analyses):
    """Generate 30/60/90 day action plan"""
    if not product_intelligence_team:
        return None
    
    combined_analysis = "\n\n".join([f"{k}: {v}" for k, v in analyses.items()])
    
    prompt = f"""Create a detailed 30/60/90 day action plan for {company_name} based on:

{combined_analysis}

## 30/60/90 Day Action Plan

### Days 1-30: Foundation & Quick Wins
**Goals:**
- Goal 1
- Goal 2

**Key Actions:**
1. Action with owner and deadline
2. Action with owner and deadline
3. Action with owner and deadline

**Success Metrics:**
- Metric 1
- Metric 2

### Days 31-60: Scale & Optimize
**Goals:**
- Goal 1
- Goal 2

**Key Actions:**
1. Action with owner and deadline
2. Action with owner and deadline
3. Action with owner and deadline

**Success Metrics:**
- Metric 1
- Metric 2

### Days 61-90: Measure & Iterate
**Goals:**
- Goal 1
- Goal 2

**Key Actions:**
1. Action with owner and deadline
2. Action with owner and deadline
3. Action with owner and deadline

**Success Metrics:**
- Metric 1
- Metric 2

Be specific, actionable, and realistic."""
    
    try:
        result = product_intelligence_team.run(prompt)
        return result.content if hasattr(result, "content") else str(result)
    except Exception as e:
        return f"Error generating action plan: {e}"

# ---------------- Helper to display response ----------------
def display_agent_response(resp):
    """Render different response structures nicely."""
    if hasattr(resp, "content") and resp.content:
        st.markdown(resp.content)
    elif hasattr(resp, "messages"):
        for m in resp.messages:
            if m.role == "assistant" and m.content:
                st.markdown(m.content)
    else:
        st.markdown(str(resp))

# Helper to expand bullet summary into 1200-word general report
def expand_insight(bullet_text: str, topic: str) -> str:
    if not product_intelligence_team:
        st.error("⚠️ Please enter both API keys in the sidebar first.")
        return ""
        
    prompt = (
        f"Using ONLY the bullet points below, craft an in-depth (~1200-word) launch analysis report on {topic}.\n"
        f"Structure:\n"
        f"1. Executive Summary (<120 words)\n"
        f"2. Strengths & Opportunities (what worked well)\n"
        f"3. Weaknesses & Gaps (what didn't work or could be improved)\n"
        f"4. Actionable Recommendations (bullet list)\n"
        f"5. Key Risks / Watch-outs\n\n"
        f"Bullet Points:\n{bullet_text}\n\n"
        f"Ensure analysis is objective, evidence-based and references the bullet insights. Keep paragraphs short (≤120 words)."
    )
    long_resp = product_intelligence_team.run(prompt)
    return long_resp.content if hasattr(long_resp, "content") else str(long_resp)

# Helper to craft competitor-focused launch report for product managers
def expand_competitor_report(bullet_text: str, competitor: str) -> str:
    if not product_intelligence_team:
        st.error("⚠️ Please enter both API keys in the sidebar first.")
        return ""

    prompt = (
        f"Transform the insight bullets below into a professional launch review for product managers analysing {competitor}.\n\n"
        f"Produce well-structured **Markdown** with a mix of tables, call-outs and concise bullet points — avoid long paragraphs.\n\n"
        f"=== FORMAT SPECIFICATION ===\n"
        f"# {competitor} – Launch Review\n\n"
        f"## 1. Market & Product Positioning\n"
        f"• Bullet point summary of how the product is positioned (max 6 bullets).\n\n"
        f"## 2. Launch Strengths\n"
        f"| Strength | Evidence / Rationale |\n|---|---|\n| … | … | (add 4-6 rows)\n\n"
        f"## 3. Launch Weaknesses\n"
        f"| Weakness | Evidence / Rationale |\n|---|---|\n| … | … | (add 4-6 rows)\n\n"
        f"## 4. Strategic Takeaways for Competitors\n"
        f"1. … (max 5 numbered recommendations)\n\n"
        f"=== SOURCE BULLETS ===\n{bullet_text}\n\n"
        f"Guidelines:\n"
        f"• Populate the tables with specific points derived from the bullets.\n"
        f"• Only include rows that contain meaningful data; omit any blank entries."
    )
    resp = product_intelligence_team.run(prompt)
    return resp.content if hasattr(resp, "content") else str(resp)

# Helper to craft market sentiment report
def expand_sentiment_report(bullet_text: str, product: str) -> str:
    if not product_intelligence_team:
        st.error("⚠️ Please enter both API keys in the sidebar first.")
        return ""

    prompt = (
        f"Use the tagged bullets below to create a concise market-sentiment brief for **{product}**.\n\n"
        f"### Positive Sentiment\n"
        f"• List each positive point as a separate bullet (max 6).\n\n"
        f"### Negative Sentiment\n"
        f"• List each negative point as a separate bullet (max 6).\n\n"
        f"### Overall Summary\n"
        f"Provide a short paragraph (≤120 words) summarising the overall sentiment balance and key drivers.\n\n"
        f"Tagged Bullets:\n{bullet_text}"
    )
    resp = product_intelligence_team.run(prompt)
    return resp.content if hasattr(resp, "content") else str(resp)

# Helper to craft launch metrics report
def expand_metrics_report(bullet_text: str, launch: str) -> str:
    if not product_intelligence_team:
        st.error("⚠️ Please enter both API keys in the sidebar first.")
        return ""

    prompt = (
        f"Convert the KPI bullets below into a launch-performance snapshot for **{launch}** suitable for an executive dashboard.\n\n"
        f"## Key Performance Indicators\n"
        f"| Metric | Value / Detail | Source |\n"
        f"|---|---|---|\n"
        f"| … | … | … |  (include one row per KPI)\n\n"
        f"## Qualitative Signals\n"
        f"• Bullet list of notable qualitative insights (max 5).\n\n"
        f"## Summary & Implications\n"
        f"Brief paragraph (≤120 words) highlighting what the metrics imply about launch success and next steps.\n\n"
        f"KPI Bullets:\n{bullet_text}"
    )
    resp = product_intelligence_team.run(prompt)
    return resp.content if hasattr(resp, "content") else str(resp)

# ---------------- UI ----------------
st.markdown('<h1 class="main-title"> 🧑‍💻AI Product LaunchIQ Intelligence Platform 🤖</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">✨ Complete Competitive Intelligence & Strategic Planning Powered by AI ✨</p>', unsafe_allow_html=True)

st.divider()

# Company input section with enhanced styling
st.markdown("### 🏢 Company Analysis Center")
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        company_name = st.text_input(
            label="Company Name",
            placeholder="🔍 Enter company name (e.g., OpenAI, Tesla, Spotify)",
            help="This company will be analyzed by the coordinated team of specialized agents",
            label_visibility="collapsed"
        )
    with col2:
        if company_name:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(0, 255, 127, 0.2), rgba(0, 200, 100, 0.2));
                padding: 12px;
                border-radius: 12px;
                text-align: center;
                border: 2px solid #00ff7f;
                animation: pulse 2s infinite;
            ">
                <span style="color: #00ff7f; font-weight: 700;">✓ Ready: <b>{company_name}</b></span>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# Create tabs for analysis types
analysis_tabs = st.tabs([
    "🔍 Competitor Analysis", 
    "💬 Market Sentiment", 
    "📈 Launch Metrics",
    "⚖️ Multi-Company Compare",
    "📊 Historical Tracking",
    "🔔 Alert Manager",
    "📊 Visualizations & Export",
    "🎯 Strategic Recommendations"
])

# Persistent storage for latest response
if "analysis_response" not in st.session_state:
    st.session_state.analysis_response = None
    st.session_state.analysis_meta = {}

# Store separate responses for each agent
if "competitor_response" not in st.session_state:
    st.session_state.competitor_response = None
if "sentiment_response" not in st.session_state:
    st.session_state.sentiment_response = None
if "metrics_response" not in st.session_state:
    st.session_state.metrics_response = None

# -------- Competitor Analysis Tab --------
with analysis_tabs[0]:
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(102, 126, 234, 0.4);
            margin-bottom: 20px;
        ">
            <h2 style="color: #667eea; margin: 0;">🔍 Competitor Launch Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("ℹ️ About this Agent", expanded=False):
            st.markdown("""
            <div style="
                background: rgba(102, 126, 234, 0.1);
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            ">
                <h4 style="color: #667eea;">Product Launch Analyst - Strategic GTM Expert</h4>
                <p style="color: #e0e0e0;">
                <b>Specializes in:</b><br>
                • Competitive positioning analysis<br>
                • Launch strategy evaluation<br>
                • Strengths & weaknesses identification<br>
                • Strategic recommendations
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        if company_name:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                analyze_btn = st.button(
                    "🚀 Analyze Competitor Strategy", 
                    key="competitor_btn", 
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                if st.session_state.get('competitor_response'):
                    st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, rgba(0, 255, 127, 0.2), rgba(0, 200, 100, 0.2));
                        padding: 12px;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #00ff7f;
                        animation: pulse 2s infinite;
                    ">
                        <span style="color: #00ff7f; font-weight: 700;">✅ Analysis Complete</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="
                        background: rgba(0, 191, 255, 0.2);
                        padding: 12px;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #00bfff;
                    ">
                        <span style="color: #00bfff; font-weight: 700;">⏳ Ready to analyze</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            if analyze_btn:
                if not product_intelligence_team:
                    st.error("⚠️ Please enter both API keys in the sidebar first.")
                else:
                    with st.spinner("🔍 Product Intelligence Team analyzing competitive strategy..."):
                        try:
                            bullets = product_intelligence_team.run(
                                f"Generate up to 16 evidence-based insight bullets about {company_name}'s most recent product launches.\n"
                                f"Format requirements:\n"
                                f"• Start every bullet with exactly one tag: Positioning | Strength | Weakness | Learning\n"
                                f"• Follow the tag with a concise statement (max 30 words) referencing concrete observations: messaging, differentiation, pricing, channel selection, timing, engagement metrics, or customer feedback."
                            )
                            long_text = expand_competitor_report(
                                bullets.content if hasattr(bullets, "content") else str(bullets),
                                company_name
                            )
                            st.session_state.competitor_response = long_text
                            save_analysis_to_history(company_name, "competitor", long_text)
                            st.success("✅ Competitor analysis ready")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            
            # Display results
            if st.session_state.get('competitor_response'):
                st.divider()
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid rgba(102, 126, 234, 0.3);
                    animation: fadeInUp 0.8s ease-out;
                ">
                    <h3 style="color: #667eea;">📊 Analysis Results</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(st.session_state.competitor_response)
        else:
            st.markdown("""
            <div style="
                background: rgba(0, 191, 255, 0.1);
                padding: 20px;
                border-radius: 12px;
                border-left: 4px solid #00bfff;
                text-align: center;
            ">
                <span style="color: #00bfff; font-size: 1.1rem;">👆 Please enter a company name above to start the analysis</span>
            </div>
            """, unsafe_allow_html=True)

# -------- Market Sentiment Tab --------
with analysis_tabs[1]:
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(240, 147, 251, 0.2), rgba(245, 87, 108, 0.2));
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(240, 147, 251, 0.4);
            margin-bottom: 20px;
        ">
            <h2 style="color: #f093fb; margin: 0;">💬 Market Sentiment Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("ℹ️ About this Agent", expanded=False):
            st.markdown("""
            <div style="
                background: rgba(240, 147, 251, 0.1);
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #f093fb;
            ">
                <h4 style="color: #f093fb;">Market Sentiment Specialist - Consumer Perception Expert</h4>
                <p style="color: #e0e0e0;">
                <b>Specializes in:</b><br>
                • Social media sentiment tracking<br>
                • Customer feedback analysis<br>
                • Brand perception monitoring<br>
                • Review pattern identification
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        if company_name:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                sentiment_btn = st.button(
                    "📊 Analyze Market Sentiment", 
                    key="sentiment_btn", 
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                if st.session_state.sentiment_response:
                    st.success("✅ Analysis Complete")
                else:
                    st.info("⏳ Ready to analyze")
            
            if sentiment_btn:
                if not product_intelligence_team:
                    st.error("⚠️ Please enter both API keys in the sidebar first.")
                else:
                    with st.spinner("💬 Product Intelligence Team analyzing market sentiment..."):
                        try:
                            bullets = product_intelligence_team.run(
                                f"Summarize market sentiment for {company_name} in <=10 bullets. "
                                f"Cover top positive & negative themes with source mentions (G2, Reddit, Twitter, customer reviews)."
                            )
                            long_text = expand_sentiment_report(
                                bullets.content if hasattr(bullets, "content") else str(bullets),
                                company_name
                            )
                            sentiment_score = calculate_sentiment_score(long_text)
                            st.session_state.sentiment_response = long_text
                            save_analysis_to_history(company_name, "sentiment", long_text, sentiment_score)
                            
                            # Check alerts
                            alerts = check_alerts(company_name, sentiment_score)
                            for alert in alerts:
                                st.warning(alert["message"])
                            
                            st.success("✅ Sentiment analysis ready")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            
            # Display results
            if st.session_state.sentiment_response:
                st.divider()
                with st.container():
                    st.markdown("### 📈 Analysis Results")
                    st.markdown(st.session_state.sentiment_response)
        else:
            st.info("👆 Please enter a company name above to start the analysis")

# -------- Launch Metrics Tab --------
with analysis_tabs[2]:
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(56, 239, 125, 0.2), rgba(17, 153, 142, 0.2));
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(56, 239, 125, 0.4);
            margin-bottom: 20px;
        ">
            <h2 style="color: #38ef7d; margin: 0;">📈 Launch Performance Metrics</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("ℹ️ About this Agent", expanded=False):
            st.markdown("""
            <div style="
                background: rgba(56, 239, 125, 0.1);
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #38ef7d;
            ">
                <h4 style="color: #38ef7d;">Launch Metrics Specialist - Performance Analytics Expert</h4>
                <p style="color: #e0e0e0;">
                <b>Specializes in:</b><br>
                • User adoption metrics tracking<br>
                • Revenue performance analysis<br>
                • Market penetration evaluation<br>
                • Press coverage monitoring
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        if company_name:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                metrics_btn = st.button(
                    "📊 Analyze Launch Metrics", 
                    key="metrics_btn", 
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                if st.session_state.metrics_response:
                    st.success("✅ Analysis Complete")
                else:
                    st.info("⏳ Ready to analyze")
            
            if metrics_btn:
                if not product_intelligence_team:
                    st.error("⚠️ Please enter both API keys in the sidebar first.")
                else:
                    with st.spinner("📈 Product Intelligence Team analyzing launch metrics..."):
                        try:
                            bullets = product_intelligence_team.run(
                                f"List (max 10 bullets) the most important publicly available KPIs & qualitative signals for {company_name}'s recent product launches. "
                                f"Include engagement stats, press coverage, adoption metrics, and market traction data if available."
                            )
                            long_text = expand_metrics_report(
                                bullets.content if hasattr(bullets, "content") else str(bullets),
                                company_name
                            )
                            st.session_state.metrics_response = long_text
                            save_analysis_to_history(company_name, "metrics", long_text)
                            st.success("✅ Metrics analysis ready")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            
            # Display results
            if st.session_state.metrics_response:
                st.divider()
                with st.container():
                    st.markdown("### 📊 Analysis Results")
                    st.markdown(st.session_state.metrics_response)
        else:
            st.info("👆 Please enter a company name above to start the analysis")

# -------- Multi-Company Comparison Tab --------
with analysis_tabs[3]:
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255, 165, 0, 0.2), rgba(255, 140, 0, 0.2));
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(255, 165, 0, 0.4);
            margin-bottom: 20px;
        ">
            <h2 style="color: #ffa500; margin: 0;">⚖️ Multi-Company Comparison</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: rgba(255, 165, 0, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <p style="color: #e0e0e0; margin: 0;">
            Compare multiple companies side-by-side to identify competitive advantages, 
            market gaps, and strategic opportunities.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Company selection
        st.subheader("Select Companies to Compare")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            company1 = st.text_input("Company 1", placeholder="e.g., OpenAI", key="comp1")
        with col2:
            company2 = st.text_input("Company 2", placeholder="e.g., Anthropic", key="comp2")
        with col3:
            company3 = st.text_input("Company 3 (Optional)", placeholder="e.g., Google", key="comp3")
        
        comparison_type = st.radio(
            "Comparison Focus",
            ["Sentiment Analysis", "Market Position", "Launch Strategy"],
            horizontal=True
        )
        
        if st.button("🔍 Run Comparison", type="primary", use_container_width=True):
            companies = [c for c in [company1, company2, company3] if c]
            
            if len(companies) < 2:
                st.error("⚠️ Please enter at least 2 companies to compare")
            elif not product_intelligence_team:
                st.error("⚠️ Please enter both API keys in the sidebar first.")
            else:
                with st.spinner(f"🔍 Analyzing {len(companies)} companies..."):
                    comparison_results = {}
                    
                    for company in companies:
                        try:
                            if comparison_type == "Sentiment Analysis":
                                bullets = product_intelligence_team.run(
                                    f"Provide 5 key sentiment insights about {company} with positive/negative indicators."
                                )
                            elif comparison_type == "Market Position":
                                bullets = product_intelligence_team.run(
                                    f"Provide 5 key insights about {company}'s market positioning and competitive advantages."
                                )
                            else:
                                bullets = product_intelligence_team.run(
                                    f"Provide 5 key insights about {company}'s launch strategy and tactics."
                                )
                            
                            result = bullets.content if hasattr(bullets, "content") else str(bullets)
                            comparison_results[company] = result
                            
                        except Exception as e:
                            st.error(f"Error analyzing {company}: {e}")
                    
                    # Display comparison
                    if comparison_results:
                        st.success("✅ Comparison complete!")
                        st.divider()
                        
                        # Side-by-side comparison
                        cols = st.columns(len(companies))
                        for idx, (company, result) in enumerate(comparison_results.items()):
                            with cols[idx]:
                                st.markdown(f"### {company}")
                                st.markdown(result)
                        
                        st.divider()
                        
                        # Generate comparative summary
                        st.markdown("### 🎯 Comparative Analysis Summary")
                        with st.spinner("Generating comparative insights..."):
                            try:
                                comparative_prompt = (
                                    f"Compare these companies based on the analysis below. "
                                    f"Create a summary table with columns: Company | Key Strengths | Key Weaknesses | Market Position\n\n"
                                    f"{json.dumps(comparison_results, indent=2)}"
                                )
                                summary = product_intelligence_team.run(comparative_prompt)
                                st.markdown(summary.content if hasattr(summary, "content") else str(summary))
                            except Exception as e:
                                st.error(f"Error generating summary: {e}")

# -------- Historical Tracking Tab --------
with analysis_tabs[4]:
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.2), rgba(75, 0, 130, 0.2));
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(138, 43, 226, 0.4);
            margin-bottom: 20px;
        ">
            <h2 style="color: #8a2be2; margin: 0;">📊 Historical Tracking & Trends</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: rgba(138, 43, 226, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <p style="color: #e0e0e0; margin: 0;">
            Track analysis history over time to identify trends, sentiment shifts, 
            and competitive dynamics.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter options
        col1, col2 = st.columns([2, 1])
        
        with col1:
            history_company = st.text_input(
                "Filter by Company", 
                placeholder="Leave empty to see all",
                key="history_filter"
            )
        
        with col2:
            st.markdown("###")
            if st.button("🔄 Refresh History", use_container_width=True):
                st.rerun()
        
        # Load history
        history = load_analysis_history(history_company if history_company else None)
        
        if not history:
            st.info("📭 No analysis history yet. Run some analyses to see trends here!")
        else:
            st.success(f"📊 Found {len(history)} historical analyses")
            
            # Convert to DataFrame
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp', ascending=False)
            
            # Sentiment trend chart
            sentiment_data = df[df['sentiment_score'].notna()]
            if not sentiment_data.empty:
                st.markdown("#### 📈 Sentiment Score Trends")
                
                fig = go.Figure()
                
                for company in sentiment_data['company'].unique():
                    company_data = sentiment_data[sentiment_data['company'] == company]
                    fig.add_trace(go.Scatter(
                        x=company_data['timestamp'],
                        y=company_data['sentiment_score'],
                        mode='lines+markers',
                        name=company,
                        line=dict(width=3),
                        marker=dict(size=8)
                    ))
                
                fig.update_layout(
                    title="Sentiment Score Over Time",
                    xaxis_title="Date",
                    yaxis_title="Sentiment Score",
                    yaxis=dict(range=[-100, 100]),
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Analysis timeline
            st.markdown("#### 📋 Analysis Timeline")
            
            # Group by company
            for company in df['company'].unique():
                with st.expander(f"🏢 {company} ({len(df[df['company'] == company])} analyses)"):
                    company_history = df[df['company'] == company]
                    
                    for _, row in company_history.iterrows():
                        col1, col2, col3 = st.columns([2, 1, 3])
                        
                        with col1:
                            st.caption(row['timestamp'].strftime("%Y-%m-%d %H:%M"))
                        
                        with col2:
                            if row['analysis_type'] == 'competitor':
                                st.markdown("🔍 **Competitor**")
                            elif row['analysis_type'] == 'sentiment':
                                st.markdown("💬 **Sentiment**")
                            else:
                                st.markdown("📈 **Metrics**")
                        
                        with col3:
                            if row.get('sentiment_score'):
                                score = row['sentiment_score']
                                color = "🟢" if score > 20 else "🟡" if score > -20 else "🔴"
                                st.caption(f"{color} Score: {score}")
                        
                        if st.button(f"View Details", key=f"view_{row['timestamp']}"):
                            st.markdown(row['full_result'])
                        
                        st.divider()
            
            # Export option
            st.markdown("#### 💾 Export Data")
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download History as CSV",
                data=csv,
                file_name=f"intelligence_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# -------- Alert Manager Tab --------
with analysis_tabs[5]:
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255, 69, 0, 0.2), rgba(255, 99, 71, 0.2));
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(255, 69, 0, 0.4);
            margin-bottom: 20px;
        ">
            <h2 style="color: #ff4500; margin: 0;">🔔 Alert Manager</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: rgba(255, 69, 0, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <p style="color: #e0e0e0; margin: 0;">
            Set up automated alerts to monitor competitor activities and market changes.
            Get notified when significant shifts occur.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create new alert
        st.subheader("➕ Create New Alert")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alert_company = st.text_input(
                "Company to Monitor",
                placeholder="e.g., OpenAI",
                key="alert_company"
            )
        
        with col2:
            alert_type = st.selectbox(
                "Alert Type",
                ["sentiment_drop", "sentiment_spike", "new_launch_detected"],
                format_func=lambda x: {
                    "sentiment_drop": "🔴 Sentiment Drop",
                    "sentiment_spike": "🟢 Sentiment Spike",
                    "new_launch_detected": "🚀 New Launch Detected"
                }[x]
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            threshold = st.slider(
                "Threshold (for sentiment changes)",
                min_value=5,
                max_value=50,
                value=15,
                help="Alert when sentiment changes by this amount"
            )
        
        with col2:
            alert_email = st.text_input(
                "Email (optional)",
                placeholder="your@email.com",
                help="Future feature: email notifications"
            )
        
        if st.button("✅ Create Alert", type="primary", use_container_width=True):
            if not alert_company:
                st.error("⚠️ Please enter a company name")
            else:
                if save_alert_config(alert_company, alert_type, threshold, alert_email):
                    st.success(f"✅ Alert created for {alert_company}!")
                    st.rerun()
        
        st.divider()
        
        # Display existing alerts
        st.subheader("📋 Active Alerts")
        
        alerts = load_alert_configs()
        
        if not alerts:
            st.info("📭 No active alerts. Create one above to start monitoring!")
        else:
            for alert_id, config in alerts.items():
                with st.expander(f"🔔 {config['company']} - {config['alert_type']}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Company", config['company'])
                    
                    with col2:
                        st.metric("Threshold", f"{config['threshold']}%")
                    
                    with col3:
                        st.metric("Created", config['created_at'][:10])
                    
                    if st.button(f"🗑️ Delete Alert", key=f"del_{alert_id}"):
                        try:
                            alerts_data = json.loads(ALERTS_FILE.read_text())
                            del alerts_data[alert_id]
                            ALERTS_FILE.write_text(json.dumps(alerts_data, indent=2))
                            st.success("✅ Alert deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting alert: {e}")
        
        st.divider()
        
        # Alert history
        st.subheader("📊 Recent Triggered Alerts")
        st.info("💡 Alerts will appear here when triggered during analysis runs")

# -------- Visualizations & Export Tab --------
with analysis_tabs[6]:
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 206, 209, 0.2), rgba(64, 224, 208, 0.2));
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(0, 206, 209, 0.4);
            margin-bottom: 20px;
        ">
            <h2 style="color: #00ced1; margin: 0;">📊 Data Visualization & Export Suite</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: rgba(0, 206, 209, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <p style="color: #e0e0e0; margin: 0;">
            Transform your intelligence data into professional visualizations and export-ready formats.
            Perfect for executive presentations and stakeholder reports.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if not company_name:
            st.info("👆 Please enter a company name and run some analyses first")
        else:
            # Check if we have analysis data
            has_data = any([
                st.session_state.get('competitor_response'),
                st.session_state.get('sentiment_response'),
                st.session_state.get('metrics_response')
            ])
            
            if not has_data:
                st.warning("⚠️ No analysis data available. Run analyses in tabs 1-3 first!")
            else:
                # Sentiment Gauge
                if st.session_state.get('sentiment_response'):
                    st.markdown("#### 📊 Sentiment Score Gauge")
                    sentiment_score = calculate_sentiment_score(st.session_state.sentiment_response)
                    fig = create_sentiment_gauge(sentiment_score)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Current Score", f"{sentiment_score:.1f}")
                    with col2:
                        if sentiment_score > 20:
                            st.metric("Status", "Positive", "🟢")
                        elif sentiment_score > -20:
                            st.metric("Status", "Neutral", "🟡")
                        else:
                            st.metric("Status", "Negative", "🔴")
                    with col3:
                        history = load_analysis_history(company_name)
                        sentiment_history = [h for h in history if h.get('sentiment_score')]
                        if len(sentiment_history) >= 2:
                            trend = sentiment_score - sentiment_history[-2]['sentiment_score']
                            st.metric("Trend", f"{trend:+.1f} pts", f"{trend:+.1f}")
                
                st.divider()
                
                # Word Cloud / Keyword Analysis
                if st.session_state.get('competitor_response') or st.session_state.get('sentiment_response'):
                    st.markdown("#### 🔤 Keyword & Theme Analysis")
                    
                    # Safely get text values, ensuring they're strings
                    competitor_text = st.session_state.get('competitor_response') or ''
                    sentiment_text = st.session_state.get('sentiment_response') or ''
                    text_to_analyze = competitor_text + ' ' + sentiment_text
                    
                    if text_to_analyze.strip():
                        word_fig = create_word_cloud_chart(text_to_analyze)
                        if word_fig:
                            st.plotly_chart(word_fig, use_container_width=True)
                
                st.divider()
                
                # Export Options
                st.markdown("#### 💾 Export Options")
                
                st.markdown("**Choose your export format:**")
                
                col1, col2, col3 = st.columns(3)
                
                # Prepare data for export
                export_data = {}
                if st.session_state.get('competitor_response'):
                    export_data['Competitor Analysis'] = st.session_state.competitor_response
                if st.session_state.get('sentiment_response'):
                    export_data['Sentiment Analysis'] = st.session_state.sentiment_response
                if st.session_state.get('metrics_response'):
                    export_data['Metrics Analysis'] = st.session_state.metrics_response
                
                with col1:
                    st.markdown("##### 📄 PDF Report")
                    st.caption("Professional executive report")
                    
                    if st.button("📥 Generate PDF", use_container_width=True, type="primary"):
                        with st.spinner("Generating PDF report..."):
                            try:
                                pdf_buffer = generate_pdf_report(company_name, export_data)
                                st.download_button(
                                    label="⬇️ Download PDF",
                                    data=pdf_buffer,
                                    file_name=f"{company_name}_intelligence_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                                st.success("✅ PDF ready for download!")
                            except Exception as e:
                                st.error(f"Error generating PDF: {e}")
                
                with col2:
                    st.markdown("##### 📊 Excel Workbook")
                    st.caption("Multi-sheet data export")
                    
                    if st.button("📥 Generate Excel", use_container_width=True, type="primary"):
                        with st.spinner("Generating Excel workbook..."):
                            try:
                                history = load_analysis_history(company_name)
                                excel_buffer = export_to_excel(company_name, export_data, history)
                                st.download_button(
                                    label="⬇️ Download Excel",
                                    data=excel_buffer,
                                    file_name=f"{company_name}_intelligence_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                                st.success("✅ Excel ready for download!")
                            except Exception as e:
                                st.error(f"Error generating Excel: {e}")
                
                with col3:
                    st.markdown("##### 📝 JSON Data")
                    st.caption("Raw data for developers")
                    
                    json_data = {
                        "company": company_name,
                        "report_date": datetime.now().isoformat(),
                        "analyses": export_data,
                        "metadata": {
                            "generated_by": "AI Product Intelligence Agent",
                            "version": "2.0"
                        }
                    }
                    
                    st.download_button(
                        label="📥 Download JSON",
                        data=json.dumps(json_data, indent=2),
                        file_name=f"{company_name}_intelligence_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                st.divider()
                
                # Shareable Link (future feature)
                st.markdown("#### 🔗 Share & Collaborate")
                st.info("🚧 Feature coming soon: Generate shareable links with expiration dates for team collaboration")

# -------- Strategic Recommendations Tab --------
with analysis_tabs[7]:
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 193, 7, 0.2));
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(255, 215, 0, 0.4);
            margin-bottom: 20px;
            animation: float 3s ease-in-out infinite;
        ">
            <h2 style="color: #ffd700; margin: 0;">🎯 Strategic Recommendations Generator</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: rgba(255, 215, 0, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <p style="color: #e0e0e0; margin: 0;">
            Transform your intelligence into actionable strategies. Generate SWOT analysis, 
            GTM playbooks, risk assessments, and prioritized action plans.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if not company_name:
            st.info("👆 Please enter a company name and run some analyses first")
        else:
            # Check if we have analysis data
            analysis_data = {}
            if st.session_state.get('competitor_response'):
                analysis_data['Competitor Analysis'] = st.session_state.competitor_response
            if st.session_state.get('sentiment_response'):
                analysis_data['Sentiment Analysis'] = st.session_state.sentiment_response
            if st.session_state.get('metrics_response'):
                analysis_data['Metrics Analysis'] = st.session_state.metrics_response
            
            if not analysis_data:
                st.warning("⚠️ No analysis data available. Run analyses in tabs 1-3 first!")
            else:
                # Strategy selection
                st.markdown("#### 🎯 Select Strategic Framework")
                
                strategy_type = st.selectbox(
                    "Choose the type of strategic output you need:",
                    [
                        "SWOT Analysis",
                        "Go-to-Market Playbook",
                        "Risk Assessment Matrix",
                        "Opportunity Scoring",
                        "30/60/90 Day Action Plan",
                        "Generate All"
                    ],
                    help="Select one or generate all strategic frameworks"
                )
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    generate_btn = st.button(
                        f"🚀 Generate {strategy_type}",
                        type="primary",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("🔄 Clear", use_container_width=True):
                        for key in ['swot', 'gtm', 'risk', 'opportunity', 'action_plan']:
                            if f'strategy_{key}' in st.session_state:
                                del st.session_state[f'strategy_{key}']
                        st.rerun()
                
                if generate_btn:
                    if not product_intelligence_team:
                        st.error("⚠️ Please enter both API keys in the sidebar first.")
                    else:
                        with st.spinner(f"🧠 AI generating {strategy_type}..."):
                            try:
                                if strategy_type == "SWOT Analysis" or strategy_type == "Generate All":
                                    st.markdown("### 📊 SWOT Analysis")
                                    result = generate_swot_analysis(company_name, analysis_data)
                                    st.session_state.strategy_swot = result
                                    st.markdown(result)
                                    st.divider()
                                
                                if strategy_type == "Go-to-Market Playbook" or strategy_type == "Generate All":
                                    st.markdown("### 🚀 Go-to-Market Playbook")
                                    result = generate_gtm_playbook(company_name, analysis_data)
                                    st.session_state.strategy_gtm = result
                                    st.markdown(result)
                                    st.divider()
                                
                                if strategy_type == "Risk Assessment Matrix" or strategy_type == "Generate All":
                                    st.markdown("### ⚠️ Risk Assessment Matrix")
                                    result = generate_risk_assessment(company_name, analysis_data)
                                    st.session_state.strategy_risk = result
                                    st.markdown(result)
                                    st.divider()
                                
                                if strategy_type == "Opportunity Scoring" or strategy_type == "Generate All":
                                    st.markdown("### 💎 Opportunity Scoring")
                                    result = generate_opportunity_scoring(company_name, analysis_data)
                                    st.session_state.strategy_opportunity = result
                                    st.markdown(result)
                                    st.divider()
                                
                                if strategy_type == "30/60/90 Day Action Plan" or strategy_type == "Generate All":
                                    st.markdown("### 📅 30/60/90 Day Action Plan")
                                    result = generate_action_plan(company_name, analysis_data)
                                    st.session_state.strategy_action_plan = result
                                    st.markdown(result)
                                    st.divider()
                                
                                st.success("✅ Strategic recommendations generated!")
                                
                            except Exception as e:
                                st.error(f"❌ Error: {e}")
                
                # Display cached strategies
                st.divider()
                st.markdown("#### 📋 Generated Strategies")
                
                strategies_generated = False
                
                if st.session_state.get('strategy_swot'):
                    strategies_generated = True
                    with st.expander("📊 SWOT Analysis", expanded=False):
                        st.markdown(st.session_state.strategy_swot)
                
                if st.session_state.get('strategy_gtm'):
                    strategies_generated = True
                    with st.expander("🚀 Go-to-Market Playbook", expanded=False):
                        st.markdown(st.session_state.strategy_gtm)
                
                if st.session_state.get('strategy_risk'):
                    strategies_generated = True
                    with st.expander("⚠️ Risk Assessment", expanded=False):
                        st.markdown(st.session_state.strategy_risk)
                
                if st.session_state.get('strategy_opportunity'):
                    strategies_generated = True
                    with st.expander("💎 Opportunity Scoring", expanded=False):
                        st.markdown(st.session_state.strategy_opportunity)
                
                if st.session_state.get('strategy_action_plan'):
                    strategies_generated = True
                    with st.expander("📅 Action Plan", expanded=False):
                        st.markdown(st.session_state.strategy_action_plan)
                
                if not strategies_generated:
                    st.info("📭 No strategies generated yet. Click the button above to create strategic recommendations!")
                
                # Export strategies
                if strategies_generated:
                    st.divider()
                    st.markdown("#### 💾 Export Strategies")
                    
                    all_strategies = {
                        "SWOT Analysis": st.session_state.get('strategy_swot', ''),
                        "GTM Playbook": st.session_state.get('strategy_gtm', ''),
                        "Risk Assessment": st.session_state.get('strategy_risk', ''),
                        "Opportunity Scoring": st.session_state.get('strategy_opportunity', ''),
                        "Action Plan": st.session_state.get('strategy_action_plan', '')
                    }
                    
                    # Remove empty strategies
                    all_strategies = {k: v for k, v in all_strategies.items() if v}
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # PDF export
                        if st.button("📄 Export as PDF", use_container_width=True):
                            with st.spinner("Generating strategy PDF..."):
                                try:
                                    pdf_buffer = generate_pdf_report(f"{company_name} - Strategic Plan", all_strategies)
                                    st.download_button(
                                        label="⬇️ Download Strategy PDF",
                                        data=pdf_buffer,
                                        file_name=f"{company_name}_strategy_{datetime.now().strftime('%Y%m%d')}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                                except Exception as e:
                                    st.error(f"Error: {e}")
                    
                    with col2:
                        # Markdown export
                        markdown_content = f"# Strategic Recommendations for {company_name}\n\n"
                        markdown_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                        markdown_content += "---\n\n"
                        
                        for title, content in all_strategies.items():
                            markdown_content += f"## {title}\n\n{content}\n\n---\n\n"
                        
                        st.download_button(
                            label="📝 Export as Markdown",
                            data=markdown_content,
                            file_name=f"{company_name}_strategy_{datetime.now().strftime('%Y%m%d')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

# ---------------- Sidebar ----------------
# Agent status indicators
with st.sidebar.container():
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(0, 255, 242, 0.3);
        margin: 20px 0;
    ">
        <h3 style="color: #00fff2; margin-top: 0;">🤖 System Status</h3>
    """, unsafe_allow_html=True)
    
    if openai_key and firecrawl_key:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0, 255, 127, 0.2), rgba(0, 200, 100, 0.2));
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #00ff7f;
            animation: pulse 2s infinite;
        ">
            <span style="color: #00ff7f; font-weight: 600;">✅ Product Intelligence Team Ready</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.2), rgba(200, 0, 80, 0.2));
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #ff0064;
        ">
            <span style="color: #ff0064; font-weight: 600;">❌ API Keys Required</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.divider()

# Multi-agent system info
with st.sidebar.container():
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(255, 0, 255, 0.3);
    ">
        <h3 style="color: #ff00ff; margin-top: 0;">🎯 Coordinated AI Team</h3>
    </div>
    """, unsafe_allow_html=True)
    
    agents_info = [
        ("🔍", "Product Launch Analyst", "Strategic GTM expert", "#667eea"),
        ("💬", "Market Sentiment Specialist", "Consumer perception expert", "#f093fb"),
        ("📈", "Launch Metrics Specialist", "Performance analytics expert", "#38ef7d")
    ]
    
    for icon, name, desc, color in agents_info:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            padding: 12px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid {color};
            transition: all 0.3s ease;
        ">
            <div style="color: {color}; font-weight: 700; font-size: 1.1rem;">{icon} {name}</div>
            <div style="color: #a0a0a0; font-size: 0.9rem; margin-top: 5px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.sidebar.divider()

# Analysis status
if company_name:
    with st.sidebar.container():
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 12px;
            border: 2px solid rgba(0, 255, 242, 0.3);
        ">
            <h3 style="color: #00fff2; margin-top: 0;">📊 Analysis Status</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="
            background: rgba(0, 255, 242, 0.1);
            padding: 8px;
            border-radius: 8px;
            margin: 10px 0;
        ">
            <span style="color: #00fff2; font-weight: 600;">🏢 Company: {company_name}</span>
        </div>
        """, unsafe_allow_html=True)
        
        status_items = [
            ("🔍", "Competitor Analysis", st.session_state.get('competitor_response'), "#667eea"),
            ("💬", "Sentiment Analysis", st.session_state.get('sentiment_response'), "#f093fb"),
            ("📈", "Metrics Analysis", st.session_state.get('metrics_response'), "#38ef7d")
        ]
        
        for icon, name, status, color in status_items:
            if status:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(0, 255, 127, 0.2), rgba(0, 200, 100, 0.2));
                    padding: 8px;
                    border-radius: 8px;
                    margin: 8px 0;
                    border-left: 3px solid #00ff7f;
                ">
                    <span style="color: #00ff7f; font-weight: 600;">{icon} {name} ✓</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    background: rgba(255, 255, 255, 0.03);
                    padding: 8px;
                    border-radius: 8px;
                    margin: 8px 0;
                    border-left: 3px solid {color};
                ">
                    <span style="color: {color}; font-weight: 600;">{icon} {name} ⏳</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.divider()

# Quick actions
with st.sidebar.container():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 242, 0.1));
        padding: 15px;
        border-radius: 12px;
        border: 2px solid rgba(255, 0, 255, 0.3);
    ">
        <h3 style="color: #ff00ff; margin-top: 0;">⚡ Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if company_name:
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.03);
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
        ">
            <div style="color: #00fff2; margin: 5px 0;"><b>J</b> - Competitor analysis</div>
            <div style="color: #f093fb; margin: 5px 0;"><b>K</b> - Market sentiment</div>
            <div style="color: #38ef7d; margin: 5px 0;"><b>L</b> - Launch metrics</div>
        </div>
        """, unsafe_allow_html=True)

st.sidebar.divider()

# Add AI.png image at the bottom of sidebar (without animation)
ai_image_path = Path("AI.png")
if ai_image_path.exists():
    with open(ai_image_path, "rb") as f:
        ai_image_data = base64.b64encode(f.read()).decode()
    st.sidebar.markdown(f"""
    <div style="
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 2px solid rgba(0, 255, 242, 0.3);
        margin-top: 20px;
    ">
        <img src="data:image/png;base64,{ai_image_data}" width="100%" style="border-radius: 10px;">
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div style="
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 2px solid rgba(0, 255, 242, 0.3);
        margin-top: 20px;
    ">
        <p style="color: #00fff2; font-size: 0.9rem;">🤖 AI Image</p>
    </div>
    """, unsafe_allow_html=True)