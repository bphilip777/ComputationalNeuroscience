import matplotlib
import numpy as np
import math

t0, tEnd = 0, 0.5
dt = 1e-4
nTims = int((tEnd-t0)/dt)+1
t = np.linspace(t0, tEnd, nTims)
V0 = np.asarray([-50, -70, -80])*10**-3
V = np.zeros((len(V0), nTims))
tau_m = 10e-3  # 10 ms

# Initialize V[0]
for i, v in enumerate(V0):
    V[i][0] = v

for i, v in enumerate(V0):
    for timestep in range(1, nTims):
        V[i][timestep] = V[i][timestep] + (V[i][timestep-1] - v) * math.exp(- t[timestep]/tau_m)

print(V[0])