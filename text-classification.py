"""pip install transformers""" #Install tranformers Library

import numpy as np
import pandas as pd
from transformers import pipeline
from tqdm import tqdm

books=pd.read_csv(r"C:\Users\ABCD\Downloads\Books_cleaned.xls")

books["categories"].value_counts().reset_index()

books["categories"].value_counts().reset_index().query("count > 50")

books[books["categories"]=="Juvenile Fiction"]

category_mapping={
    "Fiction":"Fiction",
    "Juvenile Fiction":"Children's Fiction",
    "Biography & Autobiography ":"Nonfiction",
    "History":"Nonfiction",
    "Philosophy":"Nonfiction",
    "Religion":"Nonfiction",
    "Comics & Graphic Novels":"Fiction",
    "Drama":"Fiction",
    "Juvenile Nonfiction":"Children's Nonfiction",
    "Science":"Nonfiction",
    "Poetry":"Fiction"}

books["simple_categories"]=books["categories"].map(category_mapping)

books[~(books["simple_categories"].isna())]

fiction_categories=["Fiction","NonFiction"]

pipe=pipeline("zero-shot-classification",model="facebook/bart-Large-mnli")

sequence=books.loc[books["simple_categories"]=="Fiction","description"].reset_index(drop=True)[0]

pipe(sequence,fiction_categories)

max_index=np.argmax(pipe(sequence,fiction_categories)["scores"])
max_label=pipe(sequence,fiction_categories)["labels"][max_index]
max_label

def generate_predictions(sequence,categories):
    predictions=pipe(sequence,categories)
    max_label=predictions["labels"][max_index]
    return max_label

# First, extract the filtered data once to avoid repeated filtering
fiction_descriptions = books.loc[books["simple_categories"]=="Fiction","description"].reset_index(drop=True)
nonfiction_descriptions = books.loc[books["simple_categories"]=="NonFiction","description"].reset_index(drop=True)

# Check available counts
print(f"Available Fiction books: {len(fiction_descriptions)}")
print(f"Available NonFiction books: {len(nonfiction_descriptions)}")

# Initialize lists
actual_categories = []
predicted_categories = []

# Process Fiction books (up to 300 or available count)
fiction_count = min(300, len(fiction_descriptions))
print(f"Processing {fiction_count} Fiction books...")

for i in tqdm(range(fiction_count)):
    sequence = fiction_descriptions[i]
    predicted_categories += [generate_predictions(sequence, fiction_categories)]
    actual_categories += ["Fiction"]

# Process NonFiction books (up to 300 or available count)
nonfiction_count = min(300, len(nonfiction_descriptions))
print(f"Processing {nonfiction_count} NonFiction books...")

for i in tqdm(range(nonfiction_count)):
    sequence = nonfiction_descriptions[i]
    predicted_categories += [generate_predictions(sequence, fiction_categories)]  # Changed from fiction_categories!
    actual_categories += ["NonFiction"]

print(f"Total processed: {len(predicted_categories)} books")
print(f"Fiction: {fiction_count}, NonFiction: {nonfiction_count}")


predictions_df=pd.DataFrame({"actual_categories":actual_categories,"predicted_categories":predicted_categories})
predictions_df.head()

predictions_df["correct_predictions"]=(
    np.where(predictions_df["actual_categories"]==predictions_df["predicted_categories"],1,0)
)

predictions_df["correct_predictions"].mean()

isbn=[]
predicted_cat=[]

missing_cats=books.loc[books["simple_categories"].isna(),["isbn13","description"]].reset_index(drop=True)


for i in tqdm(range(0,len(missing_cats))):
    sequence=missing_cats["description"][i]
    predicted_cat+=[generate_predictions(sequence,fiction_categories)]
    isbn+=[missing_cats["isbn13"][i]]

missing_predicted_df=pd.DataFrame({"isbn13":isbn,"predicted_categories":predicted_cat})
missing_predicted_df

books=pd.merge(books,missing_predicted_df,on="isbn13",how="left")
books["simple_categories"]=np.where(books["simple_categories"].isna(),books["predicted_categories"],books["simple_categories"])
books=books.drop(columns=["predicted_categories"])

books.to_csv("books_with_simple_categories.csv",index=False)
