from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os
import json

app = Flask(__name__)

# Load model with absolute path
model_path = os.path.join(os.getcwd(), 'model', 'optimized_predict_pricing.pkl')
model = joblib.load(model_path)

# Load data from JSON file
data_path = os.path.join(os.getcwd(), 'static_data', 'real_estate_db.housing_merge.json')
try:
    with open(data_path, 'r') as file:
        data = json.load(file)
    df = pd.DataFrame(data)
except Exception as e:
    print(f"Error loading JSON file: {e}")
    df = pd.DataFrame()

@app.route('/')
def home():
    return render_template('Main.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        zipcode = int(request.form['Zipcode'])
        sqft_living = float(request.form['Sqft'])
        budget = float(request.form['Budget'])

        # Load additional data for avg_income, bedrooms, and bathrooms from JSON data
        record = df.loc[df['zipcode'] == zipcode].head(1)
        if not record.empty:
            avg_income = float(record['avg_income'].values[0])
            bedrooms = float(record['bedrooms'].values[0]) if 'bedrooms' in record.columns else 0
            bathrooms = float(record['bathrooms'].values[0]) if 'bathrooms' in record.columns else 0
        else:
            avg_income = 0
            bedrooms = 0
            bathrooms = 0

        # Create input_data with the required fields only
        input_data = pd.DataFrame([{
            'zipcode': zipcode,
            'sqft_living': sqft_living,
            'avg_income': avg_income,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms
        }])

        # Make prediction
        predicted_price = model.predict(input_data)[0]
        predicted_price = float(predicted_price)  # Ensure it's a Python float

        recommendation = (
            f"This is a good deal in {zipcode}!"
            if predicted_price <= budget
            else f"The predicted price is higher than your budget."
        )

        # Append new record to dataframe (optional for future use)
        new_record = {
            'zipcode': zipcode,
            'sqft_living': sqft_living,
            'predicted_price': predicted_price,
            'avg_income': avg_income,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms
        }
        global df
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)

        return render_template('Main.html', prediction=f"${predicted_price:,.2f}", recommendation=recommendation)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('Main.html', prediction="Model error. Please try again later.")

# Route to provide real-time data
@app.route('/data')
def data():
    try:
        # Get the latest 20 records from JSON data
        latest_records = df.sort_index(ascending=False).head(20)
        data = latest_records.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({'error': f"Failed to load data: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
