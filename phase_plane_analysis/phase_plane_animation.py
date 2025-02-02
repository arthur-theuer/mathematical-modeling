# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

# NULLCLINES
k = 0.45
u = np.linspace(0, 1.2, 100)
v = (u**2) / (k**2 + u**2)

# QUIVER PLOT
U, V = np.meshgrid(np.linspace(0, 1.2, 30), np.linspace(0, 1.2, 30))
dUdt = V - U
dVdt = U**2 / (k**2 + U**2) - V
magnitude = np.sqrt(dUdt**2 + dVdt**2)

# FIXED POINTS
u1 = 0
u2 = (1 - np.sqrt(1 - 4 * k**2))/2
u3 = (1 + np.sqrt(1 - 4 * k**2))/2

# GENERAL PARAMETERS
t_span = [0, 40]  # time span
t_eval = np.linspace(*t_span, 400)  # time points for plotting

# TRAJECTORIES
def ode(t, y, k):
    dydt = np.array([
        y[1] - y[0],
        y[0]**2 / (k**2 + y[0]**2) - y[1]
    ])
    return dydt

# ODE SOLUTIONS
results_1 = solve_ivp(ode, t_span, [1.0, 0.2], t_eval=t_eval, args=[k])
results_2 = solve_ivp(ode, t_span, [0.1, 0.3], t_eval=t_eval, args=[k])
results_3 = solve_ivp(ode, t_span, [1.0, 1.2], t_eval=t_eval, args=[k])
results_4 = solve_ivp(ode, t_span, [0.0, 0.65], t_eval=t_eval, args=[k])
results_5 = solve_ivp(ode, t_span, [0.4, 1.2], t_eval=t_eval, args=[k])
results_6 = solve_ivp(ode, t_span, [0.0, 1.1], t_eval=t_eval, args=[k])
results_7 = solve_ivp(ode, t_span, [0.5, 0.0], t_eval=t_eval, args=[k])

# FIGURE INITIALIZATION
fig = plt.figure(figsize=(12, 8), dpi=100)
gs = plt.GridSpec(1, 1)

# PLOTTING
ax = fig.add_subplot(gs[0, 0])
ax.quiver(U, V, dUdt, dVdt, magnitude, scale=40, cmap="viridis", label="vector field", alpha=0.6)

# Plot manually computed nullclines:
ax.plot(u, u, label="$du/dt$ nullcline")
ax.plot(u, v, label="$dv/dt$ nullcline")

# Plot manually computed fixed points:
ax.plot(u1, u1, linestyle="", marker="o", color="black", label="fixed points")
ax.plot(u2, u2, linestyle="", marker="o", color="black")
ax.plot(u3, u3, linestyle="", marker="o", color="black")

# Initialize dashed lines for each trajectory:
traj_1 = ax.plot([], [], color="black", linestyle="dashed", alpha=0.7, label="trajectories")
traj_2 = ax.plot([], [], color="black", linestyle="dashed", alpha=0.7)
traj_3 = ax.plot([], [], color="black", linestyle="dashed", alpha=0.7)
traj_4 = ax.plot([], [], color="black", linestyle="dashed", alpha=0.7)
traj_5 = ax.plot([], [], color="black", linestyle="dashed", alpha=0.7)
traj_6 = ax.plot([], [], color="black", linestyle="dashed", alpha=0.7)
traj_7 = ax.plot([], [], color="black", linestyle="dashed", alpha=0.7)

# Initialize dots for each trajectory:
dot_1 = ax.plot([], [], linestyle="", marker="o", color="tab:red")
dot_2 = ax.plot([], [], linestyle="", marker="o", color="tab:red")
dot_3 = ax.plot([], [], linestyle="", marker="o", color="tab:red")
dot_4 = ax.plot([], [], linestyle="", marker="o", color="tab:red")
dot_5 = ax.plot([], [], linestyle="", marker="o", color="tab:red")
dot_6 = ax.plot([], [], linestyle="", marker="o", color="tab:red")
dot_7 = ax.plot([], [], linestyle="", marker="o", color="tab:red")

ax.set_xlabel("$u$")
ax.set_ylabel("$v$")
ax.set_title("Phase plane for $(u, v)$ with vector field and trajectories")
ax.legend()

# Function to update the animation:
def update(frame):
    traj_1[0].set_data(results_1.y[0, :frame], results_1.y[1, :frame])
    traj_2[0].set_data(results_2.y[0, :frame], results_2.y[1, :frame])
    traj_3[0].set_data(results_3.y[0, :frame], results_3.y[1, :frame])
    traj_4[0].set_data(results_4.y[0, :frame], results_4.y[1, :frame])
    traj_5[0].set_data(results_5.y[0, :frame], results_5.y[1, :frame])
    traj_6[0].set_data(results_6.y[0, :frame], results_6.y[1, :frame])
    traj_7[0].set_data(results_7.y[0, :frame], results_7.y[1, :frame])

    dot_1[0].set_data([results_1.y[0, frame]], [results_1.y[1, frame]])
    dot_2[0].set_data([results_2.y[0, frame]], [results_2.y[1, frame]])
    dot_3[0].set_data([results_3.y[0, frame]], [results_3.y[1, frame]])
    dot_4[0].set_data([results_4.y[0, frame]], [results_4.y[1, frame]])
    dot_5[0].set_data([results_5.y[0, frame]], [results_5.y[1, frame]])
    dot_6[0].set_data([results_6.y[0, frame]], [results_6.y[1, frame]])
    dot_7[0].set_data([results_7.y[0, frame]], [results_7.y[1, frame]])

plt.tight_layout()

# Create and save the animation as a GIF:
ani = FuncAnimation(fig, update, frames=results_1.y.shape[1], interval=10, repeat=False)

# ani.save("phase_plane_analysis/output/phase_plane_trajectories.gif", fps=30)
# plt.show()
