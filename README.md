# 🚀 LaunchIQ Intelligence Platform

**AI Product LaunchIQ Intelligence Platform**  
✨ *Complete Competitive Intelligence & Strategic Planning Powered by AI* ✨

**Live demo:** https://market-launch-intelligence-platforms-01-agents.streamlit.app/

**Created:** November 7, 2025

---

## 🔎 Project Summary

**LaunchIQ Intelligence Platform** is a multi-agent AI application that helps product teams plan, analyze, and optimize product launches and go-to-market strategies. The platform combines real-time web intelligence, sentiment analysis, performance metrics, and structured strategic recommendations — all orchestrated by specialized AI agents.

Key goal: make evidence-driven launch decisions faster and more reliable.

---

## 🧭 Core Capabilities

- **Comprehensive competitor analysis** (tactics, positioning, strengths/weaknesses)
- **Real-time market sentiment tracking** across social media and review sources
- **Launch performance metrics** including adoption, engagement, revenue signals
- **Multi-company side-by-side comparisons**
- **Historical tracking & trend visualizations** with export options
- **Automated alerting** for sentiment or launch-related events
- **Actionable strategic outputs** (SWOT, GTM playbooks, 30/60/90 day plans)

---

## 🤖 Architecture & Core AI System

**Multi-Agent Architecture (3 Specialized AI Agents):**

1. **Product Launch Analyst**  
   - Role: Senior GTM strategist.  
   - Tasks: Evaluate competitor positioning, analyze launch tactics, produce evidence-driven competitive analysis and prioritized recommendations.

2. **Market Sentiment Specialist**  
   - Role: Consumer perception expert.  
   - Tasks: Scrape social media, reviews, and forums; compute sentiment drivers and trend changes; produce sentiment score (-100 to +100).

3. **Launch Metrics Specialist**  
   - Role: Performance analytics expert.  
   - Tasks: Track KPIs (adoption, retention, revenue), press coverage, virality metrics and translate them into growth insights.

**Primary model:** `GPT-4o-mini` (chosen for cost-efficiency; roughly ~94% cost savings compared to larger variants).  
**Model temperature:** `0.3` (balanced creativity & accuracy).  
**Web intelligence & scraping:** Firecrawl API (real-time scraping/data aggregation).

---

## 🧩 Feature Tabs (User-Facing)

**Tab 1: 🔍 Competitor Analysis**  
- Deep dives into competitor launches  
- Tactical, strategic & positioning analysis with source links  
- Actionable recommendations

**Tab 2: 💬 Market Sentiment Analysis**  
- Social media + review sentiment aggregation  
- Drivers of positive/negative sentiment  
- Brand perception monitoring & overall sentiment score (-100 to +100)

**Tab 3: 📈 Launch Metrics**  
- KPI dashboards (user adoption, retention, revenue growth)  
- Media & press monitoring  
- Traction and virality indicators

**Tab 4: ⚖️ Multi-Company Comparison**  
- Compare 2–5 companies side-by-side  
- Modes: Sentiment, Market Position, Launch Strategy  
- Comparative insights & recommendations

**Tab 5: 📊 Historical Tracking & Trends**  
- Stores last 100 analysis entries  
- Sentiment trend visualizations (Plotly)  
- Timeline, company filtering, CSV export

**Tab 6: 🔔 Alert Manager**  
- Custom alerts (sentiment drops/spikes, new product launches)  
- Thresholds configurable (5–50%)  
- Active dashboard; email notifications marked as "future feature"

**Tab 7: 📊 Visualizations & Export Suite**  
- Interactive charts: sentiment gauges, word freq, keywords/themes  
- Export: PDF, Excel (multi-sheet), JSON, Markdown

**Tab 8: 🎯 Strategic Recommendations Generator**  
- Outputs using 5 frameworks:  
  - SWOT Analysis  
  - GTM Playbook  
  - Risk Assessment Matrix (probability × impact)  
  - Opportunity Scoring (prioritized)  
  - 30/60/90 Day Action Plan

---

## 🛠️ Tech Stack (suggested / current)

- **Frontend:** Streamlit (live app link above)  
- **AI / LLMs:** GPT-4o-mini (via OpenAI API)  
- **Web intelligence:** Firecrawl API for scraping/real-time web data  
- **Visualizations:** Plotly for interactive charts  
- **Data storage:** Lightweight DB or file store for history (CSV/JSON)  
- **Deployment:** Streamlit Cloud / any containerized host

---

## ⚙️ Installation (developer/local)

> _Replace `FIRECRAWL_API_KEY` and `OPENAI_API_KEY` with your own keys._

```bash
git clone <your-repo-url>
cd launchiq-intelligence-platform
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# env vars
export OPENAI_API_KEY="sk-..."
export FIRECRAWL_API_KEY="fc-..."

streamlit run app.py
