# Research Report Analysis Framework

## Overview

This comprehensive ML-based analysis framework is designed to extract deep insights from your collection of 2000+ research reports from 40+ research firms. The system provides **holistic views**, **individual report analysis**, and **company-specific insights** while identifying **research firm writing styles** and **analysis patterns**.

## 🎯 Analysis Approach

### **Three-Level Analysis Strategy**

#### 1. **Holistic View** 📊
- **Overall sentiment trends** across all reports
- **Common criticism patterns** and themes
- **Financial metrics focus** areas
- **Temporal analysis** of sentiment evolution
- **Topic modeling** to identify key themes
- **Company clustering** based on characteristics

#### 2. **Individual Report Focus** 📄
- **Sentiment analysis** for each report
- **Financial metrics extraction** and quantification
- **Criticism area identification** with context
- **Writing style analysis** (complexity, vocabulary, tone)
- **Recommendation extraction** and categorization

#### 3. **Company & Firm Style Analysis** 🏢
- **Company profiles** with sentiment evolution
- **Research firm writing styles** and patterns
- **Firm-specific criticism approaches**
- **Coverage analysis** and specialization
- **Comparative analysis** between firms

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configure Database
Ensure your `.env` file contains:
```
DB_HOST=localhost
DB_NAME=testudo
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

### 3. Run Analysis
```bash
python run_analysis.py
```

## 📋 Analysis Components

### **Core Framework (`ml_analysis_framework.py`)**

#### **EnhancedResearchReport Class**
```python
@dataclass
class EnhancedResearchReport:
    # Original fields
    source: str
    publication_date: date
    report_title: str
    link: str
    target_company: str
    short_seller: str
    ticker: str = ''
    
    # Enhanced ML-extracted fields
    report_text: str = ''
    word_count: int = 0
    sentiment_score: float = 0.0
    sentiment_label: str = ''
    key_topics: List[str] = None
    financial_metrics: Dict[str, float] = None
    criticism_areas: List[str] = None
    writing_style_features: Dict[str, float] = None
```

#### **ResearchReportAnalyzer Class**
Main analysis engine with methods for:
- **Text preprocessing** and cleaning
- **Sentiment analysis** using transformer models
- **Financial metrics extraction** using regex patterns
- **Topic modeling** with LDA
- **Company clustering** with K-means
- **Writing style analysis** with linguistic features

### **Data Integration (`data_loader.py`)**
- **Database connectivity** with PostgreSQL
- **Flexible querying** by company, firm, or date range
- **Export capabilities** to CSV/JSON
- **Statistics generation** for dataset overview

### **Main Analysis Script (`run_analysis.py`)**
- **Complete pipeline execution**
- **Interactive targeted analysis**
- **Visualization generation**
- **Results export and summary**

## 🔍 Analysis Features

### **Sentiment Analysis**
- **Transformer-based sentiment** using `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Context-aware scoring** with normalization
- **Sentiment evolution tracking** over time
- **Firm-specific sentiment patterns**

### **Financial Metrics Extraction**
```python
financial_keywords = {
    'revenue': ['revenue', 'sales', 'top-line', 'gross sales'],
    'profit': ['profit', 'earnings', 'net income', 'ebitda', 'ebit'],
    'debt': ['debt', 'liabilities', 'leverage', 'borrowings'],
    'cash_flow': ['cash flow', 'operating cash', 'free cash flow'],
    'valuation': ['pe ratio', 'price-to-earnings', 'ev/ebitda', 'book value'],
    'growth': ['growth rate', 'yoy growth', 'quarterly growth'],
    'efficiency': ['efficiency', 'productivity', 'operational efficiency'],
    'risk': ['risk', 'volatility', 'uncertainty', 'exposure']
}
```

### **Criticism Pattern Detection**
```python
criticism_patterns = [
    r'inefficient', r'poor', r'weak', r'declining', r'problematic',
    r'concern', r'issue', r'risk', r'overvalued', r'underperforming',
    r'management.*fail', r'strategy.*flaw', r'execution.*poor'
]
```

### **Writing Style Analysis**
- **Sentence complexity** (average length, structure)
- **Vocabulary richness** (unique word ratio)
- **Data usage** (number frequency, percentage mentions)
- **Emotional tone** (exclamation/question frequency)
- **Readability metrics** (Flesch-Kincaid, etc.)

### **Topic Modeling**
- **LDA (Latent Dirichlet Allocation)** for theme identification
- **TF-IDF vectorization** for feature extraction
- **Topic evolution** tracking over time
- **Firm-specific topic specialization**

### **Company Clustering**
- **Multi-dimensional clustering** based on:
  - Average sentiment
  - Criticism frequency
  - Report count
  - Writing style characteristics
- **t-SNE visualization** for cluster exploration
- **Cluster characteristic analysis**

## 📊 Output & Insights

### **Holistic Insights**
```json
{
  "overall_statistics": {
    "total_reports": 2000,
    "unique_companies": 150,
    "unique_firms": 40,
    "date_range": {"earliest": "2020-01-01", "latest": "2024-01-01"}
  },
  "sentiment_analysis": {
    "overall_sentiment": -0.234,
    "sentiment_distribution": {"negative": 1200, "neutral": 500, "positive": 300},
    "most_negative_reports": [...]
  },
  "common_criticism_areas": [...],
  "financial_focus_areas": {...},
  "temporal_trends": {...}
}
```

### **Individual Report Analysis**
```json
{
  "basic_info": {
    "title": "Company X: Overvalued and Inefficient",
    "company": "Company X",
    "firm": "Research Firm Y",
    "date": "2024-01-15",
    "word_count": 2500
  },
  "sentiment_analysis": {
    "score": -0.756,
    "label": "negative",
    "interpretation": "Highly negative - Strong criticism"
  },
  "financial_analysis": {
    "metrics_mentioned": ["revenue", "profit", "debt"],
    "metric_values": {"revenue": 1000000000}
  },
  "criticism_analysis": {
    "areas_criticized": ["management failure", "operational inefficiency"],
    "criticism_count": 8
  },
  "writing_style": {
    "features": {...},
    "style_characteristics": ["Complex sentence structure", "Data-driven analysis"]
  }
}
```

### **Company Profile**
```json
{
  "company_name": "Company X",
  "total_reports": 25,
  "sentiment_trends": {
    "average_sentiment": -0.345,
    "sentiment_evolution": [...]
  },
  "criticism_analysis": {
    "total_criticisms": 156,
    "common_criticism_areas": [...],
    "criticism_trends": {...}
  },
  "financial_focus": {
    "metrics_analyzed": {...},
    "financial_trends": {...}
  },
  "research_firm_analysis": {
    "firms_covering": ["Firm A", "Firm B", "Firm C"],
    "firm_sentiment_comparison": {...}
  }
}
```

### **Firm Style Profile**
```json
{
  "firm_name": "Research Firm Y",
  "total_reports": 150,
  "writing_style": {
    "average_sentence_length": 28.5,
    "vocabulary_richness": 0.72,
    "data_usage": 45.2,
    "emotional_tone": 3.1
  },
  "sentiment_profile": {
    "average_sentiment": -0.456,
    "sentiment_characterization": "Generally critical and negative"
  },
  "coverage_analysis": {
    "companies_covered": [...],
    "most_covered_companies": [...],
    "coverage_trends": {...}
  },
  "analysis_focus": {
    "common_topics": [...],
    "criticism_patterns": [...],
    "financial_focus": {...}
  }
}
```

## 🎨 Visualizations

The framework generates several key visualizations:

1. **Sentiment Distribution** - Histogram of sentiment scores
2. **Company Clusters** - t-SNE visualization of company groupings
3. **Firm Sentiment Comparison** - Bar chart of firm sentiment profiles
4. **Temporal Trends** - Line chart of sentiment evolution over time

## 🔧 Usage Examples

### **Complete Analysis**
```python
from data_loader import ResearchReportDataLoader
from ml_analysis_framework import ResearchReportAnalyzer

# Load data
loader = ResearchReportDataLoader()
reports = loader.load_reports_with_text(limit=1000)

# Run analysis
analyzer = ResearchReportAnalyzer(reports)
results = analyzer.run_complete_analysis()

# Generate insights
holistic_insights = results['holistic_insights']
print(f"Overall sentiment: {holistic_insights['sentiment_analysis']['overall_sentiment']}")
```

### **Targeted Company Analysis**
```python
# Get reports for specific company
company_reports = loader.get_reports_by_company("Tesla")
analyzer = ResearchReportAnalyzer(company_reports)
analyzer.enhance_reports()

# Generate company profile
profile = analyzer.generate_company_profile("Tesla")
print(f"Average sentiment: {profile['sentiment_trends']['average_sentiment']}")
```

### **Firm Style Analysis**
```python
# Get reports from specific firm
firm_reports = loader.get_reports_by_firm("Muddy Waters")
analyzer = ResearchReportAnalyzer(firm_reports)
analyzer.enhance_reports()
analyzer.analyze_firm_styles()

# Generate firm profile
firm_profile = analyzer.generate_firm_style_profile("Muddy Waters")
print(f"Writing style: {firm_profile['writing_style']}")
```

## 📈 Advanced Features

### **Custom Analysis**
- **Date range filtering** for temporal analysis
- **Sector-specific analysis** for industry insights
- **Comparative analysis** between companies/firms
- **Risk factor extraction** and categorization

### **Export Capabilities**
- **JSON export** for programmatic access
- **CSV export** for spreadsheet analysis
- **Visualization export** as PNG files
- **Structured data** for further processing

### **Performance Optimization**
- **Batch processing** for large datasets
- **Caching mechanisms** for repeated analysis
- **Parallel processing** for sentiment analysis
- **Memory optimization** for large report collections

## 🎯 Key Insights You'll Get

### **Holistic Understanding**
- Which companies are most frequently criticized?
- What are the most common criticism themes?
- How has overall sentiment changed over time?
- Which financial metrics are most analyzed?

### **Individual Report Insights**
- Sentiment and tone of each report
- Specific criticism areas with context
- Financial metrics mentioned and values
- Writing style characteristics

### **Company Intelligence**
- Sentiment evolution over time
- Most common criticism areas
- Financial focus patterns
- Research firm coverage and bias

### **Firm Style Analysis**
- Writing style characteristics
- Sentiment bias and approach
- Specialization areas
- Coverage patterns and trends

## 🔮 Future Enhancements

1. **Full-text scraping** from report links
2. **Advanced NLP** with custom financial domain models
3. **Real-time analysis** with streaming updates
4. **Interactive dashboard** with Plotly Dash
5. **API endpoints** for integration
6. **Predictive modeling** for sentiment forecasting

## 📞 Support

This framework provides a comprehensive foundation for analyzing your research report collection. The modular design allows for easy customization and extension based on your specific needs.

For questions or enhancements, refer to the code documentation and examples provided in each module. 