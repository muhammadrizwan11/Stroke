
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
import joblib

# Load the saved Naive Bayes model
loaded_model = joblib.load('Naive_bayes.pkl')

# Function to preprocess input data
def preprocess_input(data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    return scaled_data

# Function to make prediction
def predict_stroke(input_data):
    scaled_input = preprocess_input(input_data)
    prediction = loaded_model.predict(scaled_input)
    return prediction

# Streamlit UI
def main():
    # Title of the web app
    st.title('Stroke Risk Prediction')

    # Define login function
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "Gravis" and password == "stroke18":
                st.session_state["authenticated"] = True
            else:
                st.error("Invalid username or password.")
    else:
        # Input fields
        st.write('Enter Patient Information:')
        gender = st.radio('Gender:', ['Male', 'Female'])
        age = st.slider('Age:', min_value=0, max_value=100, value=50, step=1)
        bmi = st.number_input('BMI:', value=25.0, step=0.1)
        hypertension = st.selectbox('Hypertension:', ['No', 'Yes'])
        heart_disease = st.selectbox('Heart Disease:', ['No', 'Yes'])
        avg_glucose_level = st.number_input('Average Glucose Level:', value=100.0, step=0.1)
        ever_married = st.selectbox('Ever Married:', ['No', 'Yes'])
        work_type = st.selectbox('Work Type:', ['Private', 'Self-employed', 'Govt_job', 'Never_worked'])
        residence_type = st.selectbox('Residence Type:', ['Urban', 'Rural'])
        smoking_status = st.selectbox('Smoking Status:', ['never smoked', 'formerly smoked', 'smokes'])

        # Convert categorical input to numerical
        gender_val = 1 if gender == 'Male' else 0
        hypertension_val = 1 if hypertension == 'Yes' else 0
        heart_disease_val = 1 if heart_disease == 'Yes' else 0
        ever_married_val = 1 if ever_married == 'Yes' else 0

        work_type_mapping = {'Private': 0, 'Self-employed': 1, 'Govt_job': 2, 'Never_worked': 4}
        work_type_val = work_type_mapping[work_type]

        residence_type_val = 1 if residence_type == 'Urban' else 0

        smoking_status_mapping = {'never smoked': 0, 'formerly smoked': 1, 'smokes': 2}
        smoking_status_val = smoking_status_mapping[smoking_status]

        # Predict button
        if st.button('Predict Stroke'):
            input_data = {
                'Gender': [gender_val],
                'Age': [age],
                'BMI': [bmi],
                'Hypertension': [hypertension_val],
                'HeartDisease': [heart_disease_val],
                'AverageGlucoseLevel': [avg_glucose_level],
                'EverMarried': [ever_married_val],
                'WorkType': [work_type_val],
                'ResidenceType': [residence_type_val],
                'SmokingStatus': [smoking_status_val]
            }
            input_df = pd.DataFrame(input_data)
            prediction = predict_stroke(input_df)
            if prediction[0] == 1:
                st.error("You have high risk of stroke. Please seek advice from Heathcare professional.")
            else:
                st.success("Congratulations you have low risk of stroke.")

            # Disclaimer
            st.write("""
            ## Disclaimer:

            **Introduction:**
            The information provided by this application is intended for general informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified healthcare provider with any questions you may have regarding a medical condition.

            **Accuracy of Information:**
            The predictions and assessments provided by this application are based on statistical models and data inputs. While we strive to provide accurate and reliable predictions, they should not be considered as definitive medical diagnoses. Individual health conditions may vary, and the results generated by the application should be interpreted with caution.

            **Limitation of Liability:**
            The creators of this application do not assume any responsibility or liability for any loss or damage resulting from the use of this application or reliance on the information provided herein. Users are solely responsible for their use of the application and should consult healthcare professionals for personalized medical advice and treatment.

            **GDPR Compliance:**
            We adhere to the General Data Protection Regulation (GDPR) regulations to ensure the protection of user data and privacy. Our commitment to GDPR compliance underscores our dedication to maintaining the highest standards of data security and privacy protection.

            **Acknowledgement:**
            By using this application, you acknowledge and agree to the terms of this disclaimer.
            """)
            
# Run the main function when the script is executed
if __name__ == '__main__':
    main()
