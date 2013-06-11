var ge;
google.load("earth", "1");

function init() {
    google.earth.createInstance('map3d', initCB, failureCB);
}

function initCB(instance) {
    ge = instance;
    ge.getWindow().setVisibility(true);

    var radius_of_earth = 6371e3; // meters
    var P = 1.81; // unitless, Snyder's variable name
    var height = (P-1.0) * radius_of_earth;

    var camera = ge.getView().copyAsCamera(ge.ALTITUDE_RELATIVE_TO_GROUND);
    camera.setLatitude(55.9);
    camera.setLongitude(58.3);
    camera.setAltitude(height);

    ge.getView().setAbstractView(camera);
}

function failureCB(errorCode) {
}

google.setOnLoadCallback(init);
