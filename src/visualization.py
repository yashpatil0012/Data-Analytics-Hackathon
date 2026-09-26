import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

TABLES_DIR = r"C:\Users\yashp\.gemini\antigravity\scratch\voltRelay-data-analytics\outputs\tables"
CHARTS_DIR = r"C:\Users\yashp\.gemini\antigravity\scratch\voltRelay-data-analytics\outputs\charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

# Global professional style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 1.0

DARK_NAVY = '#1b2a4a'
ACCENT_BLUE = '#2b5c8f'
FAIL_RED = '#d9534f'
SUCCESS_GREEN = '#5cb85c'
WARNING_ORANGE = '#f0ad4e'
PURPLE = '#6f42c1'

def plot_chart1_monthly_trend():
    df = pd.read_csv(os.path.join(TABLES_DIR, "q1_monthly_network_performance.csv"))
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    color = ACCENT_BLUE
    ax1.set_xlabel('Month', fontweight='bold', labelpad=10)
    ax1.set_ylabel('Completed Swaps', color=color, fontweight='bold')
    bars = ax1.bar(df['year_month'], df['completed_swaps'], color=color, alpha=0.7, label='Completed Swaps', width=0.5)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')
    
    ax2 = ax1.twinx()  
    color = FAIL_RED
    ax2.set_ylabel('Service Failure Rate (%)', color=color, fontweight='bold')
    line = ax2.plot(df['year_month'], df['failure_rate_pct'], color=color, marker='o', linewidth=2.5, label='Failure Rate %')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('VoltRelay Network Performance: Completed Swaps vs Failure Rate (2024–2025)', fontsize=14, fontweight='bold', pad=15)
    fig.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "chart1_monthly_swap_failure_trend.png"), dpi=300)
    plt.close()
    print("Generated Chart 1: Monthly Swap & Failure Trend")

def plot_chart2_economic_trend():
    df = pd.read_csv(os.path.join(TABLES_DIR, "q1_monthly_network_performance.csv"))
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    ax1.plot(df['year_month'], df['total_revenue_inr'] / 1e6, color='#2e7d32', marker='s', linewidth=2.5, label='Revenue (₹ Million)')
    ax1.plot(df['year_month'], df['total_energy_cost_inr'] / 1e6, color='#c62828', marker='^', linewidth=2, linestyle='--', label='Energy Cost (₹ Million)')
    ax1.set_ylabel('INR (Millions)', fontweight='bold')
    ax1.set_xlabel('Month', fontweight='bold', labelpad=10)
    plt.xticks(rotation=45, ha='right')
    
    ax2 = ax1.twinx()
    ax2.plot(df['year_month'], df['contribution_margin_proxy_pct'], color='#1565c0', marker='o', linewidth=2.5, label='Contribution Margin Proxy %')
    ax2.set_ylabel('Contribution Margin Proxy (%)', color='#1565c0', fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='#1565c0')
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.title('VoltRelay Financial Evolution: Revenue, Energy Cost & Contribution Margin Proxy', fontsize=14, fontweight='bold', pad=15)
    fig.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "chart2_economic_trend.png"), dpi=300)
    plt.close()
    print("Generated Chart 2: Economic & Profitability Trend")

def plot_chart3_city_failures():
    df = pd.read_csv(os.path.join(TABLES_DIR, "q1_city_monthly_performance.csv"))
    city_avg = df.groupby('city')['failure_rate_pct'].mean().reset_index().sort_values('failure_rate_pct', ascending=False)
    
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(data=city_avg, x='city', y='failure_rate_pct', color=ACCENT_BLUE)
    plt.title('Average Service Failure Rate by City (%)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('City', fontweight='bold')
    plt.ylabel('Failure Rate (%)', fontweight='bold')
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "chart3_failure_rate_by_city.png"), dpi=300)
    plt.close()
    print("Generated Chart 3: Failure Rate by City")

def plot_chart4_top_failing_stations():
    df = pd.read_csv(os.path.join(TABLES_DIR, "q2_top_failing_stations.csv")).head(10)
    
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, y='station_id', x='failure_rate_pct', hue='city', dodge=False)
    plt.title('Top 10 High-Failure Stations (Rate-Based, Min 1,000 Attempts)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Failure Rate (%)', fontweight='bold')
    plt.ylabel('Station ID', fontweight='bold')
    
    for p in ax.patches:
        width = p.get_width()
        if width > 0:
            ax.annotate(f'{width:.2f}%', (width, p.get_y() + p.get_height() / 2.),
                        ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontweight='bold')
            
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "chart4_top_failing_stations.png"), dpi=300)
    plt.close()
    print("Generated Chart 4: Top Failing Stations")

def plot_chart5_queue_wait_outcome():
    df = pd.read_csv(os.path.join(TABLES_DIR, "q2_queue_wait_by_outcome.csv"))
    
    plt.figure(figsize=(9, 5))
    ax = sns.barplot(data=df, x='event_type', y='avg_wait_sec', color=ACCENT_BLUE)
    plt.title('Average Queue Wait Time by Swap Attempt Outcome', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Attempt Outcome', fontweight='bold')
    plt.ylabel('Average Wait Time (Seconds)', fontweight='bold')
    plt.xticks(rotation=15)
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}s', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "chart5_queue_wait_vs_outcome.png"), dpi=300)
    plt.close()
    print("Generated Chart 5: Queue Wait vs Outcome")

def plot_chart6_charger_gen():
    df = pd.read_csv(os.path.join(TABLES_DIR, "q3_charger_generation_performance.csv"))
    
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(df))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, df['failure_rate_pct'], width, label='Failure Rate %', color=FAIL_RED)
    rects2 = ax.bar(x + width/2, df['margin_proxy_pct'], width, label='Margin Proxy %', color=SUCCESS_GREEN)
    
    ax.set_ylabel('Percentage (%)', fontweight='bold')
    ax.set_title('Charger Hardware Generation Comparison: Gen1 vs Gen2 vs Gen3', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(df['charger_generation'], fontweight='bold')
    ax.legend()
    
    ax.bar_label(rects1, padding=3, fmt='%.1f%%')
    ax.bar_label(rects2, padding=3, fmt='%.1f%%')
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "chart6_charger_generation_comparison.png"), dpi=300)
    plt.close()
    print("Generated Chart 6: Charger Generation Comparison")

def plot_chart7_supplier_comparison():
    df = pd.read_csv(os.path.join(TABLES_DIR, "q4_battery_supplier_performance.csv"))
    
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(df))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, df['avg_current_soh'], width, label='Current SOH %', color=ACCENT_BLUE)
    rects2 = ax.bar(x + width/2, df['soh_degradation_pct'], width, label='Avg SOH Loss %', color=WARNING_ORANGE)
    
    ax.set_ylabel('Percentage (%)', fontweight='bold')
    ax.set_title('Battery Supplier Health & SOH Degradation Comparison', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(df['supplier'], fontweight='bold')
    ax.legend()
    
    ax.bar_label(rects1, padding=3, fmt='%.1f%%')
    ax.bar_label(rects2, padding=3, fmt='%.1f%%')
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "chart7_battery_supplier_comparison.png"), dpi=300)
    plt.close()
    print("Generated Chart 7: Battery Supplier Comparison")

def plot_chart8_zipdrop_impact():
    df = pd.read_csv(os.path.join(TABLES_DIR, "q5_zipdrop_amendment_impact.csv"))
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax = sns.barplot(data=df, x='period', y='margin_proxy_pct', color=ACCENT_BLUE)
    plt.title('ZipDrop Fleet Contract Renegotiation: Contribution Margin Proxy %', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Contract Period', fontweight='bold')
    plt.ylabel('Contribution Margin Proxy (%)', fontweight='bold')
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "chart8_zipdrop_contract_impact.png"), dpi=300)
    plt.close()
    print("Generated Chart 8: ZipDrop Contract Impact")

def plot_chart9_retention_experience():
    df = pd.read_csv(os.path.join(TABLES_DIR, "q6_retention_by_first_experience.csv"))
    
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(data=df, x='first_experience', y='retention_30d_pct', palette=['#2e7d32', '#c62828'], hue='first_experience', legend=False)
    plt.title('30-Day Rider Retention Rate by First-Swap Attempt Outcome', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('First Swap Attempt Outcome', fontweight='bold')
    plt.ylabel('30-Day Retention Rate (%)', fontweight='bold')
    plt.ylim(95.0, 100.5) # Zoom in to highlight gap
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "chart9_retention_by_first_experience.png"), dpi=300)
    plt.close()
    print("Generated Chart 9: Rider Retention by First Experience")

def run_all_plots():
    plot_chart1_monthly_trend()
    plot_chart2_economic_trend()
    plot_chart3_city_failures()
    plot_chart4_top_failing_stations()
    plot_chart5_queue_wait_outcome()
    plot_chart6_charger_gen()
    plot_chart7_supplier_comparison()
    plot_chart8_zipdrop_impact()
    plot_chart9_retention_experience()
    print("\nALL DECISION-ORIENTED CHARTS GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_plots()
