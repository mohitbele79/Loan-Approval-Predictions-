from flask import Flask,render_template,request
from utils.single_data_clean import CLEAN
from utils.data_clean import CLEAN1

import io
import os
import pickle
import pandas as pd




app = Flask(__name__)



with open("log_model_with_para.pkl", "rb") as file:
    model = pickle.load(file)


def single_preprocess(input_data):
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])
    clean = CLEAN()
    processed_data = clean.clean_data(input_data)
    return (processed_data)

# Preprocess batch data
def preprocess_batch_data(data):
    clean = CLEAN1()
    processed_data = clean.clean_data(data)
    return processed_data

def make_predict(data,model):
    predict=model.predict(data)
    return predict

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/single_prediction', methods=['GET', 'POST'])
def single_prediction():
    result = None
    show_modal = False 
    if request.method == 'POST':
        # Extract form data
        Gender = request.form['gender']
        Married = request.form['married']
        Dependents = request.form['dependents']
        Education = request.form['education']
        Self_Employed = request.form['self_employed']
        ApplicantIncome = float(request.form['applicant_income'])
        CoapplicantIncome = float(request.form['coapplicant_income'])
        LoanAmount = float(request.form['loan_amount'])
        Loan_AmountTerm = int(request.form['loan_amount_term'])
        Credit_History = int(request.form['credit_history'])
        Property_Area = request.form['property_area']
        
        
        input_data = {
                "Gender": Gender,
                "Married": Married,
                "Dependents": Dependents,
                "Education": Education,
                "Self_Employed": Self_Employed,
                "ApplicantIncome": ApplicantIncome,
                "CoapplicantIncome": CoapplicantIncome,
                "LoanAmount": LoanAmount,
                "Loan_Amount_Term": Loan_AmountTerm,
                "Credit_History": Credit_History,
                "Property_Area": Property_Area,
            }
        
        # Preprocess the input data

        preprocess=single_preprocess(input_data)
        # Get prediction from model
        result=make_predict(preprocess,model)
        result = "Approved" if result[0] == 1 else "Not Approved"
        show_modal = True


        # Get prediction from model
        
    return render_template('single_prediction.html',result=result,show_modal=show_modal)



    # Route for the batch prediction page
@app.route('/batch_prediction', methods=['GET', 'POST'])
def batch_prediction():
    result = None
    preview = None  # Preview of uploaded file
    processed_preview = None  # Preview of processed data
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                # Read the uploaded file
                data = pd.read_csv(file)
                
                # Generate a preview of the uploaded file (first 5 rows)
                preview = data.head().to_html(classes='table table-striped')
                
                # Retain Loan_ID if it exists
                loan_ids = data['Loan_ID'] if 'Loan_ID' in data.columns else None
                
                # Preprocess the data (drop Loan_ID internally)
                processed_data = preprocess_batch_data(data)
                
                # Generate a preview of the processed data (first 5 rows)
                processed_preview = processed_data.head().to_html(classes='table table-striped')
                
                # Predict results
                predictions = make_predict(processed_data, model)
                
                # Prepare the results DataFrame
                result = pd.DataFrame({
                    "Loan_ID": loan_ids if loan_ids is not None else range(1, len(predictions) + 1),
                    "Prediction": ["Approved" if pred == 1 else "Not Approved" for pred in predictions]
                })
                
                # Render all previews and results in the template
                return render_template(
                    'batch_prediction.html',
                    tables=[result.to_html(classes='table table-striped')],
                    titles=result.columns.values,
                    preview=preview,
                    processed_preview=processed_preview
                )
            except Exception as e:
                result = f"Error: {str(e)}"
    return render_template('batch_prediction.html', result=result, preview=preview, processed_preview=processed_preview)





if __name__=='__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
