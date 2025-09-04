#DOWNLOAD THESE DEPENDENCIES

"""pip install langchain-community

pip install langchain-openai

pip install -q langchain-openai langchain-chroma langchain-community

pip install sentence-transformers
"""

import pandas as pd
import re
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv()


file_path=r"C:\Users\ABCD\Downloads\Books_cleaned.xls"
books=pd.read_csv(file_path)
books

books["tagged_description"]

books["tagged_description"].to_csv("tagged_description.txt",
                                   sep="\n",
                                   index=False,
                                   header=False
                                   )
print(books["tagged_description"])

raw_documents = TextLoader("tagged_description.txt", encoding="utf-8").load()
text_splitter=CharacterTextSplitter(chunk_size=1,chunk_overlap=0,separator="\n")
documents=text_splitter.split_documents(raw_documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
db_books= Chroma.from_documents(documents,embedding=embeddings)

query="A book to teah children about nature"
docs=db_books.similarity_search(query,k=10)
docs


# Extract only digits from the string
isbn_text = docs[0].page_content.split()[0].strip()
isbn_digits = re.findall(r'\d+', isbn_text)[0]  # Get first sequence of digits
isbn_number = int(isbn_digits)

books[books["isbn13"] == isbn_number]


def retreive_semantic_recommendation(query, top_k=5):
    recs = db_books.similarity_search(query, k=top_k)
    books_list = []
    
    for i in range(0, len(recs)):
        
        raw_text = recs[i].page_content.strip('""').split()[0]
        isbn_digits = ''.join(c for c in raw_text if c.isdigit())  # Keep only numbers
        
        if len(isbn_digits) >= 10:  # Valid ISBN length
            books_list.append(int(isbn_digits))
    
    return books[books["isbn13"].isin(books_list)].head(top_k)

retreive_semantic_recommendation("A book to teach children about nature")