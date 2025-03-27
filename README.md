# project4_group2

Real Estate Pricing Forecasting

## Overview of the Analysis

The real estate market is complex and influenced by a variety of factors such as location, property size, crime rates, and income levels. Homebuyers often face challenges in identifying affordable properties that meet their criteria and in understanding market trends. This project aims to address these issues by developing a predictive model that helps users find suitable real estate options based on their budget and property preferences.

## Data Sources:

* Main Dataset: Housing Price Dataset – Historical data on real estate prices and property details.
* Supplementary Datasets:
 - Crime Rates: Crime Rates: Crime statistics by city and state.
 - Income: Average income data by zip code.
 - US Zipcode and City Data

* Dataset Size: The main dataset contains 21,613 entries.

 ## Ethical Considerations

Throughout the development of this project, we prioritized ethical considerations. The data was sourced from Kaggle and is marked under the CC0 Legal Code as Public Domain, and was anonymized to protect individual privacy. Our goal was to present real estate pricing information in an accurate, clear, and transparent manner.

## Folders/Files Breakdown

The results are stored in the folder Final_Deliverables, with the following folder/file structure:

- artifacts:
    + columns.json: Columns used for the Flask Python server.
    + optimized_predict_pricing.pickle: Final pickle model file used by the Flask Python server.
- model_building:
    + housing_ml_models_1.ipynb: Build models, test models, and test predictions.
    + housing_price_cleaning.ipynb: Jupyter notebook to clean data and engineer features.
- Output: Group presentation file, visualization files (charts/heatmaps), and Tableau dashboard.
- Resources: Four CSV datasets and one cleaned data file (housing_merge.csv) used for model building and the visualization dashboard (Tableau).
- static:
    + app.css: Stylesheet for the UI application.
    + app.js: Contains dynamic code for making HTML calls to the backend to retrieve data.
    + app.html: Contains the structure of the UI elements.
- housing.py: Flask Python server used as the backend for the UI application.
- util.py: Contains core routines for handling routing requests and responses in the Flask Python server.

## Methodology

* Data cleaning: Python Pandas
* Model Training: Scikit-learn
* Visualization: Python Matplotlib, Tableau
* User Interface: HTML/CSS, JavaScript, MongoDB Database

* Process:
  - Data Reading: The four datasets were read from the Resources folder into a Jupyter Notebook for data cleaning.
  - Data Cleaning: Removed inconsistencies, handled missing data, and converted features to their correct data types.
  - Feature Engineering: Generated additional features such as price per square foot and crime rate per capita.
  - Model building and analysis: 
        + Selected Linear Regression as the model for predicting continuous target values (price).
        + Tested multiple feature sets and used GridSearchCV to compare three models (Linear Regression, Lasso, and Decision Tree).
        + Linear Regression was selected as the best model.
        + Used Matplotlib to visualize feature-target correlations, confirming strong positive correlations.
  - Prediction: Used Python to predict real estate prices.
  - Visualization and Dashboard: Developed a Flask app for user interaction and a Tableau Dashboard to display the overall trends in real estate pricing.

## Summary of Findings

 - Achieved approximately 75% accuracy using Linear Regression.
 - Tested 18 features and narrowed them down to the top 4 using correlation analysis.
 - Used GridSearchCV to confirm that Linear Regression was the best model.

## Conclusion

* Key Takeaways
 - Data-driven models simplify complex home-buying decisions
 - Neighborhood insights based on user preferences and market data provide better decision-making tools.
 - Transparent, accurate predictions foster user trust.
* Final Thought
Smarter real estate choices start with the right data.

