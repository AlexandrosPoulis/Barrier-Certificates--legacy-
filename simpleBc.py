import numpy as np
import cvxpy as cp

V_MAX = 1.0
W_MAX = 1.2

DT = 0.1

OBSTACLES = [
    [2.0, 2.0, 0.5, 0.0, 0.0]
]
# [x, y, radius, vx, vy]

def step_unicycle(state, v, w, dt=DT):
    x, y, th = state
    x += v * np.cos(th) * dt
    y += v * np.sin(th) * dt
    th = wrap_to_pi(th + w * dt)
    return np.array([x, y, th])

def wrap_to_pi(a):
    return (a + np.pi) % (2*np.pi)

# a will be the gradient of h.[cos th, sin th, 0]

def cbf_qp(state, t, v_ref, w_ref):
    x, y, th = state
    u = cp.Variable(2) # linear and angular velocity
    uref = np.array([v_ref, w_ref])
    constraints += [u[0] >= 0.0, u[0] <= V_MAX,
                    u[1] >= -W_MAX , u[1] <= W_MAX]
    
