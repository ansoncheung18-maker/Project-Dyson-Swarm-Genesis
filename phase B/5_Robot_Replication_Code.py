# -*- coding: utf-8 -*-
"""
Project Dyson Swarm Genesis - 機械人複製模擬 (能量增殖正確版)
作者: Anson Cheung (14歲)
日期: 2026-06-27
核心邏輯: 核聚變能量自我增殖 (1→3→9→27→81...)
          電廠數量固定，但可用能量指數增長！
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ============================================================
# 1. 設定
# ============================================================

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 機械人參數
INITIAL_ROBOTS = 5000
REPLICATION_TIME = 0.01  # 年 (約3.65日)
ROBOT_MASS = 500  # kg
CARBON_PER_ROBOT = 75  # kg (500 × 15%)
ENERGY_PER_REPLICATION = 100  # MWh (複製一個機械人)
ROBOT_FAILURE_RATE = 0.01

# 材料
TOTAL_CARBON = 1.13e19  # kg
max_robots = TOTAL_CARBON / CARBON_PER_ROBOT  # 1.51e17

# 核聚變能量參數 (固定電廠，能量增殖!)
REACTORS = 800
REACTOR_POWER = 500  # MW
Q_VALUE = 3  # 能量增益
ENERGY_LOSS = 0.15  # 轉換損耗

# 初始能量 (每年)
initial_energy = REACTORS * REACTOR_POWER * 1000 * 24 * 365 / 1e3

print("=" * 70)
print("🔋 核聚變能量增殖 (正確版)")
print("=" * 70)
print(f"  核聚變電廠: {REACTORS} 座 (固定)")
print(f"  每座功率: {REACTOR_POWER} MW")
print(f"  初始每年能量: {initial_energy:.2e} MWh")
print(f"  能量增益 (Q值): {Q_VALUE}")
print(f"  能量轉換損耗: {ENERGY_LOSS*100}%")
print("=" * 70)
print(f"📦 材料上限: {max_robots:.2e} 個機械人")
print("=" * 70)

# ============================================================
# 2. 能量增殖計算
# ============================================================

def calculate_energy_gain(initial_energy, years, Q, loss):
    """計算能量增殖: 1→3→9→27→81..."""
    energy = initial_energy
    energy_history = [energy]
    gain_history = [1.0]
    
    for year in range(1, years + 1):
        # 能量增殖! 用現有能量 × Q × (1-損耗)
        energy = energy * Q * (1 - loss)
        energy_history.append(energy)
        gain_history.append(energy / initial_energy)
    
    return energy_history, gain_history

# ============================================================
# 3. 機械人複製模擬 (能量增殖驅動)
# ============================================================

def simulate_robot_replication_with_energy_gain():
    """機械人複製，由能量增殖驅動"""
    
    robots = INITIAL_ROBOTS
    material_used = 0
    failed = 0
    
    # 能量增殖歷史
    energy_history = [initial_energy]
    gain_history = [1.0]
    
    # 機械人歷史
    years = [0]
    robots_history = [robots]
    
    print(f"\n🚀 初始機械人: {INITIAL_ROBOTS:,} 個")
    print(f"⚡ 複製時間: {REPLICATION_TIME} 年/次 ({REPLICATION_TIME*365:.1f} 日)")
    print("-" * 70)
    
    for year in range(1, 51):  # 模擬50年
        # 1. 計算今年可用能量 (能量增殖!)
        current_energy = energy_history[-1] * Q_VALUE * (1 - ENERGY_LOSS)
        energy_history.append(current_energy)
        gain = current_energy / initial_energy
        gain_history.append(gain)
        
        # 2. 能量限制 (每年可複製幾多機械人)
        max_by_energy = current_energy / ENERGY_PER_REPLICATION
        
        # 3. 複製能力 (指數增長)
        replication_capacity = robots / REPLICATION_TIME
        
        # 4. 材料限制
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
        
        # 7. 顯示進度 (每年顯示)
        progress = material_used / TOTAL_CARBON * 100
        if year <= 10 or year % 5 == 0 or progress > 0.1:
            print(f"第 {year:2d} 年: 機械人 {robots:.2e} 個 | 能量增益 {gain:.1f}× | 材料進度 {progress:.6f}%")
        
        # 8. 檢查完成
        if material_used >= TOTAL_CARBON:
            print(f"\n✅✅✅ 第 {year} 年材料耗盡！機械人複製完成！")
            print(f"   📊 最終機械人: {robots:.2e} 個")
            print(f"   📊 能量增益: {gain:.1f} 倍")
            print(f"   📊 材料使用率: 100%")
            return years, robots_history, energy_history, gain_history, year, robots, gain
    
    print(f"\n⚠️ 第 {year} 年仍未完成")
    print(f"   📊 機械人: {robots:.2e} 個")
    print(f"   📊 材料進度: {progress:.6f}%")
    return years, robots_history, energy_history, gain_history, year, robots, gain

# ============================================================
# 4. 執行模擬
# ============================================================

years, robots_history, energy_history, gain_history, final_year, final_robots, final_gain = simulate_robot_replication_with_energy_gain()

# ============================================================
# 5. 結論
# ============================================================

print("\n" + "=" * 70)
print("🎯 最終結論 (能量增殖正確版)")
print("=" * 70)
print(f"""
✅ 機械人複製完成！
   - 複製完成時間: {final_year} 年
   - 最終機械人數量: {final_robots:.2e} 個
   - 能量增益: {final_gain:.1f} 倍

🔥 能量增殖循環 (Q=3) 成功！
   1× → 3× → 9× → 27× → 81× → 243× → 729× ...
   電廠數量固定 (800 座)，但可用能量指數增長！

📊 關鍵發現:
   - 頭幾年能量增殖較慢，因為機械人數量唔夠多
   - 當機械人數量增加後，能量消耗加快，材料開始被消耗
   - 最終材料喺 {final_year} 年內耗盡
""")

# ============================================================
# 6. 儲存結果
# ============================================================

with open("robot_replication_energy_gain_correct.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("機械人複製模擬結果 (能量增殖正確版)\n")
    f.write(f"執行日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"複製完成時間: {final_year} 年\n")
    f.write(f"最終機械人: {final_robots:.2e} 個\n")
    f.write(f"能量增益: {final_gain:.1f} 倍\n")
    f.write("\n")
    f.write("能量增殖路徑: 1→3→9→27→81→243→729→...\n")
    f.write("電廠數量固定 (800 座)，但可用能量指數增長！\n")
    f.write("=" * 70 + "\n")

print("\n[結果] 已儲存至: robot_replication_energy_gain_correct.txt")

# ============================================================
# 7. 圖表
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

# 圖3: 材料使用
ax3 = axes[1, 0]
material_percent = [m / TOTAL_CARBON * 100 for m in [0] + [min(1, i/len(years)) for i in range(1, len(years))]]
ax3.plot(years, material_percent[:len(years)], 'purple', linewidth=2)
ax3.set_xlabel('年數')
ax3.set_ylabel('材料使用率 (%)')
ax3.set_title('材料消耗進度')
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
plt.savefig('robot_replication_energy_gain_correct.png', dpi=150)
print("[圖表] 已儲存至: robot_replication_energy_gain_correct.png")

print("\n" + "=" * 70)
print("模擬完成！🚀")
print("=" * 70)
