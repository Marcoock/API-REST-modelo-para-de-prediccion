# Flask
from flask import Flask, render_template, request
# Data manipulation
import pandas as pd
# Matrices manipulation
import numpy as np
# Script logging
import logging
# ML model
import joblib
# JSON manipulation
import json
# Utilities
import sys
import os

# Current directory
current_dir = os.path.dirname(__file__)

# Flask app
app = Flask(__name__, static_folder = 'static', template_folder = 'template')

# Logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# Function
def ValuePredictor(data = pd.DataFrame):
	# Model name
	model_name = 'model_TT_RFC.pkl'
	# Directory where the model is stored
	model_dir = os.path.join(current_dir, model_name)
	# Load the model
	loaded_model = joblib.load(open(model_dir, 'rb'))
	# Predict the data
	result = loaded_model.predict(data)
	return result[0]

# Home page
@app.route('/')
def home():
	return render_template('index.html')

# Prediction page
@app.route('/prediction', methods = ['POST'])
def predict():
	if request.method == 'POST':
		# Get the data from form
		no2 = request.form['no2']

		# Load template of JSON file containing columns name
		# Schema name
		schema_name = 'columns_set.json'
		# Directory where the schema is stored
		schema_dir = os.path.join(current_dir, schema_name)
		with open(schema_dir, 'r') as f:
			cols =  json.loads(f.read())
		schema_cols = cols['data_columns']

		# Parse the numerical columns
		schema_cols['no2'] = no2

		# Convert the JSON into data frame
		df = pd.DataFrame(
				data = {k: [v] for k, v in schema_cols.items()},
				dtype = float
			)

		# Create a prediction
		print(df.dtypes)
		result = ValuePredictor(data = df)

		# Determine the output
		if int(result) == 1:
			prediction = 'Las cantidades de dióxido de nitrógeno en en el ambiente son peligrosas para la salud!'
		else:
			prediction = 'Los niveles de dióxido de nitrógeno en el ambiente son buenos!'

		# Return the prediction
		return render_template('prediction.html', prediction = prediction)
	
	# Something error
	else:
		# Return error
		return render_template('error.html', prediction = prediction)

if __name__ == '__main__':
    app.run(debug = True)
