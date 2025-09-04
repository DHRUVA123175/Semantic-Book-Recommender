from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import re
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Global variables for the recommendation system
db_books = None
books_df = None

def initialize_recommendation_system():
    """Initialize the semantic search system"""
    global db_books, books_df
    
    try:
        # Load the books data
        if os.path.exists("books_with_simple_categories.csv"):
            books_df = pd.read_csv("books_with_simple_categories.csv")
        else:
            print("❌ books_with_simple_categories.csv not found!")
            return False
        
        # Create tagged descriptions file if it doesn't exist
        if not os.path.exists("tagged_description.txt"):
            print("📝 Creating tagged_description.txt...")
            books_df["tagged_description"].to_csv("tagged_description.txt",
                                                 sep="\n",
                                                 index=False,
                                                 header=False)
        
        # Load documents and create embeddings
        print("📚 Loading documents...")
        raw_documents = TextLoader("tagged_description.txt", encoding="utf-8").load()
        text_splitter = CharacterTextSplitter(chunk_size=1, chunk_overlap=0, separator="\n")
        documents = text_splitter.split_documents(raw_documents)
        
        # Initialize embeddings
        print("🧠 Initializing embeddings (this may take a moment)...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Create vector database
        print("🔍 Creating vector database...")
        db_books = Chroma.from_documents(documents, embedding=embeddings)
        
        print("✅ Recommendation system initialized successfully!")
        print(f"📊 Loaded {len(books_df)} books for recommendations")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing recommendation system: {str(e)}")
        print("💡 Make sure books_with_simple_categories.csv exists in the current directory")
        return False

def retrieve_semantic_recommendation(query, top_k=5):
    """Get book recommendations based on semantic similarity"""
    try:
        if db_books is None or books_df is None:
            return []
        
        # Get similar documents
        recs = db_books.similarity_search(query, k=top_k * 2)  # Get more to filter
        books_list = []
        
        for rec in recs:
            raw_text = rec.page_content.strip('""').split()[0]
            isbn_digits = ''.join(c for c in raw_text if c.isdigit())
            
            if len(isbn_digits) >= 10:  # Valid ISBN length
                books_list.append(int(isbn_digits))
        
        # Get book details
        recommended_books = books_df[books_df["isbn13"].isin(books_list)].head(top_k)
        
        # Convert to list of dictionaries for JSON response
        recommendations = []
        for _, book in recommended_books.iterrows():
            recommendations.append({
                'title': book['title'],
                'authors': book['authors'],
                'description': book['description'][:300] + "..." if len(str(book['description'])) > 300 else book['description'],
                'thumbnail': book['thumbnail'] if pd.notna(book['thumbnail']) else '/static/default-book.png',
                'rating': float(book['average_rating']) if pd.notna(book['average_rating']) else 0.0,
                'pages': int(book['num_pages']) if pd.notna(book['num_pages']) else 0,
                'year': int(book['published_year']) if pd.notna(book['published_year']) else 0,
                'category': book['simple_categories'] if pd.notna(book['simple_categories']) else 'Unknown'
            })
        
        return recommendations
        
    except Exception as e:
        print(f"Error in recommendation: {str(e)}")
        return []

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend_books():
    """API endpoint for book recommendations"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        num_results = data.get('num_results', 6)
        
        if not query:
            return jsonify({'error': 'Please provide a description or prompt'}), 400
        
        if not db_books or books_df is None:
            return jsonify({'error': 'Recommendation system not initialized. Please wait and try again.'}), 503
        
        # Get recommendations
        recommendations = retrieve_semantic_recommendation(query, top_k=num_results)
        
        if not recommendations:
            return jsonify({'error': 'No recommendations found. Try a different description.'}), 404
        
        return jsonify({
            'success': True,
            'query': query,
            'total_books': len(books_df),
            'recommendations': recommendations
        })
        
    except Exception as e:
        print(f"Error in recommend_books: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'system_ready': db_books is not None and books_df is not None
    })

if __name__ == '__main__':
    print("🚀 Starting Semantic Book Recommender...")
    
    # Initialize the recommendation system
    if initialize_recommendation_system():
        print("🌟 Server ready! Visit http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize. Please check your data files.")