import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def inductionMotorVfControl(dictionary, fe):
    # Access the variables stored in the dictionary
    V10 = dictionary['Input rated voltage (V)']
    n = dictionary['Number of phases']
    poles = dictionary['Number of poles']
    R1 = dictionary['Stator resistance']
    X10 = dictionary['Rated stator reactance']
    X20 = dictionary['Rated referred rotor reactance']
    Xm0 = dictionary['Rated leakage inductance']
    R2 = dictionary['Referred rotor resistance']
    fe0 = dictionary['Rated supply frequency']

    # Calculating the reactance and voltage values under different frequency
    X1 = X10 * (fe / fe0)
    X2 = X20 * (fe / fe0)
    Xm = Xm0 * (fe / fe0)
    V1 = V10 * (fe / fe0)

    V1_eq = np.abs(V1 * 1j * Xm / (R1 + 1j * (X1 + Xm)))

    # Define the slip array
    start, step, end = 0, 0.01, 100
    s = start + np.arange(0, end) * step + 0.00001

    # Calculate the speed values
    omegas = 4 * np.pi * fe / poles
    ns = 120 * fe / poles
    rpm = ns * (1 - s)

    # Calculate the torque
    Tmech = (1 / omegas) * n * V1_eq ** 2 * (R2 / s) / (((R1 + R2) / s) ** 2 + (X1 + X2) ** 2)

    return rpm, Tmech


variables = {
    'Input rated voltage (V)': 400,
    'Number of phases': 3,
    'Number of poles': 2,
    'Stator resistance': 0.095,
    'Rated stator reactance': 0.68,
    'Rated referred rotor reactance': 0.672,
    'Rated leakage inductance': 18.7,
    'Referred rotor resistance': 0.2,
    'Rated supply frequency': 50
}

applied_frequency = [50, 40, 30, 20, 10]  # Set frequency values
data = {}  # set the empty dictionary

for f in applied_frequency:
    nr, Torque = inductionMotorVfControl(variables, f)
    cache = {'x' + str(f): np.array(nr).flatten(), 'y' + str(f): np.array(Torque).flatten()}
    data.update(cache)
    plt.plot(nr, Torque)

plt.show()

df = pd.DataFrame(data)

df.to_csv("inductionTorqueVf.csv", index=False, header=False)
