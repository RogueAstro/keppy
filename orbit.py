#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sp
import time

"""
This code is based on the formalism from Murray & Correia (2011), available
freely at http://arxiv.org/abs/1009.1738. The equation numbers are from this
article, unless otherwise noted.
"""

# Calculates the orbital parameter K (Eq. 66)
def K(m1, m2, n, a, I, e):
    """This is an orbital parameter. Currently not in use by the code."""
    return m2/(m1+m2)*n*a*np.sin(I)/np.sqrt(1.-e**2)

# Calculates Eq. 65
def vr(VZ, K, w, f, e):
    """The radial velocities equation."""
    w *= np.pi/180.
    return VZ + K*(np.cos(w+f) + e*np.cos(w))

# Calculates the Kepler equation (Eq. 41)
def kepler(E, e, M):
    """The Kepler equation."""
    return E - e*np.sin(E) - M

# Calculates the radial velocities for given orbital parameters
def get_RVs(K, T, t0, w, e, a, VZ, start, end, NT, N):
    """
    Function that produces the time and radial velocities arrays given the
    following parameters. Radial velocities may be shifted by one quarter of a
    period.

    K = orbit parameter [km/s]
    T = period [d]
    t0 = Time of periastron passage [d]
    w = Argument of periapse [degrees]
    e = eccentricity
    a = semi-major axis
    VZ = proper motion [km/s]
    start = start date [d]
    end = end date [d]
    NT = number of points for one period
    N = number of points between start and end dates
    """

    # Calculating RVs for one period
    t = np.linspace(t0, t0+T, NT)           # Time (days)
    M = 2*np.pi/T*(t-t0)                    # Mean anomaly
    E = np.array([sp.newton(func = kepler, x0 = Mk, args = (e, Mk)) \
                 for Mk in M])              # Eccentric anomaly
    r = a*(1.-e*np.cos(E))                  # r coordinates
    f = np.arccos(((a*(1.-e**2)/r)-1.0)/e)  # True anomalies
    f[(NT-1)/2:] += 2*(np.pi-f[(NT-1)/2:])  # Shifting the second half of f
    #f[:(NT-1)/2] += 2*(np.pi-f[:(NT-1)/2]) # Shifting the first half of f

    RV = np.array([vr(VZ, K, w, fk, e) \
                    for fk in f])           # Radial velocities (km/s)

    # Calculating RVs in the specified time interval
    ts = np.linspace(start, end, N)
    RVs = np.interp(ts, t, RV, period = T)

    return ts, RVs

# Usage example
def example():
    """Example using the parameters of the star HD 156846 and its planet
    HD 156846 b."""
    start_time = time.time()
    t, RVs = get_RVs(K = 0.464,
                     T = 359.51,
                     t0 = 3998.1,
                     w = 52.2,
                     e = 0.847,
                     a = 0.9930,
                     VZ = -68.54,
                     start = 3600.,
                     end = 4200.,
                     NT = 1000,
                     N = 1000)
    print('RV calculation took %.4f seconds' % (time.time()-start_time))

    plt.plot(t, RVs)
    plt.xlabel('JD - 2450000.0 (days)')
    plt.ylabel('RV (km/s)')
    plt.show()