import sys
import numpy as np
import matplotlib.pyplot as plt
# np.set_printoptions(threshold=sys.maxsize)  # for debugging

tau_m = 10e-3  # ms
Cm = 100e-12  # Farads
Gl = 10e-9  # Siemens = Cm / tau_m
El = -70e-3  # Volts
Vth = -50e-3  # Volts - change this to -40e-3 and nothing will fire b/c threshold > Vm_ss
Vreset = -80e-3  # Volts
Iapp = np.asarray([180e-12, 210e-12, 240e-12])

dt = 1e-4
t0, tEnd = 0, 0.5
nTims = int((tEnd-t0)/dt + 1)
t = np.linspace(t0, tEnd, nTims)

# Initialize Currents
currents = np.zeros((len(Iapp), nTims))
current_on_idx = np.bitwise_and(t >= t0 + 0.2, t <= t0 + 0.3)

for i, ia in enumerate(Iapp):
    currents[i][current_on_idx] = ia

# Initialize voltages
V = np.zeros((len(Iapp), nTims))
spikes = V.copy()
for i in range(len(Iapp)):
    V[i][0] = El

# Compute new voltages
for i, ia in enumerate(Iapp):
    for j in range(1, nTims):
        V[i][j] = V[i][j-1] + dt * ((El - V[i][j-1])*Gl + currents[i][j]) / Cm  # Super important that it's equilibrium - voltage
        if V[i][j] > Vth:
            V[i][j] = Vreset
            spikes[i][j] = 1


'''
# Visualize
fig, axs = plt.subplots(3, 3)
for i in range(len(Iapp)):
    axs[0, i].plot(t, currents[i])
    axs[0, i].set_xlim([t0, tEnd])
    axs[0, i].set_ylim([0, 300e-12])

    axs[1, i].plot(t, V[i])
    axs[1, i].set_xlim([t0, tEnd])
    axs[1, i].set_ylim([-90e-3, -40e-3])

    axs[2, i].plot(t, spikes[i])
    axs[2, i].set_xlim([t0, tEnd])
    axs[2, i].set_ylim([0, 1])

    if i == 0:
        axs[0, 0].set_ylabel("Iapp, nA")
        axs[1, 0].set_ylabel("Voltage, mV")
        axs[2, 0].set_ylabel("Spikes")

plt.show()
'''

# Increasing the current increases the firing frequency b/c the current increases the driving force making the potential reach threshold quicker = more frequently = increased firing rate
Vm_ss = (El + Iapp / Gl)
# print(f"Steady State Membrane Voltages {Vm_ss*1000} mVs")
# Neurons fire if membrane voltage's steady state is greater than threshold voltage
Ith = round(Gl*(Vth - El), 11)
# print(f"Current threshold: {Ith} A")

# Fix applied current
currents2 = np.ones((len(Iapp), nTims)).T * Iapp
currents2 = currents2.T

# Compute steady-state decay
V2 = np.zeros((len(Iapp), nTims))
for i, ia in enumerate(Iapp):
    V2[i] = Vm_ss[i] + (Vreset - Vm_ss[i]) * np.exp(-t/tau_m)

'''
# This figure shows how long it takes each signal to reach Vm_ss given different Vm_ss - the time it takes is the same
fig, axs = plt.subplots(1)
axs.plot(t, V2[0], 'b--')
axs.plot(t, V2[1], 'r--')
axs.plot(t, V2[2], 'k-')
axs.set_xlim([0, 100e-3])
#axs.set_ylim([-60, 0])
plt.show()
'''

# How to calculate the interspike interval
ISI = np.zeros(len(Vm_ss))
neural_firing_rate = ISI.copy()
for i, v in enumerate(ISI):
    num = Vm_ss[i] - Vreset
    den = Vm_ss[i] - Vth
    if den <= 0:
        ISI[i] = np.nan
    else:
        ISI[i] = tau_m * np.log((Vm_ss[i] - Vreset) / (Vm_ss[i] - Vth))

for i, v in enumerate(ISI):
    if not np.isnan(v):
        neural_firing_rate[i] = round(1 / v)
    else:
        neural_firing_rate[i] = np.nan
print(f"Interspike intervals: {ISI}")
print(f"Neural Firing Rates: {neural_firing_rate}")
