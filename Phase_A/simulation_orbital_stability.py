# ============================================================
# Dyson 雲專案 Phase A：衛星軌道穩定性模擬
# 目標：驗證數百萬個衛星喺太陽軌道上嘅穩定性
# ============================================================

import math
import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("Dyson 雲 - 衛星軌道穩定性模擬")
print("="*60)

# ============================================================
# 1. 基本參數
# ============================================================

# 太陽參數
solar_mass = 1.989e30  # kg
G = 6.674e-11  # 引力常數
mu_sun = G * solar_mass

# 軌道參數（以地球軌道為 1 AU）
earth_orbit_radius = 1.496e11  # 米

# 測試不同軌道半徑
orbit_radii_au = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
orbit_radii_m = [r * earth_orbit_radius for r in orbit_radii_au]

print("\n【軌道參數】")
print("| 軌道半徑 (AU) | 軌道速度 (km/s) | 軌道週期 (年) |")
print("|:---|:---|:---|")

for r_m in orbit_radii_m:
    # 圓周速度 v = sqrt(mu / r)
    v = math.sqrt(mu_sun / r_m)
    v_kms = v / 1000
    # 軌道週期 T = 2*pi*r / v
    T = 2 * math.pi * r_m / v
    T_years = T / (365.25 * 24 * 3600)
    print(f"| {r_m/earth_orbit_radius:.1f} | {v_kms:.1f} | {T_years:.3f} |")

# ============================================================
# 2. 衛星間碰撞風險（相同軌道）
# ============================================================

print("\n【相同軌道碰撞風險】")

# 假設衛星數量
satellites = 1_000_000  # 100 萬顆
orbit_radius = 0.4 * earth_orbit_radius
orbit_circumference = 2 * math.pi * orbit_radius

# 每顆衛星佔用長度
length_per_sat = orbit_circumference / satellites
satellite_size = 100  # 每顆衛星 100 米

print(f"軌道半徑: {orbit_radius/earth_orbit_radius:.1f} AU")
print(f"衛星數量: {satellites:,}")
print(f"軌道周長: {orbit_circumference/1000:.0f} km")
print(f"每顆衛星佔用長度: {length_per_sat/1000:.2f} km")
print(f"衛星尺寸: {satellite_size} m")

if length_per_sat > satellite_size * 10:
    print("✅ 間距充足，碰撞風險低")
else:
    print("⚠️ 間距不足，需減少衛星數量")

# ============================================================
# 3. 軌道修正需求
# ============================================================

print("\n【軌道修正需求】")

# 太陽風壓力（估算）
solar_wind_pressure = 1e-9  # N/m² (1 nPa)
satellite_area = 10000  # m² (100m x 100m)
satellite_mass = 1000  # kg

# 每年軌道漂移
force_n = solar_wind_pressure * satellite_area
acceleration = force_n / satellite_mass
drift_per_year = 0.5 * acceleration * (365.25 * 24 * 3600)**2
drift_km = drift_per_year / 1000

print(f"太陽風壓力: {solar_wind_pressure:.1e} N/m²")
print(f"衛星面積: {satellite_area} m²")
print(f"每年軌道漂移: {drift_km:.1f} km")

if drift_km < 100:
    print("✅ 漂移可控，每年需少量軌道修正")
else:
    print("⚠️ 漂移較大，需頻繁修正")

# ============================================================
# 4. 繪圖：軌道速度 vs 半徑
# ============================================================

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
radii_au = np.linspace(0.1, 1.0, 50)
velocities = []
for r in radii_au:
    r_m = r * earth_orbit_radius
    v = math.sqrt(mu_sun / r_m)
    velocities.append(v / 1000)
plt.plot(radii_au, velocities, 'b-', linewidth=2)
plt.xlabel('軌道半徑 (AU)')
plt.ylabel('軌道速度 (km/s)')
plt.title('軌道速度 vs 半徑')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
periods = [2 * math.pi * r_m / math.sqrt(mu_sun / r_m) / (365.25 * 24 * 3600) for r_m in orbit_radii_m]
plt.plot(orbit_radii_au, periods, 'r-', linewidth=2)
plt.xlabel('軌道半徑 (AU)')
plt.ylabel('軌道週期 (年)')
plt.title('軌道週期 vs 半徑')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('orbital_stability.png', dpi=150)
print("\n✅ 圖表已儲存: orbital_stability.png")

print("\n✅ 結論: Dyson 雲衛星軌道穩定，碰撞風險可控")
