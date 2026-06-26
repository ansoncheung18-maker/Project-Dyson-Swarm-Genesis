# -*- coding: utf-8 -*-
"""
Project Dyson Swarm Genesis - 機械人指數增長模擬
作者: Anson Cheung (14歲)
日期: 2026-06-26
目標: 模擬機械人自我複製同製造衛星嘅指數增長過程
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

# ============================================================
# 2. 常數定義
# ============================================================

SUN_OUTPUT_GW = 3.846e26 / 1e9
TARGET_FRACTION = 0.002
TARGET_POWER_GW = SUN_OUTPUT_GW * TARGET_FRACTION
HUMAN_ENERGY_GW = 2.0e13 / 1e9
SAT_NET_POWER_GW = 10.2  # 每個衛星淨功率 (GW)

# ============================================================
# 3. 指數增長模型
# ============================================================

def simulate_growth(seed_robots, years, replication_time, build_time, label):
    """模擬機械人指數增長"""
    robots = seed_robots
    satellites = 0
    year_history = [0]
    robot_history = [robots]
    satellite_history = [satellites]
    power_history = [0]
    
    print(f"\n--- {label} ---")
    print(f"初始機械人: {seed_robots} 個")
    print(f"複製時間: {replication_time} 年, 製造時間: {build_time} 年")
    
    for year in range(1, years + 1):
        # 機械人複製
        robots += robots / replication_time
        # 機械人製造衛星
        satellites += robots / build_time
        power = satellites * SAT_NET_POWER_GW
        
        year_history.append(year)
        robot_history.append(robots)
        satellite_history.append(satellites)
        power_history.append(power)
        
        if power >= TARGET_POWER_GW:
            print(f"✅ 第 {year} 年達到目標!")
            print(f"   機械人數量: {robots:,.0f} 個")
            print(f"   衛星數量: {satellites:,.0f} 個")
            print(f"   總功率: {power/1e6:.2f} 百萬 GW")
            print(f"   人類用量倍數: {power/HUMAN_ENERGY_GW:,.0f} 倍")
            break
    else:
        print(f"⚠️ 第 {years} 年仍未達到目標")
        print(f"   機械人數量: {robots:,.0f} 個")
        print(f"   衛星數量: {satellites:,.0f} 個")
        print(f"   總功率: {power/1e6:.2f} 百萬 GW")
    
    return {
        'label': label,
        'years': year_history,
        'robots': robot_history,
        'satellites': satellite_history,
        'power': power_history,
        'final_year': year,
        'final_power': power,
        'target_reached': power >= TARGET_POWER_GW
    }

# ============================================================
# 4. 運行三種情境
# ============================================================

print("=" * 60)
print("戴森蜂群 - 機械人指數增長模擬")
print(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

scenarios = [
    (0.5, 1.0, "基本情境 (複製 0.5 年, 製造 1 年)"),
    (0.3, 0.5, "進階情境 (複製 0.3 年, 製造 0.5 年)"),
    (1.0, 2.0, "保守情境 (複製 1.0 年, 製造 2.0 年)")
]

results = {}
for rep, build, label in scenarios:
    results[label] = simulate_growth(100, 50, rep, build, label)

# ============================================================
# 5. 儲存結果
# ============================================================

output_lines = []
output_lines.append("=" * 60)
output_lines.append("戴森蜂群 - 機械人指數增長模擬結果")
output_lines.append(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
output_lines.append("=" * 60)
output_lines.append("")
output_lines.append(f"目標: 0.2% 太陽能量 ({TARGET_POWER_GW/1e6:.0f} 百萬 GW)")
output_lines.append(f"每個衛星淨功率: {SAT_NET_POWER_GW:.1f} GW")
output_lines.append("")

for label, result in results.items():
    output_lines.append("-" * 60)
    output_lines.append(label)
    output_lines.append("-" * 60)
    output_lines.append(f"達到目標所需年數: {result['final_year']} 年")
    output_lines.append(f"最終衛星數量: {result['satellites'][-1]:,.0f} 個")
    output_lines.append(f"最終機械人數量: {result['robots'][-1]:,.0f} 個")
    output_lines.append(f"最終發電量: {result['final_power']/1e6:.2f} 百萬 GW")
    output_lines.append(f"人類用量倍數: {result['final_power']/HUMAN_ENERGY_GW:,.0f} 倍")
    output_lines.append(f"目標達成: {'✅ 是' if result['target_reached'] else '❌ 否'}")
    output_lines.append("")

with open("dyson_swarm_exponential_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("\n[結果] 已儲存至: dyson_swarm_exponential_results.txt")

# ============================================================
# 6. 生成圖表
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 圖1: 衛星數量增長 (三種情境對比)
ax1 = axes[0, 0]
colors = ['blue', 'green', 'red']
for (label, result), color in zip(results.items(), colors):
    ax1.plot(result['years'], result['satellites'], label=label, color=color, linewidth=2)
ax1.axhline(y=TARGET_POWER_GW/SAT_NET_POWER_GW, color='black', linestyle='--', label='目標衛星數量')
ax1.set_xlabel('年數')
ax1.set_ylabel('衛星數量 (個)')
ax1.set_title('衛星數量指數增長 (三種情境)')
ax1.set_yscale('log')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 圖2: 發電量增長
ax2 = axes[0, 1]
for (label, result), color in zip(results.items(), colors):
    ax2.plot(result['years'], [p/1e6 for p in result['power']], label=label, color=color, linewidth=2)
ax2.axhline(y=TARGET_POWER_GW/1e6, color='black', linestyle='--', label=f'目標 {TARGET_FRACTION*100}%')
ax2.axhline(y=HUMAN_ENERGY_GW/1e6, color='orange', linestyle=':', label='人類目前用量')
ax2.set_xlabel('年數')
ax2.set_ylabel('發電量 (百萬 GW)')
ax2.set_title('發電量增長 (三種情境)')
ax2.set_yscale('log')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 圖3: 機械人數量增長 (基本情境)
ax3 = axes[1, 0]
basic_result = results["基本情境 (複製 0.5 年, 製造 1 年)"]
ax3.plot(basic_result['years'], basic_result['robots'], color='purple', linewidth=2)
ax3.set_xlabel('年數')
ax3.set_ylabel('機械人數量 (個)')
ax3.set_title('機械人數量指數增長 (基本情境)')
ax3.set_yscale('log')
ax3.grid(True, alpha=0.3)

# 圖4: 衛星 vs 機械人 (基本情境)
ax4 = axes[1, 1]
ax4.plot(basic_result['years'], basic_result['satellites'], label='衛星', color='blue', linewidth=2)
ax4.plot(basic_result['years'], basic_result['robots'], label='機械人', color='red', linewidth=2)
ax4.set_xlabel('年數')
ax4.set_ylabel('數量 (個)')
ax4.set_title('衛星 vs 機械人數量 (基本情境)')
ax4.set_yscale('log')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('dyson_swarm_exponential_growth.png', dpi=150)
print("[圖表] 已儲存至: dyson_swarm_exponential_growth.png")

print("\n" + "=" * 60)
print("模擬 2 完成！")
print("=" * 60)
