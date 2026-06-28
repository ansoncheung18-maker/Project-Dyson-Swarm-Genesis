# -*- coding: utf-8 -*-
"""
Project Dyson Swarm Genesis - 發電量與軌道力學模擬
作者: Anson Cheung (14歲)
日期: 2026-06-26
目標: 計算衛星喺唔同軌道半徑嘅發電量、軌道參數、成本回報
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
HUMAN_ENERGY_GW = 2.0e13 / 1e9  # 人類目前用量 (GW) = 20,000 GW

# 衛星參數 (來自之前專案)
SATELLITE_AREA = 1.0  # km²
CELL_EFFICIENCY = 0.40  # 40% 高效率太陽能電池
LASER_EFFICIENCY = 0.90  # DC → 雷射 效率
TRANSMISSION_EFFICIENCY = 0.85  # 雷射傳輸效率
COOLING_POWER = 0.05  # 冷卻系統耗電 (~5%)

# ============================================================
# 2. 軌道力學函數
# ============================================================

def orbital_period(radius_au):
    """計算軌道週期 (日)"""
    radius_m = radius_au * AU
    period_sec = 2 * math.pi * math.sqrt(radius_m**3 / MU_SUN)
    return period_sec / 86400

def orbital_velocity(radius_au):
    """計算軌道速度 (km/s)"""
    radius_m = radius_au * AU
    v = math.sqrt(MU_SUN / radius_m)
    return v / 1000

def solar_intensity(radius_au):
    """計算太陽輻射強度 (kW/m²)"""
    return 1.36 / (radius_au ** 2)

def satellite_power(radius_au):
    """計算單個衛星發電量 (GW)"""
    intensity = solar_intensity(radius_au)  # kW/m²
    area_m2 = SATELLITE_AREA * 1e6  # 1 km² = 1,000,000 m²
    gross_power = intensity * area_m2 * CELL_EFFICIENCY / 1e6  # GW
    net_power = gross_power * (1 - COOLING_POWER) * LASER_EFFICIENCY * TRANSMISSION_EFFICIENCY
    return gross_power, net_power

# ============================================================
# 3. 主程式
# ============================================================

print("=" * 60)
print("戴森蜂群 - 發電量與軌道力學模擬")
print(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# 軌道殼層定義: (半徑 AU, 衛星數量)
orbital_shells = [
    (0.20, 200),   # 內層
    (0.25, 400),   # 中層
    (0.30, 400),   # 外層
]

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
print(f"   毛功率 (太陽能電池輸出): {total_gross_power:,.0f} GW")
print(f"   淨功率 (傳輸到地球後):   {total_net_power:,.0f} GW")
print(f"   每年發電量:             {total_net_power * 24 * 365 / 1000:,.0f} TWh")
print(f"   人類目前用量倍數:        {human_ratio:.2f} 倍")

# ============================================================
# 4. 成本與經濟分析
# ============================================================

COST_PER_SATELLITE = 1.5e9  # 每個衛星成本 (美元)
TOTAL_INVESTMENT = total_satellites * COST_PER_SATELLITE
TOTAL_INVESTMENT_B = TOTAL_INVESTMENT / 1e9

ENERGY_PRICE = 30  # 每 MWh 批發價 (美元)
annual_energy_mwh = total_net_power * 1000 * 24 * 365  # MWh/年
annual_revenue = annual_energy_mwh * ENERGY_PRICE  # 美元
annual_revenue_B = annual_revenue / 1e9  # 十億美元

payback_years = TOTAL_INVESTMENT / annual_revenue

print(f"\n[4] 成本與經濟分析:")
print(f"   每個衛星成本:           ${COST_PER_SATELLITE/1e9:.2f}B")
print(f"   總投資 (第一階段):      ${TOTAL_INVESTMENT_B:.0f}B")
print(f"   每年收入:               ${annual_revenue_B:.0f}B")
print(f"   回報期:                 {payback_years:.2f} 年")

# ============================================================
# 5. 太陽能量收集比例
# ============================================================

collected_fraction = total_net_power / SUN_OUTPUT_GW
print(f"\n[5] 太陽能量收集:")
print(f"   收集太陽能量比例:      {collected_fraction*100:.6f}%")
print(f"   目標 0.2% 進度:        {collected_fraction/0.002*100:.2f}%")

# ============================================================
# 6. 儲存結果
# ============================================================

output_lines = []
output_lines.append("=" * 60)
output_lines.append("戴森蜂群 - 發電量與軌道力學模擬結果")
output_lines.append(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
output_lines.append("=" * 60)
output_lines.append("")
output_lines.append(f"[1] 衛星總數: {total_satellites:,} 個")
output_lines.append("")
output_lines.append("[2] 各軌道殼層參數:")
output_lines.append(f"{'半徑 (AU)':<12} {'週期 (日)':<12} {'速度 (km/s)':<14} {'輻射 (kW/m²)':<14} {'衛星數量':<10}")
for r, n in orbital_shells:
    period = orbital_period(r)
    vel = orbital_velocity(r)
    intensity = solar_intensity(r)
    output_lines.append(f"{r:<12.2f} {period:<12.1f} {vel:<14.1f} {intensity:<14.2f} {n:<10,}")
output_lines.append("")
output_lines.append("[3] 總發電量:")
output_lines.append(f"    毛功率: {total_gross_power:,.0f} GW")
output_lines.append(f"    淨功率: {total_net_power:,.0f} GW")
output_lines.append(f"    每年發電量: {total_net_power * 24 * 365 / 1000:,.0f} TWh")
output_lines.append(f"    人類目前用量倍數: {human_ratio:.2f} 倍")
output_lines.append("")
output_lines.append("[4] 成本與經濟分析:")
output_lines.append(f"    每個衛星成本: ${COST_PER_SATELLITE/1e9:.2f}B")
output_lines.append(f"    總投資: ${TOTAL_INVESTMENT_B:.0f}B")
output_lines.append(f"    每年收入: ${annual_revenue_B:.0f}B")
output_lines.append(f"    回報期: {payback_years:.2f} 年")
output_lines.append("")
output_lines.append("[5] 太陽能量收集:")
output_lines.append(f"    收集比例: {collected_fraction*100:.6f}%")
output_lines.append(f"    目標 0.2% 進度: {collected_fraction/0.002*100:.2f}%")
output_lines.append("")
output_lines.append("=" * 60)

with open("dyson_swarm_simulation_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("\n[6] 結果已儲存至: dyson_swarm_simulation_results.txt")

# ============================================================
# 7. 生成圖表
# ============================================================

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 圖1: 軌道距離 vs 太陽輻射強度
radii = np.linspace(0.1, 0.5, 50)
intensities = [solar_intensity(r) for r in radii]

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(radii, intensities, 'b-', linewidth=2)
plt.axvline(0.2, color='r', linestyle='--', label='內層 (0.2 AU)')
plt.axvline(0.25, color='g', linestyle='--', label='中層 (0.25 AU)')
plt.axvline(0.3, color='orange', linestyle='--', label='外層 (0.3 AU)')
plt.xlabel('軌道半徑 (AU)')
plt.ylabel('太陽輻射強度 (kW/m²)')
plt.title('太陽輻射強度 vs 軌道距離')
plt.legend()
plt.grid(True, alpha=0.3)

# 圖2: 各軌道殼層發電量
shell_labels = [f"{r} AU" for r, _ in orbital_shells]
powers = []
for r, n in orbital_shells:
    _, net = satellite_power(r)
    powers.append(net * n)

plt.subplot(1, 2, 2)
bars = plt.bar(shell_labels, powers, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
plt.xlabel('軌道殼層')
plt.ylabel('淨功率 (GW)')
plt.title('各軌道殼層發電量')
for bar, power in zip(bars, powers):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'{power:.0f} GW', ha='center', va='bottom')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('dyson_swarm_analysis.png', dpi=150)
print("\n[7] 圖表已儲存至: dyson_swarm_analysis.png")

print("\n" + "=" * 60)
print("模擬 1 完成！")
print("=" * 60)
