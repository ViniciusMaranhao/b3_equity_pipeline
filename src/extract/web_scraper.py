import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile
from pathlib import Path
from config.directory_settings import raw_directory

def web_scraper(website_url):
    raw_dir = raw_directory
    url = website_url
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.select("pre a"):
        href = link.get("href")

        if ((not href) or (href == "../") or (href == "META/")):
            continue
        
        if href.endswith("/"):
            next_url = urljoin(url, href)
            web_scraper(next_url)
        
        elif href.lower().endswith(".zip"):
            zip_url = urljoin(url, href)
            zip_response = requests.get(zip_url, stream=True)
            zip_response.raise_for_status()
            
            zip_stem = Path(href).stem.replace("cia_aberta_", "")
            zip_dataset = (zip_stem.split("_"))[0]


            zip_file_path = (raw_dir / zip_dataset / zip_stem / Path(href).name)
            zip_folder_path = zip_file_path.parent
            zip_folder_path.mkdir(parents=True, exist_ok=True)

            with open(zip_file_path, "wb") as file:
                for chunk in zip_response.iter_content(chunk_size=1024*1024):
                    file.write(chunk)

            with zipfile.ZipFile(zip_file_path, "r") as zip_file:
                zip_file.extractall(zip_folder_path)
            
            zip_file_path.unlink()
            
