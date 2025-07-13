#!/usr/bin/env python3
"""
Main script to run comprehensive analysis of research reports
"""

import sys
import os
import json
from datetime import datetime, date
from typing import Dict, List

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_analysis_framework import ResearchReportAnalyzer, create_visualizations, save_analysis_results
from data_loader import ResearchReportDataLoader

def main():
    """Main analysis function"""
    print("=" * 60)
    print("RESEARCH REPORT ANALYSIS SYSTEM")
    print("=" * 60)
    
    # Initialize data loader
    print("\n1. Initializing data loader...")
    loader = ResearchReportDataLoader()
    
    # Get database statistics
    print("\n2. Getting database statistics...")
    stats = loader.get_database_statistics()
    
    if not stats:
        print("❌ Could not connect to database. Please check your .env configuration.")
        return
    
    print("📊 Database Statistics:")
    print(f"   • Total reports: {stats.get('total_reports', 0)}")
    print(f"   • Unique companies: {stats.get('unique_companies', 0)}")
    print(f"   • Unique research firms: {stats.get('unique_firms', 0)}")
    print(f"   • Date range: {stats.get('date_range', {}).get('earliest', 'N/A')} to {stats.get('date_range', {}).get('latest', 'N/A')}")
    
    # Load reports for analysis
    print("\n3. Loading reports for analysis...")
    
    # You can adjust the limit based on your needs
    # For initial testing, start with a smaller number
    sample_size = 500  # Adjust this number
    reports_data = loader.load_reports_with_text(limit=sample_size)
    
    if not reports_data:
        print("❌ No reports loaded. Please check your database connection.")
        return
    
    print(f"✅ Loaded {len(reports_data)} reports for analysis")
    
    # Initialize analyzer
    print("\n4. Initializing analysis framework...")
    analyzer = ResearchReportAnalyzer(reports_data)
    
    # Run complete analysis
    print("\n5. Running comprehensive analysis...")
    print("   This may take several minutes depending on the number of reports...")
    
    try:
        results = analyzer.run_complete_analysis()
        print("✅ Analysis completed successfully!")
        
        # Generate insights summary
        print("\n6. Generating insights summary...")
        generate_insights_summary(results)
        
        # Create visualizations
        print("\n7. Creating visualizations...")
        create_visualizations(analyzer, results)
        print("✅ Visualizations saved as PNG files")
        
        # Save results
        print("\n8. Saving analysis results...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_results_{timestamp}.json"
        save_analysis_results(results, filename)
        print(f"✅ Results saved to {filename}")
        
        # Generate individual reports
        print("\n9. Generating individual analysis examples...")
        generate_individual_examples(analyzer, results)
        
        print("\n" + "=" * 60)
        print("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Analysis failed with error: {e}")
        import traceback
        traceback.print_exc()

def generate_insights_summary(results: Dict):
    """Generate a summary of key insights"""
    print("\n📈 KEY INSIGHTS SUMMARY:")
    print("-" * 40)
    
    holistic = results.get('holistic_insights', {})
    
    # Overall statistics
    stats = holistic.get('overall_statistics', {})
    print(f"📊 Dataset Overview:")
    print(f"   • Total reports analyzed: {stats.get('total_reports', 0)}")
    print(f"   • Companies covered: {stats.get('unique_companies', 0)}")
    print(f"   • Research firms: {stats.get('unique_firms', 0)}")
    
    # Sentiment analysis
    sentiment = holistic.get('sentiment_analysis', {})
    overall_sentiment = sentiment.get('overall_sentiment', 0)
    print(f"\n😐 Overall Sentiment: {overall_sentiment:.3f}")
    
    sentiment_dist = sentiment.get('sentiment_distribution', {})
    print(f"   • Sentiment distribution:")
    for label, count in sentiment_dist.items():
        print(f"     - {label}: {count} reports")
    
    # Most negative reports
    most_negative = sentiment.get('most_negative_reports', [])
    if most_negative:
        print(f"\n⚠️  Most Critical Reports:")
        for i, (title, score) in enumerate(most_negative[:5], 1):
            print(f"   {i}. {title[:60]}... (score: {score:.3f})")
    
    # Common criticism areas
    criticisms = holistic.get('common_criticism_areas', [])
    if criticisms:
        print(f"\n🎯 Top Criticism Areas:")
        for i, (criticism, count) in enumerate(criticisms[:5], 1):
            print(f"   {i}. {criticism[:50]}... ({count} mentions)")
    
    # Financial focus
    financial = holistic.get('financial_focus_areas', {})
    if financial:
        print(f"\n💰 Financial Metrics Focus:")
        sorted_metrics = sorted(financial.items(), key=lambda x: x[1], reverse=True)
        for i, (metric, count) in enumerate(sorted_metrics[:5], 1):
            print(f"   {i}. {metric}: {count} mentions")
    
    # Topic analysis
    topics = results.get('topic_analysis', [])
    if topics:
        print(f"\n📝 Key Topics Identified:")
        for i, topic in enumerate(topics[:5], 1):
            top_words = topic.get('top_words', [])
            print(f"   {i}. {', '.join(top_words[:5])}...")
    
    # Company clusters
    clusters = results.get('company_clusters', {})
    if clusters:
        n_clusters = len(set(clusters.get('cluster_labels', [])))
        print(f"\n🏢 Company Clustering:")
        print(f"   • Companies grouped into {n_clusters} clusters")
        
        # Show cluster characteristics
        cluster_labels = clusters.get('cluster_labels', [])
        companies = clusters.get('companies', [])
        profiles = clusters.get('profiles', {})
        
        if cluster_labels and companies:
            cluster_stats = {}
            for i, label in enumerate(cluster_labels):
                company = companies[i]
                if company in profiles:
                    profile = profiles[company]
                    if label not in cluster_stats:
                        cluster_stats[label] = {
                            'count': 0,
                            'avg_sentiment': 0,
                            'companies': []
                        }
                    cluster_stats[label]['count'] += 1
                    cluster_stats[label]['avg_sentiment'] += profile.get('avg_sentiment', 0)
                    cluster_stats[label]['companies'].append(company)
            
            # Calculate averages
            for label in cluster_stats:
                count = cluster_stats[label]['count']
                cluster_stats[label]['avg_sentiment'] /= count
            
            print(f"   • Cluster characteristics:")
            for label, stats in cluster_stats.items():
                sentiment = stats['avg_sentiment']
                sentiment_desc = "negative" if sentiment < -0.1 else "positive" if sentiment > 0.1 else "neutral"
                print(f"     - Cluster {label}: {stats['count']} companies, {sentiment_desc} sentiment ({sentiment:.3f})")
    
    # Firm styles
    firm_styles = results.get('firm_styles', {})
    if firm_styles:
        print(f"\n🏢 Research Firm Analysis:")
        print(f"   • Analyzed {len(firm_styles)} research firms")
        
        # Show top firms by report count
        sorted_firms = sorted(firm_styles.items(), 
                            key=lambda x: x[1].get('report_count', 0), 
                            reverse=True)
        
        print(f"   • Top firms by report count:")
        for i, (firm, profile) in enumerate(sorted_firms[:5], 1):
            count = profile.get('report_count', 0)
            avg_sentiment = profile.get('avg_sentiment', 0)
            sentiment_desc = "negative" if avg_sentiment < -0.1 else "positive" if avg_sentiment > 0.1 else "neutral"
            print(f"     {i}. {firm}: {count} reports, {sentiment_desc} ({avg_sentiment:.3f})")

def generate_individual_examples(analyzer: ResearchReportAnalyzer, results: Dict):
    """Generate examples of individual report and company analysis"""
    print("\n📋 INDIVIDUAL ANALYSIS EXAMPLES:")
    print("-" * 40)
    
    if not analyzer.enhanced_reports:
        print("No enhanced reports available for individual analysis")
        return
    
    # Example 1: Individual report analysis
    print("\n1. 📄 Individual Report Analysis Example:")
    sample_report = analyzer.enhanced_reports[0]
    report_insights = analyzer.generate_individual_report_insights(sample_report)
    
    print(f"   Report: {report_insights['basic_info']['title']}")
    print(f"   Company: {report_insights['basic_info']['company']}")
    print(f"   Firm: {report_insights['basic_info']['firm']}")
    print(f"   Sentiment: {report_insights['sentiment_analysis']['score']:.3f} ({report_insights['sentiment_analysis']['label']})")
    print(f"   Interpretation: {report_insights['sentiment_analysis']['interpretation']}")
    print(f"   Criticism areas: {report_insights['criticism_analysis']['criticism_count']}")
    print(f"   Writing style: {', '.join(report_insights['writing_style']['style_characteristics'])}")
    
    # Example 2: Company profile
    print("\n2. 🏢 Company Profile Example:")
    companies = list(set(r.target_company for r in analyzer.enhanced_reports))
    if companies:
        sample_company = companies[0]
        company_profile = analyzer.generate_company_profile(sample_company)
        
        if 'error' not in company_profile:
            print(f"   Company: {company_profile['company_name']}")
            print(f"   Total reports: {company_profile['total_reports']}")
            print(f"   Average sentiment: {company_profile['sentiment_trends']['average_sentiment']:.3f}")
            print(f"   Total criticisms: {company_profile['criticism_analysis']['total_criticisms']}")
            print(f"   Research firms covering: {len(company_profile['research_firm_analysis']['firms_covering'])}")
            
            # Show sentiment comparison
            firm_sentiments = company_profile['research_firm_analysis']['firm_sentiment_comparison']
            if firm_sentiments:
                print(f"   Firm sentiment comparison:")
                for firm, sentiment in firm_sentiments.items():
                    sentiment_desc = "negative" if sentiment < -0.1 else "positive" if sentiment > 0.1 else "neutral"
                    print(f"     - {firm}: {sentiment:.3f} ({sentiment_desc})")
    
    # Example 3: Firm style profile
    print("\n3. 🏢 Research Firm Style Example:")
    firm_styles = results.get('firm_styles', {})
    if firm_styles:
        # Get firm with most reports
        top_firm = max(firm_styles.items(), key=lambda x: x[1].get('report_count', 0))
        firm_name, firm_profile = top_firm
        
        firm_style = analyzer.generate_firm_style_profile(firm_name)
        
        if 'error' not in firm_style:
            print(f"   Firm: {firm_style['firm_name']}")
            print(f"   Total reports: {firm_style['total_reports']}")
            print(f"   Average sentiment: {firm_style['sentiment_profile']['average_sentiment']:.3f}")
            print(f"   Sentiment characterization: {firm_style['sentiment_profile']['sentiment_characterization']}")
            print(f"   Writing style:")
            style = firm_style['writing_style']
            print(f"     - Avg sentence length: {style['average_sentence_length']:.1f} words")
            print(f"     - Vocabulary richness: {style['vocabulary_richness']:.3f}")
            print(f"     - Data usage: {style['data_usage']:.1f} numbers per report")
            print(f"     - Emotional tone: {style['emotional_tone']:.1f} exclamations per report")
            
            # Show most covered companies
            most_covered = firm_style['coverage_analysis']['most_covered_companies']
            if most_covered:
                print(f"   Most covered companies:")
                for i, (company, count) in enumerate(most_covered[:3], 1):
                    print(f"     {i}. {company}: {count} reports")

def run_targeted_analysis():
    """Run analysis on specific companies or firms"""
    print("\n🎯 TARGETED ANALYSIS OPTIONS:")
    print("-" * 40)
    
    loader = ResearchReportDataLoader()
    analyzer = None
    
    while True:
        print("\nChoose analysis type:")
        print("1. Analyze specific company")
        print("2. Analyze specific research firm")
        print("3. Analyze date range")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            company_name = input("Enter company name: ").strip()
            if company_name:
                reports = loader.get_reports_by_company(company_name)
                if reports:
                    analyzer = ResearchReportAnalyzer(reports)
                    analyzer.enhance_reports()
                    
                    company_profile = analyzer.generate_company_profile(company_name)
                    print(f"\n📊 Analysis for {company_name}:")
                    print(json.dumps(company_profile, indent=2, default=str))
                else:
                    print(f"No reports found for {company_name}")
        
        elif choice == '2':
            firm_name = input("Enter research firm name: ").strip()
            if firm_name:
                reports = loader.get_reports_by_firm(firm_name)
                if reports:
                    analyzer = ResearchReportAnalyzer(reports)
                    analyzer.enhance_reports()
                    analyzer.analyze_firm_styles()
                    
                    firm_profile = analyzer.generate_firm_style_profile(firm_name)
                    print(f"\n📊 Analysis for {firm_name}:")
                    print(json.dumps(firm_profile, indent=2, default=str))
                else:
                    print(f"No reports found for {firm_name}")
        
        elif choice == '3':
            start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date_str = input("Enter end date (YYYY-MM-DD): ").strip()
            
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                
                reports = loader.get_reports_by_date_range(start_date, end_date)
                if reports:
                    analyzer = ResearchReportAnalyzer(reports)
                    analyzer.enhance_reports()
                    
                    holistic_insights = analyzer.generate_holistic_insights()
                    print(f"\n📊 Analysis for period {start_date} to {end_date}:")
                    print(json.dumps(holistic_insights, indent=2, default=str))
                else:
                    print(f"No reports found for the specified date range")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")
        
        elif choice == '4':
            print("Exiting targeted analysis...")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    # Check if user wants targeted analysis
    print("Choose analysis mode:")
    print("1. Complete analysis (all reports)")
    print("2. Targeted analysis (specific companies/firms)")
    
    mode = input("Enter mode (1 or 2): ").strip()
    
    if mode == '2':
        run_targeted_analysis()
    else:
        main() 