from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
data_lake_directory = project_root / "data_lake"
data_warehouse_directory = project_root / "data_warehouse"

raw_directory = data_lake_directory / "raw"
bronze_directory = data_lake_directory / "bronze"
silver_directory = data_lake_directory / "silver"
error_directory = data_lake_directory / "files_error"
temporary_files_directory = data_lake_directory / "temporary_files"

log_directory = project_root / "logs"

def set_directories():
    raw_dir = raw_directory
    raw_dir.mkdir(parents=True, exist_ok=True)

    bronze_dir = bronze_directory
    bronze_dir.mkdir(parents=True, exist_ok= True)

    silver_dir = silver_directory
    silver_dir.mkdir(parents=True, exist_ok= True)

    error_dir = error_directory
    error_dir.mkdir(parents=True, exist_ok= True)

    tempo_dir = temporary_files_directory
    tempo_dir.mkdir(parents=True, exist_ok=True)

    log_dir = log_directory
    log_dir.mkdir(parents=True, exist_ok= True)

    warehouse_dir = data_warehouse_directory
    warehouse_dir.mkdir(parents=True, exist_ok=True)

