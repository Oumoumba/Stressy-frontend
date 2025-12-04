# README — Stress Forecasting System

Team: tm8 p1-stress forecasting
Course: COSC 490 / Capstone
Semester: Fall 2025


## 1. ABSTRACT

This project implements a Stress Forecasting System that predicts user stress levels based on User input data. The system is built using a FastAPI backend for machine-learning inference and a Streamlit frontend that provides a modern Fitbit-style interface. The application is lightweight, modular, and easy for peers to clone and run locally.

The goal of the project is to allow users to monitor predicted stress levels in real time while also giving developers a clean API and UI framework to extend with additional features.


## 2. SYSTEM REQUIREMENTS
•	Python 3.10 or higher  
•	FastAPI  
•	Uvicorn  
•	Streamlit  
•	NumPy  
•	Pandas  
•	Scikit-learn  
•	pip package manager  

## 3. PROJECT STRUCTURE
Stress-Forecasting/
│
├── backend/  
│   ├── main.py  
│   ├── model.pkl  
│   ├── requirements.txt  
│  
├── frontend/  
│   ├── app.py  
│   ├── assets/  
│   ├── src/  
│   ├── requirements.txt  
│  
└── README.md  


## 4. BACKEND SETUP (FASTAPI)
1.	Open terminal
2.	Navigate to backend folder:
cd backend

2.	Install required packages:
pip install -r requirements.txt

3.	Start the FastAPI server:
uvicorn main:app --reload


Backend runs at:
http://127.0.0.1:8000

Endpoints:
•	GET / → health check
•	POST /predict → returns stress prediction for input data

## 5. FRONTEND SETUP (STREAMLIT)
1.	Open a new terminal
Navigate to frontend folder:
cd frontend

2.	Install frontend packages:
pip install -r requirements.txt

3.	Run the UI:
streamlit run app.py


Frontend runs at:
http://localhost:8501

## 6. SYSTEM ARCHITECTURE

Streamlit (UI)
→ displays dashboard, graphs, user interface

FastAPI (Backend)
→ receives sensor input, loads ML model, returns prediction

Model
→ built with scikit-learn, trained on labeled stress datasets

Flow:
Streamlit → FastAPI → Model → JSON Response → Frontend Visualization


## 7. RUNNING INSTRUCTIONS
1.	Start backend first
2.	Make sure it is reachable at 127.0.0.1:8000
3.	Start frontend next
4.	The frontend automatically sends requests to FastAPI
5.	upload a csv file (found in the data folder)
6.	Stress prediction appears in the UI

## 8. Core Features
•	Predicts stress level at the moment
•	Predicts future stress level
•	Communicates data into graphing analysis

## 9. REFERENCES

[1] T. Tiangolo, “FastAPI Documentation,” https://fastapi.tiangolo.com.  
[2] Streamlit Inc., “Streamlit Documentation,” https://docs.streamlit.io.  
[3] Scikit-learn Developers, “Scikit-learn Machine Learning in Python,” https://scikit-learn.org.  
[4] Uvicorn Authors, “Uvicorn ASGI Server,” https://www.uvicorn.org.
