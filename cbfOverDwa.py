import numpy as np

alpha = 1.0
v_min, v_max = 0.0, 1.0
omega_min, omega_max = -1.2, 1.2

def B_xy (x, y):
    return (
        0.42*x**4 + 0.39*y**4 + 0.15*x**2*y**2
        + 0.08*x**3 + 0.06*y**3
        + 0.07*x**2 + 0.05*y**2 + 0.03*x*y
        + 0.02*x + 0.02*y + 0.01 
    )

def gradB_xy (x, y):
    dBx = (4*0.42*x**3 + 2*0.15*x*y**2 + 3*0.08*x**2 + 2*0.07*x + 0.03*y + 0.02)
    dBy = (4*0.39*y**3 + 2*0.15*x**2*y + 3*0.06*y**2 + 2*0.05*y + 0.03*x + 0.02)
    return dBx, dBy

def cbf_filter (u_nom, state):
    x, y, theta, v_curr, omega_curr = state
    v_nom, omega_nom = u_nom

    Bv = B_xy (x, y)
    dBx, dBy = gradB_xy (x, y)

    c, s = np.cos(theta), np.sin(theta)
    coeff_v = (dBx * c + dBy * s)

    if abs (coeff_v) < 1e-9:
        v_req = v_max if (alpha * Bv) < 0 else v_nom
    else:
        v_req = max (v_min, min (v_max, (-alpha * Bv) / coeff_v))
    
    def satisfies (v):
        return (v * coeff_v + alpha * Bv) >= -1e-9
    
    candidates = [np.clip (v_nom, v_min, v_max), v_req]

    v_filt = None

    for vv in sorted (candidates, key = lambda z: abs (z - v_nom)):
        if satisfies (vv):
            v_filt = vv
            break
        if v_filt is None:
            v_filt = np.clip (v_req, v_min, v_max)

    omega_filt = np.clip (omega_nom, omega_min, omega_max)

    return v_filt, omega_filt

