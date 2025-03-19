from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from pymongo import MongoClient
import os

app = Flask(__name__)

# Load model with absolute path
model_path = os.path.join(os.path.dirname(__file__), 'model_rf', 'housing_price.pkl')
model = joblib.load(model_path)

# Connect to MongoDB with error handling
try:
    client = MongoClient('localhost', 27017)
    db = client['real_estate_db']
    collection = db['predictions']
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def home():
    return render_template('Main.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        state = request.form['State']
        bedrooms = int(request.form['Bedrooms'])
        bathrooms = int(request.form['Bathrooms'])
        sqft = float(request.form['Sqft'])
        budget = float(request.form['Budget'])
    except (ValueError, KeyError) as e:
        return render_template('Main.html', prediction="Invalid input. Please check your entries.")

    input_data = {
        'State': state,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'Sqft': sqft,
        'Budget': budget
    }

    input_df = pd.DataFrame([input_data])

    try:
        predicted_price = model.predict(input_df)[0]
    except Exception as e:
        return render_template('Main.html', prediction="Model error. Please try again later.")

    recommendation = (
        f"This is a good deal in {state}!"
        if predicted_price <= budget
        else f"The predicted price is higher than your budget."
    )

    # Save to MongoDB
    record = {
        'input_data': input_data,
        'predicted_price': predicted_price,
        'recommendation': recommendation
    }
    collection.insert_one(record)

    return render_template('Main.html', prediction=f"${predicted_price:,.2f}", recommendation=recommendation)

# Route to provide real-time data
@app.route('/data')
def data():
    try:
        records = collection.find().sort('_id', -1).skip(0).limit(20)
        data = [
            {
                'state': record['input_data']['State'],
                'sqft': record['input_data']['Sqft'],
                'price': record['predicted_price'],
                'bedrooms': record['input_data']['Bedrooms'],
                'bathrooms': record['input_data']['Bathrooms']
            }
            for record in records
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f"Failed to load data: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
