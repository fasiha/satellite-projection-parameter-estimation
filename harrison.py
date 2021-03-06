import numpy as np
import scipy.linalg as la
import scipy.optimize as opt

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
    """Numerical example from page 322 of Snyder."""
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
    clockwise from north, and then tilted (90 degrees - omega)
    downward from horizontal, "horizontal" meaning parallel to a
    plane tangent to the sphere at (phi1, lambda0). The photograph is
    then taken, placing points (phi, lam) in positions (xt, yt), based
    on a scale reduction in R.'

    """
    (x, y) = vertical_satellite_forward(R, P, phi1, lambda0, phi, lam)
    H = R*(P-1.0)
    A = np.abs((y*np.cos(gamma) + x*np.sin(gamma)) * np.sin(omega)/H) + np.cos(omega)
    xt = np.cos(omega) / A * (x*np.cos(gamma) - y*np.sin(gamma))
    yt = (y*np.cos(gamma) + x*np.sin(gamma)) / A
    return (xt, yt)


def str2longlat(s):
    x = s.lower()
    x = float(x.rstrip('wens')) * (
        -1 if (x.find('s')>=0 or x.find('w')>=0)
        else 1)
    return x

def loaddata(fname="data.csv"):
    return np.array([(str2longlat(lo), str2longlat(lat),
                      float(x), float(y))
              for (lo,lat,x,y)
              in np.genfromtxt(fname, skip_header=1,
                               dtype=str, delimiter=',')])

def lstsq_slope_intercept(x,y):
    # Effectively polyfit(x,y,1)---though with fixed linear system
    (slope, intercept),_,_,_ = la.lstsq(np.hstack((x, np.ones_like(x))), y)
    return (slope, intercept)

def lstsq_slope_intercept_project(x,y):
    # effectively polyval with polyfit(x,y,1)
    m, b = lstsq_slope_intercept(x, y)
    return m*x + b

def paramfn(params, data, fixedR=False, returnerr=True):
    if fixedR:
        P, phi1, lambda0, omega,gamma = params
        R = 1.0
    else:
        R, P, phi1, lambda0, omega, gamma = params
    xy = np.array([tilted_satellite_forward(R,P,phi1,lambda0,omega,gamma,
                                            phi,lam)
                   for (phi,lam) in data[:,:2]])
    pixel = np.hstack((lstsq_slope_intercept_project(xy[:,:1], data[:,2:3]),
                       lstsq_slope_intercept_project(xy[:,1:], data[:,3:])))
    if returnerr:
        return (pixel - data[:,2:]).ravel()
    else:
        return pixel

def paramprinter(x, fixedR=False):
    if fixedR:
        P, phi1, lambda0, omega, gamma = x
        R = 1.0
    else:
        R, P, phi1, lambda0, omega, gamma = x
    # P = 1.0 + H/R
    print "R = %g, P = %g (-> H = %g)" % (R, P, (P-1.0)*R)
    print "lat/long: (%g, %g) deg" % tuple(np.rad2deg([phi1, lambda0]))
    print "tilt/rot: (%g, %g) deg" % tuple(np.rad2deg([omega, gamma]))

def plottest(data=None):
    # Polar:
    #R=1.0; P=9.9; phi1=np.deg2rad(90.0); lambda0=0.0; omega=0.0; gamma=0.0
    #phivec = range(-0,90,10)
    #lamvec = range(-180,180,45)

    R=1.0; P=1.9; phi1=np.deg2rad(49.0); lambda0=np.deg2rad(26.0);
    omega=np.deg2rad(0.0); gamma=np.deg2rad(-99.0)

    if data is None:
        phivec = range(30,91,15)
        lamvec = range(-30,61,15)
        phirad = np.deg2rad(np.array(phivec, dtype=float))
        lamrad = np.deg2rad(np.array(lamvec, dtype=float))
        latlong = np.array([(phi,lam) for phi in phirad for lam in lamrad])
    else:
        latlong = np.array([(lat,lon) for (lon,lat) in np.deg2rad(data[:,:2])])

    pixels=np.array([tilted_satellite_forward(R,P,phi1,lambda0,omega,gamma,
                                           phi,lam)
                     for (phi,lam) in latlong])

    import pylab
    import matplotlib.pyplot as plt
    pylab.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(pixels[:,0], pixels[:,1],'bo')
    [ax.annotate("%g,%g"%tuple(ll.tolist()), xy=tuple(a.tolist()),
                 xytext=tuple(a.tolist()))
     for (a,ll) in zip(pixels, np.rad2deg(latlong))]
    plt.show()

    return (pixels, latlong)

def imtest(data=None, im=None, final=None):
    if data is None:
        pixels = [[20,20], [40,40], [50,70]]
        labels  = pixels
    else:
        pixels = data[:,2:]
        labels = data[:,:2]
    if im is None:
        im = np.random.randn(100,100)
    import pylab
    import matplotlib.pyplot as plt
    pylab.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(im)
    [ax.annotate("%g,%g"%tuple(l), xy=tuple(p), xytext=tuple(p),
                 color='r', size=15)
     for (l,p) in zip(labels,pixels)]
    if final is not None:
        [ax.annotate("%g,%g"%tuple(l), xy=tuple(p), xytext=tuple(p),
                     size=15, color='g')
         for (l,p) in zip(labels,final)]
    plt.show()

if __name__ == '__main__':
    data = loaddata(fname='data.csv')
    #data = loaddata(fname='tributary.csv')

    # (theopix, theoll) = plottest(data)

    datarad = np.hstack((np.deg2rad(data[:,[1,0]]), data[:,2:]))
    R = 1.0
    P = 1.1
    phi1 = np.deg2rad(49.0) # lat
    lambda0 = np.deg2rad(26.0) # long
    omega = np.deg2rad(45.0) # tilt
    gamma = np.deg2rad(-99.0) # rot
    fixedR = True

    if fixedR:
        init = [P, phi1, lambda0, omega, gamma]
    else:
        init = [R, P, phi1, lambda0, omega, gamma]

    # Find parameters with minimum error
    if  True:
        solution, cov_sol, infodict, mesg, ier = opt.leastsq(
            lambda x: paramfn(x, datarad, fixedR), init,
            full_output=True, maxfev=11*1000,
            diag=([1.0]*(5 if fixedR else 6)),
            ftol=1e-10, xtol=1e-10, factor=.01)
        print ("Initial error (%g) -> final error (%g): solution:"
               % tuple(map(lambda x: percent_error(
                   paramfn(x, datarad, fixedR,
                           False).ravel(),
                   data[:,2:].ravel()),
                           [init, solution])))
        paramprinter(solution, fixedR)

    # Display image with picked points
    if True:
        import matplotlib.pyplot as plt
        im = plt.imread('1970022.jpg')
        imtest(data, im, paramfn(solution, datarad, fixedR, False))
