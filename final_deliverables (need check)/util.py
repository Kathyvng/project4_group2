import util
import json
import pickle
import numpy as np
import pandas as pd

__cities = None
__zipcodes = None
__data_columns = None
__model = None

# Load model
with open("./artifacts/optimized_predict_pricing.pickle", "rb") as f:
    __model = pickle.load(f)
    print("Model loaded successfully:", type(__model))


def get_estimated_price(bedrooms, bathrooms, sqft_living, avg_income, city, zipcode):
    X1 = np.zeros(len(__data_columns))
    X1[0] = bedrooms
    X1[1] = bathrooms
    X1[2] = sqft_living
    X1[3] = avg_income

    zipcode = str(zipcode)  # Ensure zipcode is treated as string

    # Print the processed city and zipcode for debugging
    print(f"Processed city: {city}")
    print(f"Processed zipcode: {zipcode}")

    # Check if city and zipcode are in the data columns
    try:
        loc_index1 = __data_columns.index(city)
        print(f"City '{city}' found at index {loc_index1}")
    except ValueError:
        print(f"City '{city}' not found in data columns.")
        loc_index1 = -1

    try:
        loc_index2 = __data_columns.index(zipcode)
        print(f"Zipcode '{zipcode}' found at index {loc_index2}")
    except ValueError:
        print(f"Zipcode '{zipcode}' not found in data columns.")
        loc_index2 = -1

    # Set the appropriate columns if found
    if loc_index1 >= 0:
        X1[loc_index1] = 1

    if loc_index2 >= 0:
        X1[loc_index2] = 1

    # Convert X1 to DataFrame
    X1_df = pd.DataFrame([X1], columns=__data_columns)
    print(X1_df)
    # Predict and return result
    prediction = __model.predict(X1_df)
    print(f"Predicted price: {prediction}")
    return prediction


def get_city_names():
    return __cities


def get_zipcode_names():
    return __zipcodes


def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns
    global __cities
    global __zipcodes
    global __model

    # Load columns and model
    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __cities = __data_columns[4:12]  # This should include city names
        __zipcodes = __data_columns[13:]  # This should include zipcodes

    global __model
    with open("./artifacts/optimized_predict_pricing.pickle", "rb") as f:
        __model = pickle.load(f)
        print("Loading saved artifacts...done")


if __name__ == "__main__":
    load_saved_artifacts()
    print("Cities:", get_city_names())
    print("Zipcodes:", get_zipcode_names())

    # Example test cases
    print(get_estimated_price(2, 2, 1200, 60000, "city_auburn", 98001))
    print(get_estimated_price(2, 1, 1400, 80000, "city_auburn", 98003))
    print(get_estimated_price(2, 1, 1400, 80000, "city_federal_way", 98003))
    print(get_estimated_price(2, 1, 1400, 80000, "city_federal_way", 98003))
