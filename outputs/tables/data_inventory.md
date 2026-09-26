# VoltRelay Dataset Inventory

| Filename                  |   Size (MB) |    Rows |   Cols | Primary Key                                   | Date Cols                                                     |   Num Cols Count |   Cat Cols Count | Max Missing %                |
|:--------------------------|------------:|--------:|-------:|:----------------------------------------------|:--------------------------------------------------------------|-----------------:|-----------------:|:-----------------------------|
| swap_events.csv           |      694.97 | 3877013 |     22 | event_id                                      |                                                               |               11 |               11 | 5.96% (battery_out_id)       |
| station_hourly_status.csv |      103.33 | 1487712 |     14 | None/Composite                                |                                                               |               11 |                3 | 55.24% (charged_3w_min)      |
| support_tickets.csv       |        6.23 |   44000 |     12 | ticket_id                                     |                                                               |                2 |               10 | 65.62% (csat_score)          |
| riders.csv                |        2    |   20000 |     12 | rider_id                                      | signup_date                                                   |                0 |               11 | 38.14% (partner_id)          |
| batteries.csv             |        0.6  |    6500 |     13 | battery_id                                    | manufacture_date, commission_date, retired_date               |                4 |                6 | 77.88% (retired_date)        |
| city_daily_context.csv    |        0.21 |    3282 |     12 | None/Composite                                | date                                                          |                4 |                7 | 96.65% (festival_or_event)   |
| stations.csv              |        0.02 |     152 |     22 | station_id                                    | commissioned_date, decommissioned_date, firmware_updated_date |                9 |               10 | 99.34% (decommissioned_date) |
| fleet_partners.csv        |        0    |      12 |     12 | partner_id, partner_name, contract_start_date | contract_start_date, amendment_date                           |                3 |                7 | 91.67% (amendment_date)      |

## Detailed Column Breakdown

### swap_events.csv
- **Rows**: 3,877,013 | **Cols**: 22
| Column                 | DataType   | Missing %   |   Unique Values |
|:-----------------------|:-----------|:------------|----------------:|
| event_id               | str        | 0.0%        |           50000 |
| rider_id               | str        | 0.0%        |            3836 |
| station_id             | str        | 0.0%        |              92 |
| event_ts               | str        | 0.0%        |           48295 |
| event_type             | str        | 0.0%        |               5 |
| attempt_seq            | int64      | 0.0%        |               1 |
| queue_wait_sec         | int64      | 0.0%        |            1097 |
| battery_in_id          | str        | 0.73%       |            5114 |
| battery_out_id         | str        | 5.96%       |            5111 |
| soc_in_pct             | float64    | 0.73%       |             230 |
| soh_in_pct             | float64    | 0.73%       |              44 |
| soc_out_pct            | float64    | 5.96%       |             215 |
| soh_out_pct            | float64    | 5.96%       |              45 |
| km_since_last_swap     | float64    | 0.73%       |             970 |
| tariff_code            | str        | 0.0%        |               2 |
| list_price_inr         | float64    | 0.0%        |               2 |
| discount_inr           | float64    | 0.0%        |              16 |
| amount_charged_inr     | float64    | 0.0%        |              55 |
| payment_mode           | str        | 0.0%        |               1 |
| energy_to_recharge_kwh | float64    | 5.96%       |            2256 |
| station_firmware       | str        | 0.0%        |               2 |
| sync_mode              | str        | 0.0%        |               2 |

### station_hourly_status.csv
- **Rows**: 1,487,712 | **Cols**: 14
| Column             | DataType   | Missing %   |   Unique Values |
|:-------------------|:-----------|:------------|----------------:|
| station_id         | str        | 0.0%        |               4 |
| hour_start         | str        | 0.0%        |           13128 |
| charged_2w_avg     | float64    | 0.63%       |            1872 |
| charged_2w_min     | float64    | 0.63%       |              22 |
| charged_3w_min     | float64    | 55.24%      |               5 |
| packs_charging     | float64    | 0.63%       |              19 |
| packs_quarantined  | float64    | 0.63%       |               2 |
| chargers_online    | int64      | 0.0%        |               5 |
| ambient_temp_c     | float64    | 0.63%       |             328 |
| cabinet_temp_c     | float64    | 0.63%       |             384 |
| avg_charge_minutes | float64    | 0.63%       |             656 |
| outage_minutes     | int64      | 0.0%        |               2 |
| grid_kwh           | float64    | 0.63%       |            2459 |
| telemetry_status   | str        | 0.0%        |               3 |

### support_tickets.csv
- **Rows**: 44,000 | **Cols**: 12
| Column            | DataType   | Missing %   |   Unique Values |
|:------------------|:-----------|:------------|----------------:|
| ticket_id         | str        | 0.0%        |           44000 |
| rider_id          | str        | 0.0%        |           13979 |
| station_id        | str        | 5.06%       |             152 |
| battery_id        | str        | 30.08%      |            6428 |
| created_ts        | str        | 0.0%        |           43969 |
| channel           | str        | 0.0%        |               4 |
| category          | str        | 0.0%        |               6 |
| rider_comment     | str        | 0.0%        |              89 |
| priority          | str        | 0.0%        |               3 |
| resolution_status | str        | 0.0%        |               3 |
| resolution_hours  | float64    | 13.89%      |             774 |
| csat_score        | float64    | 65.62%      |               5 |

### riders.csv
- **Rows**: 20,000 | **Cols**: 12
| Column         | DataType   | Missing %   |   Unique Values |
|:---------------|:-----------|:------------|----------------:|
| rider_id       | str        | 0.0%        |           20000 |
| partner_id     | str        | 38.14%      |              12 |
| vehicle_class  | str        | 0.0%        |               2 |
| vehicle_model  | str        | 0.0%        |               8 |
| home_zone      | str        | 0.0%        |              28 |
| signup_date    | str        | 0.0%        |             817 |
| signup_channel | str        | 0.0%        |               4 |
| plan_type      | str        | 0.0%        |               3 |
| declared_shift | str        | 18.31%      |               4 |
| age_band       | str        | 7.74%       |               4 |
| kyc_verified   | bool       | 0.0%        |               2 |
| home_city      | str        | 0.0%        |              21 |

### batteries.csv
- **Rows**: 6,500 | **Cols**: 13
| Column             | DataType   | Missing %   |   Unique Values |
|:-------------------|:-----------|:------------|----------------:|
| battery_id         | str        | 0.0%        |            6500 |
| pack_type          | str        | 0.0%        |               2 |
| supplier           | str        | 0.0%        |               3 |
| manufacturing_lot  | str        | 0.0%        |              55 |
| manufacture_date   | str        | 0.0%        |             862 |
| commission_date    | str        | 0.0%        |             826 |
| rated_capacity_kwh | float64    | 0.0%        |               2 |
| purchase_cost_inr  | int64      | 0.0%        |            4111 |
| initial_soh_pct    | float64    | 0.0%        |              23 |
| bms_firmware       | str        | 0.0%        |               3 |
| retired_date       | str        | 77.88%      |               1 |
| retirement_reason  | str        | 77.88%      |               1 |
| current_soh_pct    | float64    | 0.0%        |             247 |

### city_daily_context.csv
- **Rows**: 3,282 | **Cols**: 12
| Column                  | DataType   | Missing %   |   Unique Values |
|:------------------------|:-----------|:------------|----------------:|
| city                    | str        | 0.0%        |               6 |
| date                    | str        | 0.0%        |             547 |
| max_temp_c              | float64    | 0.0%        |             402 |
| min_temp_c              | float64    | 0.0%        |             194 |
| rainfall_mm             | float64    | 0.0%        |             407 |
| heat_alert              | bool       | 0.0%        |               2 |
| flood_disruption        | bool       | 0.0%        |               2 |
| festival_or_event       | str        | 96.65%      |               5 |
| is_public_holiday       | bool       | 0.0%        |               2 |
| grid_outage_hours       | float64    | 0.0%        |              15 |
| competitor_promo_active | bool       | 0.0%        |               2 |
| ecommerce_sale_event    | bool       | 0.0%        |               2 |

### stations.csv
- **Rows**: 152 | **Cols**: 22
| Column                        | DataType   | Missing %   |   Unique Values |
|:------------------------------|:-----------|:------------|----------------:|
| station_id                    | str        | 0.0%        |             152 |
| city                          | str        | 0.0%        |               6 |
| zone                          | str        | 0.0%        |              28 |
| latitude                      | float64    | 0.0%        |             151 |
| longitude                     | float64    | 0.0%        |             151 |
| location_type                 | str        | 0.0%        |               6 |
| host_type                     | str        | 0.0%        |               4 |
| commissioned_date             | str        | 0.0%        |             117 |
| decommissioned_date           | str        | 99.34%      |               1 |
| expansion_wave                | str        | 0.0%        |               3 |
| charger_generation            | str        | 0.0%        |               3 |
| slots_2w                      | int64      | 0.0%        |               3 |
| slots_3w                      | int64      | 0.0%        |               3 |
| inventory_target_2w           | int64      | 0.0%        |              40 |
| inventory_target_3w           | int64      | 0.0%        |               5 |
| monthly_rent_inr              | int64      | 0.0%        |             150 |
| monthly_maintenance_inr       | int64      | 0.0%        |             145 |
| grid_tariff_inr_kwh           | float64    | 0.0%        |             114 |
| connectivity_tier             | str        | 0.0%        |               3 |
| firmware_version              | str        | 0.0%        |               2 |
| firmware_updated_date         | str        | 0.0%        |               2 |
| competitor_within_1_5km_since | str        | 93.42%      |               1 |

### fleet_partners.csv
- **Rows**: 12 | **Cols**: 12
| Column                       | DataType   | Missing %   |   Unique Values |
|:-----------------------------|:-----------|:------------|----------------:|
| partner_id                   | str        | 0.0%        |              12 |
| partner_name                 | str        | 0.0%        |              12 |
| partner_segment              | str        | 0.0%        |               5 |
| vehicle_class                | str        | 0.0%        |               3 |
| contract_type                | str        | 0.0%        |               2 |
| contract_start_date          | str        | 0.0%        |              12 |
| discount_pct                 | float64    | 0.0%        |               9 |
| amendment_date               | str        | 91.67%      |               1 |
| discount_pct_after_amendment | float64    | 91.67%      |               1 |
| peak_surcharge_billable      | str        | 0.0%        |               2 |
| payment_terms_days           | int64      | 0.0%        |               3 |
| cities_active                | str        | 0.0%        |              11 |

