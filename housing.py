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
        sqft_lot = float(request.form['Sqft'])
        price = float(request.form['Budget'])

        input_data = pd.DataFrame([{
            'zipcode': zipcode,
            'sqft_lot': sqft_lot,
            'price': price
        }])

        # Make prediction
        predicted_price = model.predict(input_data)[0]

        # Convert numpy types to Python native types
        predicted_price = float(predicted_price)

        recommendation = (
            f"This is a good deal in {zipcode}!"
            if predicted_price <= price
            else f"The predicted price is higher than your budget."
        )

        # Save to MongoDB (convert numpy types to native Python types)
        record = {
            'zipcode': int(zipcode),  # Ensure it's a Python int
            'sqft_lot': float(sqft_lot),  # Ensure it's a Python float
            'price': float(predicted_price)  # Ensure it's a Python float
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
        records = collection.find().sort('_id', -1).skip(0).limit(20)
        data = [
            {
                'zipcode': int(record.get('zipcode')) if record.get('zipcode') else None,
                'sqft_lot': float(record.get('sqft_lot')) if record.get('sqft_lot') else None,
                'price': float(record.get('price')) if record.get('price') else None
            }
            for record in records
        ]
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({'error': f"Failed to load data: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)