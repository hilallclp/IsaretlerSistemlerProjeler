
import numpy as np
import matplotlib.pyplot as plt

# Frekanslar
f1 = 87
f2 = 43.5
f3 = 870

# Periyotlar
T1 = 1 / f1
T2 = 1 / f2
T3 = 1 / f3

# Zaman aralıkları
t1 = np.linspace(0, 0.035, 2000)
t2 = np.linspace(0, 0.07, 2000)
t3 = np.linspace(0, 0.0035, 2000)

# Sinyaller
y1 = np.sin(2 * np.pi * f1 * t1)
y2 = np.sin(2 * np.pi * f2 * t2)
y3 = np.sin(2 * np.pi * f3 * t3)

plt.figure(figsize=(12, 8))

# 1. Grafik
plt.subplot(3, 1, 1)
plt.plot(t1, y1)
plt.title(f"f1 = 87 Hz  |  T = {T1:.5f} s")
plt.xlabel("Zaman (s)")
plt.ylabel("Genlik")
plt.grid(True)

# 2. Grafik
plt.subplot(3, 1, 2)
plt.plot(t2, y2)
plt.title(f"f2 = 43.5 Hz  |  T = {T2:.5f} s")
plt.xlabel("Zaman (s)")
plt.ylabel("Genlik")
plt.grid(True)

# 3. Grafik
plt.subplot(3, 1, 3)
plt.plot(t3, y3)
plt.title(f"f3 = 870 Hz  |  T = {T3:.5f} s")
plt.xlabel("Zaman (s)")
plt.ylabel("Genlik")
plt.grid(True)

plt.tight_layout()
plt.show()
