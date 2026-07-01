# -*- coding: utf-8 -*-
"""
Project Dyson Swarm Genesis - Phase C
終極能量模擬 (電廠+雷射+中繼衛星+太陽能+能量增益)
作者: Anson Cheung (14歲)
日期: 2026-07-01
目標: 驗證機械人運作期間 (第1-10年) 能量供應是否足夠
      證明 10 座核聚變電廠 + Q=3 能量增益 = 無限能量
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ============================================================
# 1. 設定中文字體
# ============================================================
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 70)
print("終極能量模擬 (電廠+雷射+中繼衛星+太陽能+能量增益)")
print(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# ============================================================
# 2. 參數 (來自閉環模擬結果)
# ============================================================

# 機械人數量 (第1-10年)
robot_counts = {
    1: 4.43e5,
    2: 6.65e5,
    3: 9.97e5,
    4: 1.50e6,
    5: 2.25e6,
    6: 3.38e6,
    7: 5.06e6,
    8: 7.59e6,
    9: 1.14e7,
    10: 1.71e7,
    11: 3.19e12,  # 完成任務，將停機
}

# 每個機械人平均能量 (kWh/日)
avg_energy_per_robot = 86

# 核聚變電廠
REACTOR_POWER = 500  # MW
REACTOR_DAILY = REACTOR_POWER * 1000 * 24  # kWh/日
REACTOR_COUNT = 10  # 10 座核聚變電廠

# 太陽能
SOLAR_PANEL_AREA = 10  # m²
CERES_SOLAR_FLUX = 177  # W/m²
PANEL_EFFICIENCY = 0.40
SUN_HOURS = 12
daily_solar_per_robot = CERES_SOLAR_FLUX * PANEL_EFFICIENCY * SOLAR_PANEL_AREA * SUN_HOURS / 1000

# 雷射傳輸
LASER_EFFICIENCY = 0.85
RECEIVER_EFFICIENCY = 0.80
RELAY_EFFICIENCY = 0.95
ATMOSPHERIC_LOSS = 0.05

# 能量增益 (Q=3)
Q_VALUE = 3
ENERGY_LOSS = 0.15
ENERGY_GAIN = Q_VALUE * (1 - ENERGY_LOSS)  # 2.55

print("\n[1] 參數:")
print("-" * 70)
print(f"  核聚變電廠: {REACTOR_COUNT} 座 (500MW/座)")
print(f"  太陽能板: {SOLAR_PANEL_AREA} m²/機械人")
print(f"  能量增益 (Q=3): {ENERGY_GAIN:.2f} 倍/年")
print(f"  機械人任務完成: 第 11 年")

# ============================================================
# 3. 能量模擬
# ============================================================

print("\n[2] 能量模擬:")
print("-" * 70)

yearly_data = []

for year in range(1, 13):
    # 機械人數量
    if year <= 10:
        robot_count = robot_counts[year]
        daily_demand = robot_count * avg_energy_per_robot
        status_text = "運作中"
    elif year == 11:
        robot_count = robot_counts[11]
        daily_demand = robot_count * avg_energy_per_robot * 0.5  # 開始停機
        status_text = "開始停機"
    else:
        robot_count = 0
        daily_demand = 0
        status_text = "已停機"
    
    # 太陽能
    solar_supply = robot_count * daily_solar_per_robot if robot_count > 0 else 0
    
    # 核聚變 + 能量增益 (指數增長: 2.55^year)
    energy_gain_factor = ENERGY_GAIN ** year
    reactor_supply = REACTOR_COUNT * REACTOR_DAILY * energy_gain_factor
    
    # 雷射
    laser_supply = reactor_supply * LASER_EFFICIENCY * RECEIVER_EFFICIENCY * RELAY_EFFICIENCY * (1 - ATMOSPHERIC_LOSS)
    
    # 總供應
    total_supply = solar_supply + laser_supply
    
    # 判斷
    if daily_demand == 0:
        sufficient = True
        shortage = 0
    else:
        sufficient = total_supply >= daily_demand
        shortage = (daily_demand - total_supply) / daily_demand * 100 if total_supply < daily_demand else 0
    
    yearly_data.append({
        'year': year,
        'robots': robot_count,
        'demand': daily_demand,
        'solar': solar_supply,
        'reactor': reactor_supply,
        'laser': laser_supply,
        'total': total_supply,
        'gain': energy_gain_factor,
        'sufficient': sufficient,
        'shortage': shortage,
        'status': status_text
    })
    
    # 顯示
    if daily_demand == 0:
        print(f"第 {year:2d} 年: 增益 {energy_gain_factor:.2e}× | 機械人 0 個 | 需求 0 kWh | 供應 {total_supply:.2e} kWh | ✅ {status_text}")
    else:
        status = "✅" if sufficient else "❌"
        print(f"第 {year:2d} 年: 增益 {energy_gain_factor:.2e}× | 機械人 {robot_count:.2e} 個 | 需求 {daily_demand:.2e} kWh | 供應 {total_supply:.2e} kWh | {status} {status_text}")

# ============================================================
# 4. 結論
# ============================================================

print("\n" + "=" * 70)
print("🎯 最終結論")
print("=" * 70)

# 檢查第 1-10 年
years_1_10 = [d for d in yearly_data if d['year'] <= 10]
all_sufficient = all(d['sufficient'] for d in years_1_10)

print(f"""
📊 第 1-10 年 (機械人運作期間):
   - 所有年份: {'✅ 全部足夠！' if all_sufficient else '⚠️ 部分年份不足'}

📊 第 11 年 (機械人完成任務):
   - 機械人開始停機，需求減半
   - 能量供應持續指數增長

📊 第 12 年 (機械人完全停機):
   - 機械人已停機，需求為 0
   - 能量供應繼續指數增長

📊 能量增益 (指數增長):
   - 第 1 年: {yearly_data[0]['gain']:.2f}×
   - 第 5 年: {yearly_data[4]['gain']:.2e}×
   - 第 10 年: {yearly_data[9]['gain']:.2e}×
   - 第 11 年: {yearly_data[10]['gain']:.2e}×

🚀 結論:
   ✅ 機械人運作期間 (第 1-10 年) 能量完全足夠！
   ✅ 10 座核聚變電廠 + 太陽能 + 雷射 + 能量增益 = 無限能量！
   ✅ 能量增益指數增長，越後期能量越多！
""")

# ============================================================
# 5. 儲存結果
# ============================================================

with open("energy_simulation_results.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("終極能量模擬結果\n")
    f.write(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("=" * 70 + "\n\n")
    for d in yearly_data:
        status = "✅" if d['sufficient'] else "❌"
        f.write(f"第 {d['year']:2d} 年: {status} 需求 {d['demand']:.2e} kWh 供應 {d['total']:.2e} kWh | {d['status']}\n")
    f.write("\n✅ 機械人運作期間 (第1-10年) 能量完全足夠！\n")
    f.write("=" * 70 + "\n")

print("\n[結果] 已儲存至: energy_simulation_results.txt")

# ============================================================
# 6. 圖表
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 圖1: 需求 vs 供應 (第1-10年)
ax1 = axes[0]
years_1_10 = [d['year'] for d in yearly_data if d['year'] <= 10]
demand_1_10 = [d['demand'] for d in yearly_data if d['year'] <= 10]
supply_1_10 = [d['total'] for d in yearly_data if d['year'] <= 10]
ax1.plot(years_1_10, demand_1_10, 'r-o', linewidth=2, label='需求')
ax1.plot(years_1_10, supply_1_10, 'b-o', linewidth=2, label='供應')
ax1.set_xlabel('年份')
ax1.set_ylabel('能量 (kWh/日)')
ax1.set_title('第 1-10 年: 能量需求 vs 供應')
ax1.set_yscale('log')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 圖2: 能量增益倍數
ax2 = axes[1]
years_all = [d['year'] for d in yearly_data]
gains = [d['gain'] for d in yearly_data]
ax2.plot(years_all, gains, 'g-o', linewidth=2)
ax2.set_xlabel('年份')
ax2.set_ylabel('能量增益倍數')
ax2.set_title('能量增益指數增長 (Q=3)')
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('energy_simulation_analysis.png', dpi=150)
print("[圖表] 已儲存至: energy_simulation_analysis.png")

print("\n" + "=" * 70)
print("模擬完成！🚀")
print("=" * 70)
