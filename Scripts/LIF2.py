import numpy as np
import matplotlib.pyplot as plt

# Cell params
El = -70e-3
Rm = 5e6
Cm = 2e-9

Vth = -50e-3
Vreset = -65e-3

Iapp = np.asarray([3, 5]) * 10**-9
nIs = len(Iapp)

# Time vector
t0, tEnd = 0, 2
dt = 1e-3  # If resolution is too small, you get weird answers
nTims = int((tEnd - t0) / dt + 1)
t = np.linspace(t0, tEnd, nTims)

# Voltages
V = np.zeros((nIs, nTims))
S = V.copy()  # Spikes
for i in range(nIs):
    V[i][0] = El

# Currents
Ith = (Vth - El) / Rm
# print(f"Minimum Current to Fire {round(Ith*10**9)} nA")
I = np.zeros((nIs, nTims))
tIdx = np.logical_and(t >= 0.5, t <= 0.7)
for j in range(nIs):
    I[j][tIdx] = Iapp[j]

for j in range(nIs):
    for i in range(1, nTims):
        dV = dt * ((El - V[j][i-1]) / Rm + I[j][i]) / Cm
        V[j][i] = V[j][i-1] + dV
        if V[j][i] > Vth:
            V[j][i] = Vreset
            S[j][i] = 1

'''
fig, axs = plt.subplots(3, nIs)
for i in range(nIs):
    axs[0, i].plot(t, I[i])
    axs[0, i].set_ylim([0, max(Iapp)+1e-9])

    axs[1, i].plot(t, V[i])
    axs[2, i].plot(t, S[i])
    if i == 0:
        axs[0, i].set_ylabel("Current, nA")
        axs[1, i].set_ylabel("Voltage, mV")
        axs[2, i].set_ylabel("Spikes")
    axs[2, i].set_xlabel("Time, s")
axs[0, 0].set_title("Below Ith")
axs[0, 1].set_title("Above Ith")
plt.show()
'''


nTrials = 200
Iapp2 = np.linspace(4, 6, nTrials)*10**-9

V2 = np.zeros((nTrials, nTims))
Vm_ss = El + Iapp2 * Rm
tau_m = Rm * Cm
ISI2 = np.zeros(nTrials)
ISI3 = ISI2.copy()
Neural_Frequency = ISI2.copy()
Neural_Frequency2 = ISI3.copy()

den = Vm_ss - Vth
num = Vm_ss - Vreset
bdIdx = den <= 0
gdIdx = np.invert(bdIdx)
ISI2[bdIdx] = np.nan
ISI2[gdIdx] = tau_m * np.log(num[gdIdx] / den[gdIdx])
Neural_Frequency[bdIdx] = np.nan
Neural_Frequency[gdIdx] = 1 / ISI2[gdIdx]

left = tau_m * np.log(Iapp2 * Rm + El - Vreset)
right = tau_m * np.log(Iapp2 * Rm + El - Vth)
bdIdx = np.bitwise_or(np.isinf(left), np.isinf(right))
gdIdx = np.invert(bdIdx)
ISI3[bdIdx] = np.nan
ISI3[gdIdx] = left[gdIdx] - right[gdIdx]
Neural_Frequency2[bdIdx] = np.nan
Neural_Frequency2[gdIdx] = 1/ISI3[gdIdx]

# f-I curve
fig, axs = plt.subplots(1)
axs.plot(Neural_Frequency, Iapp2, 'b-')
axs.plot(Neural_Frequency2, Iapp2, 'k--')
axs.set_xlabel("Frequency, Hz")
axs.set_ylabel("Current, nA")
axs.set_title("F-I Curve")
plt.show()
