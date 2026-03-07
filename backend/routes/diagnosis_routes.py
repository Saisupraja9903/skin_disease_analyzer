
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict
import requests

from services.symptoms import confirm_disease_with_symptoms, process_user_responses
from apis.city_coordinates_api import get_city_coordinates
from apis.nearby_hospitals_api import get_nearby_hospitals


router = APIRouter()

import os

# the ML prediction service can run on a different port; set ML_API_URL in
# the environment (for example "http://127.0.0.1:7860/") or the default
# value below will be used.
ML_API_URL = os.getenv("ML_API_URL", "http://127.0.0.1:7860/")

# ===============================
# IMAGE UPLOAD → ML PREDICTION
# ===============================
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if file.filename == "":
        raise HTTPException(status_code=400, detail="No selected file")

    try:
        response = requests.post(
            ML_API_URL,
            files={
                "file": (
                    file.filename,
                    await file.read(),
                    file.content_type
                )
            },
            timeout=30
        )
        response.raise_for_status()
    except Exception as e:
        print("❌ ML API ERROR:", str(e))
        raise HTTPException(status_code=500, detail="ML processing failed")

    try:
        data = response.json()
        print("🔍 ML RAW RESPONSE:", data)
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid ML response")

    if "predictions" not in data or not data["predictions"]:
        raise HTTPException(status_code=500, detail="ML returned no predictions")

    # Take top 8 predictions
    top_predictions = data["predictions"][:8]

    print("✅ Predictions:", top_predictions)

    questions = confirm_disease_with_symptoms(top_predictions)

    # return the predictions as well so the client can display or log them
    return JSONResponse(content={
        "predictions": top_predictions,
        "questions": questions,
    })


# ===============================
# SYMPTOM CONFIRMATION
# ===============================
class SymptomResponse(BaseModel):
    answers: Dict[str, str]


@router.post("/confirm_symptoms")
async def confirm_symptoms(data: SymptomResponse):

    confirmed_disease, severity = process_user_responses(data.answers)

    print("✅ Confirmed Disease:", confirmed_disease)
    print("⚠️ Severity:", severity)

    return {
        "disease": confirmed_disease,
        "severity": severity
    }


# ===============================
# FINAL DISEASE INFORMATION
# ===============================
class DiseaseInfoRequest(BaseModel):
    disease: str
    severity: str
    location: str


@router.post("/get_disease_info")
async def get_disease_info(data: DiseaseInfoRequest):

    disease = data.disease
    severity = data.severity
    location = data.location

    print("📍 Location Received:", location)

    symptoms_care = f"""
### Disease: {disease}

**Severity Level:** {severity}

**Recommended Care Instructions:**
- Keep the affected area clean and dry  
- Avoid scratching or irritation  
- Use prescribed topical medication  
- Maintain good hygiene  
- Consult a dermatologist if symptoms worsen  
"""

    try:
        coords = get_city_coordinates(location)
        nearby_hospitals = get_nearby_hospitals(coords)
    except Exception:
        nearby_hospitals = []

    hospitals = []
    for i, h in enumerate(nearby_hospitals):
        tags = h.get("tags", {})
        hospital_name = tags.get("name", f"Hospital {i+1}")

        # Construct a more specific location from address tags if available
        address_parts = [
            tags.get("addr:housenumber"),
            tags.get("addr:street"),
            tags.get("addr:city"),
            tags.get("addr:postcode")
        ]
        specific_location = ", ".join(part for part in address_parts if part)
        
        hospitals.append({
            "name": hospital_name,
            # Use specific address if found, otherwise fallback to the user's input location
            "location": specific_location if specific_location else location,
            "lat": h.get('lat'),
            "lon": h.get('lon')
        })

    return {
        "disease": disease,
        "severity": severity,
        "symptoms_care": symptoms_care,
        "hospitals": hospitals
    }
