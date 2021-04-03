import math
from .wake_model import aep

def objective(layout, boundary_limits, diameter, height, z_0, wind_velocity):
    n = len(layout)/2
    cost = n*(2/3 + 1/3*math.exp(-0.00174*n**2))
    alpha = 0.5/math.log(height/z_0)
    P, penalty = aep(layout, [wind_velocity, 0], alpha, diameter/2, boundary_limits)

    return (0.33*1/P + 0.66*cost/P) + 1e-6*penalty