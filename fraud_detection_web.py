# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:58:21 2024

@author: tejas
"""

import streamlit as st
import numpy as np
import pickle
from sklearn.preprocessing import OneHotEncoder

# Load models (replace with your filepaths)
loaded_rf_model = pickle.load(open(r"C:\Users/tejas/OneDrive/Desktop/fraud_detection/RF_model.sav", 'rb'))
loaded_knn_model = pickle.load(open(r'C:\Users/tejas/OneDrive/Desktop/fraud_detection/KNN_model.sav', 'rb'))

# Title and description
st.title("Online Transaction Fraud Detection")
st.write("This web app predicts whether a transaction is fraudulent or not based on various features.")

# Feature input
st.sidebar.header("Enter Transaction Details")
step = st.sidebar.number_input("Step (Hour of the day)", min_value=1, max_value=744)
type = st.sidebar.selectbox("Transaction Type", ["CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"])
amount = st.sidebar.number_input("Amount ($)", min_value=0.0)
oldbalanceOrg = st.sidebar.number_input("Old Balance Origin", min_value=0.0)
newbalanceOrig = st.sidebar.number_input("New Balance After", min_value=0.0)
oldbalanceDest = st.sidebar.number_input("Old Balance Destination", min_value=0.0)
newbalanceDest = st.sidebar.number_input("New Balance Destination", min_value=0.0)

# Model selection
model_choice = st.sidebar.radio("Select Model:", ("Random Forest", "KNN"))

# Predict function
def predict(model, data):
    input_data_as_numpy_array = np.asarray(data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = model.predict(input_data_reshaped)
    return prediction[0]

# Prediction
if st.sidebar.button("Predict"):
    enc = OneHotEncoder(sparse=False, drop='first')
    type_encoded = enc.fit_transform([[type]])[0]
    
    input_data = (step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest)
    
    if model_choice == "Random Forest":
        prediction = predict(loaded_rf_model, input_data)
    elif model_choice == "KNN":
        prediction = predict(loaded_knn_model, input_data)

    if prediction == 0:
        st.success("The transaction seems legitimate.")
    else:
        st.error("The transaction is flagged as potentially fraudulent.")
