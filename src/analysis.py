import os
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import json

CLEAN_DATA_DIR = r"C:\Users\yashp\.gemini\antigravity\scratch\voltRelay-data-analytics\data"
OUTPUT_TABLES_DIR = r"C:\Users\yashp\.gemini\antigravity\scratch\voltRelay-data-analytics\outputs\tables"
os.makedirs(OUTPUT_TABLES_DIR, exist_ok=True)

def load_data():
    print("Loading cleaned datasets for analysis...")
    swaps = pd.read_parquet(os.path.join(CLEAN_DATA_DIR, "clean_swap_events.parquet"))
    stations = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_stations.csv"))
    riders = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_riders.csv"))
    batteries = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_batteries.csv"))
    partners = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_fleet_partners.csv"))
    context = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_city_daily_context.csv"))
    tickets = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_support_tickets.csv"))
    hourly = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_station_hourly_status.csv"))
    
    return swaps, stations, riders, batteries, partners, context, tickets, hourly

def analyze_q1_network_performance(swaps, stations):
    print("\n--- Question 1: Network Performance Analysis ---")
    
    # Merge station metadata
    swaps_merged = swaps.merge(stations[['station_id', 'city', 'grid_tariff_inr_kwh', 'charger_generation', 'expansion_wave']], on='station_id', how='left')
    
    swaps_merged['year_month'] = pd.to_datetime(swaps_merged['event_ts_corrected']).dt.to_period('M').astype(str)
    swaps_merged['is_completed'] = swaps_merged['event_type'] == 'swap_completed'
    swaps_merged['is_failed'] = swaps_merged['event_type'].isin(['failed_no_charged_battery', 'failed_system_error'])
    swaps_merged['is_abandoned'] = swaps_merged['event_type'].isin(['abandoned_queue', 'cancelled_by_rider'])
    
    # Energy cost = energy_to_recharge_kwh * grid_tariff_inr_kwh
    swaps_merged['energy_cost_inr'] = swaps_merged['energy_to_recharge_kwh'].fillna(0) * swaps_merged['grid_tariff_inr_kwh'].fillna(0)
    
    # Monthly aggregation
    monthly = swaps_merged.groupby('year_month').agg(
        total_attempts=('event_id', 'count'),
        completed_swaps=('is_completed', 'sum'),
        failed_swaps=('is_failed', 'sum'),
        abandoned_swaps=('is_abandoned', 'sum'),
        total_revenue_inr=('amount_charged_inr', 'sum'),
        total_energy_kwh=('energy_to_recharge_kwh', 'sum'),
        total_energy_cost_inr=('energy_cost_inr', 'sum')
    ).reset_index()
    
    monthly['failure_rate_pct'] = round((monthly['failed_swaps'] / monthly['total_attempts']) * 100, 2)
    monthly['disruption_rate_pct'] = round(((monthly['failed_swaps'] + monthly['abandoned_swaps']) / monthly['total_attempts']) * 100, 2)
    monthly['rev_per_completed_swap_inr'] = round(monthly['total_revenue_inr'] / monthly['completed_swaps'], 2)
    
    # Contribution Margin Proxy = Revenue - Energy Cost
    monthly['contribution_margin_proxy_inr'] = round(monthly['total_revenue_inr'] - monthly['total_energy_cost_inr'], 2)
    monthly['contribution_margin_proxy_pct'] = round((monthly['contribution_margin_proxy_inr'] / monthly['total_revenue_inr']) * 100, 2)
    
    monthly.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q1_monthly_network_performance.csv"), index=False)
    print("Monthly Network Performance Summary:")
    print(monthly[['year_month', 'total_attempts', 'completed_swaps', 'failure_rate_pct', 'total_revenue_inr', 'rev_per_completed_swap_inr', 'contribution_margin_proxy_pct']].to_string(index=False))
    
    # City monthly breakdown
    city_monthly = swaps_merged.groupby(['city', 'year_month']).agg(
        total_attempts=('event_id', 'count'),
        completed_swaps=('is_completed', 'sum'),
        failed_swaps=('is_failed', 'sum'),
        total_revenue_inr=('amount_charged_inr', 'sum'),
        total_energy_cost_inr=('energy_cost_inr', 'sum')
    ).reset_index()
    city_monthly['failure_rate_pct'] = round((city_monthly['failed_swaps'] / city_monthly['total_attempts']) * 100, 2)
    city_monthly['contribution_margin_proxy_inr'] = round(city_monthly['total_revenue_inr'] - city_monthly['total_energy_cost_inr'], 2)
    city_monthly.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q1_city_monthly_performance.csv"), index=False)
    
    return monthly, swaps_merged

def analyze_q2_service_failures(swaps_merged):
    print("\n--- Question 2: Service Failures & Customer Experience Analysis ---")
    
    swaps_merged['hour_of_day'] = pd.to_datetime(swaps_merged['event_ts_corrected']).dt.hour
    swaps_merged['day_of_week'] = pd.to_datetime(swaps_merged['event_ts_corrected']).dt.day_name()
    
    # Hour of day failure & wait breakdown
    hourly_fail = swaps_merged.groupby('hour_of_day').agg(
        total_attempts=('event_id', 'count'),
        failed_swaps=('is_failed', 'sum'),
        abandoned_swaps=('is_abandoned', 'sum'),
        avg_queue_wait_sec=('queue_wait_sec', 'mean')
    ).reset_index()
    hourly_fail['failure_rate_pct'] = round((hourly_fail['failed_swaps'] / hourly_fail['total_attempts']) * 100, 2)
    hourly_fail['avg_queue_wait_sec'] = round(hourly_fail['avg_queue_wait_sec'], 1)
    hourly_fail.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q2_hourly_failure_patterns.csv"), index=False)
    
    # Queue wait time by event outcome
    wait_by_outcome = swaps_merged.groupby('event_type').agg(
        event_count=('event_id', 'count'),
        avg_wait_sec=('queue_wait_sec', 'mean'),
        median_wait_sec=('queue_wait_sec', 'median'),
        p90_wait_sec=('queue_wait_sec', lambda x: x.quantile(0.9))
    ).reset_index()
    wait_by_outcome.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q2_queue_wait_by_outcome.csv"), index=False)
    print("Queue Wait Time by Outcome:")
    print(wait_by_outcome.to_string(index=False))
    
    # High-failure stations ranking (rate-based!)
    stn_perf = swaps_merged.groupby(['station_id', 'city']).agg(
        total_attempts=('event_id', 'count'),
        failed_swaps=('is_failed', 'sum'),
        abandoned_swaps=('is_abandoned', 'sum'),
        avg_queue_wait_sec=('queue_wait_sec', 'mean')
    ).reset_index()
    
    # Filter stations with at least 1,000 attempts for reliable rate estimation
    stn_perf_filtered = stn_perf[stn_perf['total_attempts'] >= 1000].copy()
    stn_perf_filtered['failure_rate_pct'] = round((stn_perf_filtered['failed_swaps'] / stn_perf_filtered['total_attempts']) * 100, 2)
    stn_perf_filtered['disruption_rate_pct'] = round(((stn_perf_filtered['failed_swaps'] + stn_perf_filtered['abandoned_swaps']) / stn_perf_filtered['total_attempts']) * 100, 2)
    
    top_failing_stations = stn_perf_filtered.sort_values('failure_rate_pct', ascending=False).head(15)
    top_failing_stations.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q2_top_failing_stations.csv"), index=False)
    print("\nTop 10 High-Failure Stations (Rate-Based, min 1k attempts):")
    print(top_failing_stations[['station_id', 'city', 'total_attempts', 'failed_swaps', 'failure_rate_pct', 'avg_queue_wait_sec']].head(10).to_string(index=False))
    
    return hourly_fail, top_failing_stations

def analyze_q3_station_patterns(swaps_merged, stations):
    print("\n--- Question 3: Station and Geographic Patterns Analysis ---")
    
    # Group by Expansion Wave
    wave_perf = swaps_merged.groupby('expansion_wave').agg(
        total_attempts=('event_id', 'count'),
        completed_swaps=('is_completed', 'sum'),
        failed_swaps=('is_failed', 'sum'),
        abandoned_swaps=('is_abandoned', 'sum'),
        avg_queue_wait_sec=('queue_wait_sec', 'mean'),
        total_revenue_inr=('amount_charged_inr', 'sum'),
        total_energy_cost_inr=('energy_cost_inr', 'sum')
    ).reset_index()
    wave_perf['failure_rate_pct'] = round((wave_perf['failed_swaps'] / wave_perf['total_attempts']) * 100, 2)
    wave_perf['rev_per_swap_inr'] = round(wave_perf['total_revenue_inr'] / wave_perf['completed_swaps'], 2)
    wave_perf['margin_proxy_pct'] = round(((wave_perf['total_revenue_inr'] - wave_perf['total_energy_cost_inr']) / wave_perf['total_revenue_inr']) * 100, 2)
    wave_perf.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q3_expansion_wave_performance.csv"), index=False)
    print("Expansion Wave Comparison:")
    print(wave_perf[['expansion_wave', 'total_attempts', 'failure_rate_pct', 'avg_queue_wait_sec', 'rev_per_swap_inr', 'margin_proxy_pct']].to_string(index=False))
    
    # Group by Charger Generation
    gen_perf = swaps_merged.groupby('charger_generation').agg(
        total_attempts=('event_id', 'count'),
        completed_swaps=('is_completed', 'sum'),
        failed_swaps=('is_failed', 'sum'),
        avg_queue_wait_sec=('queue_wait_sec', 'mean'),
        total_revenue_inr=('amount_charged_inr', 'sum'),
        total_energy_cost_inr=('energy_cost_inr', 'sum')
    ).reset_index()
    gen_perf['failure_rate_pct'] = round((gen_perf['failed_swaps'] / gen_perf['total_attempts']) * 100, 2)
    gen_perf['margin_proxy_pct'] = round(((gen_perf['total_revenue_inr'] - gen_perf['total_energy_cost_inr']) / gen_perf['total_revenue_inr']) * 100, 2)
    gen_perf.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q3_charger_generation_performance.csv"), index=False)
    print("\nCharger Generation Comparison:")
    print(gen_perf[['charger_generation', 'total_attempts', 'failure_rate_pct', 'avg_queue_wait_sec', 'margin_proxy_pct']].to_string(index=False))
    
    # Connectivity tier comparison
    swaps_conn = swaps_merged.merge(stations[['station_id', 'connectivity_tier', 'location_type', 'host_type', 'competitor_within_1_5km_since']], on='station_id', how='left')
    conn_perf = swaps_conn.groupby('connectivity_tier').agg(
        total_attempts=('event_id', 'count'),
        failed_swaps=('is_failed', 'sum'),
        avg_queue_wait_sec=('queue_wait_sec', 'mean')
    ).reset_index()
    conn_perf['failure_rate_pct'] = round((conn_perf['failed_swaps'] / conn_perf['total_attempts']) * 100, 2)
    conn_perf.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q3_connectivity_tier_performance.csv"), index=False)
    
    return wave_perf, gen_perf

def analyze_q4_battery_equipment(swaps, batteries):
    print("\n--- Question 4: Battery & Equipment Analysis ---")
    
    # Merge battery details with swap events (battery_out_id or battery_in_id)
    swaps_bat = swaps.merge(batteries, left_on='battery_out_id', right_on='battery_id', how='left')
    
    # Supplier performance
    supplier_perf = swaps_bat.groupby('supplier').agg(
        total_swaps=('event_id', 'count'),
        failed_swaps=('event_type', lambda x: (x.isin(['failed_no_charged_battery', 'failed_system_error'])).sum()),
        avg_initial_soh=('initial_soh_pct', 'mean'),
        avg_current_soh=('current_soh_pct', 'mean'),
        avg_energy_delivered=('energy_to_recharge_kwh', 'mean')
    ).reset_index()
    supplier_perf['failure_rate_pct'] = round((supplier_perf['failed_swaps'] / supplier_perf['total_swaps']) * 100, 2)
    supplier_perf['soh_degradation_pct'] = round(supplier_perf['avg_initial_soh'] - supplier_perf['avg_current_soh'], 2)
    supplier_perf.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q4_battery_supplier_performance.csv"), index=False)
    print("Battery Supplier Performance:")
    print(supplier_perf.to_string(index=False))
    
    # SOH vs Failure Rate correlation
    bat_summary = swaps_bat.groupby('battery_id').agg(
        total_swaps=('event_id', 'count'),
        failed_swaps=('event_type', lambda x: (x.isin(['failed_no_charged_battery', 'failed_system_error'])).sum()),
        current_soh_pct=('current_soh_pct', 'first'),
        supplier=('supplier', 'first')
    ).reset_index()
    bat_summary['failure_rate_pct'] = (bat_summary['failed_swaps'] / bat_summary['total_swaps']) * 100
    
    # Filter batteries with at least 50 swaps
    bat_filtered = bat_summary[bat_summary['total_swaps'] >= 50].dropna(subset=['current_soh_pct', 'failure_rate_pct'])
    if len(bat_filtered) > 5:
        corr_soh_fail, p_val_soh = stats.pearsonr(bat_filtered['current_soh_pct'], bat_filtered['failure_rate_pct'])
        print(f"\nPearson Correlation (SOH vs Failure Rate): {corr_soh_fail:.4f} (p-value: {p_val_soh:.4e})")
    
    return supplier_perf, bat_summary

def analyze_q5_pricing_fleet_economics(swaps_merged, partners):
    print("\n--- Question 5: Pricing & Fleet Partner Economics Analysis ---")
    
    # Tariff code breakdown
    tariff_perf = swaps_merged.groupby('tariff_code').agg(
        total_attempts=('event_id', 'count'),
        completed_swaps=('is_completed', 'sum'),
        total_revenue_inr=('amount_charged_inr', 'sum'),
        total_energy_cost_inr=('energy_cost_inr', 'sum')
    ).reset_index()
    tariff_perf['rev_per_completed_swap'] = round(tariff_perf['total_revenue_inr'] / tariff_perf['completed_swaps'], 2)
    tariff_perf['margin_proxy_pct'] = round(((tariff_perf['total_revenue_inr'] - tariff_perf['total_energy_cost_inr']) / tariff_perf['total_revenue_inr']) * 100, 2)
    tariff_perf.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q5_tariff_performance.csv"), index=False)
    print("Tariff Breakdown:")
    print(tariff_perf.to_string(index=False))
    
    # ZipDrop Contract Renegotiation Analysis (Nov 1, 2024 amendment: discount changed from 12% to 28%)
    # Merge rider partner info
    riders = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "clean_riders.csv"))
    swaps_partner = swaps_merged.merge(riders[['rider_id', 'partner_id']], on='rider_id', how='left')
    
    zipdrop_swaps = swaps_partner[swaps_partner['partner_id'] == 'FP-03'].copy()
    zipdrop_swaps['pre_amendment'] = pd.to_datetime(zipdrop_swaps['event_ts_corrected']) < '2024-11-01'
    
    zipdrop_perf = zipdrop_swaps.groupby('pre_amendment').agg(
        total_attempts=('event_id', 'count'),
        completed_swaps=('is_completed', 'sum'),
        total_revenue_inr=('amount_charged_inr', 'sum'),
        total_energy_cost_inr=('energy_cost_inr', 'sum')
    ).reset_index()
    zipdrop_perf['period'] = zipdrop_perf['pre_amendment'].map({True: 'Pre-Amendment (12% Discount)', False: 'Post-Amendment (28% Discount)'})
    zipdrop_perf['rev_per_swap_inr'] = round(zipdrop_perf['total_revenue_inr'] / zipdrop_perf['completed_swaps'], 2)
    zipdrop_perf['margin_proxy_pct'] = round(((zipdrop_perf['total_revenue_inr'] - zipdrop_perf['total_energy_cost_inr']) / zipdrop_perf['total_revenue_inr']) * 100, 2)
    zipdrop_perf.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q5_zipdrop_amendment_impact.csv"), index=False)
    print("\nZipDrop Contract Renegotiation Impact (FP-03):")
    print(zipdrop_perf[['period', 'total_attempts', 'completed_swaps', 'rev_per_swap_inr', 'margin_proxy_pct']].to_string(index=False))
    
    return tariff_perf, zipdrop_perf

def analyze_q6_rider_retention(swaps, riders, tickets):
    print("\n--- Question 6: New-Rider Retention Analysis ---")
    
    # Filter completed swaps only
    completed_swaps = swaps[swaps['event_type'] == 'swap_completed'].copy()
    completed_swaps['event_dt'] = pd.to_datetime(completed_swaps['event_ts_corrected'])
    
    # First completed swap per rider
    first_swaps = completed_swaps.groupby('rider_id').agg(
        first_swap_ts=('event_dt', 'min'),
        total_completed_swaps=('event_id', 'count')
    ).reset_index()
    
    # Merge rider metadata
    first_swaps = first_swaps.merge(riders[['rider_id', 'home_city_clean', 'vehicle_class', 'partner_id', 'signup_channel']], on='rider_id', how='left')
    
    # Calculate dataset cutoff date (2025-06-30)
    dataset_end = pd.to_datetime('2025-06-30')
    
    # 30-day retention eligibility: first swap must be <= 2025-05-31
    first_swaps['eligible_30d'] = first_swaps['first_swap_ts'] <= (dataset_end - pd.Timedelta(days=30))
    # 60-day retention eligibility: first swap must be <= 2025-04-30
    first_swaps['eligible_60d'] = first_swaps['first_swap_ts'] <= (dataset_end - pd.Timedelta(days=60))
    
    # Find second completed swap date per rider
    swaps_sorted = completed_swaps.sort_values(['rider_id', 'event_dt'])
    swaps_sorted['swap_rank'] = swaps_sorted.groupby('rider_id').cumcount() + 1
    
    second_swaps = swaps_sorted[swaps_sorted['swap_rank'] == 2][['rider_id', 'event_dt']].rename(columns={'event_dt': 'second_swap_ts'})
    first_swaps = first_swaps.merge(second_swaps, on='rider_id', how='left')
    
    first_swaps['days_to_second_swap'] = (first_swaps['second_swap_ts'] - first_swaps['first_swap_ts']).dt.total_seconds() / (24 * 3600)
    
    # Retained indicators
    first_swaps['retained_30d'] = (first_swaps['days_to_second_swap'].notnull()) & (first_swaps['days_to_second_swap'] <= 30)
    first_swaps['retained_60d'] = (first_swaps['days_to_second_swap'].notnull()) & (first_swaps['days_to_second_swap'] <= 60)
    
    # First attempt failure experience check (did the rider experience a failure on their VERY FIRST attempt?)
    all_attempts_sorted = swaps.sort_values(['rider_id', 'event_ts_corrected'])
    all_attempts_sorted['attempt_rank'] = all_attempts_sorted.groupby('rider_id').cumcount() + 1
    first_attempts = all_attempts_sorted[all_attempts_sorted['attempt_rank'] == 1][['rider_id', 'event_type', 'queue_wait_sec', 'station_id']]
    first_attempts['first_attempt_failed'] = first_attempts['event_type'].isin(['failed_no_charged_battery', 'failed_system_error', 'abandoned_queue'])
    
    first_swaps = first_swaps.merge(first_attempts[['rider_id', 'first_attempt_failed', 'queue_wait_sec']], on='rider_id', how='left')
    
    # Calculate overall retention rates
    cohort_30d = first_swaps[first_swaps['eligible_30d']]
    cohort_60d = first_swaps[first_swaps['eligible_60d']]
    
    ret_30d_pct = round((cohort_30d['retained_30d'].sum() / len(cohort_30d)) * 100, 2)
    ret_60d_pct = round((cohort_60d['retained_60d'].sum() / len(cohort_60d)) * 100, 2)
    
    print(f"Eligible 30-Day Cohort: {len(cohort_30d):,}, Retained 30d: {ret_30d_pct}%")
    print(f"Eligible 60-Day Cohort: {len(cohort_60d):,}, Retained 60d: {ret_60d_pct}%")
    
    # Retention by First Attempt Experience
    exp_ret = cohort_30d.groupby('first_attempt_failed').agg(
        eligible_riders=('rider_id', 'count'),
        retained_30d=('retained_30d', 'sum')
    ).reset_index()
    exp_ret['retention_30d_pct'] = round((exp_ret['retained_30d'] / exp_ret['eligible_riders']) * 100, 2)
    exp_ret['first_experience'] = exp_ret['first_attempt_failed'].map({True: 'Failed/Abandoned First Attempt', False: 'Successful First Attempt'})
    print("\nRetention by First Attempt Experience:")
    print(exp_ret[['first_experience', 'eligible_riders', 'retained_30d', 'retention_30d_pct']].to_string(index=False))
    
    # Chi-Square Test of Independence (First Experience vs 30-day Retention)
    contingency = pd.crosstab(cohort_30d['first_attempt_failed'], cohort_30d['retained_30d'])
    chi2, p_val_chi2, dof, _ = stats.chi2_contingency(contingency)
    print(f"Chi-Square Test (First Experience vs 30-Day Retention): Chi2 = {chi2:.4f}, p-value = {p_val_chi2:.4e}")
    
    first_swaps.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q6_rider_retention_dataset.csv"), index=False)
    exp_ret.to_csv(os.path.join(OUTPUT_TABLES_DIR, "q6_retention_by_first_experience.csv"), index=False)
    
    return cohort_30d, cohort_60d, exp_ret

def run_all_analyses():
    swaps, stations, riders, batteries, partners, context, tickets, hourly = load_data()
    
    monthly, swaps_merged = analyze_q1_network_performance(swaps, stations)
    hourly_fail, top_failing_stations = analyze_q2_service_failures(swaps_merged)
    wave_perf, gen_perf = analyze_q3_station_patterns(swaps_merged, stations)
    supplier_perf, bat_summary = analyze_q4_battery_equipment(swaps, batteries)
    tariff_perf, zipdrop_perf = analyze_q5_pricing_fleet_economics(swaps_merged, partners)
    cohort_30d, cohort_60d, exp_ret = analyze_q6_rider_retention(swaps, riders, tickets)
    
    print("\n=======================================================")
    print("ALL CORE ANALYSES COMPLETED & RESULT TABLES EXPORTED!")
    print("=======================================================")

if __name__ == "__main__":
    run_all_analyses()
