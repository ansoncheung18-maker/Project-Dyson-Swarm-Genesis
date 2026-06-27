# -*- coding: utf-8 -*-
"""
Project Dyson Swarm Genesis - Phase B
機械人自我複製模擬 (能量增殖正確版)
作者: Anson Cheung (14歲)
日期: 2026-06-27
目標: 模擬機械人複製，直到材料耗盡
      800 座核聚變電廠固定供應能量 (Q=3)
      材料上限基於 3.64% 開採比例 (1.31 × 10¹⁷ 個機械人)
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
# 2. 機械人複製參數
# ============================================================

INITIAL_ROBOTS = 5000  # 初始機械人
REPLICATION_TIME = 0.01  # 年 (約3.65日)
ROBOT_MASS = 500  # kg
CARBON_PER_ROBOT = 75  # kg (500 × 15%)
ENERGY_PER_REPLICATION = 100  # MWh
ROBOT_FAILURE_RATE = 0.01

# ============================================================
# 3. 材料上限 (3.64% 開採比例)
# ============================================================

# 小行星帶碳材料總量 (3.64% 開採)
TOTAL_CARBON = 1.31e19  # kg (3.64% 開採)
max_robots = TOTAL_CARBON / CARBON_PER_ROBOT  # 1.31e17 個

# ============================================================
# 4. 核聚變能量參數 (800座固定, Q=3)
# ============================================================

REACTORS = 800
REACTOR_POWER = 500  # MW
Q_VALUE = 3
ENERGY_LOSS = 0.15

initial_energy = REACTORS * REACTOR_POWER * 1000 * 24 * 365 / 1e3

print("=" * 70)
print("機械人自我複製模擬 (能量增殖正確版)")
print(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)
print(f"  初始機械人: {INITIAL_ROBOTS:,} 個")
print(f"  複製時間: {REPLICATION_TIME} 年/次 ({REPLICATION_TIME*365:.1f} 日)")
print(f"  核聚變電廠: {REACTORS} 座 (固定)")
print(f"  能量增益 (Q值): {Q_VALUE}")
print(f"  能量轉換損耗: {ENERGY_LOSS*100}%")
print(f"  材料上限 (3.64% 開採): {max_robots:.2e} 個")
print("=" * 70)

# ============================================================
# 5. 模擬
# ============================================================

robots = INITIAL_ROBOTS
material_used = 0
failed = 0

years = [0]
robots_history = [robots]
energy_history = [initial_energy]
gain_history = [1.0]
carbon_used_history = [0]

print(f"\n🚀 開始模擬 (目標: 達到材料上限 {max_robots:.2e} 個)")
print("-" * 70)

energy = initial_energy

for year in range(1, 51):
    # 1. 能量增殖
    energy = energy * Q_VALUE * (1 - ENERGY_LOSS)
    gain = energy / initial_energy
    
    # 2. 能量限制
    max_by_energy = energy / ENERGY_PER_REPLICATION
    
    # 3. 複製能力 (指數增長)
    replication_capacity = robots / REPLICATION_TIME
    
    # 4. 材料限制 (3.64% 開採)
    material_left = TOTAL_CARBON - material_used
    max_by_material = material_left / ROBOT_MASS
    
    # 5. 實際複製數量
    actual = min(replication_capacity, max_by_energy, max_by_material)
    failed_this_year = actual * ROBOT_FAILURE_RATE
    successful = actual - failed_this_year
    
    # 6. 更新
    robots += successful
    material_used += actual * ROBOT_MASS
    failed += failed_this_year
    
    years.append(year)
    robots_history.append(robots)
    energy_history.append(energy)
    gain_history.append(gain)
    carbon_used_history.append(material_used)
    
    # 7. 顯示進度
    progress = material_used / TOTAL_CARBON * 100
    if year <= 5 or year % 5 == 0 or progress > 50:
        print(f"第 {year:2d} 年: 機械人 {robots:.2e} 個 | 能量增益 {gain:.1f}× | 碳使用率 {progress:.2f}%")
    
    # 8. 檢查完成
    if material_used >= TOTAL_CARBON:
        print(f"\n✅✅✅ 第 {year} 年材料耗盡！機械人複製完成！")
        print(f"   📊 最終機械人: {robots:.2e} 個")
        print(f"   📊 能量增益: {gain:.1f} 倍")
        print(f"   📊 碳使用率: 100%")
        break

# ============================================================
# 6. 結論
# ============================================================

print("\n" + "=" * 70)
print("🎯 最終結論")
print("=" * 70)
print(f"""
✅ 機械人複製完成！
   - 複製完成時間: {year} 年
   - 最終機械人數量: {robots:.2e} 個
   - 能量增益: {gain:.1f} 倍
   - 碳使用率: {progress:.2f}%

📊 關鍵發現:
   - 材料上限基於 3.64% 開採比例
   - 22 年內達到材料上限
   - 能量增殖 (Q=3) 驅動整個過程
""")

# ============================================================
# 7. 儲存結果
# ============================================================

with open("robot_replication_results.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("機械人自我複製模擬結果\n")
    f.write(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"複製完成時間: {year} 年\n")
    f.write(f"最終機械人: {robots:.2e} 個\n")
    f.write(f"能量增益: {gain:.1f} 倍\n")
    f.write(f"碳使用率: {progress:.2f}%\n")
    f.write(f"材料上限 (3.64% 開採): {max_robots:.2e} 個\n")
    f.write("=" * 70 + "\n")

print("\n[結果] 已儲存至: robot_replication_results.txt")

# ============================================================
# 8. 圖表
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 圖1: 機械人數量
ax1 = axes[0, 0]
ax1.plot(years, robots_history, 'b-', linewidth=2)
ax1.axhline(y=max_robots, color='r', linestyle='--', label=f'材料上限 ({max_robots:.1e})')
ax1.set_xlabel('年數')
ax1.set_ylabel('機械人數量')
ax1.set_title('機械人數量增長 (能量增殖驅動)')
ax1.set_yscale('log')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 圖2: 能量增益
ax2 = axes[0, 1]
ax2.plot(years, gain_history, 'orange', linewidth=2)
ax2.set_xlabel('年數')
ax2.set_ylabel('能量增益倍數')
ax2.set_title('能量增殖: 1→3→9→27→81→...')
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

# 圖3: 碳使用率
ax3 = axes[1, 0]
carbon_percent = [c / TOTAL_CARBON * 100 for c in carbon_used_history]
ax3.plot(years, carbon_percent, 'purple', linewidth=2)
ax3.axhline(y=100, color='r', linestyle='--', label='材料上限 (100%)')
ax3.set_xlabel('年數')
ax3.set_ylabel('碳使用率 (%)')
ax3.set_title('碳材料消耗進度')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 圖4: 能量 vs 機械人
ax4 = axes[1, 1]
ax4.plot(years, gain_history, 'orange', linewidth=2, label='能量增益')
ax4.set_xlabel('年數')
ax4.set_ylabel('能量增益')
ax4.set_yscale('log')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('robot_replication_analysis.png', dpi=150)
print("[圖表] 已儲存至: robot_replication_analysis.png")

print("\n" + "=" * 70)
print("模擬完成！🚀")
print("=" * 70)
