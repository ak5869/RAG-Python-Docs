# fetch_content.py
import requests
from bs4 import BeautifulSoup

def get_text_from_url(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return text

# Example
docs = get_text_from_url("https://docs.python.org/3/tutorial/index.html")
with open("python_docs.txt", "w", encoding="utf-8") as f:
    f.write(docs)
