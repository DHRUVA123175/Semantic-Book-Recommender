![Project Thumbnail](Designer.jpeg)
# 📚 Semantic Book Recommender

An interactive web application that recommends books based on semantic similarity using LangChain, Hugging Face transformers, and Flask.

## ✨ Features

- **Semantic Search**: Uses advanced NLP models to understand your book preferences
- **Interactive UI**: Beautiful, responsive web interface with colorful design
- **Smart Recommendations**: Get personalized book suggestions based on your description
- **Rich Book Information**: View book details including ratings, descriptions, and thumbnails
- **Real-time Results**: Fast recommendations powered by vector similarity search

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone or download this project** to your local machine

2. **Ensure you have the required data file**:
   - Make sure `books_with_simple_categories.csv` is in the project directory
   - This file should contain your book dataset with columns: isbn13, title, authors, description, etc.

3. **Run the setup script**:
   ```bash
   python run.py
   ```
   
   This will:
   - Install all required dependencies
   - Initialize the recommendation system
   - Start the Flask web server

4. **Open your browser** and go to: `http://localhost:5000`

### Manual Installation

If you prefer to install manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

## 🎯 How to Use

1. **Open the web application** in your browser
2. **Enter a description** of what kind of book you're looking for in the text area
3. **Click "Find My Perfect Books"** to get recommendations
4. **Browse the results** with book details, ratings, and descriptions

### Example Queries

Try these example prompts:

- "A thrilling mystery set in Victorian London"
- "A heartwarming story about friendship and growing up"
- "A science fiction novel about space exploration"
- "A book to teach children about nature and animals"
- "An inspiring biography of a successful entrepreneur"

## 🛠️ Technical Details

### Architecture

- **Backend**: Flask web framework
- **Frontend**: HTML, CSS, JavaScript with responsive design
- **ML Models**: Hugging Face sentence transformers
- **Vector Database**: ChromaDB for similarity search
- **Text Processing**: LangChain for document processing

### Key Components

- `app.py` - Main Flask application with API endpoints
- `templates/index.html` - Interactive web interface
- `run.py` - Setup and startup script
- `requirements.txt` - Python dependencies

### API Endpoints

- `GET /` - Main web interface
- `POST /api/recommend` - Get book recommendations
- `GET /api/health` - System health check

## 📁 Project Structure

```
semantic-book-recommender/
├── app.py                           # Main Flask application
├── run.py                          # Setup and startup script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── books_with_simple_categories.csv # Book dataset (required)
├── templates/
│   └── index.html                  # Web interface
└── static/                         # Static assets (CSS, JS, images)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for any API keys or configuration:

```env
# Add any environment variables here
# OPENAI_API_KEY=your_key_here (if using OpenAI embeddings)
```

### Customization

- **Modify the UI**: Edit `templates/index.html` for design changes
- **Adjust recommendations**: Modify the `retrieve_semantic_recommendation()` function in `app.py`
- **Change the model**: Update the embedding model in the initialization function

## 🚨 Troubleshooting

### Common Issues

1. **"books_with_simple_categories.csv not found"**
   - Make sure your book dataset file is in the project directory
   - Check that the file has the correct column names

2. **Import errors**
   - Run `pip install -r requirements.txt` to install dependencies
   - Make sure you're using Python 3.8+

3. **Slow initialization**
   - The first startup may take a few minutes to download the ML model
   - Subsequent starts will be faster

4. **No recommendations found**
   - Try different, more descriptive queries
   - Check that your dataset has sufficient book descriptions

### Performance Tips

- The system works best with descriptive, specific queries
- Initial model download may take time but only happens once
- Vector database is created on first run and cached for future use

## 🤝 Contributing

Feel free to contribute by:
- Improving the UI/UX design
- Adding new features (filters, sorting, etc.)
- Optimizing the recommendation algorithm
- Adding more book metadata

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **LangChain** for document processing capabilities
- **Hugging Face** for pre-trained transformer models
- **ChromaDB** for vector similarity search
- **Flask** for the web framework

---

**Happy Reading! 📖✨**
