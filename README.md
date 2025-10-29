Stress Forecast App (Frontend)

This is the Streamlit frontend for our Capstone Project — Neural Network Stress Forecasting & Detection App.
It provides a web dashboard that visualizes Electrodermal Activity (EDA) data and simulates short-term stress forecasts.

How to Run:
	1.	Clone the repo
git clone https://github.com/maphi12/Stressy.git
cd Stressy
	2.	Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
	3.	Install requirements
pip install -r requirements.txt
	4.	Run the app
streamlit run app.py

Then open the local URL shown (usually http://localhost:8501).

Files:
	•	app.py — main Streamlit dashboard
	•	src/predict.py — handles prediction logic (mock or model call)
	•	assets/styles.css — UI theme and layout
	•	requirements.txt — dependencies

Notes for Team:
	•	Use sample mode to test visuals.
	•	Upload CSVs with an EDA column for real data.
	•	Backend model API integration will be added later.
	•	Keep branches small and push changes often.
