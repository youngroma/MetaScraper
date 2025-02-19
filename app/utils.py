import csv
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.models import URL, Metadata

from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)  # Must be a scheme and domain

def process_csv(file_path: str) -> list:
    urls = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                url = row[0].strip()  # Delete any gaps
                if is_valid_url(url):
                    urls.append(url)
                else:
                    print(f"Skipping invalid URL: {url}")
    return urls


def scrape_metadata_from_url(url_obj: URL, db: Session) -> Metadata:
    try:
        response = requests.get(url_obj.url, timeout=5)
        response.raise_for_status()
        print(f"Fetched {url_obj.url} successfully.")
    except requests.RequestException as e:
        print(f"Error fetching {url_obj.url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("title").get_text() if soup.find("title") else None
    description = None
    keywords = None

    if soup.find("meta", attrs={"name": "description"}):
        description = soup.find("meta", attrs={"name": "description"}).get("content")

    if soup.find("meta", attrs={"name": "keywords"}):
        keywords = soup.find("meta", attrs={"name": "keywords"}).get("content")

    print(f"Extracted metadata for {url_obj.url}: Title={title}, Description={description}, Keywords={keywords}")

    metadata = Metadata(url_id=url_obj.id, title=title, description=description, keywords=keywords)
    db.add(metadata)
    db.commit()
    print(f"Metadata saved for {url_obj.url}")

    return metadata


