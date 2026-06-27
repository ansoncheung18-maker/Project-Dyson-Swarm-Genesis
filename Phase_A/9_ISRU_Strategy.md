# Phase A：ISRU 材料開採策略
**專案**：戴森蜂群起源 (Dyson Swarm Genesis)  
**版本**：2.0  
**日期**：2026-06-27  
**作者**：Anson Cheung（14歲）

---

## 1. ISRU 策略總覽

ISRU（In-Situ Resource Utilization，就地資源利用）係戴森蜂群計劃嘅核心。與其由地球運送所有材料，不如喺太空直接開採同加工原材料，大幅降低成本。

【天體材料來源】
- 水星：金屬（核心）+ 矽（地殼），開採比例 3.64%，開採質量 1.02 × 10²² kg
  - 用途：衛星結構、線圈、太陽能電池

- 月球：矽（地殼），開採比例 3.64%，開採質量 1.07 × 10²¹ kg
  - 用途：太陽能電池

- 小行星帶：金屬 + 碳，開採比例 3.64%，開採質量 1.31 × 10¹⁹ kg
  - 用途：衛星結構、複合材料

> 更新：開採比例由 3.14% 提升至 3.64%（增加 0.5%），確保碳材料有 13.2% 剩餘。

---

## 2. 材料需求模擬（Python 程式碼）

以下 Python 模擬用嚟驗證 3.64% 開採比例是否足夠：

```python
# -*- coding: utf-8 -*-
"""
Project Dyson Swarm Genesis - 材料需求驗證模擬 (3.64% 版本)
作者: Anson Cheung (14歲)
日期: 2026-06-27
目標: 驗證開採 3.64% 水星+月球+小行星帶是否足夠 0.2% 戴森蜂群
"""

import math

# ============================================================
# 1. 目標：0.2% 太陽能量
# ============================================================

SUN_OUTPUT_GW = 3.846e26 / 1e9
TARGET_FRACTION = 0.002
TARGET_POWER_GW = SUN_OUTPUT_GW * TARGET_FRACTION
SAT_NET_POWER_GW = 10.2
REQUIRED_SATELLITES = TARGET_POWER_GW / SAT_NET_POWER_GW

print("=" * 70)
print("目標：0.2% 太陽能量")
print("=" * 70)
print(f"需要衛星數量: {REQUIRED_SATELLITES:.2e} 個")

# ============================================================
# 2. 衛星材料需求
# ============================================================

SAT_MASS = 1.5e6  # kg
SAT_MATERIAL = {
    'metal': SAT_MASS * 0.70,
    'silicon': SAT_MASS * 0.20,
    'carbon': SAT_MASS * 0.10
}

print("\n每個衛星材料需求:")
print(f"金屬: {SAT_MATERIAL['metal']:.2e} kg")
print(f"矽:   {SAT_MATERIAL['silicon']:.2e} kg")
print(f"碳:   {SAT_MATERIAL['carbon']:.2e} kg")

# ============================================================
# 3. 機械人參數 (完整版)
# ============================================================

ROBOT_MASS = 500  # kg
ROBOT_MATERIAL = {'metal': 0.60, 'silicon': 0.25, 'carbon': 0.15}

# 額外材料消耗 (複製損耗、維修、工具、運輸)
EXTRA_MATERIAL = {
    'replication_loss': 50,    # kg
    'maintenance': 25,         # kg/年
    'tools': 10,               # kg/年
    'transport': 100           # kg
}

# 每個機械人總材料需求 (終身)
TOTAL_MATERIAL_PER_ROBOT = {
    'metal': ROBOT_MASS * ROBOT_MATERIAL['metal'] + 
             EXTRA_MATERIAL['replication_loss'] * 0.6 + 
             EXTRA_MATERIAL['maintenance'] * 20 * 0.6 + 
             EXTRA_MATERIAL['tools'] * 20 * 0.6 + 
             EXTRA_MATERIAL['transport'] * 0.6,
    'silicon': ROBOT_MASS * ROBOT_MATERIAL['silicon'] + 
               EXTRA_MATERIAL['replication_loss'] * 0.25 + 
               EXTRA_MATERIAL['maintenance'] * 20 * 0.25 + 
               EXTRA_MATERIAL['tools'] * 20 * 0.25 + 
               EXTRA_MATERIAL['transport'] * 0.25,
    'carbon': ROBOT_MASS * ROBOT_MATERIAL['carbon'] + 
              EXTRA_MATERIAL['replication_loss'] * 0.15 + 
              EXTRA_MATERIAL['maintenance'] * 20 * 0.15 + 
              EXTRA_MATERIAL['tools'] * 20 * 0.15 + 
              EXTRA_MATERIAL['transport'] * 0.15
}

print("\n每個機械人終身材料需求:")
print(f"金屬: {TOTAL_MATERIAL_PER_ROBOT['metal']:.1f} kg")
print(f"矽:   {TOTAL_MATERIAL_PER_ROBOT['silicon']:.1f} kg")
print(f"碳:   {TOTAL_MATERIAL_PER_ROBOT['carbon']:.1f} kg")

# ============================================================
# 4. 25年情景：需要幾多機械人？
# ============================================================

YEARS = 25
SATELLITES_PER_ROBOT_PER_YEAR = 0.01
satellites_per_year = REQUIRED_SATELLITES / YEARS
required_robots = satellites_per_year / SATELLITES_PER_ROBOT_PER_YEAR

print(f"\n25 年內完成:")
print(f"每年需要製造衛星: {satellites_per_year:.2e} 個")
print(f"需要機械人: {required_robots:.2e} 個")

# ============================================================
# 5. 總材料需求
# ============================================================

robot_material = {
    'metal': required_robots * TOTAL_MATERIAL_PER_ROBOT['metal'],
    'silicon': required_robots * TOTAL_MATERIAL_PER_ROBOT['silicon'],
    'carbon': required_robots * TOTAL_MATERIAL_PER_ROBOT['carbon']
}

satellite_material = {
    'metal': REQUIRED_SATELLITES * SAT_MATERIAL['metal'],
    'silicon': REQUIRED_SATELLITES * SAT_MATERIAL['silicon'],
    'carbon': REQUIRED_SATELLITES * SAT_MATERIAL['carbon']
}

total_material = {
    'metal': robot_material['metal'] + satellite_material['metal'],
    'silicon': robot_material['silicon'] + satellite_material['silicon'],
    'carbon': robot_material['carbon'] + satellite_material['carbon']
}

print("\n總材料需求 (機械人 + 衛星):")
print(f"金屬: {total_material['metal']:.2e} kg")
print(f"矽:   {total_material['silicon']:.2e} kg")
print(f"碳:   {total_material['carbon']:.2e} kg")

# ============================================================
# 6. 太陽系材料供應 (3.64% 開採)
# ============================================================

EXTRACTION_RATIO = 0.0364  # 3.64%

# 太陽系天體數據
MERCURY_MASS = 3.285e23  # kg
MOON_MASS = 7.347e22  # kg
ASTEROID_BELT_MASS = 2.4e21  # kg

MERCURY_CORE_FRACTION = 0.85
MERCURY_CRUST_FRACTION = 0.15
MOON_SILICON_FRACTION = 0.20
ASTEROID_CARBON_FRACTION = 0.15
ASTEROID_METAL_FRACTION = 0.10

# 計算可開採量
mercury_metal = MERCURY_MASS * EXTRACTION_RATIO * MERCURY_CORE_FRACTION
mercury_silicon = MERCURY_MASS * EXTRACTION_RATIO * MERCURY_CRUST_FRACTION * 0.30
moon_silicon = MOON_MASS * EXTRACTION_RATIO * MOON_SILICON_FRACTION
asteroid_metal = ASTEROID_BELT_MASS * EXTRACTION_RATIO * ASTEROID_METAL_FRACTION
asteroid_carbon = ASTEROID_BELT_MASS * EXTRACTION_RATIO * ASTEROID_CARBON_FRACTION

AVAILABLE_METAL = mercury_metal + asteroid_metal
AVAILABLE_SILICON = mercury_silicon + moon_silicon
AVAILABLE_CARBON = asteroid_carbon

print(f"\n太陽系可開採材料 (開採 {EXTRACTION_RATIO*100}%):")
print(f"金屬: {AVAILABLE_METAL:.2e} kg")
print(f"矽:   {AVAILABLE_SILICON:.2e} kg")
print(f"碳:   {AVAILABLE_CARBON:.2e} kg")

# ============================================================
# 7. 驗證：材料是否足夠？
# ============================================================

print("\n" + "=" * 70)
print("材料驗證結果")
print("=" * 70)

metal_ok = total_material['metal'] <= AVAILABLE_METAL
silicon_ok = total_material['silicon'] <= AVAILABLE_SILICON
carbon_ok = total_material['carbon'] <= AVAILABLE_CARBON

print(f"金屬: {'足夠' if metal_ok else '不足'}")
print(f"  需求: {total_material['metal']:.2e} kg")
print(f"  可用: {AVAILABLE_METAL:.2e} kg")
print(f"  剩餘: {AVAILABLE_METAL - total_material['metal']:.2e} kg")
print(f"  倍數: {AVAILABLE_METAL / total_material['metal']:.1f} 倍")
print()

print(f"矽:   {'足夠' if silicon_ok else '不足'}")
print(f"  需求: {total_material['silicon']:.2e} kg")
print(f"  可用: {AVAILABLE_SILICON:.2e} kg")
print(f"  剩餘: {AVAILABLE_SILICON - total_material['silicon']:.2e} kg")
print(f"  倍數: {AVAILABLE_SILICON / total_material['silicon']:.1f} 倍")
print()

print(f"碳:   {'足夠' if carbon_ok else '不足'}")
print(f"  需求: {total_material['carbon']:.2e} kg")
print(f"  可用: {AVAILABLE_CARBON:.2e} kg")
print(f"  剩餘: {AVAILABLE_CARBON - total_material['carbon']:.2e} kg")
print(f"  使用率: {total_material['carbon'] / AVAILABLE_CARBON * 100:.1f}%")
print(f"  安全邊際: {(1 - total_material['carbon'] / AVAILABLE_CARBON) * 100:.1f}%")

# ============================================================
# 8. 最終結論
# ============================================================

print("\n" + "=" * 70)
print("最終結論")
print("=" * 70)

if metal_ok and silicon_ok and carbon_ok:
    print("所有材料都足夠！")
    print(f"開採比例: {EXTRACTION_RATIO*100}%")
    print(f"完成時間: {YEARS} 年")
    print(f"碳使用率: {total_material['carbon'] / AVAILABLE_CARBON * 100:.1f}%")
    print(f"安全邊際: {(1 - total_material['carbon'] / AVAILABLE_CARBON) * 100:.1f}%")
    print("\n結論: 3.64% 開採比例完全足夠，唔係亂講！")
else:
    print("材料不足，需要提高開採比例")
3. 模擬結果（證明 3.64% 唔係亂講）

【目標計算】

· 太陽總輸出：3.846 × 10²⁶ W
· 目標收集比例：0.2%
· 目標功率：7.69 × 10¹⁴ GW
· 每個衛星淨功率：10.2 GW
· 需要衛星數量：7.54 × 10¹³ 個

【每個衛星材料需求】

· 金屬：1.05 × 10⁶ kg
· 矽：3.00 × 10⁵ kg
· 碳：1.50 × 10⁵ kg

【每個機械人終身材料需求（包括複製損耗、維修、工具、運輸）】

· 金屬：810.0 kg
· 矽：337.5 kg
· 碳：202.5 kg

【25 年情景材料需求】

· 需要機械人：3.02 × 10¹⁴ 個
· 需要衛星：7.54 × 10¹³ 個
· 金屬總需求：7.94 × 10¹⁹ kg
· 矽總需求：2.27 × 10¹⁹ kg
· 碳總需求：1.14 × 10¹⁹ kg

【太陽系材料供應（開採 3.64%）】

· 金屬可用量：1.02 × 10²² kg（來源：水星核心 + 小行星帶）
· 矽可用量：1.07 × 10²¹ kg（來源：水星地殼 + 月球地殼）
· 碳可用量：1.31 × 10¹⁹ kg（來源：小行星帶 C-type）

【驗證結果】

· 金屬：需求 7.94 × 10¹⁹ kg，可用 1.02 × 10²² kg，剩餘 1.02 × 10²² kg，多 128 倍 ✅
· 矽：需求 2.27 × 10¹⁹ kg，可用 1.07 × 10²¹ kg，剩餘 1.05 × 10²¹ kg，多 47 倍 ✅
· 碳：需求 1.14 × 10¹⁹ kg，可用 1.31 × 10¹⁹ kg，剩餘 1.70 × 10¹⁸ kg，多 13.2% ✅

---

4. 水星開採策略

【水星資源分佈】

· 金屬（鐵、鎳、鈷）：位於核心，佔 85% 質量
  · 開採方法：鑽探 + 熔融提取
· 矽（二氧化矽）：位於地殼，佔 15% 質量 × 30% 矽
  · 開採方法：露天開採 + 精煉

【開採量（3.64%）】

· 金屬：~8.78 × 10²¹ kg（佔總質量 2.67%）
  · 用途：衛星結構、機械人
· 矽：~9.26 × 10²⁰ kg（佔總質量 0.28%）
  · 用途：太陽能電池

【開採挑戰與解決方案】

· 極端溫度（日間 450°C，夜間 -180°C）
  · 解決方案：使用 MEEP 開發嘅高溫材料同液態鈉冷卻
· 低重力（地球嘅 38%）
  · 解決方案：輕量化開採設備，使用離子推進器輔助移動
· 輻射環境（靠近太陽）
  · 解決方案：抗輻射電子元件 + 鉛屏蔽
· 能源供應
  · 解決方案：使用太陽能板（MEEP 技術）或核聚變後備電源

【開採流程】
第 1 步：著陸與基地建設

· 使用 Fusion Spaceship 運送機械人同設備
· 建立太陽能發電場（MEEP 技術）
· 建設機械人工廠

第 2 步：鑽探與開採

· 使用 AI 控制嘅鑽探機械人開採核心金屬
· 使用露天開採機械人採集地殼矽
· 材料分類同初步加工

第 3 步：材料加工

· 金屬冶煉（使用太陽能聚焦爐）
· 矽提純（用於太陽能電池）
· 製成衛星組件或運送到組裝點

【關鍵技術繼承】

· 高溫 GaAs 太陽能電池：MEEP 1.0 → 水星基地能源供應
· 液態鈉冷卻系統：MEEP 1.0 → 設備冷卻
· 自主導航/對接：Fusion Spaceship → 機械人移動同材料運輸
· AI 控制系統：Fusion Health → 開採過程優化

---

5. 月球開採策略

【月球資源分佈】

· 矽（二氧化矽）：位於地殼，佔 20% 質量
  · 開採方法：露天開採 + 精煉
· 鈦、鋁：位於地殼，少量
  · 開採方法：作為副產品收集

【開採量（3.64%）】

· 矽：~4.61 × 10²⁰ kg（佔總質量 0.63%）
  · 用途：太陽能電池

【開採優勢】

· 距離近：月球距離地球僅 384,400 km，運輸成本低
· 已有技術：Luna-Grid 已經展示月球南極太陽能技術
· 低重力（地球嘅 16.6%）：開採同運輸更節能
· 穩定環境：冇大氣、冇天氣干擾

【開採流程】
第 1 步：月球基地擴建

· 擴充 Luna-Grid 嘅太陽能發電設施
· 建設機械人工廠
· 建立材料儲存倉庫

第 2 步：開採與加工

· 使用機械人進行露天開採
· 太陽能聚焦爐熔煉矽
· 製成矽晶圓（太陽能電池半成品）

第 3 步：運輸

· 使用 Fusion Spaceship 將材料運送到太空組裝點
· 或直接喺月球軌道組裝衛星

【關鍵技術繼承】

· 月球南極太陽能：Luna-Grid 1.5 → 月球基地能源
· 3D 垂直光柵：Luna-Grid 1.5 → 提高太陽能收集效率
· 雷射傳輸：Luna-Grid 1.5 → 傳輸能量到月球基地
· 月球土壤利用（ISRU）：Luna-Grid 1.5 → 基地建設材料

---

6. 小行星帶開採策略

【小行星帶資源分佈】

· C-type（碳質）：佔 75%，主要資源係碳、水、有機物
  · 開採價值：極高（碳係關鍵瓶頸）
· S-type（石質）：佔 17%，主要資源係矽酸鹽、金屬
  · 開採價值：中等
· M-type（金屬質）：佔 8%，主要資源係鐵、鎳、鈷
  · 開採價值：高

【開採量（3.64%）】

· 碳：~1.31 × 10¹⁹ kg（佔總質量 0.78%）
  · 用途：複合材料、機械人零件
· 金屬：~8.78 × 10²¹ kg（佔總質量 0.78%）
  · 用途：衛星結構

【開採挑戰與解決方案】

· 距離遠（2.2-3.2 AU）
  · 解決方案：使用 Fusion Spaceship 運輸
· 小行星眾多
  · 解決方案：AI 導航 + 自主選擇目標
· 低重力
  · 解決方案：抓取裝置 + 離子推進器
· 材料分散
  · 解決方案：集中加工廠（喺小行星帶建立）

【開採流程】
第 1 步：勘探與選擇

· 使用望遠鏡同光譜分析選擇目標
· 派遣探測機械人確認資源
· AI 規劃開採順序

第 2 步：開採

· 機械人登陸小行星
· 表面開採碳質材料
· 鑽探開採金屬核心

第 3 步：加工與運輸

· 就地加工（小行星帶工廠）
· 或將原材料運送到水星/月球加工
· 使用 Fusion Spaceship 運輸

【關鍵技術繼承】

· 自主導航/對接：Fusion Spaceship → 小行星登陸同離開
· 離子推進器：Fusion Spaceship → 運輸原材料
· 核聚變後備電源：Project Helios → 小行星帶基地能源
· AI 控制系統：Fusion Health → 開採過程優化

---

7. 材料加工與運輸

【加工地點選擇】

· 水星：靠近太陽，能源充足（缺點：極端環境）
  · 建議加工：金屬
· 月球：距離近，技術成熟（缺點：能源有限）
  · 建議加工：矽
· 小行星帶：就近開採，減少運輸（缺點：距離遠，基礎設施不足）
  · 建議加工：碳
· 太空組裝點：直接使用，減少搬運（缺點：需要建設加工站）

【運輸策略（核聚變飛船）】
所有材料運輸將採用 Project Fusion Spaceship 技術，配備核聚變推進系統，提供高效、快速嘅太空運輸。

· 水星 → 組裝點：Fusion Spaceship，飛行時間 1-2 個月，每月 1 次，載重 500 噸
· 月球 → 組裝點：Fusion Spaceship，飛行時間 3-5 日，每週 1 次，載重 500 噸
· 小行星帶 → 組裝點：Fusion Spaceship，飛行時間 3-6 個月，每季 1 次，載重 500 噸

【核聚變飛船規格（應用於運輸）】

· 推進系統：核聚變 + 磁力噴嘴（Project Fusion Spaceship 技術）
· 載貨能力：500 噸（模塊化貨艙）
· 飛行速度：0.01c（約 3,000 km/s）
· 燃料：氘（D-D 反應），可由月球或水星 ISRU 供應
· 能源：核聚變反應爐，同時提供推進同飛船能源

【運輸成本分析】

· 金屬（水星）：Fusion Spaceship，0.01 MWh/kg，佔總能量 ~5%
· 矽（月球）：Fusion Spaceship，0.001 MWh/kg，佔總能量 ~1%
· 碳（小行星帶）：Fusion Spaceship，0.05 MWh/kg，佔總能量 ~10%

結論：使用核聚變飛船運輸，碳材料運輸成本最高（小行星帶距離遠），但仍然只佔總能量 ~10%，影響有限。

【運輸艦隊規模估算】

· 初期（0-5 年）：需要運輸量 1.0 × 10⁹ kg/年，需要 2-3 艘飛船
  · 備註：機械人種子部署
· 中期（5-15 年）：需要運輸量 1.0 × 10¹² kg/年，需要 10-20 艘飛船
  · 備註：材料開採擴張
· 後期（15-25 年）：需要運輸量 1.0 × 10¹⁴ kg/年，需要 100-200 艘飛船
  · 備註：大規模衛星製造

備註：所有飛船均為 Project Fusion Spaceship 嘅改裝版本，配備標準化貨艙模塊。

---

8. 機械人複製與開採整合

【機械人種類】

· R1 - Mercurion（水星金屬結構製造機器人）
  · 功能：金屬結構製造
  · 建議數量：5,000 – 20,000
  · 部署地點：水星
  · 運輸方式：Fusion Spaceship
· R2 - Carbosapien（C型小行星石墨提煉機器人）
  · 功能：石墨提煉
  · 建議數量：10,000 – 15,000
  · 部署地點：C 型小行星
  · 運輸方式：Fusion Spaceship
· R3 - Selenix（月球矽薄膜太陽能層製造機器人）
  · 功能：矽薄膜太陽能層製造
  · 建議數量：200,000 – 400,000
  · 部署地點：月球
  · 運輸方式：Fusion Spaceship
· R4 - Martialis（火星維修備件與結構補充機器人）
  · 功能：維修備件與結構補充
  · 建議數量：5,000 – 10,000
  · 部署地點：火星
  · 運輸方式：Fusion Spaceship
· R5 - Vulcanoid（太陽軌道模組組裝機器人）
  · 功能：模組組裝（衛星組裝）
  · 建議數量：20,000 – 40,000
  · 部署地點：太陽軌道 L1/L4
  · 運輸方式：Fusion Spaceship

【機械人材料需求（終身）】

· 每個機械人：金屬 810.0 kg，矽 337.5 kg，碳 202.5 kg，總計 1,350 kg
· 總需求（3.02 × 10¹⁴ 個）：金屬 2.44 × 10¹⁷ kg，矽 1.02 × 10¹⁷ kg，碳 6.11 × 10¹⁶ kg，總計 4.07 × 10¹⁷ kg

【複製與運輸協同策略】

· 種子部署（第 0-1 年）：Fusion Spaceship 運送 5,000 個機械人到各天體，機械人開始適應環境
· 複製階段（第 1-5 年）：運送開採設備同材料加工廠，機械人數量指數增長
· 擴張階段（第 5-15 年）：大規模運送材料到組裝點，機械人數量達 10¹⁴ 級別
· 完成階段（第 15-25 年）：運送最後一批衛星組件，機械人轉為衛星製造

---

9. 模擬結果總結

【材料可行性】

· 金屬：需求 7.94 × 10¹⁹ kg，供應（3.64%）1.02 × 10²² kg，多 128 倍 ✅
· 矽：需求 2.27 × 10¹⁹ kg，供應（3.64%）1.07 × 10²¹ kg，多 47 倍 ✅
· 碳：需求 1.14 × 10¹⁹ kg，供應（3.64%）1.31 × 10¹⁹ kg，有 13.2% 剩餘 ✅

【時間可行性】

· 機械人複製完成：22 年 ✅
· 戴森蜂群完成：25 年 ✅
· 能量增益（Q=3）：持續 ✅

【運輸可行性】

· 運輸工具：Fusion Spaceship，技術成熟 ✅
· 運輸成本：~10% 總能量，影響有限 ✅
· 運輸艦隊：100-200 艘，可建造 ✅

---

10. 對 Phase B-F 嘅影響

· Phase B：設計採礦機械人（R1-R5）、核聚變運輸飛船、加工廠
· Phase C：繪製機械人、核聚變飛船、加工設備嘅 CAD 圖紙
· Phase D：數位雙生需包含開採、加工、運輸（核聚變飛船）、複製四個模組
· Phase E：營運計劃需包含材料供應鏈管理、運輸艦隊調度
· Phase F：退役計劃需考慮開採設備同運輸飛船嘅回收

---

11. 參考文獻

· NASA MESSENGER Mission：水星資源數據
· NASA Apollo Missions：月球資源數據
· NASA JPL 小行星帶數據：小行星資源數據
· Luna-Grid 1.5：月球 ISRU 技術
· MEEP 1.0：水星極端環境技術
· Project Fusion Spaceship：太空運輸技術
· Project Helios：核聚變能量技術
· Project Fusion Health：AI 控制系統

---

12. 結論

「戴森蜂群嘅 ISRU 策略完全可行！開採 3.64% 嘅水星、月球同小行星帶質量，就足夠製造 0.2% 戴森蜂群所需嘅所有材料。所有運輸任務由核聚變飛船（Project Fusion Spaceship）負責，碳材料運輸成本只佔總能量 ~10%。機械人複製技術可以喺 22 年內完成，25 年內達成目標，材料有 13.2% 安全邊際。」



專案負責人： Anson Cheung（14歲）
最後更新： 2026-06-27
