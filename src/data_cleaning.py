import os
import pandas as pd
import numpy as np

DATA_DIR = r"C:\Users\yashp\Downloads"
OUTPUT_TABLES_DIR = r"C:\Users\yashp\.gemini\antigravity\scratch\voltRelay-data-analytics\outputs\tables"
CLEAN_DATA_DIR = r"C:\Users\yashp\.gemini\antigravity\scratch\voltRelay-data-analytics\data"

os.makedirs(OUTPUT_TABLES_DIR, exist_ok=True)
os.makedirs(CLEAN_DATA_DIR, exist_ok=True)

def clean_stations():
    print("--- Cleaning Stations Data ---")
    df = pd.read_csv(os.path.join(DATA_DIR, "stations.csv"))
    raw_count = len(df)
    
    # Exclude Test Stations (STN-TST-*)
    test_mask = df['station_id'].str.startswith('STN-TST')
    test_stations = df[test_mask]['station_id'].tolist()
    
    clean_df = df[~test_mask].copy()
    clean_count = len(clean_df)
    
    print(f"Stations Raw: {raw_count}, Test Stations Excluded: {len(test_stations)} ({test_stations}), Clean: {clean_count}")
    clean_df.to_csv(os.path.join(CLEAN_DATA_DIR, "clean_stations.csv"), index=False)
    return clean_df, test_stations

def clean_riders():
    print("--- Cleaning Riders Data ---")
    df = pd.read_csv(os.path.join(DATA_DIR, "riders.csv"))
    
    # Strip whitespace from home_city
    df['home_city_raw'] = df['home_city'].astype(str).str.strip()
    
    # City Standardization Mapping
    city_map = {
        'Blr': 'Bengaluru',
        'BLR': 'Bengaluru',
        'Bangalore': 'Bengaluru',
        'bengaluru': 'Bengaluru',
        'Delhi': 'Delhi NCR',
        'NCR': 'Delhi NCR',
        'New Delhi': 'Delhi NCR',
        'Gurgaon': 'Delhi NCR',
        'Hyd': 'Hyderabad',
        'HYD': 'Hyderabad',
        'hyderabad': 'Hyderabad',
        'PUN': 'Pune',
        'Puuune': 'Pune',
        'pune': 'Pune',
        'Bombay': 'Mumbai',
        'MUM': 'Mumbai',
        'JAI': 'Jaipur',
        'jaipur': 'Jaipur'
    }
    
    before_counts = df['home_city_raw'].value_counts(dropna=False).to_dict()
    df['home_city_clean'] = df['home_city_raw'].replace(city_map)
    after_counts = df['home_city_clean'].value_counts(dropna=False).to_dict()
    
    # Save mapping documentation
    mapping_doc = []
    for orig, cnt in before_counts.items():
        mapped = city_map.get(orig, orig)
        mapping_doc.append({
            "Original City": str(orig),
            "Count Before": cnt,
            "Standardized City": mapped
        })
    mapping_df = pd.DataFrame(mapping_doc)
    mapping_df.to_csv(os.path.join(OUTPUT_TABLES_DIR, "city_name_standardization.csv"), index=False)
    print("City Mapping Summary:")
    print(mapping_df.to_string(index=False))
    
    df.to_csv(os.path.join(CLEAN_DATA_DIR, "clean_riders.csv"), index=False)
    return df

def clean_batteries():
    print("--- Cleaning Batteries Data ---")
    df = pd.read_csv(os.path.join(DATA_DIR, "batteries.csv"))
    df['soh_invalid'] = (df['current_soh_pct'] < 0) | (df['current_soh_pct'] > 100)
    print(f"Batteries Total: {len(df)}, Invalid SOH: {df['soh_invalid'].sum()}")
    df.to_csv(os.path.join(CLEAN_DATA_DIR, "clean_batteries.csv"), index=False)
    return df

def clean_fleet_partners():
    print("--- Cleaning Fleet Partners Data ---")
    df = pd.read_csv(os.path.join(DATA_DIR, "fleet_partners.csv"))
    df.to_csv(os.path.join(CLEAN_DATA_DIR, "clean_fleet_partners.csv"), index=False)
    return df

def clean_city_daily_context():
    print("--- Cleaning City Daily Context Data ---")
    df = pd.read_csv(os.path.join(DATA_DIR, "city_daily_context.csv"))
    df.to_csv(os.path.join(CLEAN_DATA_DIR, "clean_city_daily_context.csv"), index=False)
    return df

def clean_support_tickets():
    print("--- Cleaning Support Tickets Data ---")
    df = pd.read_csv(os.path.join(DATA_DIR, "support_tickets.csv"))
    csat_missing_pct = round(df['csat_score'].isnull().sum() / len(df) * 100, 2)
    print(f"Support Tickets Total: {len(df)}, CSAT Missing: {csat_missing_pct}%")
    df.to_csv(os.path.join(CLEAN_DATA_DIR, "clean_support_tickets.csv"), index=False)
    return df

def clean_station_hourly_status():
    print("--- Cleaning Station Hourly Status Data ---")
    filepath = os.path.join(DATA_DIR, "station_hourly_status.csv")
    df = pd.read_csv(filepath)
    total_rows = len(df)
    missing_telemetry_count = df['telemetry_status'].value_counts(dropna=False).to_dict()
    print(f"Station Hourly Status Rows: {total_rows:,}")
    print("Telemetry Status Breakdown:", missing_telemetry_count)
    df.to_csv(os.path.join(CLEAN_DATA_DIR, "clean_station_hourly_status.csv"), index=False)
    return df

def clean_swap_events(test_stations):
    print("--- Cleaning Swap Events Data (3.87M rows) ---")
    filepath = os.path.join(DATA_DIR, "swap_events.csv")
    
    chunks = []
    total_raw = 0
    excluded_test_swaps = 0
    dup_count = 0
    fw_adjusted_count = 0
    
    for chunk in pd.read_csv(filepath, chunksize=200000, low_memory=False):
        total_raw += len(chunk)
        
        # Exclude test stations
        test_mask = chunk['station_id'].isin(test_stations)
        excluded_test_swaps += test_mask.sum()
        chunk = chunk[~test_mask].copy()
        
        # Parse timestamp
        chunk['event_ts_raw'] = pd.to_datetime(chunk['event_ts'])
        
        # Firmware v3.2.0 timestamp correction (10 March 2025 to 14 April 2025)
        fw_mask = (chunk['station_firmware'] == 'v3.2.0') & \
                  (chunk['event_ts_raw'] >= '2025-03-10') & \
                  (chunk['event_ts_raw'] <= '2025-04-14 23:59:59')
        
        fw_adjusted_count += fw_mask.sum()
        chunk['event_ts_corrected'] = chunk['event_ts_raw']
        chunk.loc[fw_mask, 'event_ts_corrected'] = chunk.loc[fw_mask, 'event_ts_raw'] + pd.Timedelta(hours=5, minutes=30)
        
        # Invalid km flag
        chunk['km_invalid'] = (chunk['km_since_last_swap'] < 0) | (chunk['km_since_last_swap'] > 500)
        
        # Invalid SOC flag
        chunk['soc_invalid'] = (chunk['soc_in_pct'] < 0) | (chunk['soc_in_pct'] > 100) | \
                              (chunk['soc_out_pct'] < 0) | (chunk['soc_out_pct'] > 100)
        
        # Deduplication flag (offline_batch duplicates within 60s window)
        chunk = chunk.sort_values(['rider_id', 'station_id', 'event_ts_corrected'])
        chunk['time_diff_sec'] = chunk.groupby(['rider_id', 'station_id', 'event_type'])['event_ts_corrected'].diff().dt.total_seconds()
        
        dup_mask = (chunk['sync_mode'] == 'offline_batch') & (chunk['time_diff_sec'] < 60) & (chunk['time_diff_sec'].notnull())
        dup_count += dup_mask.sum()
        chunk['is_duplicate'] = dup_mask
        
        chunks.append(chunk)
        
    df = pd.concat(chunks, ignore_index=True)
    
    cleaning_summary = {
        "Total Raw Swap Events": total_raw,
        "Excluded Test Station Events": excluded_test_swaps,
        "Firmware v3.2.0 Adjusted Events": fw_adjusted_count,
        "Offline Batch Duplicates Identified": dup_count,
        "Invalid KM Events": int(df['km_invalid'].sum()),
        "Invalid SOC Events": int(df['soc_invalid'].sum()),
        "Final Clean Swap Events": len(df[~df['is_duplicate']])
    }
    
    print("\nSwap Events Cleaning Summary:")
    for k, v in cleaning_summary.items():
        print(f"  {k}: {v:,}")
        
    summary_df = pd.DataFrame([cleaning_summary])
    summary_df.to_csv(os.path.join(OUTPUT_TABLES_DIR, "swap_events_cleaning_summary.csv"), index=False)
    
    df_clean = df[~df['is_duplicate']].copy()
    df_clean.to_parquet(os.path.join(CLEAN_DATA_DIR, "clean_swap_events.parquet"), index=False)
    print("Saved clean_swap_events.parquet successfully!")
    return df_clean

if __name__ == "__main__":
    st_clean, test_stns = clean_stations()
    rd_clean = clean_riders()
    bt_clean = clean_batteries()
    fp_clean = clean_fleet_partners()
    cc_clean = clean_city_daily_context()
    tk_clean = clean_support_tickets()
    sh_clean = clean_station_hourly_status()
    sw_clean = clean_swap_events(test_stns)
    print("\nFull Data Cleaning Pipeline Completed Successfully!")
