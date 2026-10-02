import duckdb
from config.directory_settings import raw_directory
from config.directory_settings import bronze_directory
from config.directory_settings import error_directory
from config.directory_settings import temporary_files_directory
from pathlib import Path

def raw_to_bronze():
    raw_dir = raw_directory
    bronze_dir = bronze_directory
    error_dir = error_directory
    tempo_dir = temporary_files_directory

    for dataset_dir in raw_dir.iterdir():
        if not dataset_dir.is_dir():
            continue
        for date_dir in dataset_dir.iterdir():
            if not date_dir.is_dir():
                continue
            for csv_file in date_dir.glob("*.csv"):
                file_name = csv_file.stem.replace("cia_aberta_", "")
                converted_file = tempo_dir / f"{file_name}_utf8.csv"

                with open(csv_file, "r", encoding="latin-1") as source:
                    with open(converted_file, "w", encoding="utf-8") as destination:
                        for line in source:
                            destination.write(line)

                data = duckdb.read_csv(converted_file, delimiter=";")
                print(Path(converted_file).stem)
