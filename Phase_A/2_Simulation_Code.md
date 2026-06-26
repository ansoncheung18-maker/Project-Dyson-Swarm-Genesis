# Phase A：模擬程式碼
**專案**：戴森蜂群起源 (Dyson Swarm Genesis)  
**版本**：1.0  
**日期**：2026-06-26  
**作者**：Anson Cheung（14歲）

---

## 1. 模擬總覽

本檔案包含三個獨立嘅 Python 模擬，用於驗證戴森蜂群嘅核心假設：

| # | 模擬名稱 | 用途 | 輸出 |
|:---|:---|:---|:---|
| 1 | 發電量與軌道力學模擬 | 計算衛星發電量、軌道參數、成本回報 | 文字結果 + 圖表 |
| 2 | 機械人指數增長模擬 | 驗證機械人複製能否喺合理時間內製造足夠衛星 | 文字結果 + 圖表 |
| 3 | 材料供應鏈模擬 | 驗證水星、月球、小行星帶原材料是否足夠 | 文字結果 + 圖表 |

所有模擬均以 **Python 3** 編寫，依賴以下函式庫：
- `math` (標準庫)
- `numpy`
- `matplotlib`
- `datetime` (標準庫)

---

## 2. 模擬 1：發電量與軌道力學

### 2.1 說明
計算衛星喺唔同軌道半徑嘅發電量、軌道週期、速度，並估算成本同回報期。

### 2.2 程式碼

```python
# -*- coding: utf-8 -*-
"""
Project Dyson Swarm Genesis - 發電量與軌道力學模擬
作者: Anson Cheung (14歲)
日期: 2026-06-26
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ============================================================
# 1. 常數定義
# ============================================================

AU = 1.496e11  # 1 天文單位 (米)
MU_SUN = 1.327e20  # 太陽引力常數 (m³/s²)
SUN_OUTPUT_GW = 3.846e26 / 1e9  # 太陽總輸出 (GW)
HUMAN_ENERGY_GW = 2.0e13 / 1e9  # 人類目前用量 (GW)

# 衛星參數
SATELLITE_AREA = 1.0  # km²
CELL_EFFICIENCY = 0.40
LASER_EFFICIENCY = 0.90
TRANSMISSION_EFFICIENCY = 0.85
COOLING_POWER = 0.05
SAT_NET_POWER_GW = 14.0 * (1 - COOLING_POWER) * LASER_EFFICIENCY * TRANSMISSION_EFFICIENCY

# ============================================================
# 2. 軌道力學函數
# ============================================================

def orbital_period(radius_au):
    radius_m = radius_au * AU
    period_sec = 2 * math.pi * math.sqrt(radius_m**3 / MU_SUN)
    return period_sec / 86400

def orbital_velocity(radius_au):
    radius_m = radius_au * AU
    return math.sqrt(MU_SUN / radius_m) / 1000

def solar_intensity(radius_au):
    return 1.36 / (radius_au ** 2)

def satellite_power(radius_au):
    intensity = solar_intensity(radius_au)
    area_m2 = SATELLITE_AREA * 1e6
    gross_power = intensity * area_m2 * CELL_EFFICIENCY / 1e6
    net_power = gross_power * (1 - COOLING_POWER) * LASER_EFFICIENCY * TRANSMISSION_EFFICIENCY
    return gross_power, net_power

# ============================================================
# 3. 主程式
# ============================================================

print("=" * 60)
print("戴森蜂群 - 發電量與軌道力學模擬")
print(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

orbital_shells = [(0.20, 200), (0.25, 400), (0.30, 400)]
total_satellites = sum(n for _, n in orbital_shells)

print(f"\n[1] 衛星總數: {total_satellites:,} 個")
print("\n[2] 各軌道殼層參數:")
print("-" * 60)
print(f"{'半徑 (AU)':<12} {'週期 (日)':<12} {'速度 (km/s)':<14} {'輻射 (kW/m²)':<14} {'衛星數量':<10}")
print("-" * 60)

total_gross_power = 0.0
total_net_power = 0.0

for r, n in orbital_shells:
    period = orbital_period(r)
    vel = orbital_velocity(r)
    intensity = solar_intensity(r)
    gross, net = satellite_power(r)
    total_gross_power += gross * n
    total_net_power += net * n
    print(f"{r:<12.2f} {period:<12.1f} {vel:<14.1f} {intensity:<14.2f} {n:<10,}")

print("-" * 60)

# 人類用量倍數
human_ratio = total_net_power / HUMAN_ENERGY_GW
print(f"\n[3] 總發電量:")
print(f"   毛功率: {total_gross_power:,.0f} GW")
print(f"   淨功率: {total_net_power:,.0f} GW")
print(f"   每年發電量: {total_net_power * 24 * 365 / 1000:,.0f} TWh")
print(f"   人類目前用量倍數: {human_ratio:.2f} 倍")

# 成本分析
COST_PER_SATELLITE = 1.5e9
TOTAL_INVESTMENT = total_satellites * COST_PER_SATELLITE
TOTAL_INVESTMENT_B = TOTAL_INVESTMENT / 1e9
ENERGY_PRICE = 30
annual_energy_mwh = total_net_power * 1000 * 24 * 365
annual_revenue = annual_energy_mwh * ENERGY_PRICE
annual_revenue_B = annual_revenue / 1e9
payback_years = TOTAL_INVESTMENT / annual_revenue

print(f"\n[4] 成本與經濟分析:")
print(f"   每個衛星成本: ${COST_PER_SATELLITE/1e9:.2f}B")
print(f"   總投資: ${TOTAL_INVESTMENT_B:.0f}B")
print(f"   每年收入: ${annual_revenue_B:.0f}B")
print(f"   回報期: {payback_years:.2f} 年")

# 太陽能量收集
collected_fraction = total_net_power / SUN_OUTPUT_GW
print(f"\n[5] 太陽能量收集:")
print(f"   收集比例: {collected_fraction*100:.6f}%")
print(f"   目標 0.2% 進度: {collected_fraction/0.002*100:.2f}%")

# 儲存結果
with open("dyson_swarm_simulation_results.txt", "w", encoding="utf-8") as f:
    f.write(f"戴森蜂群 - 發電量與軌道力學模擬結果\n")
    f.write(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("=" * 60 + "\n")
    f.write(f"衛星總數: {total_satellites:,} 個\n")
    f.write(f"淨功率: {total_net_power:,.0f} GW\n")
    f.write(f"人類用量倍數: {human_ratio:.2f} 倍\n")
    f.write(f"總投資: ${TOTAL_INVESTMENT_B:.0f}B\n")
    f.write(f"回報期: {payback_years:.2f} 年\n")
    f.write(f"太陽收集比例: {collected_fraction*100:.6f}%\n")

print("\n✅ 結果已儲存至: dyson_swarm_simulation_results.txt")
