#!/usr/bin/env python3
"""
Quick test script to verify the Flask app can start
"""

import os
import sys

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import flask
        import pandas as pd
        import langchain_community
        import langchain_huggingface
        import sentence_transformers
        print("✅ All required packages are available")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_data_file():
    """Test if the data file exists and can be loaded"""
    try:
        import pandas as pd
        
        if not os.path.exists("books_with_simple_categories.csv"):
            print("❌ books_with_simple_categories.csv not found")
            return False
        
        df = pd.read_csv("books_with_simple_categories.csv")
        print(f"✅ Dataset loaded: {len(df)} books found")
        
        # Check required columns
        required_cols = ['isbn13', 'title', 'authors', 'description', 'tagged_description']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
            return False
        
        print("✅ All required columns present")
        return True
        
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return False

def main():
    print("🧪 Testing Semantic Book Recommender Setup...")
    print()
    
    # Test imports
    if not test_imports():
        return False
    
    # Test data file
    if not test_data_file():
        return False
    
    print()
    print("✅ All tests passed! The app should work correctly.")
    print("🚀 Run 'python app.py' or 'python run.py' to start the server")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)