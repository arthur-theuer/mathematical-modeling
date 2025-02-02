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

# ASCENDING SIGNAL
S_asc = np.linspace(min_S, max_S, int((max_S - min_S) / 0.01) + 1)  # signal range
R_ss_asc = np.zeros_like(S_asc)
R_ss_gk_asc = np.zeros_like(S_asc)

for i in range(len(S_asc)):
    p[-1] = S_asc[i]  # set current signal strength
    # Solve ODE numerically and update arrays:
    results = solve_ivp(ode, t_span, y0, t_eval=t_eval, args=p)
    R_ss_asc[i] = results.y[0, -1]  # get final value of R for current signal
    t_total += results.t[-1]
    # Compute Goldbeter-Koshland approximation for previous numerical solution:
    gk = solve_ivp(ode_gk, t_span, y0_gk, t_eval=t_eval, args=p)
    R_ss_gk_asc[i] = gk.y[0, -1]
    # Update initial conditions:
    y0 = results.y[:, -1]
    y0_gk = gk.y[:, -1]

# DESCENDING SIGNAL
S_desc = np.linspace(max_S, min_S, int((max_S - min_S) / 0.01) + 1)  # signal range
R_ss_desc = np.zeros_like(S_desc)
R_ss_gk_desc = np.zeros_like(S_desc)

for i in range(len(S_desc)):
    p[-1] = S_desc[i]  # set current signal strength
    # Solve ODE numerically and update arrays:
    results = solve_ivp(ode, t_span, y0, t_eval=t_eval, args=p)
    R_ss_desc[i] = results.y[0, -1]  # get final value of R for current signal
    t_total += results.t[-1]
    # Compute Goldbeter-Koshland approximation for previous numerical solution:
    gk = solve_ivp(ode_gk, t_span, y0_gk, t_eval=t_eval, args=p)
    R_ss_gk_desc[i] = gk.y[0, -1]
    # Update initial conditions:
    y0 = results.y[:, -1]
    y0_gk = gk.y[:, -1]

# FIGURE 1 INITIALIZATION
fig = plt.figure(figsize=(12, 6), dpi=100)
gs = plt.GridSpec(1, 1)

ax = fig.add_subplot(gs[0, 0])
ax.plot(S_asc, R_ss_asc, label="$R_{SS}$", color="tab:gray", alpha=0.5)
#ax.plot(S_asc, R_ss_gk_asc, label="$R_{SS, GK}$", color="tab:blue")
ax.plot(S_desc, R_ss_desc, color="tab:gray", alpha=0.5)
#ax.plot(S_desc, R_ss_gk_desc, color="tab:red")
ax.set_title("Steady-state response of the irreversible switch (ascending | descending signal)")
ax.set_xlabel("Signal strength $S$")
ax.set_ylabel("Steady-state response $R_{SS}$")

line_R_gk_asc, = ax.plot([], [], label="$R_{SS, GK}$ (ascending)", color="tab:blue", linewidth=2, linestyle="dashed")
line_R_gk_desc, = ax.plot([], [], label="$R_{SS, GK}$ (descending)", color="tab:red", linewidth=2, linestyle="dashed")

ax.legend(loc = "lower right")

# Vertical line and point marker:
vline = ax.axvline(S_asc[0], color="tab:gray", linestyle="dotted")
point, = ax.plot([], [], marker="o", color="black", markersize=6)

# Function to update the animation:
def update(frame):
    if frame < len(S_asc):
        S_current, R_current = S_asc[frame], R_ss_asc[frame]
        line_R_gk_asc.set_data(S_asc[:frame], R_ss_gk_asc[:frame])
    else:
        S_current, R_current = S_desc[frame - len(S_asc)], R_ss_desc[frame - len(S_asc)]
        line_R_gk_asc.set_data(S_asc, R_ss_gk_asc)
        line_R_gk_desc.set_data(S_desc[:frame - len(S_asc)], R_ss_gk_desc[:frame - len(S_asc)])

    vline.set_xdata([S_current])
    point.set_data([S_current], [R_current])

plt.tight_layout()

# Create and save the animation as a GIF:
ani = FuncAnimation(fig, update, frames=len(S_asc)+len(S_desc), interval=10, repeat=False)

# ani.save("signaling_response/output/steady_state_response.gif", fps=30)
# plt.show()
