# Project Title

Welcome to the **Treeleaf-Intern-Task** repository! This project contains various components including a chatbot application, trained models, data processing scripts, and analysis reports of Bank Loan Classification. Below you'll find the folder structure and instructions on how to set up and run the project.

## Folder Structure

```
.
├── chatbot             <- Contains the chatbot app
├── models              <- Trained and serialized models, model predictions, or model summaries
│   ├── data
│   │   ├── processed   <- The final, canonical data sets for modeling.
│   │   └── raw         <- The original, immutable data dump.
├── notebooks           <- Jupyter notebooks. Naming convention is a number (for ordering),
│                          the creator's initials, and a short `-` delimited description, e.g.`1.0-jqp-initial-data-exploration`.
├── reports             <- Generated analysis as HTML, PDF, LaTeX, etc.
├── image_task          <- Consist of task 2 for image rectangle
└── README.md           <- The top-level README for developers using this project.
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Pip

### Install the required packages

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

## Running the Chatbot App

### Backend

1. Navigate to the `chatbot` directory:

    ```bash
    cd chatbot/
    ```

2. Run the following command to start the FastAPI backend:

    ```bash
    uvicorn main:app --reload
    ```

### Frontend

1. With the backend running, open a new terminal window.
2. Navigate to the `chatbot` directory if not already there:

    ```bash
    cd chatbot/
    ```

3. Run the following command to start the Streamlit frontend:

    ```bash
    streamlit run bot.py
    ```

## Additional Information

This README provides an overview of the project's structure and setup instructions. For more detailed information, refer to the comments within the respective files. 

Enjoy working with the **Treeleaf-Intern-Task** repository!