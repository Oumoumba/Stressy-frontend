# Stressy
# Stressy Setup (Quick Version)

## Backend (FastAPI)
1. Open terminal/cmd
2. Go inside backend folder:
   cd backend
3. Run:
   uvicorn main:app --reload --port 8000

Backend will be at:  
http://127.0.0.1:8000  
Docs at:  
http://127.0.0.1:8000/docs

**Keep this terminal open.**

---

## Frontend (Streamlit)
1. Open a NEW terminal/cmd
2. Go inside frontend folder:
   cd frontend
3. Run:
   streamlit run app.py

App opens at:  
http://localhost:8501

---

## Group Notes
- Backend does predictions.  
- Frontend shows the dashboard.  
- They connect through:  
  http://127.0.0.1:8000/predict

Anyone can edit UI in `frontend/app.py` or model logic in `backend/main.py`.

Done.
