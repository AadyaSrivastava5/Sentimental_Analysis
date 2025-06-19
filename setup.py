#!/usr/bin/env python3
"""
Setup script for Car Rental Customer Feedback Analyzer
This script sets up the environment and generates sample data
"""

import subprocess
import sys
import os
from synthetic_data_generator import SyntheticDataGenerator

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data for TextBlob"""
    print("Downloading NLTK data for TextBlob...")
    try:
        import nltk
        nltk.download('punkt')
        nltk.download('brown')
        print("✅ NLTK data downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False

def generate_sample_data():
    """Generate sample data for testing"""
    print("Generating sample data for testing...")
    try:
        generator = SyntheticDataGenerator()
        df = generator.generate_synthetic_data(num_records=500)
        df = generator.add_realistic_variations(df)
        filename = generator.save_to_csv(df, "sample_car_rental_reviews.csv")
        
        print(f"✅ Sample data generated successfully!")
        print(f"   - {len(df)} reviews created")
        print(f"   - Rating distribution: {dict(df['rating'].value_counts().sort_index())}")
        print(f"   - Saved as: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error generating sample data: {e}")
        return False

def create_project_structure():
    """Create necessary project directories"""
    print("Creating project structure...")
    try:
        directories = ['data', 'reports', 'outputs']
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"   Created directory: {directory}")
        print("✅ Project structure created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating project structure: {e}")
        return False

def main():
    """Main setup function"""
    print("🚗 Car Rental Customer Feedback Analyzer Setup")
    print("=" * 50)
    
    steps = [
        ("Installing Python packages", install_requirements),
        ("Downloading NLTK data", download_nltk_data),
        ("Creating project structure", create_project_structure),
        ("Generating sample data", generate_sample_data)
    ]
    
    success_count = 0
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}...")
        if step_function():
            success_count += 1
        else:
            print(f"⚠️  {step_name} failed, but continuing...")
    
    print(f"\n🎉 Setup completed! ({success_count}/{len(steps)} steps successful)")
    
    if success_count == len(steps):
        print("\n🚀 You can now run the application with:")
        print("   streamlit run car_rental_analyzer.py")
    else:
        print("\n⚠️  Some setup steps failed. Please check the errors above.")
        print("   You may need to install packages manually or check your environment.")
    
    print("\n📖 Additional Information:")
    print("   - Sample data: sample_car_rental_reviews.csv")
    print("   - Main application: car_rental_analyzer.py")
    print("   - Data generator: synthetic_data_generator.py")

if __name__ == "__main__":
    main()