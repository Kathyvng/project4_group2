from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load the trained model
model_path = os.path.join('model', 'housing_price.pkl')
model = joblib.load(model_path)

@app.route('/')
def home():
    return render_template('Main.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data
    state = request.form['State']
    bedrooms = int(request.form['Bedrooms'])
    bathrooms = int(request.form['Bathrooms'])
    sqft = float(request.form['Sqft'])
    budget = float(request.form['Budget'])
    
    # Prepare data for model prediction
    input_data = {
        'State': state,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'Sqft': sqft,
        'Budget': budget
    }
    
    input_df = pd.DataFrame([input_data])

    # Make prediction
    predicted_price = model.predict(input_df)[0]

    # Generate recommendation based on the budget and state
    if predicted_price <= budget:
        recommendation = f"This is a good deal in {state}!"
    else:
        recommendation = f"The predicted price is higher than your budget. Try a different location or reduce criteria."

    return render_template('Main.html', prediction=f"${predicted_price:,.2f}", recommendation=recommendation)

if __name__ == '__main__':
    app.run(debug=True)
