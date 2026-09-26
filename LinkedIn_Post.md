# 🚀 Excited to share our final submission for the Gradient Learnings Data Analytics Hackathon 2026!

We tackled the operational and financial challenges facing **VoltRelay Energy** — an EV battery-swapping network operating across 6 major Indian metros (Bengaluru, Delhi NCR, Hyderabad, Pune, Mumbai, Jaipur). ⚡🔋

While VoltRelay's monthly swap volume surged **3.06x from 108K to over 331K swap attempts/month**, the business faced mounting service failures during summer heatwaves, rider churn risks, and contract discount margin compression.

Here is how we harnessed data to build an actionable strategic roadmap:

### 📊 What We Analyzed:
- **3.81 Million Clean Swap Events** across 150 operational stations
- **20,000 Registered Riders** & **6,500 Battery Packs**
- Fixed a **5h 30m firmware timestamp anomaly** across 139K events
- Standardized city names & excluded test stations
- Evaluated cohort retention with strict right-censoring control

### 💡 Key Evidence-Backed Findings:
1️⃣ **First Impressions Count:** Riders experiencing a failure or queue abandonment on their first swap attempt show a statistically significant reduction in 30-day retention (**98.91% vs 99.60%**, $\chi^2 = 8.0035, p = 0.00467$).  
2️⃣ **Summer Heatwave Spikes:** Failure rates jumped to **8.12% in May 2024** and **6.53% in May 2025** (vs 2.6% winter baseline) due to thermal throttling.  
3️⃣ **Hardware Matters:** Legacy Gen1 chargers exhibit **4.64% failure rates** — 54% higher than Gen2 (2.99%) & Gen3 (3.01%) chargers.  
4️⃣ **Battery Degradation:** Kyron battery packs suffered **35.6% SOH loss**, almost double Cellora & Amptek (~18.6%).  
5️⃣ **Contract Unit Economics:** ZipDrop's contract renegotiation (28% discount) reduced revenue per swap from ₹57.48 to ₹48.64.

### 🎯 Strategic Recommendations:
✅ Deploy a **New-Rider First-Swap VIP Guarantee** to reserve charged batteries for onboarding riders  
✅ Install **Solar Battery Prep-Cooling** at high-heat hubs in Delhi NCR & Jaipur  
✅ Upgrade legacy **Gen1 power modules to Gen3 standards**  
✅ Restructure fleet partner contracts to include peak surcharge billability  

Special thanks to the **Gradient Learnings** team for an incredible hackathon challenge!

What strategies do you think are most critical for EV battery swapping networks scaling in tropical climates? Let's discuss in the comments below! 👇

#DataAnalytics #DataAnalyticsHackathon #DataScience #Analytics #BuildWithData #ProductSpace #ElectricVehicles #EVIndia #DataDriven
