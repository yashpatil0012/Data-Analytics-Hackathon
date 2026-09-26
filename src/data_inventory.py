import os
import sys
import pandas as pd
import numpy as np
import json

DATA_DIR = r"C:\Users\yashp\Downloads"
OUTPUT_DIR = r"C:\Users\yashp\.gemini\antigravity\scratch\voltRelay-data-analytics\outputs\tables"

os.makedirs(OUTPUT_DIR, exist_ok=True)

DATASETS = [
    "swap_events.csv",
    "station_hourly_status.csv",
    "support_tickets.csv",
    "riders.csv",
    "batteries.csv",
    "city_daily_context.csv",
    "stations.csv",
    "fleet_partners.csv"
]

def analyze_dataset(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    
    file_size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
    print(f"\nAnalyzing {filename} ({file_size_mb} MB)...")
    
    # For large datasets, sample or process in chunks
    is_large = file_size_mb > 50
    
    if is_large:
        # Read header & sample first 100k rows for types & missingness estimation, count total rows with chunking
        sample_df = pd.read_csv(filepath, nrows=50000)
        col_names = list(sample_df.columns)
        num_cols = len(col_names)
        
        # Count total rows
        total_rows = 0
        missing_counts = pd.Series(0, index=col_names)
        
        for chunk in pd.read_csv(filepath, chunksize=100000, low_memory=False):
            total_rows += len(chunk)
            missing_counts += chunk.isnull().sum()
            
        df_for_stats = sample_df # use sample for unique counts & dtypes
    else:
        df = pd.read_csv(filepath, low_memory=False)
        total_rows = len(df)
        col_names = list(df.columns)
        num_cols = len(col_names)
        missing_counts = df.isnull().sum()
        df_for_stats = df
        
    missing_pct = {col: round((missing_counts[col] / total_rows) * 100, 2) for col in col_names}
    dtypes = {col: str(df_for_stats[col].dtype) for col in col_names}
    unique_counts = {col: df_for_stats[col].nunique() for col in col_names}
    
    # Identify column types
    date_cols = [c for c in col_names if 'date' in c.lower() or 'time' in c.lower() or 'timestamp' in c.lower() or c.endswith('_at')]
    num_cols_list = [c for c in col_names if c not in date_cols and df_for_stats[c].dtype in ['int64', 'float64', 'int32', 'float32']]
    cat_cols_list = [c for c in col_names if c not in date_cols and c not in num_cols_list]
    
    # Primary Key detection
    potential_pk = [c for c in col_names if unique_counts[c] == total_rows or (is_large and unique_counts[c] == len(df_for_stats))]
    
    info = {
        "filename": filename,
        "file_size_mb": file_size_mb,
        "num_rows": total_rows,
        "num_cols": num_cols,
        "col_names": col_names,
        "dtypes": dtypes,
        "missing_pct": missing_pct,
        "unique_counts": unique_counts,
        "potential_pk": potential_pk,
        "date_cols": date_cols,
        "num_cols_list": num_cols_list,
        "cat_cols_list": cat_cols_list
    }
    return info

def run_inventory():
    inventory_data = []
    summary_rows = []
    
    for ds in DATASETS:
        info = analyze_dataset(ds)
        if info:
            inventory_data.append(info)
            summary_rows.append({
                "Filename": info["filename"],
                "Size (MB)": info["file_size_mb"],
                "Rows": info["num_rows"],
                "Cols": info["num_cols"],
                "Primary Key": ", ".join(info["potential_pk"]) if info["potential_pk"] else "None/Composite",
                "Date Cols": ", ".join(info["date_cols"]),
                "Num Cols Count": len(info["num_cols_list"]),
                "Cat Cols Count": len(info["cat_cols_list"]),
                "Max Missing %": f"{max(info['missing_pct'].values())}% ({[k for k,v in info['missing_pct'].items() if v == max(info['missing_pct'].values())][0]})" if info["missing_pct"] else "0%"
            })
            
    summary_df = pd.DataFrame(summary_rows)
    print("\n=== DATASET INVENTORY SUMMARY ===")
    print(summary_df.to_string(index=False))
    
    # Save CSV & Markdown
    summary_df.to_csv(os.path.join(OUTPUT_DIR, "data_inventory.csv"), index=False)
    with open(os.path.join(OUTPUT_DIR, "data_inventory.md"), "w", encoding="utf-8") as f:
        f.write("# VoltRelay Dataset Inventory\n\n")
        f.write(summary_df.to_markdown(index=False))
        f.write("\n\n## Detailed Column Breakdown\n\n")
        for info in inventory_data:
            f.write(f"### {info['filename']}\n")
            f.write(f"- **Rows**: {info['num_rows']:,} | **Cols**: {info['num_cols']}\n")
            col_df = pd.DataFrame({
                "Column": info["col_names"],
                "DataType": [info["dtypes"][c] for c in info["col_names"]],
                "Missing %": [f"{info['missing_pct'][c]}%" for c in info["col_names"]],
                "Unique Values": [info["unique_counts"][c] for c in info["col_names"]]
            })
            f.write(col_df.to_markdown(index=False))
            f.write("\n\n")

if __name__ == "__main__":
    run_inventory()
