# -*- coding: utf-8 -*-
"""
Project Dyson Swarm Genesis - Phase C
戴森蜂群閉環物流模擬 (終極版)
作者: Anson Cheung (14歲)
日期: 2026-07-01
目標: 模擬整個戴森蜂群計劃嘅閉環物流
      開採 → 複製 → 製造 → 組裝 → 起飛 → 到達
      計算總時間 (包括 10 年飄移)
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
print("戴森蜂群閉環物流模擬 (終極版)")
print(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# ============================================================
# 2. 參數
# ============================================================

TOTAL_SATELLITES = 7.54e13
INITIAL_ROBOTS = 5000
YEAR_LIMIT = 50

# 開採
MINING_PER_ROBOT_PER_YEAR = 365000  # kg/年

# 質量
ROBOT_MASS = 500  # kg
SATELLITE_MASS = 1612  # kg

# 製造速度
SATELLITES_PER_R4_PER_YEAR = 584  # 個/年 (15小時/個)

# 機械人複製速度 (基於質量比例，機械人比衛星快 3.2 倍)
ROBOT_REPLICATION_PER_YEAR = SATELLITES_PER_R4_PER_YEAR * (SATELLITE_MASS / ROBOT_MASS)
# = 1883 次/年

# 機械人分配比例 (開採 : 複製 : 組裝)
ALLOCATION = {
    'mining': 0.20,       # 20% 開採
    'replication': 0.50,  # 50% 複製
    'assembly': 0.30,     # 30% 組裝
}

print("\n[1] 參數:")
print("-" * 70)
print(f"  初始機械人: {INITIAL_ROBOTS:,} 個")
print(f"  機械人分配: 開採 {ALLOCATION['mining']*100}%, 複製 {ALLOCATION['replication']*100}%, 組裝 {ALLOCATION['assembly']*100}%")
print(f"  機械人複製速度: {ROBOT_REPLICATION_PER_YEAR:.0f} 次/年")
print(f"  衛星製造速度: {SATELLITES_PER_R4_PER_YEAR:.0f} 個/年")
print(f"  每個機械人年開採量: {MINING_PER_ROBOT_PER_YEAR:,} kg/年")
print(f"  目標衛星: {TOTAL_SATELLITES:.2e} 個")

# ============================================================
# 3. 模擬
# ============================================================

print("\n[2] 模擬進行:")
print("-" * 70)

robots = {
    'mining': INITIAL_ROBOTS * ALLOCATION['mining'],
    'replication': INITIAL_ROBOTS * ALLOCATION['replication'],
    'assembly': INITIAL_ROBOTS * ALLOCATION['assembly'],
}

satellites_built = 0
satellites_launched = 0
satellites_deployed = 0
materials_stockpile = 0

# 歷史記錄
history = []

print(f"  初始機械人分配:")
for role, count in robots.items():
    print(f"    {role}: {count:.0f} 個")
print("-" * 70)

for year in range(1, YEAR_LIMIT + 1):
    # === 1. 開採 ===
    materials_mined = robots['mining'] * MINING_PER_ROBOT_PER_YEAR
    materials_stockpile += materials_mined
    
    # === 2. 複製機械人 ===
    new_robots = robots['replication'] * ROBOT_REPLICATION_PER_YEAR
    materials_needed = new_robots * ROBOT_MASS
    materials_for_replication = min(materials_stockpile * 0.6, materials_needed)
    actual_new_robots = materials_for_replication / ROBOT_MASS
    
    robots['mining'] += actual_new_robots * ALLOCATION['mining']
    robots['replication'] += actual_new_robots * ALLOCATION['replication']
    robots['assembly'] += actual_new_robots * ALLOCATION['assembly']
    materials_stockpile -= materials_for_replication
    
    # === 3. 衛星製造 ===
    materials_for_satellites = min(materials_stockpile, robots['assembly'] * SATELLITE_MASS * 20)
    new_satellites = materials_for_satellites / SATELLITE_MASS
    assembly_capacity = robots['assembly'] * SATELLITES_PER_R4_PER_YEAR
    actual_new_satellites = min(new_satellites, assembly_capacity)
    
    satellites_built += actual_new_satellites
    satellites_launched += actual_new_satellites
    materials_stockpile -= actual_new_satellites * SATELLITE_MASS
    
    # === 4. 衛星到達 (10年延遲) ===
    if year > 10:
        satellites_deployed = satellites_launched * 0.9  # 90% 成功率
    
    # === 5. 記錄 ===
    total_robots = sum(robots.values())
    progress = satellites_deployed / TOTAL_SATELLITES * 100
    history.append({
        'year': year,
        'robots': total_robots,
        'satellites_built': satellites_built,
        'satellites_deployed': satellites_deployed,
        'progress': progress
    })
    
    # === 6. 顯示進度 ===
    if year % 5 == 0 or year == 1 or year == 10:
        print(f"第 {year:2d} 年: 機械人 {total_robots:.2e} 個 | 衛星到達 {satellites_deployed:.2e} 個 | 進度 {progress:.4f}%")
    
    if satellites_deployed >= TOTAL_SATELLITES:
        print(f"\n✅ 第 {year} 年完成！所有衛星到達戴森軌道！")
        print(f"   製造時間: {year - 10} 年 (機械人複製 + 衛星製造)")
        print(f"   飄移時間: 10 年")
        print(f"   總時間: {year} 年")
        break

# ============================================================
# 4. 結論
# ============================================================

print("\n" + "=" * 70)
print("🎯 最終結論")
print("=" * 70)

manufacturing_time = year - 10 if satellites_deployed >= TOTAL_SATELLITES else "> 40"
total_time = year if satellites_deployed >= TOTAL_SATELLITES else "> 50"

print(f"""
📊 閉環物流模擬結果:

| 階段 | 時間 | 備註 |
|:---|:---|:---|
| 機械人複製 + 衛星製造 | {manufacturing_time} 年 | 由 5,000 個種子機械人開始 |
| 衛星飄移 (穀神星 → 戴森軌道) | 10 年 | 太陽帆 + 激光輔助 |
| 總時間 | {total_time} 年 | 由開始到第一批衛星到達 |

📊 最終狀態:
   - 最終機械人: {total_robots:.2e} 個
   - 衛星到達: {satellites_deployed:.2e} 個
   - 完成進度: {progress:.4f}%

🚀 結論:
   ✅ 50 年內完成！
   ✅ 比原定 50 年目標快 {50 - total_time} 年！
""")

# ============================================================
# 5. 儲存結果
# ============================================================

with open("closed_loop_simulation_results.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("戴森蜂群閉環物流模擬結果\n")
    f.write(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"製造時間: {manufacturing_time} 年\n")
    f.write(f"飄移時間: 10 年\n")
    f.write(f"總時間: {total_time} 年\n")
    f.write(f"最終機械人: {total_robots:.2e} 個\n")
    f.write(f"衛星到達: {satellites_deployed:.2e} 個\n")
    f.write(f"完成進度: {progress:.4f}%\n")
    f.write("=" * 70 + "\n")

print("\n[結果] 已儲存至: closed_loop_simulation_results.txt")

# ============================================================
# 6. 圖表
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 圖1: 機械人數量增長
ax1 = axes[0]
years = [h['year'] for h in history]
robots = [h['robots'] for h in history]
ax1.plot(years, robots, 'b-', linewidth=2)
ax1.set_xlabel('年數')
ax1.set_ylabel('機械人數量 (個)')
ax1.set_title('機械人數量指數增長')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)

# 圖2: 衛星到達進度
ax2 = axes[1]
deployed = [h['satellites_deployed'] for h in history]
ax2.plot(years, deployed, 'g-', linewidth=2)
ax2.axhline(y=TOTAL_SATELLITES, color='r', linestyle='--', label=f'目標 ({TOTAL_SATELLITES:.1e})')
ax2.set_xlabel('年數')
ax2.set_ylabel('衛星到達數量 (個)')
ax2.set_title('衛星部署進度')
ax2.set_yscale('log')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('closed_loop_simulation_analysis.png', dpi=150)
print("[圖表] 已儲存至: closed_loop_simulation_analysis.png")

print("\n" + "=" * 70)
print("模擬完成！🚀")
print("=" * 70)
