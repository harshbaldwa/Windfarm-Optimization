#!/usr/bin/env python3

import numpy as np
import math

def area_overlap_sr(dx, dy, alpha, rr):
    r1 = rr+ alpha*dx
    in_wake = (dy < r1+rr) and dx>0

    rr2 = rr**2
    r12 = r1**2

    if in_wake:

        # totally inside wake
        if dy<=r1-rr:
            return(np.pi*rr2)

        # partially inside wake
        y_int = (r12 - rr2 + dy**2)/(2*dy)
        x_int = np.sqrt(r12 - y_int**2)
        print(x_int, y_int)

        theta1 = math.atan2(x_int, y_int)
        thetar = math.atan2(x_int, dy-y_int )

        print(theta1, thetar)
        s1 = theta1*r12
        sr = thetar*rr2
        t1 = y_int*x_int
        tr = (dy - y_int)*x_int

        Aovp = s1+sr-t1-tr

        Aovp = Aovp
        return(Aovp)
    else:
        return(0)
area_overlap = np.vectorize(area_overlap_sr, otypes=[np.float64])


def wake_model(x, y,wx, wy, alpha, rr, a):
    X = np.vstack([x,y])

    theta = np.atan2(wy, wx)
    u0 = np.sqrt(wx**2+wy**2)

    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    X = np.dot(rot, X)

    udefAo2 = np.zeros(len(x))

    for i in range(len(x)):
        dx = X[0, :] - X[0, i]
        dy = X[1, :] - X[1, i]
        Ao = area_overlap(dx, dy, alpha, rr)
        udef = 2*a/((1+ alpha*dx)**2)
        udefAo2 = udefAo2 + (udef*Ao)**2
    udefAoA = np.sqrt(udefAo2)/(np.pi*rr*rr)
    u = u0*(1-udefAoA)
    return(u)