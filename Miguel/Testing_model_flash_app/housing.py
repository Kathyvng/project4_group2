from flask import Flask, render_template, request
import pandas as pd
import joblib
import os


app = Flask(__name__)

# Load model with absolute path
model_path = os.path.join(os.getcwd(), 'model', 'optimized_predict_pricing.pkl')
model = joblib.load(model_path)



@app.route('/')
def home():
    return render_template('main.html')

@app.route('/predict', methods=['POST'])
def predict():
   

        # Get user inputs from form
        bedrooms= int(request.form['bedrooms'])
        bathrooms = float(request.form["bathrooms"])
        sqft_living = int(request.form['sqft_living'])
        #code help from Project 4 example in class https://github.com/mflynn2u/Project_4_Sample/tree/main?tab=readme-ov-file
        #initialize city's
        city_list = ['city_Auburn','city_Bellevue',
       'city_Federal Way', 'city_Kent', 'city_Kirkland', 'city_Redmond',
       'city_Renton', 'city_Sammamish', 'city_Seattle']
        #setting to default 0
        city_data = {i: 0 for i in city_list}
        selected_city = request.form['city']
        city_data[f'city_{selected_city}']=1

     


        # Create input_data with the required fields only
        input_data = pd.DataFrame([{
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sqft_living': sqft_living,
            
            **city_data
         
        }])

        print(f"Input Data: {input_data}")

        # Make prediction
        predicted_price = model.predict(input_data)
        predicted_price = float(predicted_price[0])  # Ensure it's a Python float

        # Generate recommendation based on budget
        ##recommendation = (
        ##    f"This is a good deal in {zipcode}!"
       ##     if predicted_price <= budget
        ##    else f"The predicted price is higher than your budget."
       ## )



        # Add new data to df
        #df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)

        return render_template('main.html', prediction=f"${predicted_price:,.2f}")


# Route to provide real-time data
#

if __name__ == '__main__':
    app.run(debug=True)
