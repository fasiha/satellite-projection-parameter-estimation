import numpy as np

def vertical_satellite_forward(R, P, phi1, lambda0, phi, lam):
    cos_c = (np.sin(phi1)*np.sin(phi)
             + np.cos(phi1) * np.cos(phi) * np.cos(lam-lambda0))
    kprime = (P-1.0) / (P-cos_c)
    x = R * kprime * np.cos(phi) * np.sin(lam-lambda0)
    y = R * kprime * (np.cos(phi1)*np.sin(phi)
                           - np.sin(phi1)
                           * np.cos(phi)
                           * np.cos(lam-lambda0))
    return (x,y)

def percent_error(true, estimated):
    return np.sqrt(np.sum(np.abs(true-estimated)**2)) / np.sqrt(np.sum(true**2))
def tilted_satellite_forward_test():
    R = 6371e3 # m
    H = 500e3 # m
    phi1 = +39.0 # deg
    lambda0 = -77.0 # deg
    omega = 30 # deg
    gamma = 50 # deg
    phi = +41.0 # deg
    lam = -74.0 # deg

    true_xy = np.array([-8.3400123, 277.34759])*1e3 # m

    P = 1.0 + H/R
    (x, y) = tilted_satellite_forward(R, P, np.deg2rad(phi1),
                                        np.deg2rad(lambda0),
                                        np.deg2rad(omega),
                                        np.deg2rad(gamma),
                                        np.deg2rad(phi), np.deg2rad(lam))


    assert(percent_error(true_xy, np.array([x,y])) < 1e-3)
    return (x,y)

def vertical_satellite_forward_test():
    """ Numerical example from page 320 of Snyder.
    """
    R = 6371e3 # m
    H = 500e3 # m
    phi1 = +39.0 # deg
    lambda0 = -77.0 # deg
    phi = +41.0 # deg
    lam = -74.0 # deg

    true_xy = np.array([247.19409, 222.48596])*1e3 # m

    P = 1.0 + H/R
    (x, y) = vertical_satellite_forward(R, P, np.deg2rad(phi1),
                                        np.deg2rad(lambda0),
                                        np.deg2rad(phi), np.deg2rad(lam))


    assert(percent_error(true_xy, np.array([x,y])) < 1e-3)
    return (x,y)

def tilted_satellite_forward(R, P, phi1, lambda0, omega, gamma, phi, lam):
    """From Snyder, page 175:

    'In terms of a camera in space, the camera is placed at a distance
    RP from the center of the Earth, perpendicularly over point (phi1,
    lambda0). The camera is horizontally turned to face gamma
    clockwise from north, and then tilted (90°-omega) downward from
    horizontal, "horizontal" meaning parallel to a plane tangent to
    the sphere at (phi1, lambda0). The photograph is then taken,
    placing points (phi, lam) in positions (xt, yt), based on a scale
    reduction in R.'

    """
    (x, y) = vertical_satellite_forward(R, P, phi1, lambda0, phi, lam)
    H = R*(P-1.0)
    A = np.abs((y*np.cos(gamma) + x*np.sin(gamma)) * np.sin(omega)/H) + np.cos(omega)
    xt = np.cos(omega) / A * (x*np.cos(gamma) - y*np.sin(gamma))
    yt = (y*np.cos(gamma) + x*np.sin(gamma)) / A
    return (xt, yt)
