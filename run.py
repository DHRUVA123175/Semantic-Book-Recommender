#!/usr/bin/env python3
"""
Semantic Book Recommender - Startup Script
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required files exist"""
    required_files = [
        "books_with_simple_categories.csv",
        "app.py",
        "templates/index.html"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def install_requirements():
    """Install required packages"""
    try:
        print("📦 Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please install manually:")
        print("   pip install -r requirements.txt")
        return False

def main():
    print("🚀 Starting Semantic Book Recommender Setup...")
    
    # Check if requirements file exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
    
    # Check required files
    if not check_requirements():
        print("\n💡 Make sure you have all the required files in the current directory.")
        return
    
    # Ask user if they want to install requirements
    install_deps = input("\n📦 Install required packages? (y/n): ").lower().strip()
    if install_deps in ['y', 'yes']:
        if not install_requirements():
            return
    
    print("\n🌟 Setup complete! Starting the application...")
    print("🌐 The app will be available at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    # Start the Flask app
    try:
        from app import app, initialize_recommendation_system
        
        if initialize_recommendation_system():
            app.run(debug=True, host='0.0.0.0', port=5000)
        else:
            print("❌ Failed to initialize the recommendation system.")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required packages are installed.")
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()