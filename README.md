🚗 Car Rental Customer Feedback Analyzer
A comprehensive Python application for analyzing customer reviews of car rental services. This tool performs sentiment analysis, feature extraction, and generates automated performance reports to help service teams understand customer feedback and improve their services.

🎯 Features
Sentiment Analysis: Automatically classify reviews as positive, negative, or neutral
Feature Extraction: Identify key topics mentioned in reviews (car condition, delivery, staff service, pricing, etc.)
Performance Reporting: Generate comprehensive summaries with actionable insights
Interactive Dashboard: Web-based interface built with Streamlit
Data Visualization: Rich charts and graphs to visualize trends and patterns
Export Functionality: Save analysis results as JSON reports
Synthetic Data Generation: Built-in sample data generator for testing
📋 Requirements
Python 3.8 or higher
pip (Python package installer)
Internet connection (for initial setup and package downloads)
🚀 Quick Start
Option 1: Automated Setup (Recommended)
Clone or download all project files to a directory
Run the setup script:
bash
python setup.py
Start the application:
bash
streamlit run car_rental_analyzer.py
Option 2: Manual Setup
Install required packages:
bash
pip install -r requirements.txt
Download NLTK data (required for TextBlob):
python
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
Generate sample data:
bash
python synthetic_data_generator.py
Run the application:
bash
streamlit run car_rental_analyzer.py
📁 Project Structure
car-rental-analyzer/
├── car_rental_analyzer.py          # Main application file
├── synthetic_data_generator.py     # Sample data generator
├── setup.py                        # Automated setup script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── sample_car_rental_reviews.csv   # Generated sample data
├── data/                           # Directory for your data files
├── reports/                        # Directory for generated reports
└── outputs/                        # Directory for analysis outputs
💻 Usage
Using the Web Interface
Start the application:
bash
streamlit run car_rental_analyzer.py
Open your browser and navigate to http://localhost:8501
Upload your data or use the sample data provided
View the analysis results including:
Sentiment distribution
Feature analysis
Performance metrics
Interactive visualizations
Data Format
Your CSV file should contain the following columns:

Column	Description	Example
customer_id	Unique customer identifier	CUST_12345
review_text	The actual review content	"Great service, clean car..."
rating	Numerical rating (1-5)	4
review_date	Date of review (YYYY-MM-DD)	2024-01-15
location	Rental location (optional)	"New York, NY"
Sample Data
The project includes a synthetic data generator that creates realistic car rental reviews for testing. Run:

bash
python synthetic_data_generator.py
This generates 500 sample reviews with:

Realistic sentiment distribution (70% positive, 20% negative, 10% neutral)
Various car rental scenarios and issues
Multiple locations and time periods
Diverse customer feedback patterns
📊 Analysis Features
Sentiment Analysis
Polarity scoring (-1 to 1, negative to positive)
Subjectivity scoring (0 to 1, objective to subjective)
Automatic classification into positive, negative, neutral categories
Feature Extraction
The system identifies mentions of key aspects:

Car Condition: cleanliness, damage, maintenance
Delivery/Pickup: timing, punctuality, delays
Staff Service: helpfulness, professionalism, courtesy
Pricing: value, fees, affordability
Booking Process: ease of use, website, reservations
Car Performance: mechanical issues, features, reliability
Reporting
Performance summary with key metrics
Issue identification from negative reviews
Trend analysis over time
Location-based insights
Exportable JSON reports
🛠️ Customization
Adding New Feature Categories
Edit the feature_categories dictionary in CarRentalFeedbackAnalyzer:

python
self.feature_categories = {
    'your_category': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing categories
}
Modifying Sentiment Thresholds
Adjust sentiment classification in the analyze_sentiment method:

python
if polarity > 0.1:          # Positive threshold
    sentiment = 'Positive'
elif polarity < -0.1:       # Negative threshold
    sentiment = 'Negative'
else:
    sentiment = 'Neutral'
Adding New Visualizations
The create_visualizations method can be extended with additional Plotly charts.

📈 Example Analysis Output
json
{
  "total_reviews": 500,
  "average_rating": 3.82,
  "sentiment_distribution": {
    "positive": "68.2%",
    "negative": "21.4%",
    "neutral": "10.4%"
  },
  "top_issues": [
    ["late", 45],
    ["dirty", 38],
    ["damaged", 32]
  ],
  "most_mentioned_features": [
    ["staff_service", 156],
    ["car_condition", 134],
    ["delivery_pickup", 89]
  ]
}
🔧 Troubleshooting
Common Issues
NLTK Data Error:
bash
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
Streamlit Not Found:
bash
pip install streamlit
Module Import Errors:
bash
pip install -r requirements.txt
Port Already in Use:
bash
streamlit run car_rental_analyzer.py --server.port 8502
Performance Optimization
For large datasets (>10,000 reviews):

Consider processing in batches
Use data sampling for initial exploration
Optimize text preprocessing steps
🤝 Contributing
Fork the repository
Create a feature branch
Make your changes
Add tests if applicable
Submit a pull request
📄 License
This project is open source and available under the MIT License.

🆘 Support
If you encounter any issues:

Check the troubleshooting section above
Ensure all dependencies are properly installed
Verify your data format matches the expected structure
Check the console output for specific error messages
🎉 Getting Started Checklist
 Python 3.8+ installed
 All files downloaded to a directory
 Run python setup.py for automated setup
 OR manually install requirements with pip install -r requirements.txt
 Download NLTK data for TextBlob
 Generate sample data with the synthetic data generator
 Run the application with streamlit run car_rental_analyzer.py
 Open browser to http://localhost:8501
 Upload your data or use sample data
 Explore the analysis results and visualizations
Happy Analyzing! 🚗📊

