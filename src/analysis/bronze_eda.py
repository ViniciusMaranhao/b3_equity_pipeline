from data_profiling import ProfileReport
import duckdb
from pathlib import Path
from config.directory_settings import bronze_eda_directory

def bronze_eda(folder_path: Path):
    bronze_eda_dir = bronze_eda_directory
    bronze_eda_dir.mkdir(parents=True, exist_ok=True)

    df = duckdb.read_parquet(
        f"{folder_path}/*.parquet",
        union_by_name=True
    ).df()

    profiling_file_name = folder_path.name
    profiling_parent_name = f"{folder_path.parent.name}_report"

    profiling_folder_path = Path(f"{bronze_eda_dir}/{profiling_parent_name}")
    profiling_folder_path.mkdir(parents=True, exist_ok=True)

    report = ProfileReport(df,
                           title = f"{profiling_file_name} EDA",
                           explorative=True,
                           minimal=True,
                           correlations= None,
                           interactions=None,
                           progress_bar = False)

    report.to_file(f"{profiling_folder_path}/{profiling_file_name}_profile.html")
     
