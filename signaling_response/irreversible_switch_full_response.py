import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp


def ode(t, y, k_0, k_1, k_2, k_3, k_4, K_M3, K_M4, E_T, S):
    dydt = np.array([
        k_0 * y[1] + k_1 * S - k_2 * y[0],
        k_3 * y[0] * (E_T - y[1]) / (K_M3 + E_T - y[1]) - k_4 * (y[1]) / (K_M4 + y[1])
    ])
    return dydt


def goldbeter_koshland(u_1, u_2, J_1, J_2):
    B = u_2 - u_1 + J_1 * u_2 + J_2 * u_1
    return (2 * u_1 * J_2) / (B + np.sqrt(B**2 - 4 * (u_2 - u_1) * u_1 * J_2))


def ode_gk(t, y, k_0, k_1, k_2, k_3, k_4, K_M3, K_M4, E_T, S):
    dydt = np.zeros([1, 1])
    E_p = goldbeter_koshland(k_3*y[0], k_4, K_M3/E_T, K_M4/E_T) * E_T
    dydt[0] = k_0 * E_p + k_1 * S - k_2 * y[0]
    return dydt


# GENERAL PARAMETERS
t_span = [0, 400]  # time span
t_eval = np.linspace(*t_span, 2000)  # time points for plotting

# PARAMETERS VALUES
k_0 = 0.4
k_1 = 0.01
k_2 = 1
k_3 = 1
k_4 = 0.2
K_M3 = 0.4
K_M4 = 0.4
E_T = 1  # total enzyme concentration

p = [k_0, k_1, k_2, k_3, k_4, K_M3, K_M4, E_T, 0]  # parameter vector, leave S = 0 for now

# INITIAL CONDITIONS
y0 = [0, 0]  #  initial conditions for R, E*
y0_gk = [0]  # initial condition for Goldbeter-Koshland approximation
t_total = 0  # to keep track of time

min_S = 0
max_S = 4

# ARRAYS TO STORE RESULTS
S_full = np.zeros([1, 1])
R_full = np.zeros([1, 1])
R_full_gk = np.zeros([1, 1])
E_full = np.zeros([1, 1])
t_full = np.zeros([1, 1])

# ASCENDING SIGNAL
S_asc = np.linspace(min_S, max_S, int((max_S - min_S) / 0.1) + 1)  # signal range

for i in range(len(S_asc)):
    p[-1] = S_asc[i]  # set current signal strength
    # Solve ODE numerically and update arrays:
    results = solve_ivp(ode, t_span, y0, t_eval=t_eval, args=p)
    R_full = np.append(R_full, results.y[0])
    E_full = np.append(E_full, results.y[1])
    t_full = np.append(t_full, results.t + t_total)
    S_full = np.append(S_full, np.full_like(results.t, S_asc[i]))
    t_total += results.t[-1]
    # Compute Goldbeter-Koshland approximation for previous numerical solution:
    gk = solve_ivp(ode_gk, t_span, y0_gk, t_eval=t_eval, args=p)
    R_full_gk = np.append(R_full_gk, gk.y[0])
    # Update initial conditions:
    y0 = results.y[:, -1]
    y0_gk = gk.y[:, -1]

# DESCENDING SIGNAL
S_desc = np.linspace(max_S, min_S, int((max_S - min_S) / 0.5) + 1)  # signal range

for i in range(len(S_desc)):
    p[-1] = S_desc[i]  # set current signal strength
    # Solve ODE numerically and update arrays:
    results = solve_ivp(ode, t_span, y0, t_eval=t_eval, args=p)
    R_full = np.append(R_full, results.y[0])
    E_full = np.append(E_full, results.y[1])
    t_full = np.append(t_full, results.t + t_total)
    S_full = np.append(S_full, np.full_like(results.t, S_desc[i]))
    t_total += results.t[-1]
    # Compute Goldbeter-Koshland approximation for previous numerical solution:
    gk = solve_ivp(ode_gk, t_span, y0_gk, t_eval=t_eval, args=p)
    R_full_gk = np.append(R_full_gk, gk.y[0])
    # Update initial conditions:
    y0 = results.y[:, -1]
    y0_gk = gk.y[:, -1]

# FIGURE INITIALIZATION
fig = plt.figure(figsize=(12, 6), dpi=100)
gs = plt.GridSpec(1, 1)


# This is the animated part of the plot:
ax = fig.add_subplot(gs[0, 0])
ax.set_title("Full response of the irreversible switch (ascending | descending signal)")
ax.set_xlabel("Time $t$")
ax.set_ylabel("Response $R$")

ax2 = ax.twinx()
ax2.set_ylabel("Signal $S$")

# Initialize line objects for the final subplot:
line_R, = ax.plot([], [], label="$R$", color="tab:orange", linewidth=2)
line_R_gk, = ax.plot([], [], label="$R_{GK}$", color="tab:green", linewidth=1)
line_S, = ax2.plot([], [], label="$S$", color="tab:blue")

vline = ax2.axvline((int((max_S - min_S) / 0.1) + 1) * 400, color="black", linewidth=1)  # only shows up later

# Combine subplot legends and set location:
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines2 + lines, labels2 + labels, loc="upper left")

# Function to update the animation:
def update(frame):
    if frame == 0:
        return  # skip the first frame to avoid empty arrays

    line_R.set_data(t_full[:frame], R_full[:frame])
    line_R_gk.set_data(t_full[:frame], R_full_gk[:frame])
    line_S.set_data(t_full[:frame], S_full[:frame])

    ax.set_xlim(t_full[0], t_full[frame])
    ax.set_ylim(R_full[:frame].min(), R_full[:frame].max() * 1.05)
    ax2.set_ylim(S_full[:frame].min(), S_full[:frame].max() * 1.05)

    return line_R, line_R_gk, line_S

# Generate frame indices based on increasing skip:
frame_indices = np.cumsum(np.linspace(1, len(t_full)/5, len(t_full), dtype=int))
frame_indices = frame_indices[frame_indices < len(t_full)]  # ensure available frames are not exceeded

plt.tight_layout()

# Create and save the animation as a GIF:
ani = FuncAnimation(fig, update, frames=frame_indices[100:], interval=10, repeat=False)

# ani.save("signaling_response/output/full_response.gif", fps=30)
# plt.show()
