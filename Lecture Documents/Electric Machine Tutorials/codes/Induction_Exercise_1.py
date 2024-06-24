import numpy as np
from prettytable import PrettyTable


def unit(value, scale):
    if scale == "u":
        return value * 10**6
    if scale == "k":
        return value * 10**(-3)


# Exercise 1 ---------------------------------------

# (i) Find the efficiency (eta) of an induction motor operating at full load.
# The machine details are given as following:

# Equivalent Circuit....

# o----Rs---jXs--o--jXr----
#                |         |
#              -----       |
#             |     |      |
# V_in       Rc    jXm    Rr/s
#             |     |      |
#              _____       |
#                |         |
# o--------------o---------

# GIVEN PARAMETERS ---------------------------------
V_in = 2300  # input voltage (wye connection)
P_vent = 0  # ventilation power loos
P = 4  # number of poles
f_s = 50  # supply frequency
s = 0.03746  # slip value
R_s, R_r, R_c = 0.02, 0.12, 451.2
X_s, X_r, X_m = 0.32, 0.32, 50.00
# --------------------------------------------------
# The equivalent circuit of the induction motor is utilised to solve the problem. First, calculate the equivalent input
# impedance (Z_in) of the induction motor. This is achieved by finding the equivalent impedance between the magnetising
# and core-loss resistance, and then the combined impedance of this with the rotor impedance is found, which, when added
# to the stator impedance, gives the equivalent impedance of the induction machine.

# --------------------------------------------------
# CIRCUIT CALCULATION
# --------------------------------------------------

# Magnetising-branch equivalent impedance:
Z_mag = 1j * X_m * R_c / (R_c + 1j * X_m)
# Rotor impedance
Z_r = R_r / s + 1j * X_r
# Equivalent rotor and magnetising impedance:
Z_eq = Z_mag * Z_r / (Z_mag + Z_r)
# Motor Equivalent Impedance
Z_in = R_s + 1j * X_s + Z_eq
# Phase Input Voltage (Remember! it is a wye connection)
V_phase = V_in / np.sqrt(3)
# Stator Current:
I_s = V_phase / Z_in
# Rotor Current:
I_r = I_s / (1 + Z_r / Z_mag)
# Core Loss Current:
I_c = (I_s - I_r) * Z_mag / R_c

# --------------------------------------------------
# SPEED CALCULATION
# --------------------------------------------------

# Stator angular speed:
w_s = 2 * np.pi * f_s
# Rotor angular speed:
w_r = (1 - s) * w_s

# --------------------------------------------------
# POWER/TORQUE/EFFICIENCY CALCULATION
# --------------------------------------------------

# Air-gap torque
T_air = 3 * P / 2 * np.abs(I_r)**2 * R_r / (s * w_s)
# Shaft Power
P_shaft = 3 * np.abs(I_r)**2 * R_r * (1 - s) / s
# Shaft Power
T_shaft = P_shaft / w_r
# Input Power
P_in = unit(3 * V_in * np.real(I_s), "k")
# Stator Copper Losses
P_stator = unit(3 * np.abs(I_s)**2 * R_s, "k")
# Stator Copper Losses
P_rotor = unit(3 * np.abs(I_r)**2 * R_r, "k")
# Core Losses
P_core = unit(3 * np.abs(I_c)**2 * R_c, "k")

# Specify the Column Names while initializing the Table
Results = PrettyTable(["Definition", "Symbol", "Value", "Unit"])
Results.align["Definition"] = "r"
Results.align["Symbol"] = "c"

# Add rows
Results.title = 'Results for Exercise 1 (i)'
Results.add_row(["Magnetising imp.", "Z_0", Z_mag, "Ohm"])
Results.add_row(["Rotor imp.", "Z_r", Z_r, "Ohm"])
Results.add_row(["Eq. rotor & magnetising imp.", "Z_eq", Z_eq, "Ohm"])
Results.add_row(["Eq. machine imp.", "Z_in", Z_in, "Ohm"])
Results.add_row(
    ["****************************", "************", "****", "****"])
Results.add_row(["Phase Input Voltage", "V_in", V_phase, "Volt"])
Results.add_row(["Stator Current", "I_s", I_s, "A"])
Results.add_row(["Rotor Current", "I_r", I_s, "A"])
Results.add_row(
    ["****************************", "************", "****", "****"])
Results.add_row(["Stator angular speed", "w_s", w_s, "rad/s"])
Results.add_row(["Rotor angular speed", "w_r", w_r, "rad/s"])
Results.add_row(
    ["****************************", "************", "****", "****"])
Results.add_row(["Air-gap torque:", "T_air", T_air, "N.m"])
Results.add_row(["Shaft Power", "P_shaft", unit(P_shaft, "k"), "kW"])
Results.add_row(["Shaft Torque", "T_shaft", T_shaft, "N.m"])
Results.add_row(["Real Power", "P_in", P_in, "kW"])
Results.add_row(["Stator Copper Losses", "P_stator", P_stator, "kW"])
Results.add_row(["Rotor Copper Losses", "P_rotor", P_rotor, "kW"])
Results.add_row(["Core Losses", "P_core", P_core, "kW"])

print(Results)

# (ii) The principle of power-factor improvement with capacitor installation at the machine stator terminals is based on
# the capacitor's drawing a leading reactive current from the supply to cancel the lagging reactive current drawn by the
# induction machine. In order for the line power factor to be unity, the reactive component of the line current must be
# zero. The reactive line current is the sum of the capacitor and induction machine reactive currents. Therefore, the
# capacitive reactive current (I_cap) has to be equal in magnitude but opposite in direction to the machine lagging
# reactive current, but the machine reactive current is the imaginary part of the stator current and is given by;

I_cap = -1j * np.imag(I_s)

C = I_cap / (1j * w_s * V_phase)

Results = PrettyTable(["Definition", "Symbol", "Value", "Unit"])
Results.align["Definition"] = "r"
Results.align["Symbol"] = "c"

Results.title = 'Results for Exercise 1 (ii)'
Results.add_row(["Capacitor Current", "I_cap", I_cap, "A"])
Results.add_row(["Rotor imp.", "Z_r", unit(C, "u"), "uF"])

print(Results)
