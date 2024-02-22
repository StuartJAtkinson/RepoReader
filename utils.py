import re
import os
import requests
import zipfile
from io import BytesIO
import nltk

def download_and_extract_punkt(root_directory):
    punkt_url = "https://github.com/nltk/nltk_data/raw/gh-pages/packages/tokenizers/punkt.zip"
    response = requests.get(punkt_url)

    # Define the full path to the 'tokenizers' directory
    tokenizer_dir = os.path.join(root_directory, 'tokenizers')

    # Ensure the 'tokenizers' directory exists
    if not os.path.exists(tokenizer_dir):
        os.makedirs(tokenizer_dir)

    if response.status_code == 200:
        # Extract the zip file directly into the 'tokenizers' directory
        with zipfile.ZipFile(BytesIO(response.content)) as punkt_zip:
            punkt_zip.extractall(tokenizer_dir)
        print("Successfully downloaded and extracted 'punkt' to the tokenizer directory.")
    else:
        print(f"Failed to download 'punkt'. HTTP status code: {response.status_code}")

# Specify the root directory where 'tokenizers' should reside
# This should be adjusted to your specific project structure
root_directory = os.path.dirname(__file__)  # Adjust this path as needed

# Download and extract the 'punkt' dataset to the specified directory
download_and_extract_punkt(root_directory)

# Ensure nltk is pointed to use the custom tokenizer directory
nltk.data.path.append(root_directory)

def clean_and_tokenize(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\b(?:http|ftp)s?://\S+', '', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    return nltk.word_tokenize(text)

def format_documents(documents):
    numbered_docs = "\n".join([f"{i+1}. {os.path.basename(doc.metadata['source'])}: {doc.page_content}" for i, doc in enumerate(documents)])
    return numbered_docs

def format_user_question(question):
    question = re.sub(r'\s+', ' ', question).strip()
    return question