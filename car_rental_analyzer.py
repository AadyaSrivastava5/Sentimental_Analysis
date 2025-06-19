import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import json
import os

class CarRentalFeedbackAnalyzer:
    def __init__(self):
        self.df = None
        self.sentiment_results = None
        self.feature_extraction_results = None
        
        # Define key features/categories to extract
        self.feature_categories = {
            'car_condition': ['clean', 'dirty', 'damaged', 'scratch', 'dent', 'interior', 'exterior', 'maintenance'],
            'delivery_pickup': ['late', 'on time', 'early', 'delivery', 'pickup', 'punctual', 'delayed'],
            'staff_service': ['staff', 'employee', 'service', 'helpful', 'rude', 'friendly', 'professional', 'courteous'],
            'pricing': ['price', 'cost', 'expensive', 'cheap', 'affordable', 'value', 'money', 'fee'],
            'booking_process': ['booking', 'reservation', 'website', 'app', 'easy', 'difficult', 'confusing'],
            'car_performance': ['engine', 'brake', 'air conditioning', 'radio', 'gps', 'fuel', 'performance']
        }
    
    def load_data(self, file_path):
        """Load customer feedback data from CSV file"""
        try:
            self.df = pd.read_csv(file_path)
            self.df['review_date'] = pd.to_datetime(self.df['review_date'])
            return True
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return False
    
    def preprocess_text(self, text):
        """Clean and preprocess text data"""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def analyze_sentiment(self):
        """Perform sentiment analysis on customer reviews"""
        if self.df is None:
            return None
        
        sentiments = []
        polarities = []
        subjectivities = []
        
        for review in self.df['review_text']:
            blob = TextBlob(str(review))
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment = 'Positive'
            elif polarity < -0.1:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
            
            sentiments.append(sentiment)
            polarities.append(polarity)
            subjectivities.append(subjectivity)
        
        self.df['sentiment'] = sentiments
        self.df['polarity'] = polarities
        self.df['subjectivity'] = subjectivities
        
        # Calculate sentiment statistics
        self.sentiment_results = {
            'positive_count': len([s for s in sentiments if s == 'Positive']),
            'negative_count': len([s for s in sentiments if s == 'Negative']),
            'neutral_count': len([s for s in sentiments if s == 'Neutral']),
            'avg_polarity': np.mean(polarities),
            'avg_subjectivity': np.mean(subjectivities)
        }
        
        return self.sentiment_results
    
    def extract_features(self):
        """Extract key features and issues from reviews"""
        if self.df is None:
            return None
        
        feature_mentions = {category: [] for category in self.feature_categories}
        
        for idx, review in enumerate(self.df['review_text']):
            processed_review = self.preprocess_text(review)
            
            for category, keywords in self.feature_categories.items():
                mentions = []
                for keyword in keywords:
                    if keyword in processed_review:
                        mentions.append(keyword)
                
                feature_mentions[category].append(mentions)
        
        # Add feature mentions to dataframe
        for category in self.feature_categories:
            self.df[f'{category}_mentions'] = feature_mentions[category]
            self.df[f'{category}_count'] = [len(mentions) for mentions in feature_mentions[category]]
        
        # Calculate feature statistics
        self.feature_extraction_results = {}
        for category in self.feature_categories:
            total_mentions = sum(self.df[f'{category}_count'])
            avg_mentions = np.mean(self.df[f'{category}_count'])
            
            self.feature_extraction_results[category] = {
                'total_mentions': total_mentions,
                'avg_mentions_per_review': avg_mentions,
                'reviews_mentioning': len([count for count in self.df[f'{category}_count'] if count > 0])
            }
        
        return self.feature_extraction_results
    
    def identify_common_issues(self, top_n=10):
        """Identify most common issues from negative reviews"""
        if self.df is None:
            return None
        
        negative_reviews = self.df[self.df['sentiment'] == 'Negative']
        
        # Extract common words/phrases from negative reviews
        all_negative_text = ' '.join(negative_reviews['review_text'].astype(str))
        processed_text = self.preprocess_text(all_negative_text)
        
        # Split into words and count frequency
        words = processed_text.split()
        
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'were', 'are', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'this', 'that', 'these', 'those'}
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequency
        word_counts = Counter(filtered_words)
        
        return word_counts.most_common(top_n)
    
    def generate_performance_summary(self):
        """Generate comprehensive performance summary"""
        if self.df is None or self.sentiment_results is None:
            return None
        
        total_reviews = len(self.df)
        
        # Calculate ratings statistics
        avg_rating = self.df['rating'].mean()
        rating_distribution = self.df['rating'].value_counts().sort_index()
        
        # Calculate sentiment percentages
        positive_pct = (self.sentiment_results['positive_count'] / total_reviews) * 100
        negative_pct = (self.sentiment_results['negative_count'] / total_reviews) * 100
        neutral_pct = (self.sentiment_results['neutral_count'] / total_reviews) * 100
        
        # Identify top issues
        common_issues = self.identify_common_issues()
        
        # Feature analysis
        most_mentioned_features = {}
        for category, stats in self.feature_extraction_results.items():
            most_mentioned_features[category] = stats['total_mentions']
        
        # Sort features by mention count
        sorted_features = sorted(most_mentioned_features.items(), key=lambda x: x[1], reverse=True)
        
        summary = {
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2),
            'rating_distribution': rating_distribution.to_dict(),
            'sentiment_distribution': {
                'positive': f"{positive_pct:.1f}%",
                'negative': f"{negative_pct:.1f}%",
                'neutral': f"{neutral_pct:.1f}%"
            },
            'average_polarity': round(self.sentiment_results['avg_polarity'], 3),
            'top_issues': common_issues[:5] if common_issues else [],
            'most_mentioned_features': sorted_features[:5],
            'feature_analysis': self.feature_extraction_results
        }
        
        return summary
    
    def create_visualizations(self):
        """Create various visualizations for the analysis"""
        if self.df is None:
            return None
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Sentiment Distribution', 'Rating Distribution', 
                          'Feature Mentions', 'Sentiment vs Rating'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # 1. Sentiment Distribution (Pie Chart)
        sentiment_counts = self.df['sentiment'].value_counts()
        fig.add_trace(
            go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values, name="Sentiment"),
            row=1, col=1
        )
        
        # 2. Rating Distribution (Bar Chart)
        rating_counts = self.df['rating'].value_counts().sort_index()
        fig.add_trace(
            go.Bar(x=rating_counts.index, y=rating_counts.values, name="Rating"),
            row=1, col=2
        )
        
        # 3. Feature Mentions (Bar Chart)
        feature_totals = {}
        for category in self.feature_categories:
            feature_totals[category] = sum(self.df[f'{category}_count'])
        
        sorted_features = sorted(feature_totals.items(), key=lambda x: x[1], reverse=True)
        feature_names = [item[0].replace('_', ' ').title() for item in sorted_features]
        feature_values = [item[1] for item in sorted_features]
        
        fig.add_trace(
            go.Bar(x=feature_names, y=feature_values, name="Features"),
            row=2, col=1
        )
        
        # 4. Sentiment vs Rating (Scatter Plot)
        fig.add_trace(
            go.Scatter(
                x=self.df['rating'], 
                y=self.df['polarity'],
                mode='markers',
                text=self.df['sentiment'],
                name="Sentiment vs Rating"
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(height=800, showlegend=False, title_text="Car Rental Service Analysis Dashboard")
        
        return fig
    
    def save_report(self, filename="car_rental_analysis_report.json"):
        """Save analysis results to JSON file"""
        if self.df is None:
            return False
        
        summary = self.generate_performance_summary()
        
        # Convert numpy types to native Python types for JSON serialization
        def convert_numpy_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # Clean summary for JSON serialization
        json_summary = json.loads(json.dumps(summary, default=convert_numpy_types))
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'summary': json_summary,
            'detailed_results': {
                'sentiment_analysis': self.sentiment_results,
                'feature_extraction': self.feature_extraction_results
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=convert_numpy_types)
            return True
        except Exception as e:
            st.error(f"Error saving report: {str(e)}")
            return False

def main():
    st.set_page_config(page_title="Car Rental Feedback Analyzer", layout="wide")
    
    st.title("🚗 Car Rental Customer Feedback Analyzer")
    st.markdown("Analyze customer reviews to identify sentiment, key issues, and generate performance insights.")
    
    # Initialize analyzer
    analyzer = CarRentalFeedbackAnalyzer()
    
    # Sidebar for file upload
    st.sidebar.header("Data Upload")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file with customer reviews", type="csv")
    
    # Sample data option
    if st.sidebar.button("Use Sample Data"):
        if os.path.exists("sample_car_rental_reviews.csv"):
            analyzer.load_data("sample_car_rental_reviews.csv")
            st.sidebar.success("Sample data loaded successfully!")
        else:
            st.sidebar.error("Sample data file not found. Please upload your own data.")
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_reviews.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if analyzer.load_data("temp_reviews.csv"):
            st.sidebar.success("Data loaded successfully!")
        
        # Clean up temporary file
        if os.path.exists("temp_reviews.csv"):
            os.remove("temp_reviews.csv")
    
    # Main analysis section
    if analyzer.df is not None:
        st.header("📊 Analysis Results")
        
        # Display basic data info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Reviews", len(analyzer.df))
        with col2:
            st.metric("Average Rating", f"{analyzer.df['rating'].mean():.2f}")
        with col3:
            st.metric("Date Range", f"{analyzer.df['review_date'].min().strftime('%Y-%m-%d')} to {analyzer.df['review_date'].max().strftime('%Y-%m-%d')}")
        with col4:
            st.metric("Unique Customers", analyzer.df['customer_id'].nunique())
        
        # Perform analysis
        with st.spinner("Analyzing sentiment..."):
            sentiment_results = analyzer.analyze_sentiment()
        
        with st.spinner("Extracting features..."):
            feature_results = analyzer.extract_features()
        
        # Display results
        if sentiment_results and feature_results:
            # Sentiment Analysis Results
            st.subheader("😊 Sentiment Analysis")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Positive Reviews", sentiment_results['positive_count'], 
                         f"{(sentiment_results['positive_count']/len(analyzer.df)*100):.1f}%")
            with col2:
                st.metric("Negative Reviews", sentiment_results['negative_count'],
                         f"{(sentiment_results['negative_count']/len(analyzer.df)*100):.1f}%")
            with col3:
                st.metric("Neutral Reviews", sentiment_results['neutral_count'],
                         f"{(sentiment_results['neutral_count']/len(analyzer.df)*100):.1f}%")
            
            # Visualizations
            st.subheader("📈 Visualizations")
            fig = analyzer.create_visualizations()
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Performance Summary
            st.subheader("📋 Performance Summary")
            summary = analyzer.generate_performance_summary()
            
            if summary:
                # Display summary in expandable sections
                with st.expander("📊 Overall Performance Metrics"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Total Reviews:** {summary['total_reviews']}")
                        st.write(f"**Average Rating:** {summary['average_rating']}/5")
                        st.write(f"**Average Polarity:** {summary['average_polarity']}")
                    with col2:
                        st.write("**Sentiment Distribution:**")
                        for sentiment, percentage in summary['sentiment_distribution'].items():
                            st.write(f"- {sentiment.title()}: {percentage}")
                
                with st.expander("🔍 Top Issues Identified"):
                    if summary['top_issues']:
                        for i, (issue, count) in enumerate(summary['top_issues'], 1):
                            st.write(f"{i}. **{issue}** (mentioned {count} times)")
                    else:
                        st.write("No specific issues identified.")
                
                with st.expander("🏷️ Feature Analysis"):
                    for feature, count in summary['most_mentioned_features']:
                        st.write(f"**{feature.replace('_', ' ').title()}:** {count} mentions")
                
                # Save report button
                if st.button("💾 Save Analysis Report"):
                    if analyzer.save_report():
                        st.success("Report saved as 'car_rental_analysis_report.json'")
                    else:
                        st.error("Failed to save report")
        
        # Raw data view
        with st.expander("📄 View Raw Data"):
            st.dataframe(analyzer.df)
    
    else:
        st.info("Please upload a CSV file or use sample data to begin analysis.")
        st.markdown("""
        ### Expected CSV Format:
        Your CSV file should contain the following columns:
        - `customer_id`: Unique identifier for each customer
        - `review_text`: The actual review text
        - `rating`: Numerical rating (1-5)
        - `review_date`: Date of the review (YYYY-MM-DD format)
        - `location`: Rental location (optional)
        """)

if __name__ == "__main__":
    main()