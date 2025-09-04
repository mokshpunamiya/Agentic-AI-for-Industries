# 🧠 Agentic AI System for Ministry of Industries

![Status](https://img.shields.io/badge/status-active-brightgreen)  
![License](https://img.shields.io/badge/license-MIT-blue)  
![Python](https://img.shields.io/badge/python-3.10+-yellow)  
![Streamlit](https://img.shields.io/badge/streamlit-%E2%9C%85-lightgrey)

Agentic AI System is an intelligent analytical tool built for the **Ministry of Industries**, designed to process, compare, and suggest insights across sectors and PSUs (Public Sector Units). It leverages **multi-agent AI frameworks** to provide prompt-based querying and sector-specific decision support.

---

## 🚀 Features

- 📊 Interactive analysis of 5-year performance trends across sectors (2020–2024)
- 🧠 Agent-based architecture (e.g., Analyzer Agent, Sector Agent, Policy Agent)
- 🔍 Prompt-based natural language query engine
- 📈 Sector-wise visualizations and comparisons
- 🧩 Policy and Analyst modes for custom use cases
- ✅ 100% profitable PSU analysis coverage

---

## 🖼️ UI Screens

### 🔎 Query-Based Analysis Output

![Query Results](./assets/query-results.jpeg)

### 🧠 Application Dashboard

![Dashboard UI](./assets/app-dashboard.png)

---

## 📊 Example Insights from AI Agents

**Query Asked:**  
> _Show 5-year performance trends — give this in bullet points._

**Agentic AI Response:**

### 🔧 Sector-wise Trends (2020–2024)

**Energy Sector**  
- **Revenue Growth**: 9.2% per year  
- **Net Profit Margin**: 4.8% → 6.5%  
- **Key Driver**: Expansion in renewable energy projects  

**Manufacturing Sector**  
- **Revenue Growth**: 7.8%  
- **Net Profit Margin**: 5.5% → 7.3%  
- **Key Driver**: Efficiency and cost optimization  

_...and more across Telecom, Transportation, Mining_

---

## 🧱 Tech Stack

- ⚙️ **Python 3.10+**
- 🎨 **Streamlit** (for interactive UI)
- 🕵️‍♂️ **LangChain / AutoGen** (for agent orchestration)
- 📁 **Pandas / NumPy** (for data preprocessing)
- 📊 **Plotly / Matplotlib** (for visualizations)

---

## 🧠 Agent Architecture

- **User Prompt Agent** → Routes to relevant agents  
- **Sector Analysis Agent** → Processes individual sector KPIs  
- **Policy Recommender Agent** → Generates improvement suggestions  
- **Result Formatter Agent** → Compiles human-readable output  

---

## 🧪 How to Run Locally

```bash
git clone https://github.com/your-username/agentic-ai-ministry.git
cd agentic-ai-ministry
pip install -r requirements.txt
streamlit run app.py
