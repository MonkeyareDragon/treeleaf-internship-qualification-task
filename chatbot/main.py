from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel, Field
import numpy as np

app = FastAPI()


MODEL_PATH = '../models/bank_loan_model.pkl'
model = joblib.load(MODEL_PATH)

# Define the input data model
class LoanApplication(BaseModel):
    Age: int
    Gender: int
    Experience: int
    Income: float
    Family: int
    CCAvg: float
    Education: int
    Mortgage: float
    HomeOwnership: int
    SecuritiesAccount: int
    CDAccount: int
    Online: float
    CreditCard: int

@app.post("/predict")
def predict_loan(application: LoanApplication):
    # Prepare the input data for prediction
    input_data = np.array([
        application.Age,
        application.Gender,
        application.Experience,
        application.Income,
        application.Family,
        application.CCAvg,
        application.Education,
        application.Mortgage,
        application.HomeOwnership,
        application.SecuritiesAccount,
        application.CDAccount,
        application.Online,
        application.CreditCard
    ]).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_data)
    
    # Return the prediction result
    return {"loan_approved": bool(prediction[0])}

# Run the server if this file is executed directly
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
