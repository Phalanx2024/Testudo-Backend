import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import json
from datetime import datetime, date
from dataclasses import dataclass
import re
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ML Libraries
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.cluster import KMeans, DBSCAN
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from textblob import TextBlob
import transformers
from transformers import pipeline, AutoTokenizer, AutoModel
import torch

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

@dataclass
class EnhancedResearchReport:
    """Enhanced research report with extracted features"""
    # Original fields
    source: str
    publication_date: date
    report_title: str
    link: str
    target_company: str
    short_seller: str
    ticker: str = ''
    
    # Enhanced fields
    report_text: str = ''
    word_count: int = 0
    sentiment_score: float = 0.0
    sentiment_label: str = ''
    key_topics: List[str] = None
    financial_metrics: Dict[str, float] = None
    criticism_areas: List[str] = None
    recommendations: List[str] = None
    risk_factors: List[str] = None
    writing_style_features: Dict[str, float] = None
    
    def __post_init__(self):
        if self.key_topics is None:
            self.key_topics = []
        if self.financial_metrics is None:
            self.financial_metrics = {}
        if self.criticism_areas is None:
            self.criticism_areas = []
        if self.recommendations is None:
            self.recommendations = []
        if self.risk_factors is None:
            self.risk_factors = []
        if self.writing_style_features is None:
            self.writing_style_features = {}

class ResearchReportAnalyzer:
    """Comprehensive analyzer for research reports"""
    
    def __init__(self, reports_data: List[Dict]):
        self.reports_data = reports_data
        self.enhanced_reports = []
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize ML models
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.topic_model = None
        self.company_clusters = None
        self.firm_style_profiles = {}
        
        # Financial keywords for extraction
        self.financial_keywords = {
            'revenue': ['revenue', 'sales', 'top-line', 'gross sales'],
            'profit': ['profit', 'earnings', 'net income', 'ebitda', 'ebit'],
            'debt': ['debt', 'liabilities', 'leverage', 'borrowings'],
            'cash_flow': ['cash flow', 'operating cash', 'free cash flow'],
            'valuation': ['pe ratio', 'price-to-earnings', 'ev/ebitda', 'book value'],
            'growth': ['growth rate', 'yoy growth', 'quarterly growth'],
            'efficiency': ['efficiency', 'productivity', 'operational efficiency'],
            'risk': ['risk', 'volatility', 'uncertainty', 'exposure']
        }
        
        # Criticism patterns
        self.criticism_patterns = [
            r'inefficient', r'poor', r'weak', r'declining', r'problematic',
            r'concern', r'issue', r'risk', r'overvalued', r'underperforming',
            r'management.*fail', r'strategy.*flaw', r'execution.*poor'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
        
        # Basic cleaning
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize and lemmatize
        doc = self.nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and len(token.text) > 2]
        
        return ' '.join(tokens)
    
    def extract_sentiment(self, text: str) -> Tuple[float, str]:
        """Extract sentiment from text"""
        if not text:
            return 0.0, "neutral"
        
        try:
            result = self.sentiment_analyzer(text[:512])[0]  # Limit text length
            score = result['score']
            label = result['label']
            
            # Normalize score
            if label == 'NEGATIVE':
                score = -score
            elif label == 'NEUTRAL':
                score = 0
            
            return score, label.lower()
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 0.0, "neutral"
    
    def extract_financial_metrics(self, text: str) -> Dict[str, float]:
        """Extract financial metrics mentioned in text"""
        metrics = {}
        
        for category, keywords in self.financial_keywords.items():
            for keyword in keywords:
                # Look for patterns like "revenue of $X" or "revenue: $X"
                pattern = rf'{keyword}.*?(\$[\d,]+\.?\d*[mbk]?)'
                matches = re.findall(pattern, text.lower())
                if matches:
                    # Convert to numeric value
                    value_str = matches[0].replace('$', '').replace(',', '')
                    if 'm' in value_str:
                        value = float(value_str.replace('m', '')) * 1e6
                    elif 'b' in value_str:
                        value = float(value_str.replace('b', '')) * 1e9
                    elif 'k' in value_str:
                        value = float(value_str.replace('k', '')) * 1e3
                    else:
                        value = float(value_str)
                    metrics[category] = value
        
        return metrics
    
    def extract_criticism_areas(self, text: str) -> List[str]:
        """Extract areas of criticism from text"""
        criticism_areas = []
        
        for pattern in self.criticism_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                # Get surrounding context
                for match in matches:
                    start = text.lower().find(match)
                    context = text[max(0, start-50):start+len(match)+50]
                    criticism_areas.append(context.strip())
        
        return list(set(criticism_areas))  # Remove duplicates
    
    def analyze_writing_style(self, text: str) -> Dict[str, float]:
        """Analyze writing style features"""
        if not text:
            return {}
        
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        
        style_features = {
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'sentence_count': len(sentences),
            'word_count': len(words),
            'unique_word_ratio': len(set(words)) / len(words) if words else 0,
            'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'number_count': len(re.findall(r'\d+', text)),
            'percentage_count': len(re.findall(r'\d+%', text))
        }
        
        return style_features
    
    def enhance_reports(self):
        """Enhance all reports with extracted features"""
        print("Enhancing reports with extracted features...")
        
        for report in self.reports_data:
            # Create enhanced report
            enhanced_report = EnhancedResearchReport(
                source=report.get('source', ''),
                publication_date=report.get('publication_date'),
                report_title=report.get('report_title', ''),
                link=report.get('link', ''),
                target_company=report.get('target_company', ''),
                short_seller=report.get('short_seller', ''),
                ticker=report.get('ticker', ''),
                report_text=report.get('report_text', '')
            )
            
            # Extract features
            if enhanced_report.report_text:
                enhanced_report.word_count = len(enhanced_report.report_text.split())
                enhanced_report.sentiment_score, enhanced_report.sentiment_label = self.extract_sentiment(enhanced_report.report_text)
                enhanced_report.financial_metrics = self.extract_financial_metrics(enhanced_report.report_text)
                enhanced_report.criticism_areas = self.extract_criticism_areas(enhanced_report.report_text)
                enhanced_report.writing_style_features = self.analyze_writing_style(enhanced_report.report_text)
            
            self.enhanced_reports.append(enhanced_report)
        
        print(f"Enhanced {len(self.enhanced_reports)} reports")
    
    def perform_topic_modeling(self, n_topics: int = 10):
        """Perform topic modeling on all reports"""
        print("Performing topic modeling...")
        
        # Prepare text data
        texts = [report.report_text for report in self.enhanced_reports if report.report_text]
        preprocessed_texts = [self.preprocess_text(text) for text in texts]
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            min_df=5,
            max_df=0.7
        )
        
        tfidf_matrix = vectorizer.fit_transform(preprocessed_texts)
        
        # Apply LDA
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=50
        )
        
        lda.fit(tfidf_matrix)
        
        # Extract topics
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[-10:]]
            topics.append({
                'topic_id': topic_idx,
                'top_words': top_words,
                'topic_weight': topic.sum()
            })
        
        self.topic_model = {
            'lda_model': lda,
            'vectorizer': vectorizer,
            'topics': topics,
            'tfidf_matrix': tfidf_matrix
        }
        
        print(f"Identified {n_topics} topics")
        return topics
    
    def cluster_companies(self, n_clusters: int = 8):
        """Cluster companies based on their characteristics"""
        print("Clustering companies...")
        
        # Create company profiles
        company_profiles = defaultdict(lambda: {
            'reports': [],
            'avg_sentiment': 0,
            'criticism_count': 0,
            'financial_metrics': defaultdict(list),
            'writing_style': defaultdict(list)
        })
        
        for report in self.enhanced_reports:
            company = report.target_company
            company_profiles[company]['reports'].append(report)
            
            if report.sentiment_score != 0:
                company_profiles[company]['avg_sentiment'] += report.sentiment_score
            
            company_profiles[company]['criticism_count'] += len(report.criticism_areas)
            
            for metric, value in report.financial_metrics.items():
                company_profiles[company]['financial_metrics'][metric].append(value)
            
            for feature, value in report.writing_style_features.items():
                company_profiles[company]['writing_style'][feature].append(value)
        
        # Calculate averages
        for company in company_profiles:
            report_count = len(company_profiles[company]['reports'])
            company_profiles[company]['avg_sentiment'] /= report_count
            company_profiles[company]['report_count'] = report_count
        
        # Create feature matrix for clustering
        companies = list(company_profiles.keys())
        features = []
        
        for company in companies:
            profile = company_profiles[company]
            feature_vector = [
                profile['avg_sentiment'],
                profile['criticism_count'],
                profile['report_count'],
                np.mean(profile['writing_style'].get('avg_sentence_length', [0])),
                np.mean(profile['writing_style'].get('unique_word_ratio', [0]))
            ]
            features.append(feature_vector)
        
        # Perform clustering
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(features_scaled)
        
        # Store results
        self.company_clusters = {
            'companies': companies,
            'cluster_labels': cluster_labels,
            'profiles': company_profiles,
            'cluster_centers': kmeans.cluster_centers_
        }
        
        print(f"Clustered {len(companies)} companies into {n_clusters} groups")
        return self.company_clusters
    
    def analyze_firm_styles(self):
        """Analyze writing styles of different research firms"""
        print("Analyzing firm writing styles...")
        
        firm_styles = defaultdict(lambda: {
            'reports': [],
            'avg_sentiment': 0,
            'writing_features': defaultdict(list),
            'common_topics': [],
            'criticism_patterns': []
        })
        
        for report in self.enhanced_reports:
            firm = report.short_seller
            firm_styles[firm]['reports'].append(report)
            
            if report.sentiment_score != 0:
                firm_styles[firm]['avg_sentiment'] += report.sentiment_score
            
            for feature, value in report.writing_style_features.items():
                firm_styles[firm]['writing_features'][feature].append(value)
        
        # Calculate averages and patterns
        for firm in firm_styles:
            report_count = len(firm_styles[firm]['reports'])
            firm_styles[firm]['avg_sentiment'] /= report_count
            firm_styles[firm]['report_count'] = report_count
            
            # Calculate average writing features
            for feature in firm_styles[firm]['writing_features']:
                firm_styles[firm]['writing_features'][feature] = np.mean(firm_styles[firm]['writing_features'][feature])
        
        self.firm_style_profiles = dict(firm_styles)
        print(f"Analyzed styles for {len(firm_styles)} research firms")
        return self.firm_style_profiles
    
    def generate_holistic_insights(self) -> Dict:
        """Generate holistic insights across all reports"""
        print("Generating holistic insights...")
        
        insights = {
            'overall_statistics': {
                'total_reports': len(self.enhanced_reports),
                'unique_companies': len(set(r.target_company for r in self.enhanced_reports)),
                'unique_firms': len(set(r.short_seller for r in self.enhanced_reports)),
                'date_range': {
                    'earliest': min(r.publication_date for r in self.enhanced_reports),
                    'latest': max(r.publication_date for r in self.enhanced_reports)
                }
            },
            'sentiment_analysis': {
                'overall_sentiment': np.mean([r.sentiment_score for r in self.enhanced_reports]),
                'sentiment_distribution': Counter([r.sentiment_label for r in self.enhanced_reports]),
                'most_negative_reports': sorted(
                    [(r.report_title, r.sentiment_score) for r in self.enhanced_reports],
                    key=lambda x: x[1]
                )[:10]
            },
            'common_criticism_areas': self._extract_common_criticism_areas(),
            'financial_focus_areas': self._extract_financial_focus_areas(),
            'temporal_trends': self._analyze_temporal_trends()
        }
        
        return insights
    
    def _extract_common_criticism_areas(self) -> List[Tuple[str, int]]:
        """Extract most common criticism areas"""
        all_criticisms = []
        for report in self.enhanced_reports:
            all_criticisms.extend(report.criticism_areas)
        
        # Count and return top criticisms
        criticism_counts = Counter(all_criticisms)
        return criticism_counts.most_common(20)
    
    def _extract_financial_focus_areas(self) -> Dict[str, int]:
        """Extract most common financial metrics mentioned"""
        metric_counts = defaultdict(int)
        for report in self.enhanced_reports:
            for metric in report.financial_metrics:
                metric_counts[metric] += 1
        
        return dict(metric_counts)
    
    def _analyze_temporal_trends(self) -> Dict:
        """Analyze trends over time"""
        # Group by month/year
        monthly_data = defaultdict(list)
        for report in self.enhanced_reports:
            month_key = f"{report.publication_date.year}-{report.publication_date.month:02d}"
            monthly_data[month_key].append(report.sentiment_score)
        
        # Calculate monthly averages
        monthly_trends = {
            month: np.mean(scores) for month, scores in monthly_data.items()
        }
        
        return monthly_trends
    
    def generate_individual_report_insights(self, report: EnhancedResearchReport) -> Dict:
        """Generate detailed insights for an individual report"""
        insights = {
            'basic_info': {
                'title': report.report_title,
                'company': report.target_company,
                'firm': report.short_seller,
                'date': report.publication_date,
                'word_count': report.word_count
            },
            'sentiment_analysis': {
                'score': report.sentiment_score,
                'label': report.sentiment_label,
                'interpretation': self._interpret_sentiment(report.sentiment_score)
            },
            'financial_analysis': {
                'metrics_mentioned': list(report.financial_metrics.keys()),
                'metric_values': report.financial_metrics
            },
            'criticism_analysis': {
                'areas_criticized': report.criticism_areas,
                'criticism_count': len(report.criticism_areas)
            },
            'writing_style': {
                'features': report.writing_style_features,
                'style_characteristics': self._characterize_writing_style(report.writing_style_features)
            }
        }
        
        return insights
    
    def _interpret_sentiment(self, score: float) -> str:
        """Interpret sentiment score"""
        if score < -0.5:
            return "Highly negative - Strong criticism"
        elif score < -0.1:
            return "Negative - Critical analysis"
        elif score < 0.1:
            return "Neutral - Balanced analysis"
        elif score < 0.5:
            return "Positive - Favorable analysis"
        else:
            return "Highly positive - Strong endorsement"
    
    def _characterize_writing_style(self, features: Dict[str, float]) -> List[str]:
        """Characterize writing style based on features"""
        characteristics = []
        
        if features.get('avg_sentence_length', 0) > 25:
            characteristics.append("Complex sentence structure")
        elif features.get('avg_sentence_length', 0) < 15:
            characteristics.append("Concise writing style")
        
        if features.get('unique_word_ratio', 0) > 0.7:
            characteristics.append("Rich vocabulary")
        
        if features.get('exclamation_count', 0) > 5:
            characteristics.append("Emotional tone")
        
        if features.get('number_count', 0) > 20:
            characteristics.append("Data-driven analysis")
        
        return characteristics
    
    def generate_company_profile(self, company_name: str) -> Dict:
        """Generate comprehensive profile for a specific company"""
        company_reports = [r for r in self.enhanced_reports if r.target_company == company_name]
        
        if not company_reports:
            return {"error": f"No reports found for {company_name}"}
        
        profile = {
            'company_name': company_name,
            'total_reports': len(company_reports),
            'date_range': {
                'earliest': min(r.publication_date for r in company_reports),
                'latest': max(r.publication_date for r in company_reports)
            },
            'sentiment_trends': {
                'average_sentiment': np.mean([r.sentiment_score for r in company_reports]),
                'sentiment_evolution': self._analyze_company_sentiment_evolution(company_reports)
            },
            'criticism_analysis': {
                'total_criticisms': sum(len(r.criticism_areas) for r in company_reports),
                'common_criticism_areas': self._extract_company_criticisms(company_reports),
                'criticism_trends': self._analyze_company_criticism_trends(company_reports)
            },
            'financial_focus': {
                'metrics_analyzed': self._extract_company_financial_focus(company_reports),
                'financial_trends': self._analyze_company_financial_trends(company_reports)
            },
            'research_firm_analysis': {
                'firms_covering': list(set(r.short_seller for r in company_reports)),
                'firm_sentiment_comparison': self._compare_firm_sentiments(company_reports)
            }
        }
        
        return profile
    
    def _analyze_company_sentiment_evolution(self, reports: List[EnhancedResearchReport]) -> List[Dict]:
        """Analyze how sentiment towards a company has evolved over time"""
        sorted_reports = sorted(reports, key=lambda x: x.publication_date)
        
        evolution = []
        for i, report in enumerate(sorted_reports):
            evolution.append({
                'date': report.publication_date,
                'sentiment': report.sentiment_score,
                'firm': report.short_seller,
                'title': report.report_title
            })
        
        return evolution
    
    def _extract_company_criticisms(self, reports: List[EnhancedResearchReport]) -> List[Tuple[str, int]]:
        """Extract common criticism areas for a specific company"""
        all_criticisms = []
        for report in reports:
            all_criticisms.extend(report.criticism_areas)
        
        criticism_counts = Counter(all_criticisms)
        return criticism_counts.most_common(10)
    
    def _analyze_company_criticism_trends(self, reports: List[EnhancedResearchReport]) -> Dict:
        """Analyze criticism trends for a company over time"""
        # Group by year
        yearly_criticisms = defaultdict(int)
        for report in reports:
            year = report.publication_date.year
            yearly_criticisms[year] += len(report.criticism_areas)
        
        return dict(yearly_criticisms)
    
    def _extract_company_financial_focus(self, reports: List[EnhancedResearchReport]) -> Dict[str, int]:
        """Extract financial metrics focus for a company"""
        metric_counts = defaultdict(int)
        for report in reports:
            for metric in report.financial_metrics:
                metric_counts[metric] += 1
        
        return dict(metric_counts)
    
    def _analyze_company_financial_trends(self, reports: List[EnhancedResearchReport]) -> Dict:
        """Analyze financial metric trends for a company"""
        # Group by year and metric
        yearly_metrics = defaultdict(lambda: defaultdict(list))
        for report in reports:
            year = report.publication_date.year
            for metric, value in report.financial_metrics.items():
                yearly_metrics[year][metric].append(value)
        
        # Calculate yearly averages
        trends = {}
        for year in yearly_metrics:
            trends[year] = {
                metric: np.mean(values) for metric, values in yearly_metrics[year].items()
            }
        
        return trends
    
    def _compare_firm_sentiments(self, reports: List[EnhancedResearchReport]) -> Dict[str, float]:
        """Compare sentiment scores from different research firms for a company"""
        firm_sentiments = defaultdict(list)
        for report in reports:
            firm_sentiments[report.short_seller].append(report.sentiment_score)
        
        return {
            firm: np.mean(scores) for firm, scores in firm_sentiments.items()
        }
    
    def generate_firm_style_profile(self, firm_name: str) -> Dict:
        """Generate detailed style profile for a research firm"""
        if firm_name not in self.firm_style_profiles:
            return {"error": f"No data found for {firm_name}"}
        
        profile = self.firm_style_profiles[firm_name]
        
        firm_profile = {
            'firm_name': firm_name,
            'total_reports': profile['report_count'],
            'writing_style': {
                'average_sentence_length': profile['writing_features'].get('avg_sentence_length', 0),
                'vocabulary_richness': profile['writing_features'].get('unique_word_ratio', 0),
                'data_usage': profile['writing_features'].get('number_count', 0),
                'emotional_tone': profile['writing_features'].get('exclamation_count', 0)
            },
            'sentiment_profile': {
                'average_sentiment': profile['avg_sentiment'],
                'sentiment_characterization': self._characterize_firm_sentiment(profile['avg_sentiment'])
            },
            'coverage_analysis': {
                'companies_covered': list(set(r.target_company for r in profile['reports'])),
                'most_covered_companies': self._get_most_covered_companies(profile['reports']),
                'coverage_trends': self._analyze_firm_coverage_trends(profile['reports'])
            },
            'analysis_focus': {
                'common_topics': self._extract_firm_topics(profile['reports']),
                'criticism_patterns': self._extract_firm_criticism_patterns(profile['reports']),
                'financial_focus': self._extract_firm_financial_focus(profile['reports'])
            }
        }
        
        return firm_profile
    
    def _characterize_firm_sentiment(self, avg_sentiment: float) -> str:
        """Characterize a firm's overall sentiment approach"""
        if avg_sentiment < -0.3:
            return "Generally critical and negative"
        elif avg_sentiment < -0.1:
            return "Slightly critical"
        elif avg_sentiment < 0.1:
            return "Balanced and neutral"
        elif avg_sentiment < 0.3:
            return "Generally positive"
        else:
            return "Highly positive and supportive"
    
    def _get_most_covered_companies(self, reports: List[EnhancedResearchReport]) -> List[Tuple[str, int]]:
        """Get companies most frequently covered by a firm"""
        company_counts = Counter(r.target_company for r in reports)
        return company_counts.most_common(10)
    
    def _analyze_firm_coverage_trends(self, reports: List[EnhancedResearchReport]) -> Dict:
        """Analyze a firm's coverage trends over time"""
        yearly_coverage = defaultdict(int)
        for report in reports:
            year = report.publication_date.year
            yearly_coverage[year] += 1
        
        return dict(yearly_coverage)
    
    def _extract_firm_topics(self, reports: List[EnhancedResearchReport]) -> List[str]:
        """Extract common topics in a firm's reports"""
        # This would be enhanced with actual topic modeling results
        # For now, return common words
        all_words = []
        for report in reports:
            if report.report_text:
                words = self.preprocess_text(report.report_text).split()
                all_words.extend(words)
        
        word_counts = Counter(all_words)
        return [word for word, count in word_counts.most_common(20)]
    
    def _extract_firm_criticism_patterns(self, reports: List[EnhancedResearchReport]) -> List[str]:
        """Extract common criticism patterns used by a firm"""
        all_criticisms = []
        for report in reports:
            all_criticisms.extend(report.criticism_areas)
        
        criticism_counts = Counter(all_criticisms)
        return [criticism for criticism, count in criticism_counts.most_common(10)]
    
    def _extract_firm_financial_focus(self, reports: List[EnhancedResearchReport]) -> Dict[str, int]:
        """Extract financial metrics most commonly analyzed by a firm"""
        metric_counts = defaultdict(int)
        for report in reports:
            for metric in report.financial_metrics:
                metric_counts[metric] += 1
        
        return dict(metric_counts)
    
    def run_complete_analysis(self) -> Dict:
        """Run complete analysis pipeline"""
        print("Starting complete analysis pipeline...")
        
        # Step 1: Enhance reports
        self.enhance_reports()
        
        # Step 2: Topic modeling
        topics = self.perform_topic_modeling()
        
        # Step 3: Company clustering
        clusters = self.cluster_companies()
        
        # Step 4: Firm style analysis
        firm_styles = self.analyze_firm_styles()
        
        # Step 5: Generate insights
        holistic_insights = self.generate_holistic_insights()
        
        # Compile complete results
        results = {
            'holistic_insights': holistic_insights,
            'topic_analysis': topics,
            'company_clusters': clusters,
            'firm_styles': firm_styles,
            'enhanced_reports': self.enhanced_reports
        }
        
        print("Complete analysis finished!")
        return results

# Example usage and visualization functions
def create_visualizations(analyzer: ResearchReportAnalyzer, results: Dict):
    """Create comprehensive visualizations"""
    
    # 1. Sentiment Distribution
    sentiments = [r.sentiment_score for r in analyzer.enhanced_reports]
    plt.figure(figsize=(10, 6))
    plt.hist(sentiments, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('Distribution of Report Sentiments')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Number of Reports')
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.7)
    plt.savefig('sentiment_distribution.png')
    plt.close()
    
    # 2. Company Clusters Visualization
    if analyzer.company_clusters:
        # Use t-SNE for dimensionality reduction
        tsne = TSNE(n_components=2, random_state=42)
        features_scaled = StandardScaler().fit_transform([
            [analyzer.company_clusters['profiles'][company]['avg_sentiment'],
             analyzer.company_clusters['profiles'][company]['criticism_count'],
             analyzer.company_clusters['profiles'][company]['report_count']]
            for company in analyzer.company_clusters['companies']
        ])
        
        features_2d = tsne.fit_transform(features_scaled)
        
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(features_2d[:, 0], features_2d[:, 1], 
                            c=analyzer.company_clusters['cluster_labels'], 
                            cmap='viridis', alpha=0.7)
        plt.title('Company Clusters (t-SNE Visualization)')
        plt.xlabel('t-SNE Component 1')
        plt.ylabel('t-SNE Component 2')
        plt.colorbar(scatter)
        plt.savefig('company_clusters.png')
        plt.close()
    
    # 3. Firm Sentiment Comparison
    firm_sentiments = []
    firm_names = []
    for firm, profile in analyzer.firm_style_profiles.items():
        if profile['report_count'] >= 5:  # Only firms with sufficient reports
            firm_sentiments.append(profile['avg_sentiment'])
            firm_names.append(firm)
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(firm_names)), firm_sentiments, 
                   color=['red' if s < 0 else 'green' for s in firm_sentiments])
    plt.title('Average Sentiment by Research Firm')
    plt.xlabel('Research Firms')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(range(len(firm_names)), firm_names, rotation=45, ha='right')
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.tight_layout()
    plt.savefig('firm_sentiment_comparison.png')
    plt.close()
    
    # 4. Temporal Trends
    if results['holistic_insights']['temporal_trends']:
        months = list(results['holistic_insights']['temporal_trends'].keys())
        sentiments = list(results['holistic_insights']['temporal_trends'].values())
        
        plt.figure(figsize=(12, 6))
        plt.plot(months, sentiments, marker='o', linewidth=2, markersize=6)
        plt.title('Sentiment Trends Over Time')
        plt.xlabel('Month')
        plt.ylabel('Average Sentiment Score')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('temporal_trends.png')
        plt.close()

def save_analysis_results(results: Dict, filename: str = 'analysis_results.json'):
    """Save analysis results to JSON file"""
    # Convert dataclass objects to dictionaries
    def convert_to_serializable(obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    # Recursively convert all objects
    def recursive_convert(obj):
        if isinstance(obj, dict):
            return {k: recursive_convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [recursive_convert(item) for item in obj]
        else:
            return convert_to_serializable(obj)
    
    serializable_results = recursive_convert(results)
    
    with open(filename, 'w') as f:
        json.dump(serializable_results, f, indent=2, default=str)
    
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    # Example usage
    print("Research Report Analysis Framework")
    print("=" * 50)
    
    # Load your data here
    # reports_data = load_your_reports_data()
    
    # Initialize analyzer
    # analyzer = ResearchReportAnalyzer(reports_data)
    
    # Run complete analysis
    # results = analyzer.run_complete_analysis()
    
    # Create visualizations
    # create_visualizations(analyzer, results)
    
    # Save results
    # save_analysis_results(results)
    
    print("Framework ready for use!") 