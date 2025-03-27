from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os
import json

app = Flask(__name__)

# Load model with absolute path
model_path = os.path.join(os.getcwd(), "model", "optimized_predict_pricing.pkl")
model = joblib.load(model_path)

# Load data from JSON file
data_path = os.path.join(
    os.getcwd(), "static_data", "real_estate_db.housing_merge.json"
)
try:
    with open(data_path, "r") as file:
        data = json.load(file)
    df = pd.DataFrame(data)
except Exception as e:
    print(f"Error loading JSON file: {e}")
    df = pd.DataFrame()


# Function to preprocess input data before feeding to model
def preprocess_input_data(input_data):
    input_data_encoded = pd.get_dummies(
        input_data, columns=["city", "zipcode"], drop_first=True
    )

    # Ensure input data has all the required columns
    model_columns = list(
        df.columns
    )  # Assuming df contains columns used during training
    missing_cols = set(model_columns) - set(input_data_encoded.columns)
    for col in missing_cols:
        input_data_encoded[col] = 0  # Add missing columns with 0

    # Reorder columns to match the model's expected input
    input_data_encoded = input_data_encoded[model_columns]

    return input_data_encoded


# Helper function to get user input from HTML form
def get_user_input_from_form(form_data):
    # Extract user inputs from form (with default values)
    bedrooms = int(form_data.get("bedrooms", 3))
    bathrooms = float(form_data.get("bathrooms", 2.0))
    sqft_living = int(form_data.get("sqft_living", 1500))
    avg_income = float(form_data.get("avg_income", 65000))
    city = form_data.get("city", "Seattle")
    zipcode = form_data.get("zipcode", "98105")

    return pd.DataFrame(
        [[bedrooms, bathrooms, sqft_living, city, zipcode, avg_income]],
        columns=[
            "bedrooms",
            "bathrooms",
            "sqft_living",
            "city",
            "zipcode",
            "avg_income",
        ],
    )


@app.route("/")
def home():
    return render_template("Main.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user inputs from form
        input_data = get_user_input_from_form(request.form)

        # Preprocess input data
        input_data_encoded = preprocess_input_data(input_data)

        # Make prediction
        predicted_price = model.predict(input_data_encoded)[0]
        predicted_price = float(predicted_price)  # Ensure it's a Python float

        # Get the budget from user input, also handling default values
        budget = float(
            request.form.get("budget", 1000000)
        )  # Default budget is 1 million

        # Generate recommendation based on budget
        recommendation = (
            f"This is a good deal in {input_data['zipcode'][0]}!"
            if predicted_price <= budget
            else f"The predicted price is higher than your budget."
        )

        # Return results to template
        return render_template(
            "Main.html",
            prediction=f"${predicted_price:,.2f}",
            recommendation=recommendation,
        )

    except Exception as e:
        print(f"Error: {e}")
        return render_template(
            "Main.html", prediction="Model error. Please try again later."
        )


# Route to provide real-time data
@app.route("/data")
def data():
    try:
        # Get the latest 20 records from JSON data
        latest_records = df.sort_index(ascending=False).head(20)
        data = latest_records.to_dict(orient="records")
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": f"Failed to load data: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
