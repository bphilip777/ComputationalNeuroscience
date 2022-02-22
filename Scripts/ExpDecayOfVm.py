import matplotlib.pyplot as plt
import numpy as np
import math

t0, tEnd = 0, 100e-3  # ms
dt = 1e-3
nTims = int((tEnd-t0)/dt)+1
t = np.linspace(t0, tEnd, nTims)
V0 = np.asarray([-50, -70, -80])*10**-3
V = np.zeros((len(V0), nTims))
V1 = V.copy()
tau_m = 10e-3  # 10 ms
tau_m1 = 20e-3  # Double the time constant
El = -70e-3

# Initialize voltage values
for i, v in enumerate(V0):
    V[i][0] = v
    V1[i][0] = v

# Compute next voltage values
for i in range(len(V0)):
    for j in range(1, nTims):
        V[i][j] = El + (V[i][0] - El) * math.exp(-t[j]/tau_m)  # Here it is important to remember it's the initial voltage - the Leak voltage

for i in range(len(V0)):
    for j in range(1, nTims):
        V1[i][j] = El + (V1[i][0] - El) * math.exp(-t[j]/tau_m1)

fig, axs = plt.subplots(1,3)
axs[0].plot(t, np.exp(-t/tau_m), 'k-')
axs[0].plot(t, np.exp(-t/tau_m1), 'b--')
axs[0].set_xlabel("Time, s")
axs[0].set_ylabel("Voltage, mV")
axs[0].set_title(f"Blue: {tau_m}, Black: {tau_m1}")

axs[1].plot(t, V[0], 'k-')
axs[1].plot(t, V[1], 'k--')
axs[1].plot(t, V[2], 'k-')
axs[1].set_xlabel("Time, s")
axs[1].set_ylabel("Vm, mV")
axs[1].set_ylim([-80e-3, -50e-3])
axs[1].set_xlim([0, 0.05])
axs[1].set_title(f"Tau {tau_m} ms")

axs[2].plot(t, V1[0], 'b-')
axs[2].plot(t, V1[1], 'b--')
axs[2].plot(t, V1[2], 'b-')
axs[2].set_xlabel("Time, s")
axs[2].set_ylabel("Vm, mV")
#axs[2].set_ylim([-80e-3, -50e-3])
#axs[2].set_xlim([0, 0.1])
axs[2].set_title(f"Tau: {tau_m1} ms")

# Show visual
plt.show()

