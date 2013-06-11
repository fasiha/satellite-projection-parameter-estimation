//http://www.nytimes.com/interactive/2013/03/01/world/americas/border-graphic.html
var svg = d3.select("svg");

var width = tributary.sw;
var height = tributary.sh;

var world = tributary.world110;
var countries = topojson.object(world, world.objects.countries);
var us = tributary.us;
//var states = topojson.object(us, us.objects.land);
var globe = {type: "Sphere"};
var d = 1.82;
var projection = d3.geo.satellite()
    .distance(d)
    .scale(944)
    .rotate([-58.3, -56.9, -82])//-long,-lat,rot clockwise from north
    .center([0, 0])
    .translate([294,653])
    .tilt(-12)
    .clipAngle(Math.acos(1 / d) * 180 / Math.PI - 1e-6);

//var projection = d3.geo.mercator()
//.scale(650)

// The reference 74ºW, 41ºN is at 181px, 710px.
//var offset = projection.translate([-181, -710])([-74, 41]);
//projection.translate([-offset[0], -offset[1]]);
//alert(([0.0,0.0]))


var graticule = d3.geo.graticule()
      .extent([[-40, 40], [40 + 1e-6, 70 + 1e-6]])//[long,lat]
    .step([10, 10]);

var path = d3.geo.path()
    .projection(projection);

svg.append("path")
    .datum(graticule)
    .attr("class", "graticule")
    .attr("d", path);

svg.append("path")
.datum(countries)
.attr("class", "land")
.attr("d", path);
