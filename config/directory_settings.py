from pathlib import Path
# root
project_root = Path(__file__).resolve().parents[1]

# datalake
data_lake_directory = project_root / "data_lake"

raw_directory = data_lake_directory / "raw"
bronze_directory = data_lake_directory / "bronze"
silver_directory = data_lake_directory / "silver"
error_directory = data_lake_directory / "files_error"
temporary_files_directory = data_lake_directory / "temporary_files"
reports_directory = data_lake_directory / "reports"
bronze_eda_directory = reports_directory / "bronze_eda"

# data warehouse
data_warehouse_directory = project_root / "data_warehouse"
gold_directory = data_warehouse_directory / "gold"

#logs
log_directory = project_root / "logs"
