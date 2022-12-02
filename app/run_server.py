# https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers

import dill
import pandas as pd
import numpy as np
import os
dill._dill._reverse_typemap['ClassType'] = type
import flask
from flask import Flask, request, render_template
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import sys
import pathlib

cwd = pathlib.Path().cwd()
sys.path.append(cwd.as_posix())
model_folder = cwd.joinpath('models')

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)

#modelpath = "app/models/Churning_pipeline.dill"
modelpath = "/app/app/models/Churning_pipeline.dill"
load_model(modelpath)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():

	dt = strftime("[%Y-%b-%d %H:%M:%S]")

	to_predict = request.form.to_dict()
    #print(to_predict["Total_Trans_Amt"])

	if to_predict["Total_Ct_Chng_Q4_Q1"]:
		Total_Ct_Chng_Q4_Q1 = float(to_predict['Total_Ct_Chng_Q4_Q1'])

	if to_predict["Total_Trans_Amt"]:
		Total_Trans_Amt = int(to_predict['Total_Trans_Amt'])

	if to_predict["Total_Trans_Ct"]:
		Total_Trans_Ct = int(to_predict['Total_Trans_Ct'])

	if to_predict["Total_Relationship_Count"]:
		Total_Relationship_Count = int(to_predict['Total_Relationship_Count'])

	if to_predict["Total_Amt_Chng_Q4_Q1"]:
		Total_Amt_Chng_Q4_Q1 = float(to_predict['Total_Amt_Chng_Q4_Q1'])

	if to_predict["Months_Inactive_12_mon"]:
		Months_Inactive_12_mon = int(to_predict['Months_Inactive_12_mon'])

	if to_predict["Total_Revolving_Bal"]:
		Total_Revolving_Bal = int(to_predict['Total_Revolving_Bal'])

	logger.info(f"{dt} Data: Total_Trans_Amt={Total_Trans_Amt}, Total_Trans_Ct={Total_Trans_Ct}, \
	    Total_Relationship_Count={Total_Relationship_Count}, Total_Amt_Chng_Q4_Q1={Total_Amt_Chng_Q4_Q1}, \
	    Months_Inactive_12_mon={Months_Inactive_12_mon}, Total_Revolving_Bal={Total_Revolving_Bal}")

	try:
		preds = model.predict_proba(pd.DataFrame({
			                                      "Total_Ct_Chng_Q4_Q1": [Total_Ct_Chng_Q4_Q1],
			                                      "Total_Trans_Amt": [Total_Trans_Amt],
												  "Total_Trans_Ct": [Total_Trans_Ct],
												  "Total_Relationship_Count": [Total_Relationship_Count],
												  "Total_Amt_Chng_Q4_Q1": [Total_Amt_Chng_Q4_Q1],
												  "Months_Inactive_12_mon": [Months_Inactive_12_mon],
												  "Total_Revolving_Bal": [Total_Revolving_Bal]
												  }))

	except AttributeError as e:
		logger.warning(f'{dt} Exception: {str(e)}')
		result = str(e)
		return render_template('index.html', result=f'Mistake: ${result}')
	result = preds[:, 1][0]
	return render_template('index.html', result=f'Probability churning customer: ${result}')

if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='0.0.0.0', debug=True, port=port)
