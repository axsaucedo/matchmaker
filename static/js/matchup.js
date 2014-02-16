var matchup = {
    init : function() {

        $("#find-location-button").bind("click", function lookupGeoData() {
            console.log("here");
            myGeoPositionGeoPicker({
                startAddress     : 'University of Sheffield, Sheffield, UK',//'White House, Washington',
                returnFieldMap   : {
                    'match-form-lat' : '<LAT>',
                    'match-form-long' : '<LNG>',
                    'match-form-city' : '<CITY>',
                    'match-form-country' : '<COUNTRY>',
                    'match-form-zip' : ' <ZIP>',
                    'match-form-address' : '<ADDRESS>'
                }
            });
        });

    }
}

$(function() {
    matchup.init();
});