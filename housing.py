from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from pymongo import MongoClient
import os

app = Flask(__name__)

# Load model with absolute path
model_path = os.path.join(os.getcwd(), 'model', 'optimized_predict_pricing.pkl')
model = joblib.load(model_path)

# Connect to MongoDB with error handling
try:
    client = MongoClient('localhost', 27017)
    db = client['real_estate_db']
    collection = db['housing_merge']
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def home():
    return render_template('Main.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        zipcode = int(request.form['Zipcode'])
        sqft_living = float(request.form['Sqft'])
        budget = float(request.form['Budget'])

        # Load additional data for avg_income from MongoDB
        record = collection.find_one({'zipcode': zipcode})
        avg_income = float(record.get('avg_income')) if record else 0

        input_data = pd.DataFrame([{
            'zipcode': zipcode,
            'sqft_living': sqft_living,
            'price': budget,
            'avg_income': avg_income
        }])

        # Make prediction
        predicted_price = model.predict(input_data)[0]
        predicted_price = float(predicted_price)  # Ensure it's a Python float

        recommendation = (
            f"This is a good deal in {zipcode}!"
            if predicted_price <= budget
            else f"The predicted price is higher than your budget."
        )

        # Save to MongoDB
        record = {
            'zipcode': int(zipcode),
            'sqft_living': float(sqft_living),
            'price': float(predicted_price),
            'avg_income': float(avg_income)  # Ensure it's a float
        }
        collection.insert_one(record)

        return render_template('Main.html', prediction=f"${predicted_price:,.2f}", recommendation=recommendation)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('Main.html', prediction="Model error. Please try again later.")


# Route to provide real-time data
@app.route('/data')
def data():
    try:
        # Pull the latest 20 records from MongoDB
        records = collection.find().sort('_id', -1).limit(20)
        data = [
            {
                'zipcode': int(record.get('zipcode')) if record.get('zipcode') else None,
                'sqft_living': float(record.get('sqft_living')) if record.get('sqft_living') else None,
                'price': float(record.get('price')) if record.get('price') else None,
                'avg_income': float(record.get('avg_income')) if record.get('avg_income') else None, # Added avg_income
                'crime_rate_per_capita': float(record.get('crime_rate_per_capita')) if record.get('crime_rate_per_capita') else None
            }
            for record in records
        ]
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({'error': f"Failed to load data: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True)
