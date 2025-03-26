// Fix for getting the selected bedroom value
function getBedValue() {
    var uiBedrooms = document.getElementsByName("uiBedroom");
    for (var i in uiBedrooms) {
        if (uiBedrooms[i].checked) {
            return parseInt(uiBedrooms[i].value); // Return the value of the selected radio button
        }
    }
    return -1; // Invalid value if no bedroom selected
}

// Fix for getting the selected bathroom value
function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathroom");
    for (var i in uiBathrooms) {
        if (uiBathrooms[i].checked) {  // Corrected: check uiBathrooms instead of uiBedrooms
            return parseFloat(uiBathrooms[i].value); // Return the value of the selected radio button
        }
    }
    return -1; // Invalid value if no bathroom selected
}

function onClickedEstimatePrice() {

    console.log("Estimate price button clicked");

    var bedroom = getBedValue();
    var bathroom = getBathValue();
    var sqft_living = document.getElementById('uiSqft').value;
    var avg_income = document.getElementById('uiIncome').value;
    var city = document.getElementById('uiCities').value;
    var zipcode = document.getElementById('uiZipcodes').value;
    var estPrice = document.getElementById("uiPredictPrice");

    var url = "/get_estimated_price";

    // Send a POST request to the Flask API
    // $.post(url, {
    //     bedrooms: bedroom,
    //     bathrooms: bathroom,
    //     sqft_living: parseFloat(document.getElementById('uiSqft').value),
    //     avg_income: parseFloat(document.getElementById('uiIncome').value),
    //     city: document.getElementById('uiCities').value,       // No need for .value
    //     zipcode: document.getElementById('uiZipcodes').value  // No need for .value
    // }, function (data) {
    //     console.log(data.estimated_price);
    //     estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " USD</h2>";
    // })
    
    // $.post(url, JSON.stringify({
    //     bedrooms: 3,
    //     bathrooms: 2,
    //     sqft_living: 1200,
    //     avg_income: 50000,
    //     city: "city_seattle",       // No need for .value
    //     zipcode: "zipcode_98002"  // No need for .value
    // }), function (data) {
    //     console.log(data.estimated_price);
    //     estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " USD</h2>";
    // }) 
    $.ajax({
        url: url,
        type: "POST",
        data: JSON.stringify({
            bedrooms: bedroom,
            bathrooms: bathroom,
            sqft_living: parseFloat(document.getElementById('uiSqft').value),
            avg_income: parseFloat(document.getElementById('uiIncome').value),
            city: document.getElementById('uiCities').value,       // No need for .value
            zipcode: document.getElementById('uiZipcodes').value  // No need for .value
        }),
        headers: {                  
            "Content-Type": "application/json"
          },
          dataType: "json",
        success: function (data) {
            console.log(data.estimated_price);
            estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " USD</h2>";
        },
      });
}

// On page load, populate cities and zipcodes
function onPageLoad1() {
    console.log("Document loaded");
    var url = "http://localhost:5000/get_city_names";
    $.get(url, function(data, status) {
        console.log("Got response for get_city_names request");
        if (data) {
            var cities = data.cities;
            var uiCities = document.getElementById("uiCities");
            $('#uiCities').empty();
            for (var i = 0; i < cities.length; i++) {
                var opt = new Option(cities[i]);
                $('#uiCities').append(opt);
            }
        }
    });
}

function onPageLoad2() {
    console.log("Document loaded");
    var url = "http://localhost:5000/get_zipcode_names";
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