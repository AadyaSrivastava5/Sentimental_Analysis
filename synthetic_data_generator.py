import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid

class SyntheticDataGenerator:
    def __init__(self):
        # Sample review templates for different sentiments and categories
        self.positive_reviews = [
            "Excellent service! The car was clean and well-maintained. Staff was very helpful and professional.",
            "Great experience with car rental. The vehicle was delivered on time and in perfect condition.",
            "Outstanding customer service. The booking process was easy and the car exceeded my expectations.",
            "Very satisfied with the rental. Clean car, friendly staff, and reasonable pricing.",
            "Perfect car for my trip. Everything worked smoothly and the pickup was punctual.",
            "Highly recommend this service. The car was spotless and the staff was courteous.",
            "Amazing experience! The car was brand new and the service was exceptional.",
            "Great value for money. The car was clean, comfortable, and fuel efficient.",
            "Professional service from start to finish. The car was well-maintained and reliable.",
            "Excellent customer support. They were helpful throughout the entire rental period."
        ]
        
        self.negative_reviews = [
            "Terrible experience. The car was dirty and had several scratches. Very disappointed.",
            "Poor service quality. The delivery was late and the staff was rude and unprofessional.",
            "The car had mechanical issues and the air conditioning wasn't working properly.",
            "Overpriced and poor quality. The car interior was dirty and smelled bad.",
            "Very frustrating experience. The booking website was confusing and the car was damaged.",
            "Late delivery ruined my plans. The car also had engine problems during the trip.",
            "Worst car rental experience ever. The staff was unhelpful and the car was in poor condition.",
            "The car broke down during my trip. No proper assistance was provided by the company.",
            "Hidden fees and expensive charges. The car was not as described in the booking.",
            "Poor maintenance of vehicles. The car had brake issues and was unsafe to drive."
        ]
        
        self.neutral_reviews = [
            "Average service. The car was okay but nothing special. Could be better.",
            "Standard car rental experience. No major issues but room for improvement.",
            "The car was functional but not exceptional. Service was adequate.",
            "Decent rental service. The car met basic requirements but lacked some features.",
            "Okay experience overall. The car was clean but the service could be more efficient.",
            "Average quality car with standard service. Nothing particularly good or bad.",
            "The rental process was smooth but the car was just average.",
            "Fair service and pricing. The car was in acceptable condition.",
            "Standard car rental experience. Met expectations but didn't exceed them.",
            "The car was reliable but the service was just okay. Nothing outstanding."
        ]
        
        self.locations = [
            "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ",
            "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "San Jose, CA",
            "Austin, TX", "Jacksonville, FL", "Fort Worth, TX", "Columbus, OH", "Charlotte, NC",
            "San Francisco, CA", "Indianapolis, IN", "Seattle, WA", "Denver, CO", "Boston, MA"
        ]
    
    def generate_customer_id(self):
        """Generate a unique customer ID"""
        return f"CUST_{random.randint(10000, 99999)}"
    
    def generate_review_date(self, start_date=None, end_date=None):
        """Generate a random review date within the specified range"""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
        
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)
    
    def generate_review_text_and_rating(self):
        """Generate review text and corresponding rating based on sentiment"""
        # Determine sentiment distribution (70% positive, 20% negative, 10% neutral)
        sentiment_choice = random.uniform(0, 1)
        
        if sentiment_choice <= 0.7:  # Positive
            review_text = random.choice(self.positive_reviews)
            rating = random.choices([4, 5], weights=[0.3, 0.7])[0]
        elif sentiment_choice <= 0.9:  # Negative
            review_text = random.choice(self.negative_reviews)
            rating = random.choices([1, 2], weights=[0.6, 0.4])[0]
        else:  # Neutral
            review_text = random.choice(self.neutral_reviews)
            rating = 3
        
        # Add some variations to make reviews more realistic
        variations = [
            " The booking process was straightforward.",
            " I would consider using this service again.",
            " The location was convenient for pickup.",
            " Overall, it met my transportation needs.",
            " The car was suitable for my requirements.",
            " The pricing was competitive compared to others.",
            " The return process was quick and easy.",
            " I appreciated the clear communication.",
            " The vehicle was appropriate for city driving.",
            " The service met industry standards."
        ]
        
        # 30% chance to add a variation
        if random.random() < 0.3:
            review_text += random.choice(variations)
        
        return review_text, rating
    
    def generate_synthetic_data(self, num_records=500):
        """Generate synthetic car rental review data"""
        data = []
        
        # Generate unique customer IDs (some customers may have multiple reviews)
        customer_ids = [self.generate_customer_id() for _ in range(int(num_records * 0.8))]
        
        for i in range(num_records):
            # Some customers might have multiple reviews
            if random.random() < 0.2 and customer_ids:  # 20% chance of repeat customer
                customer_id = random.choice(customer_ids)
            else:
                customer_id = self.generate_customer_id()
                customer_ids.append(customer_id)
            
            review_text, rating = self.generate_review_text_and_rating()
            review_date = self.generate_review_date()
            location = random.choice(self.locations)
            
            data.append({
                'customer_id': customer_id,
                'review_text': review_text,
                'rating': rating,
                'review_date': review_date.strftime('%Y-%m-%d'),
                'location': location
            })
        
        return pd.DataFrame(data)
    
    def add_realistic_variations(self, df):
        """Add more realistic variations to the synthetic data"""
        # Add some specific issues/compliments
        issue_additions = {
            'car_condition': [
                " The car had a small dent on the side.",
                " The interior was immaculate and well-maintained.",
                " There were some minor scratches but nothing major.",
                " The car was spotless inside and out."
            ],
            'delivery_timing': [
                " The delivery was 15 minutes late.",
                " They arrived exactly on time as promised.",
                " The pickup was delayed by 30 minutes.",
                " Early delivery was a pleasant surprise."
            ],
            'staff_interaction': [
                " The staff member was very knowledgeable.",
                " Customer service could be more responsive.",
                " The representative was friendly and efficient.",
                " Staff training seems to be lacking."
            ],
            'pricing_feedback': [
                " The pricing was transparent with no hidden fees.",
                " A bit expensive but worth the quality.",
                " Great value for the money spent.",
                " Unexpected charges were added at the end."
            ]
        }
        
        # Randomly add specific feedback to some reviews
        for idx, row in df.iterrows():
            if random.random() < 0.3:  # 30% chance to add specific feedback
                category = random.choice(list(issue_additions.keys()))
                addition = random.choice(issue_additions[category])
                df.at[idx, 'review_text'] += addition
        
        return df
    
    def save_to_csv(self, df, filename="sample_car_rental_reviews.csv"):
        """Save the generated data to CSV file"""
        df.to_csv(filename, index=False)
        print(f"Synthetic data saved to {filename}")
        return filename

def main():
    """Generate and save synthetic car rental review data"""
    generator = SyntheticDataGenerator()
    
    # Generate synthetic data
    print("Generating synthetic car rental review data...")
    df = generator.generate_synthetic_data(num_records=500)
    
    # Add realistic variations
    print("Adding realistic variations...")
    df = generator.add_realistic_variations(df)
    
    # Display basic statistics
    print(f"\nGenerated {len(df)} reviews")
    print(f"Rating distribution:")
    print(df['rating'].value_counts().sort_index())
    print(f"\nDate range: {df['review_date'].min()} to {df['review_date'].max()}")
    print(f"Number of unique customers: {df['customer_id'].nunique()}")
    print(f"Number of locations: {df['location'].nunique()}")
    
    # Save to CSV
    filename = generator.save_to_csv(df)
    
    # Display sample data
    print(f"\nSample data:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    synthetic_data = main()