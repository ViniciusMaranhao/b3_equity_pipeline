import duckdb
import pandas as pd
from pathlib import Path

def bronze_meta_data(folder_path: Path):
    total_datasets = sum(1 for item in folder_path.iterdir() if item.is_dir())
    
    for subfolder in folder_path.iterdir():
        if not subfolder.is_dir():
            continue
        subfolder_name = subfolder.name
        file_path = Path(f"{folder_path}/{subfolder}/*.parquet")    
        
        subfolder_db = duckdb.read_parquet(file_path,
                                           union_by_name=True)
    
    # TODO
    # 1) EACH DATASET INDIVIDUALLY
    
    # how many datasets in total - DONE
    # all column names and data types from each dataset
    # duplicated values
    # what are all columns where all values are the same
    # what are the first n DIFFERENT values from each column (special case for numeric values)
    # columns with NULL (and how much NULL values)

    # 2) COMPARING THE DATASETS
    
    # see if cd_cvm and cnpj_cia also matches among same companies
    # see if all CNPJ_CIA matches among datasets
    # see if there is different DENOM_CIA for the same CNPJ_CIA
    # see if all DT_REF (reference date) matches among datasets 
    # columns of different datasets with same name (and if all values match among them)
    
    # create an html file with this information and load it
        print('')
