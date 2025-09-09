

# 🧠 Agentic AI System for Ministry of Industries

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)

Agentic AI System is an intelligent analytical tool built for the Ministry of Industries, designed to process, compare, and suggest insights across sectors and PSUs (Public Sector Units). It leverages multi-agent AI frameworks to provide prompt-based querying and sector-specific decision support.

## 🎯 Overview

This application delivers real, analytical value through:
- **Multi-Agent Architecture**: Specialized AI agents for different analytical tasks
- **Interactive Data Analysis**: 5-year performance trends across sectors (2020–2024)
- **Natural Language Interface**: Prompt-based querying for intuitive access
- **Sector-Specific Insights**: Tailored analysis for different industry sectors
- **Decision Support**: Policy recommendations and strategic insights

## 🏗️ Project Structure

```
agentic-ai-ministry/
├── main.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── agents.py                 # AI agent implementations
│   ├── __init__.py
│   ├── user_prompt_agent.py    # Handles user input and routing
│   ├── sector_agent.py         # Processes sector-specific 
├── tools.py
│   ├── analyzer_agent.py       # Performs data analysis
│   ├── policy_agent.py         # Generates policy 
├── data/                   # Data storage and processing
│   ├── raw/                   # Raw data files
│   ├── processed/             # Processed datasets
│   └── database/              # Database files
├── data_manager.py            # Data loading utilities
├── ui.py                      # Visualization functions
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Modern web browser
- Internet connection (for API calls)

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/agentic-ai-ministry.git

# Navigate to the project directory
cd agentic-ai-ministry

# Install required packages
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Configuration
Update the configuration in `utils/config.py`:
- Database connection settings
- API keys for external services
- Model parameters and thresholds
- User access permissions

## 🌾 Key Features

### 📊 Data Analysis Capabilities
- **5-Year Performance Trends**: Comprehensive analysis from 2020-2024
- **Sector Comparisons**: Cross-sector performance metrics
- **PSU Analysis**: Detailed evaluation of Public Sector Units
- **Profitability Assessment**: 100% profitable PSU analysis coverage
- **Forecasting**: Predictive modeling for future trends

### 🧠 Agent-Based Architecture
- **User Prompt Agent**: Interprets and routes user queries
- **Sector Analysis Agent**: Processes sector-specific KPIs
- **Policy Recommender Agent**: Generates improvement suggestions
- **Result Formatter Agent**: Compiles human-readable outputs
- **Analyzer Agent**: Performs complex data analysis tasks

### 🎨 User Interface
- **Interactive Dashboard**: Streamlit-based responsive interface
- **Natural Language Queries**: Prompt-based interaction
- **Rich Visualizations**: Charts and graphs for data representation
- **Multiple Analysis Modes**: Policy and Analyst modes for different use cases
- **Export Functionality**: Download reports in various formats

## 📊 Data Structure

### Database Schema
The system uses a structured database with the following key tables:

#### Sectors Table
```sql
CREATE TABLE sectors (
    sector_id INT PRIMARY KEY,
    sector_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### PSUs Table
```sql
CREATE TABLE psus (
    psu_id INT PRIMARY KEY,
    psu_name VARCHAR(150) NOT NULL,
    sector_id INT,
    location VARCHAR(100),
    established_year INT,
    FOREIGN KEY (sector_id) REFERENCES sectors(sector_id)
);
```

#### Performance Data Table
```sql
CREATE TABLE performance_data (
    data_id INT PRIMARY KEY,
    psu_id INT,
    year INT,
    revenue DECIMAL(15,2),
    profit DECIMAL(15,2),
    assets DECIMAL(15,2),
    employees INT,
    roi DECIMAL(5,2),
    market_share DECIMAL(5,2),
    FOREIGN KEY (psu_id) REFERENCES psus(psu_id)
);
```

#### KPIs Table
```sql
CREATE TABLE kpis (
    kpi_id INT PRIMARY KEY,
    kpi_name VARCHAR(100) NOT NULL,
    description TEXT,
    unit VARCHAR(20),
    sector_id INT,
    FOREIGN KEY (sector_id) REFERENCES sectors(sector_id)
);
```

### Data Processing Pipeline
1. **Data Collection**: Raw data from government sources and PSU reports
2. **Validation**: Data quality checks and normalization
3. **Transformation**: Feature engineering and aggregation
4. **Storage**: Processed data stored in structured database
5. **Analysis**: AI agents process data for insights and recommendations

## 🖼️ UI Screens

### 🔎 Query-Based Analysis Output
![Query Results](assets/query_results.png)

### 🧠 Application Dashboard
![Dashboard UI](assets/dashboard.png)

## 📊 Example Insights from AI Agents

**Query Asked:**
```
Show 5-year performance trends — give this in bullet points.
```

**Agentic AI Response:**
🔧 **Sector-wise Trends (2020–2024)**

**Energy Sector**
- Revenue Growth: 9.2% per year
- Net Profit Margin: 4.8% → 6.5%
- Key Driver: Expansion in renewable energy projects

**Manufacturing Sector**
- Revenue Growth: 7.8%
- Net Profit Margin: 5.5% → 7.3%
- Key Driver: Efficiency and cost optimization

**Telecom Sector**
- Revenue Growth: 6.5%
- Net Profit Margin: 8.2% → 9.1%
- Key Driver: Digital transformation and 5G rollout

**Transportation Sector**
- Revenue Growth: 5.7%
- Net Profit Margin: 3.9% → 5.2%
- Key Driver: Infrastructure modernization

**Mining Sector**
- Revenue Growth: 8.3%
- Net Profit Margin: 7.1% → 8.9%
- Key Driver: Commodity price increases and operational efficiency

## 🧱 Tech Stack

### Backend
- **Python 3.10+**: Core programming language
- **Streamlit**: Interactive web application framework
- **LangChain / AutoGen**: Agent orchestration and management
- **Pandas / NumPy**: Data manipulation and numerical operations
- **SQLAlchemy**: Database ORM and interaction

### AI/ML
- **OpenAI / Hugging Face Models**: Language models for natural language processing
- **Scikit-learn**: Machine learning algorithms
- **TensorFlow/PyTorch**: Deep learning frameworks (optional for advanced features)
- **Plotly / Matplotlib**: Data visualization libraries

### Infrastructure
- **SQLite/PostgreSQL**: Database management
- **Docker**: Containerization (optional)
- **GitHub**: Version control and collaboration

## 🧠 Agent Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  User Prompt    │───▶│  Routing Agent   │───▶│ Sector Analysis │
│     Agent       │    │                  │    │      Agent       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Result         │◀───│  Formatter       │◀───│  Analyzer       │
│  Formatter      │    │      Agent       │    │     Agent       │
│     Agent       │    └──────────────────┘    └─────────────────┘
└─────────────────┘                                       │
                                                        ▼
                                                ┌─────────────────┐
                                                │  Policy         │
                                                │  Recommender    │
                                                │      Agent      │
                                                └─────────────────┘
```

## 🧪 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/agentic-ai-ministry.git

# Navigate to the project directory
cd agentic-ai-ministry

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

Access the application at `http://localhost:8501` in your web browser.

## 📹 Demo Video

https://github.com/user-attachments/assets/742f7fea-745b-4a0f-aa51-4bd8a0ca9105

[![Demo Video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://youtu.be/JZ6Isim2e48)

*Click the image above to watch the demo video showcasing the Agentic AI System in action.*

## 📈 Business Value

### For Ministry of Industries
- **Data-Driven Decisions**: Evidence-based policy formulation
- **Efficiency Gains**: Automated analysis reduces manual workload
- **Strategic Planning**: Long-term forecasting and trend identification
- **Performance Monitoring**: Real-time PSU performance tracking

### For Public Sector Units
- **Benchmarking**: Performance comparison across sectors
- **Improvement Areas**: Identification of operational inefficiencies
- **Best Practices**: Knowledge sharing across organizations
- **Resource Optimization**: Better allocation of resources

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **RAM**: Minimum 4GB, recommended 8GB or more
- **Storage**: Minimum 2GB free space
- **Processor**: Modern CPU with multi-core support

### Software Requirements
- **Python**: 3.10 or higher
- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **Internet Connection**: Required for API calls and model downloads

## 🚀 Deployment Options

### Local Development
- Use the provided installation steps
- Configure local database settings in `utils/config.py`

### Cloud Deployment
#### Docker Deployment
```bash
# Build Docker image
docker build -t agentic-ai-ministry .

# Run container
docker run -p 8501:8501 agentic-ai-ministry
```

#### Cloud Platforms
- **AWS**: Deploy using EC2 or Elastic Beanstalk
- **Google Cloud**: Use Cloud Run or App Engine
- **Azure**: Deploy on Azure App Service
- **Heroku**: Platform-as-a-Service deployment

## 📚 Usage Examples

### Basic Analysis
1. Launch the application
2. Select the desired sector or PSU
3. Enter a natural language query (e.g., "Show profit trends for last 5 years")
4. View the generated insights and visualizations

### Advanced Analysis
1. Switch to "Analyst Mode" for detailed technical analysis
2. Use "Policy Mode" for strategic recommendations
3. Export reports in PDF or CSV format
4. Compare multiple sectors or PSUs using the comparison tool

## 🎯 Competitive Advantages

### Multi-Agent Architecture
- **Specialized Expertise**: Each agent focuses on specific analytical tasks
- **Scalability**: Easy to add new agents for additional capabilities
- **Modularity**: Independent development and testing of components

### Natural Language Interface
- **Accessibility**: No technical knowledge required
- **Flexibility**: Supports a wide range of queries
- **Intuitive**: Similar to conversing with a human analyst

### Comprehensive Analysis
- **Holistic View**: Considers multiple factors and interdependencies
- **Historical Context**: Incorporates trends over time
- **Actionable Insights**: Provides specific recommendations

## 🔄 Future Enhancements

Planned improvements include:
- **Mobile Application**: Native iOS and Android apps
- **Voice Interface**: Integration with voice assistants
- **Real-time Data**: Live data feeds from PSUs
- **Advanced Forecasting**: Improved predictive models
- **Collaboration Features**: Multi-user analysis and sharing
- **Integration with Government Systems**: Direct data exchange capabilities

## 📞 Support

For questions, issues, or feature requests:
- Check the documentation in this README
- Review the `/docs` folder for detailed guides
- Contact the development team at support@example.com
- Report bugs via the issue tracker on GitHub

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Empowering Decision-Makers - The Agentic AI System is committed to leveraging artificial intelligence to enhance industrial policy formulation and improve PSU performance through data-driven insights.*
