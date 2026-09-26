# VoltRelay Energy — Data Analytics Hackathon 2026

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Data Analytics](https://img.shields.io/badge/hackathon-submission-brightgreen)

An end-to-end, submission-ready data analytics project investigating network performance, service failure root causes, battery equipment degradation, fleet contract economics, and new-rider retention for **VoltRelay Energy**'s EV battery-swapping network across 6 Indian metropolitan cities.

---

## 📌 Executive Summary

VoltRelay Energy operates an electric 2-wheeler (2W) and 3-wheeler (3W) battery-swapping network across **Bengaluru, Delhi NCR, Hyderabad, Pune, Mumbai, and Jaipur**.

Between January 2024 and June 2025:
- Total swap attempts grew from **108,269 swaps/month to 331,693 swaps/month** (over 3x expansion).
- Service failure rates exhibited severe summer spikes (**8.12% in May 2024** and **6.53% in May 2025** vs 2.6% winter baseline).
- **New-rider 30-day retention stands at 99.57%** across 18,643 eligible first-swap riders. First-swap attempt failures impose a statistically significant retention penalty (**98.91% vs 99.60%**, $\chi^2 = 8.0035, p = 0.00467$).
- **Gen1 charger hardware** experienced a 4.64% failure rate (54% higher than Gen2/Gen3).
- **ZipDrop (FP-03)** contract renegotiation (discount increased from 12% to 28%) eroded unit revenue from ₹57.48 to ₹48.64 per swap.

---

## 📁 Project Directory Structure

```
voltRelay-data-analytics/
├── data/                                 # Cleaned dataset storage (.parquet & .csv)
│   ├── clean_swap_events.parquet         # 3.81M cleaned swap events
│   ├── clean_stations.csv                # 150 operational stations
│   ├── clean_riders.csv                  # 20,000 riders with standardized cities
│   ├── clean_batteries.csv               # 6,500 battery packs
│   ├── clean_fleet_partners.csv          # Fleet partner contract data
│   ├── clean_city_daily_context.csv      # Weather, holidays, grid outages
│   └── clean_support_tickets.csv         # 44,000 support tickets
├── notebooks/
│   └── VoltRelay_Data_Analytics_Hackathon.ipynb   # Top-to-bottom reproducible notebook
├── src/
│   ├── data_inventory.py                 # Stage 1: Data inventory & dictionary generator
│   ├── data_cleaning.py                  # Stage 2 & 3: Data cleaning & quality audit
│   ├── analysis.py                       # Stage 4: Core analyses for Q1–Q6
│   ├── visualization.py                  # Stage 5: Decision-oriented charts
│   ├── report_generator.py               # Stage 9: PDF Report compiler
│   └── notebook_generator.py             # Stage 8: Notebook compiler
├── outputs/
│   ├── charts/                           # High-res decision-oriented visualizations (.png)
│   └── tables/                           # Summary analytical tables (.csv & .md)
├── report/
│   └── VoltRelay_Analysis_Report.pdf     # Submission PDF Report
├── Three_Minute_Video_Script.md          # 3-minute video presentation script
├── LinkedIn_Post.md                      # Professional LinkedIn submission post
├── README.md                             # Project documentation
└── requirements.txt                      # Dependencies
```

---

## 🛠️ Data Quality & Data Cleaning Audit

1. **Test Station Exclusion**: Filtered 62,031 events associated with test stations (`STN-TST-01`, `STN-TST-02`).
2. **Firmware v3.2.0 Timestamp Correction**: Corrected +5 hours 30 minutes offset across 139,490 events recorded under firmware v3.2.0 between March 10, 2025 and April 14, 2025 to reconstruct true local event time.
3. **City Name Standardization**: Standardized 18 non-standard city name variations across rider records (e.g. *Bombay, BLR, PUN, Hyd, Gurgaon, New Delhi, bengaluru*) into 6 primary metros.
4. **Duplicate Handling**: Removed 277 `offline_batch` duplicate records within 60-second sync windows.
5. **Anomaly Flags**: Flagged 7,687 invalid km records ($<0$ or $>500$ km) and 3,634 invalid SOC records.
6. **CSAT Missingness**: Explicitly documented that CSAT score is 65.62% missing and non-randomly sampled.

---

## 📊 Summary of Key Findings

| Domain | Key Metric / Insight | Evidence / Data Support |
| ------ | -------------------- | ----------------------- |
| **Network Growth** | Volume expanded 3.06x | Swaps grew from 108K (Jan 2024) to 331K (June 2025) |
| **Summer Failures** | Severe seasonality | Failure rate spiked to 8.12% in May 2024 & 6.53% in May 2025 |
| **Queue Abandonment** | Long wait threshold | Avg wait for abandoned swaps was 702.8s (~11.7 min) vs 243.7s for completed |
| **Hardware Generation** | Gen1 lagging | Gen1 failure rate (4.64%) vs Gen2 (2.99%) & Gen3 (3.01%) |
| **Battery Degradation** | Kyron pack issues | Kyron SOH loss = 35.6% vs ~18.6% for Cellora & Amptek |
| **Rider Retention** | First-swap penalty | First-swap failure drops 30-day retention from 99.60% to 98.91% ($p = 0.00467$) |

---

## 🎯 Prioritized Strategic Recommendation Matrix

| Priority | Operational Problem | Recommended Action | Expected Impact | Owner |
| -------- | ------------------- | ------------------ | --------------- | ----- |
| **P1** | First-Swap Churn | Implement VIP dispatch & inventory reservation for new riders | +0.7-1.2% Retention Boost ($p<0.01$) | Customer Experience |
| **P1** | Summer Heatwave Failure | Install solar prep-cooling & active thermal management at heat hubs | -50% Summer Failure Spike | Operations |
| **P2** | Gen1 Hardware Failure | Upgrade Gen1 power modules to Gen3 standard | -35% Gen1 Failure Rate | Network Planning |
| **P2** | ZipDrop Discount Erosion | Restructure volume discount tiers to include peak surcharges | +₹3.5/swap Margin Recovery | Fleet Partnerships |
| **P3** | Queue Wait Drop-off | Dynamic peak pricing & real-time queue redirection | -25% Peak Hour Wait | Pricing & Tech |

---

## 🚀 How to Run the Project

### Prerequisites
Install dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 1: Run Data Inventory & Quality Audit
```bash
python src/data_inventory.py
python src/data_cleaning.py
```

### Step 2: Run Core Analyses & Visualizations
```bash
python src/analysis.py
python src/visualization.py
```

### Step 3: Generate PDF Report & Notebook
```bash
python src/report_generator.py
python src/notebook_generator.py
```

---

## ⚠️ Limitations & Disclaimers

1. **Non-Causal Inference**: Associations observed in observational swap data (e.g. queue wait time vs abandonment) represent statistical correlations and do not assert direct causality.
2. **CSAT Missingness**: CSAT scores are missing for 65.62% of tickets and are not randomly missing; averages are treated as conditional feedback.
3. **Contribution Margin Proxy**: Labeled as a proxy because fixed network overheads, battery capital depreciation, and station land leases are excluded from grid energy cost subtractions.
