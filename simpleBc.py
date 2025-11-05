import numpy as np

DT = 0.1

def step_unicycle(state, v, w, dt=DT):
    x, y, th = state
    x += v * np.cos(th) * dt
    y += v * np.sin(th) * dt
    th = wrap_to_pi(th + w * dt)
    return np.array([x, y, th])

def wrap_to_pi(a):
    return (a + np.pi) % (2*np.pi)

# a will be the gradient of h.[cos th, sin th, 0]