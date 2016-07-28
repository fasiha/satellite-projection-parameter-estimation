Parameter estimation of satellite-projected maps
================================================

Background
----------

Richard Edes Harrison was a famous cartographic artist who created a map titled ["Europe from the East"](http://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~266329~5504885:Europe-From-The-East#) for his 1944 book, *Look at the World: the Fortune Atlas For world Strategy*. The David Rumsey Map Collection has a [reproduction](http://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~266329~5504885:Europe-From-The-East#) of this map (included in this repository without permission). To me, this is a masterpiece of visual art.

In her 1998 paper, ["Richard Edes Harrison and the challenge to American cartography"](http://www.jstor.org/stable/1151400) (in *Imago Mundi*, vol. 50, pp. 174--188), Susan Schulten wrote about Harrison's methods in producing this map (and many others): he would photograph a large globe---and as he worked in an era before computing, the rest is not hard to visualize.

The map is, if Harrison stayed true to his photograph of a globe, governed by the satellite (or near-sided perspective) projection. D3, a Javascript graphics library which includes this projection, provides [an example of the satellite projection](http://bl.ocks.org/mbostock/3790444). Note that a number of parameters are used to exactly specify the view desired (see the example's calls to `distance` and `rotate` and `tilt`).

Given a scan of "Europe from the East", we are interested in reproducing the map in modern cartographic software, and this requires estimating the several parameters that entirely capture the underlying cartographic projection.

The satellite projection
------------------------

While at the United States Geological Survey, John Snyder wrote his 1987 opus, *Map Projections---A Working Manual* (available as [PDF via USGS](http://pubs.er.usgs.gov/publication/pp1395) and completely online at [Google Books](http://books.google.com/books?id=nPdOAAAAMAAJ)). Among the many *hundreds* of projections that Snyder details mathematically---their forward and inverse transforms, worked examples (that is, unit tests), several examples, histories---are, starting on page 173, the vertical and tilted perspective projections, i.e., the satellite projection. For the case of the tilted satellite projection assuming a perfectly spherical earth, five parameters characterize the projection:

- base latitude `phi_1`,
- base longitude `lambda_0`,
- tilt angle `omega`,
- rotation angle `gamma`, and
- altitude, or alternatively, a ratio between the altitude and the radius of the earth, which Snyder denotes as `P = 1 + H/R` (for altitude `H` and radius `R`).

(The radius itself, `R`, can be flexible, but we assume this to be fixed, given Harrison's modus operandi.) See Snyder on page 175 for a detailed discussion, a particularly illuminating paragraph being excerpted here:

> In terms of a camera in space, the camera is placed at a distance
> `R*P` from the center of the Earth, perpendicularly over point
> `(phi1, lambda0)`. The camera is horizontally turned to face `gamma`
> clockwise from north, and then tilted `90 - omega` (in degrees)
> downward from horizontal, "horizontal" meaning parallel to a plane
> tangent to the sphere at `(phi1, lambda0)`. The photograph is then
> taken, placing points `(phi, lam)` in positions `(xt, yt)`, based on
> a scale reduction in `R`.

(The equations relating arbitrary lat/longs `(phi, lam)` to xy positions on one's map `(xt, yt)` is given on the same page.)

This implementation
-------------------
`harrison.py` in this repository implements the forward transform which converts lat/long into xy positions on a map, given the five parameters mentioned in the previous section, in Python. It also implements a parameter search (technically, a non-linear least squares function optimization, provided by [Scipy's `leastsq`]http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.leastsq.html), which allows one to find these five parameters given a list of lat/longs with their associated xy points on a map.

When I run `harrison.py` against the "Europe from the East" data samples, my 2009 Macbook Pro produces a result in a second. The results, for sixteen lat/long/x/y-tuples in `data.csv` are:

> R = 1, P = 1.82443 (-> H = 0.824428)
> lat/long: (55.9175, 58.2941) deg
> tilt/rot: (12.1078, -82.0505) deg

Validation of the results with Tributary.io/D3 (see below) and Google Earth (see `googearth.html`) have been positive.

Included with the Harrison map (`1970022.jpg`, obtained from the David Rumsey Map Collection, with lat/long/x/y truth data in `data.csv` (originally from `data.org`)) is a screenshot of my [Tributary.io inlet rendering a satellite projection using D3.geo](http://tributary.io/inlet/5654960) (`tributary.png` with data in `tributary.org` and `tributary.csv`; a backup of the inlet's Javascript is in `tributary.js`).

Challenges and going forward
----------------------------

As mentioned above, validation of the projection parameters calculated using sixteen two-dimensional data points using the Google Earth Javascript API (open `googearth.html` in your local browser) has been positive. However, two major challenges remain:

- Terrain. Harrison must have free-drawn the mountains, since they display extreme exaggeration. (To see this, recall that the projection places the camera 0.8 earth radii above the earth's surface, while Mount Everest is at most 0.001 earth radii above mean sea level. And yet in his [map](http://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~266329~5504885:Europe-From-The-East#), even the Atlas mountains in Morocco are towering over the curvature of the earth: totally unrealistic, but very artistic and educational.) In order to generate imagery with Harrison's level of vertical exaggeration, non-standard GIS techniques will have to be used (Google Earth limits the vertical exaggeration to three times).
- Lens. Harrison could have used wide-angle or telephoto lenses to photograph his globe. Both projection-based and 3D renderers such as Google Earth seem to be limited to non-lensed ray tracing, thus incapable of capturing any useful lens-induced distortion. The small but annoying residual between the final calculated pixel locations and the actual pixel locations in Harrison's map may be due to unmodeled lens effects (indicating, indirectly, that the lens used might have been close to normal).
