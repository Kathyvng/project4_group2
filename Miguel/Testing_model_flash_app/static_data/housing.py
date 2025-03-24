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

        zipcode_list= ['zipcode_98001','zipcode_98002', 'zipcode_98003', 'zipcode_98004', 'zipcode_98005',
       'zipcode_98006', 'zipcode_98007', 'zipcode_98008', 'zipcode_98023',
       'zipcode_98030', 'zipcode_98031', 'zipcode_98032', 'zipcode_98033',
       'zipcode_98034', 'zipcode_98042', 'zipcode_98052', 'zipcode_98053',
       'zipcode_98055', 'zipcode_98056', 'zipcode_98058', 'zipcode_98059',
       'zipcode_98074', 'zipcode_98075', 'zipcode_98092', 'zipcode_98102',
       'zipcode_98103', 'zipcode_98105', 'zipcode_98106', 'zipcode_98107',
       'zipcode_98108', 'zipcode_98109', 'zipcode_98112', 'zipcode_98115',
       'zipcode_98116', 'zipcode_98117', 'zipcode_98118', 'zipcode_98119',
       'zipcode_98122', 'zipcode_98125', 'zipcode_98126', 'zipcode_98133',
       'zipcode_98136', 'zipcode_98144', 'zipcode_98146', 'zipcode_98148',
       'zipcode_98155', 'zipcode_98166', 'zipcode_98168', 'zipcode_98177',
       'zipcode_98178', 'zipcode_98188', 'zipcode_98198', 'zipcode_98199']
        
        # setting to default 0
        zipcode_data = {col:0 for col in zipcode_list}
        zipcode = str(request.form['zipcode'])  # Zipcode should be a string
        zipcode_data[f'zipcode_{zipcode}']= 1


        # Create input_data with the required fields only
        input_data = pd.DataFrame([{
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sqft_living': sqft_living,
            'zipcode': zipcode,
            **city_data
            **zipcode_data
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
