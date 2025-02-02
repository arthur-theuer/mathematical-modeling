# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp


def goldbeter_koshland(u_1, u_2, J_1, J_2):
    B = u_2 - u_1 + J_1 * u_2 + J_2 * u_1
    return (2 * u_1 * J_2) / (B + np.sqrt(B**2 - 4 * (u_2 - u_1) * u_1 * J_2))


def ode_sd(t, y, k_0_prime, k_0, k_1, k_2, k_3, k_4, J_3, J_4, S, E_T):
    Ep_gk = goldbeter_koshland(k_3 * y[1], k_4, J_3, J_4)
    dydt = np.array([
        k_1 * S - y[0] * (k_0_prime + k_0 * Ep_gk),
        y[0] * (k_0_prime + k_0 * Ep_gk) - k_2 * y[1]
    ])
    return dydt


def nullclines_sd():
    r_linspace = np.linspace(0.01, 1.2, 100)
    Ep_gk_r = goldbeter_koshland(k_3 * r_linspace, k_4, J_3, J_4)
    r_nullcline = (k_2 * r_linspace) / (k_0_prime + k_0 * Ep_gk_r)

    r_linspace_2 = np.linspace(0.1035, 1.2, 100)
    Ep_gk_r_2 = goldbeter_koshland(k_3 * r_linspace_2, k_4, J_3, J_4)
    x_nullcline = (k_1 * S) / (k_0_prime + k_0 * Ep_gk_r_2)

    return r_nullcline, r_linspace, x_nullcline, r_linspace_2


def phase_vectors_sd():
    X, R = np.meshgrid(np.linspace(0, 5, 30), np.linspace(0, 1.2, 30))
    Ep_gk = goldbeter_koshland(k_3 * R, k_4, J_3, J_4)
    dXdt = k_1 * S - X * (k_0_prime + k_0 * Ep_gk)
    dRdt = X * (k_0_prime + k_0 * Ep_gk) - k_2 * R
    magnitude = np.sqrt(dXdt**2 + dRdt**2)

    return X, R, dXdt, dRdt, magnitude


def ode_ai(t, y, k_2_prime, k_0, k_1, k_2, k_3, k_4, k_5, k_6, J_3, J_4, S, E_T):
    Ep_gk = goldbeter_koshland(k_3 * y[1], k_4, J_3, J_4)
    dydt = np.array([
        k_5 * y[1] - k_6 * y[0],
        k_1 * S + k_0 * Ep_gk - y[1] * (k_2 + k_2_prime * y[0])
    ])
    return dydt


def nullclines_ai():
    # NULLCLINES:
    x_linspace = np.linspace(0, 2, 100)
    x_nullcline = (k_6 * x_linspace) / k_5  # plot against X, so 

    r_linspace = np.linspace(0.1, 2.5, 100)
    Ep_gk_r = goldbeter_koshland(k_3 * r_linspace, k_4, J_3, J_4)
    r_nullcline = (k_1 * S + k_0 * Ep_gk_r) / (r_linspace * k_2_prime) - k_2 / k_2_prime

    return x_linspace, x_nullcline, r_nullcline, r_linspace


def phase_vectors_ai():
    # QUIVER PLOT:
    X, R = np.meshgrid(np.linspace(0, 2, 30), np.linspace(0, 2.5, 30))
    Ep_gk = goldbeter_koshland(k_3 * R, k_4, J_3, J_4)
    dXdt = k_5 * R - k_6 * X
    dRdt = k_1 * S + k_0 * Ep_gk - R * (k_2 + k_2_prime * X)
    magnitude = np.sqrt(dXdt**2 + dRdt**2)

    return X, R, dXdt, dRdt, magnitude

# GENERAL PARAMETERS
t_span = [0, 100]  # time span
t_eval = np.linspace(*t_span, 1200)  # time points for plotting

# PARAMETERS FOR THE FIRST MODEL
k_0_prime = 0
k_0 = 0.4
k_1 = 1
k_2 = 1
k_3 = 1
k_4 = 0.4
J_3 = 0.5
J_4 = 0.5
S = 0.2
E_T = 1

p = [k_0_prime, k_0, k_1, k_2, k_3, k_4, J_3, J_4, S, E_T]

# NULLCLINES AND PHASE VECTORS
sd_r_null, sd_r_lin, sd_x_null, sd_x_lin = nullclines_sd()
sd_pv = phase_vectors_sd()

# ODE SOLUTIONS
sd_results_1 = solve_ivp(ode_sd, t_span, [1.0, 0.2], t_eval=t_eval, args=p)
sd_results_2 = solve_ivp(ode_sd, t_span, [0.5, 1.0], t_eval=t_eval, args=p)
sd_results_3 = solve_ivp(ode_sd, t_span, [3.0, 0.4], t_eval=t_eval, args=p)
sd_results_4 = solve_ivp(ode_sd, t_span, [3.0, 1.2], t_eval=t_eval, args=p)




k_2_prime = 1
k_0 = 4
k_1 = 1
k_2 = 1
k_3 = 1
k_4 = 1
k_5 = 0.1
k_6 = 0.075
J_3 = 0.3
J_4 = 0.3
S = 0.2
E_T = 1

p = [k_2_prime, k_0, k_1, k_2, k_3, k_4, k_5, k_6, J_3, J_4, S, E_T]

# NULLCLINES AND PHASE VECTORS
ai_x_lin, ai_x_null, ai_r_null, ai_r_lin = nullclines_ai()
ai_pv = phase_vectors_ai()

# ODE SOLUTIONS
ai_results_1 = solve_ivp(ode_ai, t_span, [1.5, 2.0], t_eval=t_eval, args=p)
ai_results_2 = solve_ivp(ode_ai, t_span, [0.5, 0.3], t_eval=t_eval, args=p)
ai_results_3 = solve_ivp(ode_ai, t_span, [0.25, 1.0], t_eval=t_eval, args=p)
ai_results_4 = solve_ivp(ode_ai, t_span, [1.25, 2.0], t_eval=t_eval, args=p)
ai_results_5 = solve_ivp(ode_ai, t_span, [1.0, 1.0], t_eval=t_eval, args=p)

# FIGURE INITIALIZATION
fig = plt.figure(figsize=(12, 6), dpi=100)
gs = plt.GridSpec(1, 2)

# PLOTTING FOR SUBSTRATE DEPLETION MODEL
ax1 = fig.add_subplot(gs[0, 0])
ax1.quiver(sd_pv[0], sd_pv[1], sd_pv[2], sd_pv[3], sd_pv[4], scale=30, cmap="viridis_r", label="vector field", alpha=0.6)

# Plot manually computed nullclines:
ax1.plot(sd_x_null, sd_x_lin, label="$dX/dt$ nullcline")
ax1.plot(sd_r_null, sd_r_lin, label="$dR/dt$ nullcline")

# Initialize dashed lines for each trajectory:
sd_traj_1 = ax1.plot([], [], color="black", linestyle="dashed", alpha=0.7, label="trajectories")
sd_traj_2 = ax1.plot([], [], color="black", linestyle="dashed", alpha=0.7)
sd_traj_3 = ax1.plot([], [], color="black", linestyle="dashed", alpha=0.7)
sd_traj_4 = ax1.plot([], [], color="black", linestyle="dashed", alpha=0.7)

# Initialize dots for each trajectory:
sd_dot_1 = ax1.plot([], [], linestyle="", marker="o", color="tab:red")
sd_dot_2 = ax1.plot([], [], linestyle="", marker="o", color="tab:red")
sd_dot_3 = ax1.plot([], [], linestyle="", marker="o", color="tab:red")
sd_dot_4 = ax1.plot([], [], linestyle="", marker="o", color="tab:red")

ax1.set_xlabel("$X$")
ax1.set_ylabel("$R$")
ax1.set_title("Substrate-depletion oscillator $(X, R)$ phase plane")
ax1.legend()

# PLOTTING FOR ACTIVATOR INHIBITOR MODEL
ax2 = fig.add_subplot(gs[0, 1])
ax2.quiver(ai_pv[0], ai_pv[1], ai_pv[2], ai_pv[3], ai_pv[4], scale=45, cmap="viridis_r", label="vector field", alpha=0.6)

# Plot manually computed nullclines:
ax2.plot(ai_x_lin, ai_x_null, label="$dX/dt$ nullcline")
ax2.plot(ai_r_null, ai_r_lin, label="$dR/dt$ nullcline")

# Initialize dashed lines for each trajectory:
ai_traj_1 = ax2.plot([], [], color="black", linestyle="dashed", alpha=0.7, label="trajectories")
ai_traj_2 = ax2.plot([], [], color="black", linestyle="dashed", alpha=0.7)
ai_traj_3 = ax2.plot([], [], color="black", linestyle="dashed", alpha=0.7)
ai_traj_4 = ax2.plot([], [], color="black", linestyle="dashed", alpha=0.7)
ai_traj_5 = ax2.plot([], [], color="black", linestyle="dashed", alpha=0.7)

# Initialize dots for each trajectory:
ai_dot_1 = ax2.plot([], [], linestyle="", marker="o", color="tab:red")
ai_dot_2 = ax2.plot([], [], linestyle="", marker="o", color="tab:red")
ai_dot_3 = ax2.plot([], [], linestyle="", marker="o", color="tab:red")
ai_dot_4 = ax2.plot([], [], linestyle="", marker="o", color="tab:red")
ai_dot_5 = ax2.plot([], [], linestyle="", marker="o", color="tab:red")

ax2.set_xlabel("$X$")
ax2.set_ylabel("$R$")
ax2.set_title("Activator-inhibitor oscillator $(X, R)$ phase plane")
ax2.legend()

# Function to update the animation:
def update(frame):
    sd_traj_1[0].set_data(sd_results_1.y[0, :frame], sd_results_1.y[1, :frame])
    sd_traj_2[0].set_data(sd_results_2.y[0, :frame], sd_results_2.y[1, :frame])
    sd_traj_3[0].set_data(sd_results_3.y[0, :frame], sd_results_3.y[1, :frame])
    sd_traj_4[0].set_data(sd_results_4.y[0, :frame], sd_results_4.y[1, :frame])

    sd_dot_1[0].set_data([sd_results_1.y[0, frame]], [sd_results_1.y[1, frame]])
    sd_dot_2[0].set_data([sd_results_2.y[0, frame]], [sd_results_2.y[1, frame]])
    sd_dot_3[0].set_data([sd_results_3.y[0, frame]], [sd_results_3.y[1, frame]])
    sd_dot_4[0].set_data([sd_results_4.y[0, frame]], [sd_results_4.y[1, frame]])

    ai_traj_1[0].set_data(ai_results_1.y[0, :frame], ai_results_1.y[1, :frame])
    ai_traj_2[0].set_data(ai_results_2.y[0, :frame], ai_results_2.y[1, :frame])
    ai_traj_3[0].set_data(ai_results_3.y[0, :frame], ai_results_3.y[1, :frame])
    ai_traj_4[0].set_data(ai_results_4.y[0, :frame], ai_results_4.y[1, :frame])
    ai_traj_5[0].set_data(ai_results_5.y[0, :frame], ai_results_5.y[1, :frame])

    ai_dot_1[0].set_data([ai_results_1.y[0, frame]], [ai_results_1.y[1, frame]])
    ai_dot_2[0].set_data([ai_results_2.y[0, frame]], [ai_results_2.y[1, frame]])
    ai_dot_3[0].set_data([ai_results_3.y[0, frame]], [ai_results_3.y[1, frame]])
    ai_dot_4[0].set_data([ai_results_4.y[0, frame]], [ai_results_4.y[1, frame]])
    ai_dot_5[0].set_data([ai_results_5.y[0, frame]], [ai_results_5.y[1, frame]])



plt.tight_layout()

# Create and save the animation as a GIF:
ani = FuncAnimation(fig, update, frames=sd_results_1.y.shape[1], interval=10, repeat=False)

ani.save("phase_plane_analysis/output/limit_cycles.gif", fps=30)
# plt.show()
