# VoltRelay Data Analytics Hackathon 2026 — 3-Minute Presentation Video Script

**Speaker:** Data Analytics Project Lead  
**Target Duration:** Exactly 3 Minutes (180 Seconds)  
**Tone:** Confident, Business-Oriented, Empirical, Executive

---

## 0:00 – 0:25 | Business Problem
*(Visual: Slide 1 showing VoltRelay network map across Bengaluru, Delhi NCR, Hyderabad, Pune, Mumbai, Jaipur with key metrics)*

**Spoken Script:**
"Hello everyone! I'm thrilled to present our submission for the VoltRelay Data Analytics Hackathon. 

VoltRelay operates an EV battery-swapping network for commercial 2-wheeler and 3-wheeler fleets across 6 major Indian metros. While monthly swap volumes grew more than threefold—from 108,000 swap attempts in January 2024 to over 331,000 in June 2025—VoltRelay faced three critical operational bottlenecks: mounting service failures during peak windows, rider retention friction, and margin compression across renegotiated fleet partner contracts. 

Our goal: diagnose the operational root causes and build an actionable, high-impact growth strategy."

---

## 0:25 – 0:55 | Dataset & Analytical Approach
*(Visual: Slide 2 showcasing Data Cleaning Pipeline, 3.81M swap events, firmware timestamp correction, test station filtering)*

**Spoken Script:**
"To solve this, we analyzed 8 primary datasets covering 3.87 million raw swap attempts, 150 operational stations, 20,000 registered riders, and 6,500 battery packs. 

We performed a comprehensive data quality audit:
First, we filtered out 62,031 test station events across test stations STN-TST-01 and STN-TST-02. 
Second, we corrected a 5-hour-30-minute timestamp offset on 139,490 events recorded under firmware v3.2.0 during March and April 2025 to reconstruct true local event time. 
Third, we standardized 18 inconsistent city name spellings across rider records into 6 primary metros. 
Finally, we evaluated 30-day and 60-day cohort retention across 18,643 eligible first-swap riders with strict right-censoring controls and established a transparent Contribution Margin Proxy defined as Revenue minus Grid Energy Tariff costs."

---

## 0:55 – 2:10 | Most Important Insights
*(Visual: Slide 3 displaying Charts 1, 6, 7 & 9 — Summer Failure Spike, Gen1 vs Gen3, Battery Degradation, First-Swap Retention Penalty)*

**Spoken Script:**
"Here are our key empirical findings:

**First, First-Swap Service Failures Statistically Penalize Rider Retention.**  
Riders whose initial swap attempt resulted in failure or queue abandonment had a 30-day retention rate of 98.91% compared to 99.60% for riders with a successful first swap. A Chi-Square test confirmed this difference is statistically significant (Chi-Square = 8.0035, p = 0.00467).

**Second, Summer Heatwaves Drive Severe Failure Seasonality.**  
Service failure rates spiked to 8.12% in May 2024 and 6.53% in May 2025, compared to a 2.6% winter baseline. Ambient temperatures exceeding 42°C in Delhi NCR and Jaipur caused battery thermal throttling and grid instability.

**Third, Legacy Gen1 Chargers Drive Outsized System Failures.**  
Gen1 chargers recorded a 4.64% failure rate—54% higher than Gen2 (2.99%) and Gen3 (3.01%) stations.

**Fourth, Kyron Batteries Experience Accelerated Degradation.**  
Kyron battery packs suffered a 35.6% average SOH loss (current SOH 63.6% vs initial 99.2%), nearly double the ~18.6% degradation observed in Cellora and Amptek packs.

**Fifth, ZipDrop Contract Amendment Eroded Unit Revenue.**  
Following the November 2024 contract amendment increasing ZipDrop's discount from 12% to 28%, revenue per swap dropped from ₹57.48 to ₹48.64, eroding our Contribution Margin Proxy from 64.0% to 62.7% across 358,000 post-amendment swaps."

---

## 2:10 – 2:45 | Actionable Recommendations
*(Visual: Slide 4 showing Prioritized Recommendation Matrix)*

**Spoken Script:**
"Based on these empirical findings, we propose a prioritized strategic roadmap:

1. **Priority 1 (Customer Experience):** Implement a 'First-Swap VIP Guarantee' algorithm that reserves fully charged Gen3 batteries for new riders during their first 3 swaps.
2. **Priority 1 (Operations):** Retrofit high-temperature stations in Delhi NCR and Jaipur with solar battery prep-cooling to eliminate summer thermal throttling.
3. **Priority 2 (Network Planning):** Accelerate Gen1 hardware retrofits to Gen3 power module standards.
4. **Priority 2 (Fleet Partnerships):** Restructure volume-tiered fleet contracts to include peak-hour surcharge billability, recovering ₹3.50 per swap in unit margin."

---

## 2:45 – 3:00 | Conclusion
*(Visual: Slide 5 summarizing Key Takeaways & Submission Highlights)*

**Spoken Script:**
"By aligning operational execution with data-backed insights, VoltRelay can eliminate service disruption, protect unit economics, and secure market leadership in India's EV revolution. 

Thank you for your time, and we look forward to your questions!"
