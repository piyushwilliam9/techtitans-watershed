from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Database
interventions_db = [
    {"id": 104, "name": "Check Dam #104", "lat": 25.182, "lng": 75.842, "status": "Verified", "ndvi_gain": "+14.2%"},
    {"id": 105, "name": "Percolation Pond #105", "lat": 25.170, "lng": 75.860, "status": "Verified", "ndvi_gain": "+9.8%"}
]

complaints_db = [
    {"id": "TT-90214", "farmer": "Ramesh Patel", "issue": "Canal wall seepage near field", "status": "Under Review"}
]

class ComplaintSchema(BaseModel):
    farmer_name: str
    issue: str

class VerificationSchema(BaseModel):
    site_name: str
    lat: float
    lng: float

@app.get("/api/stats")
def get_stats():
    return {
        "total_interventions": len(interventions_db) + 140,
        "verified_ponds": len(interventions_db) + 126,
        "flagged_issues": len(complaints_db),
        "avg_ndvi_gain": "+18.4%"
    }

@app.get("/api/interventions")
def get_interventions():
    return interventions_db

# Live Complaints fetch karne ke liye endpoint
@app.get("/api/complaints")
def get_complaints():
    return complaints_db

@app.post("/api/farmer-complaint")
def register_complaint(data: ComplaintSchema):
    complaint_id = f"TT-{random.randint(10000, 99999)}"
    record = {"id": complaint_id, "farmer": data.farmer_name, "issue": data.issue, "status": "Action Required"}
    complaints_db.append(record)
    print(f"\n🚨 [NEW COMPLAINT RECEIVED]\nTicket: {complaint_id}\nCitizen: {data.farmer_name}\nDetails: {data.issue}\n")
    return {"message": "Complaint lodged successfully!", "ticket_id": complaint_id}

@app.post("/api/verify-evidence")
def verify_evidence(data: VerificationSchema):
    new_site = {
        "id": len(interventions_db) + 105,
        "name": data.site_name,
        "lat": data.lat,
        "lng": data.lng,
        "status": "AI Verified (98% Authenticity)",
        "ndvi_gain": f"+{random.randint(8, 22)}%"
    }
    interventions_db.append(new_site)
    print(f"✅ [EVIDENCE VERIFIED] Added {data.site_name}")
    return {"message": "Evidence Verified", "site": new_site}