#!/usr/bin/env python3
"""
Test script to verify the research report analysis setup
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        print("✅ scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ scikit-learn import failed: {e}")
        return False
    
    try:
        import nltk
        print("✅ nltk imported successfully")
    except ImportError as e:
        print(f"❌ nltk import failed: {e}")
        return False
    
    try:
        import spacy
        print("✅ spacy imported successfully")
    except ImportError as e:
        print(f"❌ spacy import failed: {e}")
        return False
    
    try:
        from transformers import pipeline
        print("✅ transformers imported successfully")
    except ImportError as e:
        print(f"❌ transformers import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ matplotlib import failed: {e}")
        return False
    
    try:
        import psycopg2
        print("✅ psycopg2 imported successfully")
    except ImportError as e:
        print(f"❌ psycopg2 import failed: {e}")
        return False
    
    return True

def test_custom_modules():
    """Test that our custom modules can be imported"""
    print("\n🔍 Testing custom modules...")
    
    try:
        from data_loader import ResearchReportDataLoader
        print("✅ data_loader imported successfully")
    except ImportError as e:
        print(f"❌ data_loader import failed: {e}")
        return False
    
    try:
        from ml_analysis_framework import ResearchReportAnalyzer, EnhancedResearchReport
        print("✅ ml_analysis_framework imported successfully")
    except ImportError as e:
        print(f"❌ ml_analysis_framework import failed: {e}")
        return False
    
    return True

def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    
    try:
        from data_loader import ResearchReportDataLoader
        loader = ResearchReportDataLoader()
        
        # Test connection
        connection = loader.get_connection()
        if connection:
            print("✅ Database connection successful")
            connection.close()
            
            # Test statistics
            stats = loader.get_database_statistics()
            if stats:
                print(f"✅ Database statistics retrieved:")
                print(f"   • Total reports: {stats.get('total_reports', 0)}")
                print(f"   • Unique companies: {stats.get('unique_companies', 0)}")
                print(f"   • Unique firms: {stats.get('unique_firms', 0)}")
                return True
            else:
                print("❌ Could not retrieve database statistics")
                return False
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_analysis_framework():
    """Test the analysis framework with sample data"""
    print("\n🔍 Testing analysis framework...")
    
    try:
        from ml_analysis_framework import ResearchReportAnalyzer, EnhancedResearchReport
        
        # Create sample data
        sample_reports = [
            {
                'source': 'test',
                'publication_date': datetime.now().date(),
                'report_title': 'Test Company: Overvalued and Inefficient',
                'link': 'https://example.com',
                'target_company': 'Test Company',
                'short_seller': 'Test Firm',
                'ticker': 'TEST',
                'report_text': 'This company is overvalued and has poor management. Revenue declined by 20% and debt increased significantly.'
            },
            {
                'source': 'test',
                'publication_date': datetime.now().date(),
                'report_title': 'Another Company: Strong Fundamentals',
                'link': 'https://example.com',
                'target_company': 'Another Company',
                'short_seller': 'Test Firm',
                'ticker': 'ANOTHER',
                'report_text': 'This company shows strong growth potential with excellent management and solid financials.'
            }
        ]
        
        # Initialize analyzer
        analyzer = ResearchReportAnalyzer(sample_reports)
        print("✅ Analyzer initialized successfully")
        
        # Test enhancement
        analyzer.enhance_reports()
        print(f"✅ Enhanced {len(analyzer.enhanced_reports)} reports")
        
        # Test individual report analysis
        if analyzer.enhanced_reports:
            sample_report = analyzer.enhanced_reports[0]
            insights = analyzer.generate_individual_report_insights(sample_report)
            print("✅ Individual report analysis successful")
            print(f"   • Sentiment: {insights['sentiment_analysis']['score']:.3f}")
            print(f"   • Criticism count: {insights['criticism_analysis']['criticism_count']}")
        
        # Test holistic insights
        holistic_insights = analyzer.generate_holistic_insights()
        print("✅ Holistic insights generation successful")
        print(f"   • Overall sentiment: {holistic_insights['sentiment_analysis']['overall_sentiment']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis framework test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_nlp_components():
    """Test NLP components"""
    print("\n🔍 Testing NLP components...")
    
    try:
        import nltk
        
        # Test NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            print("✅ NLTK punkt tokenizer available")
        except LookupError:
            print("⚠️  NLTK punkt tokenizer not found - will download automatically")
        
        try:
            nltk.data.find('corpora/stopwords')
            print("✅ NLTK stopwords available")
        except LookupError:
            print("⚠️  NLTK stopwords not found - will download automatically")
        
        try:
            nltk.data.find('corpora/wordnet')
            print("✅ NLTK wordnet available")
        except LookupError:
            print("⚠️  NLTK wordnet not found - will download automatically")
        
        # Test spaCy
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy English model loaded successfully")
        except OSError:
            print("⚠️  spaCy English model not found - run: python -m spacy download en_core_web_sm")
        
        return True
        
    except Exception as e:
        print(f"❌ NLP components test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("RESEARCH REPORT ANALYSIS - SETUP TEST")
    print("=" * 60)
    
    tests = [
        ("Import Tests", test_imports),
        ("Custom Module Tests", test_custom_modules),
        ("Database Connection Test", test_database_connection),
        ("Analysis Framework Test", test_analysis_framework),
        ("NLP Components Test", test_nlp_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready for analysis.")
        print("\nNext steps:")
        print("1. Run: python run_analysis.py")
        print("2. Check the generated visualizations and results")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues before proceeding.")
        
        if not any(name == "Database Connection Test" and result for name, result in results):
            print("\nDatabase connection issues:")
            print("- Check your .env file configuration")
            print("- Ensure PostgreSQL is running")
            print("- Verify database credentials")
        
        if not any(name == "NLP Components Test" and result for name, result in results):
            print("\nNLP setup issues:")
            print("- Run: python -m spacy download en_core_web_sm")
            print("- Install missing packages: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 