import logging as lg
from config.directory_settings import log_directory
from datetime import datetime

def logging_raw_to_bronze():
    file_path = log_directory / "raw_to_bronze_log"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_name = file_path / f"{timestamp}.log"
    
    lg.basicConfig(
        filename= file_name,
        level=lg.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )