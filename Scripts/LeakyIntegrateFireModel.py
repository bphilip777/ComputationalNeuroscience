import sys
import numpy as np
import matplotlib.pyplot as plt
# np.set_printoptions(threshold=sys.maxsize)  # for debugging

tau_m = 10e-3  # ms
Cm = 100e-12  # Farads
Gl = 10e-9  # Siemens = Cm / tau_m
El = -70e-3  # Volts
Vth = -50e-3  # Volts
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

plt.show()

# Increasing the current increases the firing frequency b/c the current increases the driving force making the potential reach threshold quicker = more frequently = increased firing rate
