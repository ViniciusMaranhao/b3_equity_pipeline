import duckdb
import pandas as pd
from pathlib import Path
from config.directory_settings import reports_directory

def bronze_meta_data_eda(folder_path: Path):
        reports_dir = reports_directory
        topic_name = folder_path.name

        for subtopic_folder in folder_path.iterdir():
            if not subtopic_folder.is_dir():
                 continue
            subtopic_name = subtopic_folder.name
            
            file_path = Path(f"{subtopic_folder}/*.parquet")    
            
            subtopic_db = duckdb.read_parquet(file_path,
                                            union_by_name=True)
            duckdb.register('subtopic db', subtopic_db)

            # 2. Total Rows & Columns Count
            total_rows = duckdb.sql("SELECT COUNT(*) FROM subtopic_db").fetchone()[0]
            schema_df = duckdb.sql("DESCRIBE subtopic_db").df()
            total_columns = len(schema_df)

            # 3. Total Duplicate Rows (Out-of-core distinct check)
            total_duplicate_rows = duckdb.sql("""
                SELECT (SELECT COUNT(*) FROM subtopic_db) - (SELECT COUNT(*) FROM (SELECT DISTINCT * FROM subtopic_db))
            """).fetchone()[0]

            # 4. Column-Level Metrics: Nulls & Constants (Table 2 data)
            nulls_and_constants_df = duckdb.sql(f"""
                SELECT 
                    column_name,
                    column_type,
                    CAST((null_percentage / 100.0) * {total_rows} AS BIGINT) AS total_nulls,
                    null_percentage,
                    approx_unique,
                    CASE WHEN approx_unique = 1 THEN TRUE ELSE FALSE END AS is_constant
                FROM (SUMMARIZE subtopic_db)
            """).df()

            # Extract list of columns where all values inside are the same
            constant_columns = nulls_and_constants_df[nulls_and_constants_df['is_constant']]['column_name'].tolist()

            # 5. First 5 Distinct Values in a Wide Format (Table 3 data)
            # Columns = dataset columns, Rows = first 5 distinct values (padded with None if fewer exist)
            columns = schema_df['column_name'].tolist()
            n_distinct = 5
            distinct_wide_data = {}

            for col in columns:
                safe_col = f'"{col}"'
                res = duckdb.sql(f"""
                    SELECT LIST(DISTINCT {safe_col}) 
                    FROM (SELECT {safe_col} FROM subtopic_db WHERE {safe_col} IS NOT NULL LIMIT 1000)
                """).fetchone()[0]
                
                top_values = res[:n_distinct] if res else []
                # Pad list with None so all columns have exactly 5 elements for the DataFrame
                while len(top_values) < n_distinct:
                    top_values.append(None)
                
                distinct_wide_data[col] = top_values

            # Create wide DataFrame where headers are dataset columns and rows are the first 5 values
            distinct_values_wide_df = pd.DataFrame(distinct_wide_data)
            distinct_values_wide_df.index = [f"Distinct Value {i+1}" for i in range(n_distinct)]

            # --- HTML CONVERSION ---
            html_schema = schema_df.to_html(classes='table', index=False)
            html_metrics = nulls_and_constants_df.to_html(classes='table', index=False)
            html_distinct_wide = distinct_values_wide_df.to_html(classes='table', index=True)

            html_report = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Optimized Dataset Exploration Report</title>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; color: #333; }}
                    h1, h2 {{ color: #2c3e50; }}
                    .metrics-box {{ background: #f8f9fa; padding: 20px; border-radius: 6px; margin-bottom: 25px; border-left: 4px solid #3498db; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
                    .metrics-box p {{ margin: 8px 0; }}
                    .table-container {{ overflow-x: auto; margin-bottom: 35px; }}
                    table {{ border-collapse: collapse; width: 100%; font-size: 13px; white-space: nowrap; }}
                    th, td {{ border: 1px solid #e0e0e0; padding: 10px; text-align: left; }}
                    th {{ background-color: #f1f5f8; font-weight: 600; }}
                    tr:nth-child(even) {{ background-color: #fafbfc; }}
                </style>
            </head>
            <body>
                <h1>Dataset Exploration Report</h1>
                
                <div class="metrics-box">
                    <p><strong>Total Rows:</strong> {total_rows:,}</p>
                    <p><strong>Total Columns:</strong> {total_columns:,}</p>
                    <p><strong>Total Duplicate Rows:</strong> {total_duplicate_rows:,}</p>
                    <p><strong>Columns Where All Values Are The Same:</strong> {constant_columns if constant_columns else "None"}</p>
                </div>

                <h2>1. Dataset Schema (Names & Data Types)</h2>
                <div class="table-container">{html_schema}</div>

                <h2>2. Column-Level Intelligence (Nulls & Uniqueness)</h2>
                <div class="table-container">{html_metrics}</div>

                <h2>3. First 5 Distinct Values per Column</h2>
                <div class="table-container">{html_distinct_wide}</div>

            </body>
            </html>
            """

            # Save the variables into an actual HTML file
            report_path = Path(f"{reports_dir}/bronze_reports/{topic_name}_reports")
            report_path.mkdir(parents=True, exist_ok=True)

            with open(f"{report_path}/{subtopic_name}_report.html", "w", encoding="utf-8") as f:
                f.write(html_report)