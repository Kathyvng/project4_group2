// Fix for getting the selected bedroom value
function getBedValue() {
    var uiBedrooms = document.getElementsByName("uiBedroom");
    for (var i in uiBedrooms) {
        if (uiBedrooms[i].checked) {
            return parseInt(i)+1; // Return the value of the selected radio button
        }
    }
    return -1; // Invalid value if no bedroom selected
}

// Fix for getting the selected bathroom value
function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathroom");
    for (var i in uiBathrooms) {
        if (uiBathrooms[i].checked) {  // Corrected: check uiBathrooms instead of uiBedrooms
            return parseInt(i) + 1; // Return the value of the selected radio button
        }
    }
    return -1; // Invalid value if no bathroom selected
}

function onClickedEstimatePrice(event) {
    event.preventDefault();  // Prevent form submission when the button is clicked

    console.log("Estimate price button clicked");

    var bedroom = getBedValue();
    var bathroom = getBathValue();
    var sqft_living = document.getElementById('uiSqft').value;
    var avg_income = document.getElementById('uiIncome').value;
    var city = document.getElementById('uiCities').value;
    var zipcode = document.getElementById('uiZipcodes').value;
    var estPrice = document.getElementById("uiPredictPrice");

    var url = "http://127.0.0.1:5000/predict_home_price";

    // Send a POST request to the Flask API
    $.post(url, {
        bedroom: bedroom,
        bathroom: bathroom,
        sqft_living: parseFloat(sqft_living),
        avg_income: parseFloat(avg_income),
        city: city,       // No need for .value
        zipcode: zipcode  // No need for .value
    })
    .done(function (data) {
        console.log(data.estimated_price);
        estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " USD</h2>";
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
        console.log("Error: " + textStatus + ", " + errorThrown);
        estPrice.innerHTML = "<h2>Something went wrong, please try again.</h2>";
    });
}

// On page load, populate cities and zipcodes
function onPageLoad1() {
    console.log("Document loaded");
    var url = "http://127.0.0.1:5000/get_city_names";
    $.get(url, function(data, status) {
        console.log("Got response for get_city_names request");
        if (data) {
            var cities = data.cities;
            var uiCities = document.getElementById("uiCities");
            $('#uiCities').empty();
            for (var i in cities) {
                var opt = new Option(cities[i]);
                $('#uiCities').append(opt);
            }
        }
    });
}

function onPageLoad2() {
    console.log("Document loaded");
    var url = "http://127.0.0.1:5000/get_zipcode_names";
    $.get(url, function(data, status) {
        console.log("Got response for get_zipcode_names request");
        if (data) {
            var zipcodes = data.zipcodes;
            var uiZipcode = document.getElementById("uiZipcodes");
            $('#uiZipcodes').empty();
            for (var i in zipcodes) {
                var opt = new Option(zipcodes[i]);
                $('#uiZipcodes').append(opt);
            }
        }
    });
}

// Ensure both onPageLoad functions are called when the page loads
window.onload = function() {
    onPageLoad1();
    onPageLoad2();
};