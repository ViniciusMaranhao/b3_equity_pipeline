from pathlib import Path
from datetime import datetime
import logging as lg

from src.extract.web_scraper import web_scraper
from src.extract.raw_to_bronze import raw_to_bronze

from src.analysis.bronze_meta_data_eda import bronze_meta_data_eda

from config.directory_settings import log_directory
from config.directory_settings import bronze_directory

if __name__ == "__main__":

    log_dir = log_directory
    bronze_dir = bronze_directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = log_dir / f"{timestamp}.log"
    web_scraper_link = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/"
    
    lg.basicConfig(
        filename= file_name,
        level=lg.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        force=True
    )

    web_scraper(web_scraper_link)
    
    raw_to_bronze()
    
    for topic in bronze_directory.iterdir():
        if not topic.is_dir():
            continue
        bronze_meta_data_eda(Path(topic))