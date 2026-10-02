from config.directory_settings import set_directories
from src.extract.web_scraper import web_scraper

if __name__ == "__main__":
    web_scraper_link = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/"

    set_directories()
    web_scraper(web_scraper_link)
