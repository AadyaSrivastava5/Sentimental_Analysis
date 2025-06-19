#!/usr/bin/env python3
"""
Simple script to run the Car Rental Customer Feedback Analyzer
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'pandas', 'textblob', 'plotly']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def main():
    print("🚗 Car Rental Customer Feedback Analyzer")
    print("=" * 45)
    
    # Check if main application file exists
    if not os.path.exists('car_rental_analyzer.py'):
        print("❌ Error: car_rental_analyzer.py not found!")
        print("   Please ensure all project files are in the current directory.")
        return
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print("❌ Missing required packages:", ", ".join(missing))
        print("   Please run: python setup.py")
        print("   Or install manually: pip install -r requirements.txt")
        return
    
    print("✅ All dependencies found!")
    
    # Check for sample data
    if not os.path.exists('sample_car_rental_reviews.csv'):
        print("⚠️  Sample data not found. Generating...")
        try:
            from synthetic_data_generator import SyntheticDataGenerator
            generator = SyntheticDataGenerator()
            df = generator.generate_synthetic_data(num_records=500)
            df = generator.add_realistic_variations(df)
            generator.save_to_csv(df, "sample_car_rental_reviews.csv")
            print("✅ Sample data generated!")
        except Exception as e:
            print(f"⚠️  Could not generate sample data: {e}")
    
    # Run the Streamlit application
    print("\n🚀 Starting the application...")
    print("   The app will open in your default web browser")
    print("   URL: http://localhost:8501")
    print("   Press Ctrl+C to stop the application")
    print("-" * 45)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "car_rental_analyzer.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")
        print("   Try running manually: streamlit run car_rental_analyzer.py")

if __name__ == "__main__":
    main()