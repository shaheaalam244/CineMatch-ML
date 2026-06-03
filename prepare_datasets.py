"""
Dataset Preparation Helper Script
This script helps you prepare and validate your movie datasets
"""

import pandas as pd
import os

def check_dataset(filepath, dataset_name):
    """Check if dataset exists and has required columns"""
    print(f"\n{'='*50}")
    print(f"Checking {dataset_name}...")
    print(f"{'='*50}")
    
    if not os.path.exists(filepath):
        print(f"❌ {filepath} NOT FOUND")
        print(f"   Please add {filepath} to the project folder")
        return False
    
    try:
        df = pd.read_csv(filepath)
        print(f"✅ {filepath} found!")
        print(f"   Total movies: {len(df)}")
        print(f"   Columns: {', '.join(df.columns.tolist())}")
        
        # Check required columns
        required_cols = ['title', 'overview']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"⚠️  Missing required columns: {', '.join(missing_cols)}")
        else:
            print(f"✅ All required columns present")
        
        # Check for missing values
        print(f"\n   Missing values:")
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                print(f"   - {col}: {missing} ({missing/len(df)*100:.1f}%)")
        
        # Show sample data
        print(f"\n   Sample movie:")
        sample = df.iloc[0]
        print(f"   Title: {sample.get('title', 'N/A')}")
        if 'genre' in df.columns:
            print(f"   Genre: {sample.get('genre', 'N/A')}")
        if 'vote_average' in df.columns:
            print(f"   Rating: {sample.get('vote_average', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading {filepath}: {str(e)}")
        return False


def create_sample_bollywood_dataset():
    """Create a sample Bollywood dataset if not exists"""
    if os.path.exists('bollywood.csv'):
        print("\nbollywood.csv already exists. Skipping creation.")
        return
    
    print("\n" + "="*50)
    print("Creating sample Bollywood dataset...")
    print("="*50)
    
    sample_data = {
        'id': [1, 2, 3, 4, 5],
        'title': [
            '3 Idiots',
            'Dangal',
            'PK',
            'Bajrangi Bhaijaan',
            'Taare Zameen Par'
        ],
        'genre': [
            'Comedy,Drama',
            'Biography,Drama,Sport',
            'Comedy,Drama,Sci-Fi',
            'Adventure,Comedy,Drama',
            'Drama,Family'
        ],
        'overview': [
            'Two friends embark on a quest for a lost buddy. On this journey, they encounter a long forgotten bet, a wedding they must crash, and a funeral that goes impossibly out of control.',
            'Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression.',
            'A stranger in the city asks questions no one has asked before. Known only by his initials, P.K., his innocent questions and childlike curiosity will take him on a journey of love and laughter.',
            'A young mute girl from Pakistan loses herself in India with no way to head back. A devoted man with a magnanimous spirit undertakes the task to get her back to her motherland.',
            'An eight-year-old boy is thought to be lazy and a troublemaker, until the new art teacher has the patience to discover the real problem behind his struggles in school.'
        ],
        'popularity': [85.5, 92.3, 78.4, 81.2, 73.8],
        'vote_average': [8.0, 8.4, 8.1, 7.9, 8.3],
        'vote_count': [5234, 6789, 4567, 3456, 4123],
        'release_date': ['2009-12-25', '2016-12-23', '2014-12-19', '2015-07-17', '2007-12-21']
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('bollywood.csv', index=False)
    print("✅ Sample bollywood.csv created with 5 movies!")
    print("   You can replace this with a real Bollywood dataset later.")


def create_sample_webseries_dataset():
    """Create a sample Web Series dataset if not exists"""
    if os.path.exists('webseries.csv'):
        print("\nwebseries.csv already exists. Skipping creation.")
        return
    
    print("\n" + "="*50)
    print("Creating sample Web Series dataset...")
    print("="*50)
    
    sample_data = {
        'id': [1, 2, 3, 4, 5],
        'title': [
            'Breaking Bad',
            'Game of Thrones',
            'Stranger Things',
            'The Crown',
            'Money Heist'
        ],
        'genre': [
            'Crime,Drama,Thriller',
            'Action,Adventure,Drama',
            'Drama,Fantasy,Horror',
            'Drama,History',
            'Action,Crime,Mystery'
        ],
        'overview': [
            'A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine in order to secure his family\'s future.',
            'Nine noble families fight for control over the lands of Westeros, while an ancient enemy returns after being dormant for millennia.',
            'When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces and one strange little girl.',
            'Follows the political rivalries and romance of Queen Elizabeth II\'s reign and the events that shaped the second half of the 20th century.',
            'An unusual group of robbers attempt to carry out the most perfect robbery in Spanish history - stealing 2.4 billion euros from the Royal Mint of Spain.'
        ],
        'popularity': [95.8, 98.2, 88.7, 76.4, 92.1],
        'vote_average': [9.5, 9.3, 8.7, 8.6, 8.3],
        'vote_count': [12456, 15678, 9876, 5432, 10234],
        'release_date': ['2008-01-20', '2011-04-17', '2016-07-15', '2016-11-04', '2017-05-02']
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('webseries.csv', index=False)
    print("✅ Sample webseries.csv created with 5 series!")
    print("   You can replace this with a real Web Series dataset later.")


def validate_all_datasets():
    """Validate all datasets"""
    print("\n" + "="*60)
    print("🎬 MOVIE RECOMMENDATION SYSTEM - DATASET CHECKER")
    print("="*60)
    
    datasets = [
        ('dataset.csv', 'Hollywood Movies'),
        ('bollywood.csv', 'Bollywood Movies'),
        ('webseries.csv', 'Web Series')
    ]
    
    results = {}
    for filepath, name in datasets:
        results[name] = check_dataset(filepath, name)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for name, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}: {'Ready' if status else 'Not Ready'}")
    
    if all(results.values()):
        print("\n🎉 All datasets are ready! You can run the app now.")
    elif results['Hollywood Movies']:
        print("\n⚠️  App will work with Hollywood movies only.")
        print("   Add Bollywood and Web Series datasets for full functionality.")
    else:
        print("\n❌ Hollywood dataset (dataset.csv) is required!")
        print("   Please add dataset.csv to continue.")
    
    print("\n" + "="*60)


def main():
    """Main function"""
    print("Movie Recommendation System - Dataset Preparation Tool\n")
    
    # Check if datasets exist
    validate_all_datasets()
    
    # Offer to create sample datasets
    print("\n" + "="*60)
    print("OPTIONAL: Create Sample Datasets")
    print("="*60)
    
    if not os.path.exists('bollywood.csv'):
        response = input("\nCreate sample Bollywood dataset? (y/n): ")
        if response.lower() == 'y':
            create_sample_bollywood_dataset()
    
    if not os.path.exists('webseries.csv'):
        response = input("\nCreate sample Web Series dataset? (y/n): ")
        if response.lower() == 'y':
            create_sample_webseries_dataset()
    
    # Final validation
    if not all([os.path.exists('bollywood.csv'), os.path.exists('webseries.csv')]):
        validate_all_datasets()
    
    print("\n✅ Dataset preparation complete!")
    print("\nNext steps:")
    print("1. Make sure you have TMDB API key in app.py")
    print("2. Run: python app.py")
    print("3. Open: http://127.0.0.1:5000/")


if __name__ == "__main__":
    main()