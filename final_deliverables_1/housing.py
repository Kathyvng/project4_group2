from flask import Flask, request, jsonify, render_template
import util  # Ensure this module is available and has the necessary functions

app = Flask(__name__)


# Define a route for the root URL ("/")
@app.route("/", methods=["GET"])
def index():
    return render_template("app.html")


# Define a route for getting city names
@app.route("/get_city_names", methods=["GET"])
def get_city_names():
    # Call the function that returns a list of city names
    cities = util.get_city_names()
    response = jsonify({"cities": cities})  # Corrected syntax with colon
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response  # Return the JSON response


# Define a route for getting zipcode names
@app.route("/get_zipcode_names", methods=["GET"])
def get_zipcode_names():
    # Call the function that returns a list of zipcodes
    zipcodes = util.get_zipcode_names()
    response = jsonify({"zipcodes": zipcodes})  # Corrected syntax with colon
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response  # Return the JSON response


@app.route("/get_estimated_price", methods=["OPTIONS", "POST"])
def get_estimated_price():
    if request.method == "OPTIONS":
        # Respond to the preflight request with necessary CORS headers
        response = app.make_response("")
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5501")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.status_code = 200  # Set status to 200 OK for OPTIONS request
        return response

    if request.method == "POST":
        # Your logic for POST request goes here
        data = request.get_json()

    # Ensure the data contains the required fields
    required_fields = [
        "bedrooms",
        "bathrooms",
        "sqft_living",
        "avg_income",
        "city",
        "zipcode",
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Extract the data from the request
    bedroom = float(data["bedrooms"])
    bathroom = float(data["bathrooms"])
    sqft_living = float(data["sqft_living"])  # Corrected typo here
    avg_income = float(data["avg_income"])
    city = data["city"]
    zipcode = data["zipcode"]

    # Call the utility function to get the estimated price
    estimated_price = util.get_estimated_price(
        bedroom, bathroom, sqft_living, avg_income, city, zipcode
    )

    # Return the estimated price as a JSON response
    response = jsonify({"estimated_price": estimated_price[0]})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# Add your other routes for predictions here

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction....")
    util.load_saved_artifacts()
    app.run(debug=False)
