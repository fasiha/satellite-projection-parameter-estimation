var ge;
google.load("earth", "1");

function init() {
    google.earth.createInstance('map3d', initCB, failureCB);
}

function initCB(instance) {
    ge = instance;
    ge.getWindow().setVisibility(true);
    ge.getLayerRoot().enableLayerById(ge.LAYER_BORDERS, true);
    ge.getOptions().setGridVisibility(true);

    var radius_of_earth = 6371e3; // meters

    // My estimate of Harrison's "Europe from the East"
    var Peurope = 1.82;
    var lateurope = 55.9;
    var loneurope = 58.3;
    var roleurope = -82.1;
    var tileurope = 12.1;

    // Snyder's figure 37
    var Ps = 160e3 / radius_of_earth + 1.0;
    var lats = 41.0;
    var lons = -74.0;
    var tils = 55; // omega
    var rols = 210; // gamma

    if (1) {
        var P = Peurope;
        var lat = lateurope;
        var lon = loneurope;
        var til = tileurope;
        var rol = roleurope;
    } else {
        var P = Ps;
        var lat = lats;
        var lon = lons;
        var til = tils;
        var rol = rols;
    }


    var height = (P-1.0) * radius_of_earth;

    var camera = ge.getView().copyAsCamera(ge.ALTITUDE_RELATIVE_TO_GROUND);
    camera.setLatitude(lat);
    camera.setLongitude(lon);
    camera.setAltitude(height);

    camera.setHeading(rol);
    camera.setTilt(til);

    ge.getView().setAbstractView(camera);
}

function failureCB(errorCode) {
}

google.setOnLoadCallback(init);
