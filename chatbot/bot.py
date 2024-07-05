import streamlit as st
import requests
import time

api_url = "http://127.0.0.1:8000/predict"

# Function to interact with the FastAPI endpoint
def get_prediction(data):
    response = requests.post(api_url, json=data)
    return response.json()

# Set page configuration for the Streamlit app
st.set_page_config(page_title="Loan Chatbot", page_icon="💰", layout="wide")

# Define the questions for the bot to ask
questions = [
    "What is your age?",
    "What is your gender? (0 for female, 1 for male)",
    "How many years of experience do you have?",
    "What is your annual income in thousands?",
    "How many family members do you have?",
    "What is your average credit card spending per month?",
    "What is your education level? (1 for Undergrad, 2 for Graduate, 3 for Advanced/Professional)",
    "What is your mortgage value if any?",
    "What is your home ownership status? (0 for own, 1 for rent, 2 for neither)",
    "Do you have a securities account? (0 for no, 1 for yes)",
    "Do you have a CD account? (0 for no, 1 for yes)",
    "Do you use online banking? (0 for no, 1 for yes)",
    "Do you have a credit card issued by the bank? (0 for no, 1 for yes)"
]

# Initialize chat history and session variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'loan_details' not in st.session_state:
    st.session_state.loan_details = {}

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("You:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.loan_details[questions[st.session_state.current_question]] = user_input
    st.session_state.current_question += 1

    if st.session_state.current_question < len(questions):
        next_question = questions[st.session_state.current_question]
        st.session_state.messages.append({"role": "assistant", "content": next_question})
        with st.chat_message("assistant"):
            st.markdown(next_question)
    else:
        input_data = {
            "Age": int(st.session_state.loan_details[questions[0]]),
            "Gender": int(st.session_state.loan_details[questions[1]]),
            "Experience": int(st.session_state.loan_details[questions[2]]),
            "Income": float(st.session_state.loan_details[questions[3]]),
            "Family": int(st.session_state.loan_details[questions[4]]),
            "CCAvg": float(st.session_state.loan_details[questions[5]]),
            "Education": int(st.session_state.loan_details[questions[6]]),
            "Mortgage": float(st.session_state.loan_details[questions[7]]),
            "HomeOwnership": int(st.session_state.loan_details[questions[8]]),
            "SecuritiesAccount": int(st.session_state.loan_details[questions[9]]),
            "CDAccount": int(st.session_state.loan_details[questions[10]]),
            "Online": float(st.session_state.loan_details[questions[11]]),
            "CreditCard": int(st.session_state.loan_details[questions[12]])
        }
        
        # Get prediction from FastAPI endpoint
        prediction_response = get_prediction(input_data)
        loan_approved = prediction_response['loan_approved']
        
        bot_response = "Loan Approved" if loan_approved else "Loan Not Approved"
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

# Initialize the first question
if st.session_state.current_question == 0 and not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": questions[0]})
    st.experimental_rerun()
