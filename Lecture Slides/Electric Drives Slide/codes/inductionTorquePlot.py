import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

V1 = 230 / np.sqrt(3)

n = 3
poles = 4
fs = 50
R1 = 0.095
X1 = 0.68
X2 = 0.672
Xm = 18.7
R2 = 0.2
omegas = 4 * np.pi * fs / poles
ns = 120 * fs / poles

Z1_eq = 1j * Xm * (R1 + 1j * X1) / (R1 + 1j * (X1 + Xm))
R1_eq = np.real(Z1_eq)
X1_eq = np.imag(Z1_eq)

V1_eq = np.abs(V1 * 1j * Xm / (R1 + 1j * (X1 + Xm)))

start = -3
step = 0.01
num = 600

s = start + np.arange(0, num) * step + 0.00001

rpm = ns * (1 - s)

I2 = np.abs(V1_eq / (Z1_eq + 1j * X2 + R2 / s))
Tmech = n * np.abs(I2) ** 2 * R2 / (s * omegas)

print(s[:-1])

plt.plot(rpm, Tmech)
plt.show()

data = {
    'X': np.array(rpm).flatten(),
    'y': np.array(Tmech).flatten(),
}
df = pd.DataFrame(data)

df.to_csv("inductionTorque.csv", index=False, header=False)
