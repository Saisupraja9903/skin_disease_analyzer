# from fastapi import APIRouter, File, UploadFile, HTTPException, Form
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import Dict
# import requests
# from dotenv import load_dotenv
# import os

# from services.symptoms import confirm_disease_with_symptoms, process_user_responses
# from services.out_of_class import detect_unknown_disease

# router = APIRouter()

# # Load environment variables from .env file
# load_dotenv()

# # ML_API_URL = os.getenv("ML_API_URL")

# ML_API_URL = "http://127.0.0.1:8000/"


# # @router.post("/upload")
# # async def upload_file(file: UploadFile = File(...)):
# #     if not file:
# #         raise HTTPException(status_code=400, detail="No file uploaded")
# #     if file.filename == "":
# #         raise HTTPException(status_code=400, detail="No selected file")

# #     response = requests.post(ML_API_URL,files={"file": ("image.jpg", await file.read(), file.content_type)})

# #     if response.status_code != 200:
# #         return JSONResponse(status_code=500, content={"error": "ML API failed"})

# #     top_3_predictions = response.json().get("predictions")

# #     print("Top 3 Predictions:", top_3_predictions)

# #     if detect_unknown_disease(top_3_predictions):
# #         return JSONResponse(content={"message": "Unknown disease detected."})

# #     questions = confirm_disease_with_symptoms(top_3_predictions)
# #     return JSONResponse(content={"questions": questions})

# @router.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     if not file:
#         raise HTTPException(status_code=400, detail="No file uploaded")

#     if file.filename == "":
#         raise HTTPException(status_code=400, detail="No selected file")

#     try:
#         response = requests.post(
#             ML_API_URL,
#             files={
#                 "file": (
#                     file.filename,
#                     await file.read(),
#                     file.content_type
#                 )
#             },
#             timeout=30
#         )
#         response.raise_for_status()
#     except Exception as e:
#         print("❌ ML API ERROR:", str(e))
#         raise HTTPException(
#             status_code=500,
#             detail="ML processing failed"
#         )

#     try:
#         data = response.json()
#     except Exception:
#         raise HTTPException(
#             status_code=500,
#             detail="Invalid response from ML model"
#         )

#     if "predictions" not in data or not data["predictions"]:
#         raise HTTPException(
#             status_code=500,
#             detail="ML returned no predictions"
#         )

#     top_3_predictions = data["predictions"]
#     print("Top 3 Predictions:", top_3_predictions)

#     if detect_unknown_disease(top_3_predictions):
#         return JSONResponse(content={"message": "Unknown disease detected."})

#     questions = confirm_disease_with_symptoms(top_3_predictions)
#     return JSONResponse(content={"questions": questions})

# class SymptomResponse(BaseModel):
#     answers: Dict[str, str]  # symptom name -> '1' or '0' 

# @router.post("/confirm_symptoms")
# async def confirm_symptoms(data: SymptomResponse):
#     print("Received Data:", data)
    
#     confirmed_disease, severity = process_user_responses(data.answers)

#     print("Confirmed Disease:", confirmed_disease)
#     print("Estimated Severity:", severity)

#     return {
#         "disease": confirmed_disease,
#         "severity": severity,
#         "message": f"Disease: {confirmed_disease}, Severity: {severity}"
#     }


#------------------------------------------------------------------------------------------------------------------

# from fastapi import APIRouter, File, UploadFile, HTTPException, Form
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import Dict
# import requests

# from services.symptoms import confirm_disease_with_symptoms, process_user_responses
# from services.out_of_class import detect_unknown_disease

# router = APIRouter()

# # ✅ ML API root endpoint (your ML app uses POST "/")
# ML_API_URL = "http://127.0.0.1:8000/"


# @router.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     # -------------------------------
#     # 1. Validate file
#     # -------------------------------
#     if not file:
#         raise HTTPException(status_code=400, detail="No file uploaded")

#     if file.filename == "":
#         raise HTTPException(status_code=400, detail="No selected file")

#     # -------------------------------
#     # 2. Send image to ML API
#     # -------------------------------
#     try:
#         response = requests.post(
#             ML_API_URL,
#             files={
#                 "file": (
#                     file.filename,
#                     await file.read(),
#                     file.content_type
#                 )
#             },
#             timeout=30
#         )
#         response.raise_for_status()
#     except Exception as e:
#         print("❌ ML API ERROR:", str(e))
#         raise HTTPException(
#             status_code=500,
#             detail="ML processing failed"
#         )

#     # -------------------------------
#     # 3. Parse ML response
#     # -------------------------------
#     try:
#         data = response.json()
#         print("🔍 ML RAW RESPONSE:", data)
#     except Exception:
#         raise HTTPException(
#             status_code=500,
#             detail="Invalid response from ML model"
#         )

#     # -------------------------------
#     # 4. Validate predictions
#     # -------------------------------
#     if "predictions" not in data or not data["predictions"]:
#         raise HTTPException(
#             status_code=500,
#             detail="ML returned no predictions"
#         )

#     top_3_predictions = data["predictions"]
#     print("✅ Top 3 Predictions:", top_3_predictions)

#     # -------------------------------
#     # 5. Out-of-class detection
#     # -------------------------------
#     if detect_unknown_disease(top_3_predictions):
#         return JSONResponse(
#             content={"message": "Unknown disease detected."}
#         )

#     # -------------------------------
#     # 6. Generate symptom questions
#     # -------------------------------
#     questions = confirm_disease_with_symptoms(top_3_predictions)
#     return JSONResponse(content={"questions": questions})


# # ===============================
# # SYMPTOM CONFIRMATION
# # ===============================
# class SymptomResponse(BaseModel):
#     answers: Dict[str, str]  # symptom -> '1' or '0'


# @router.post("/confirm_symptoms")
# async def confirm_symptoms(data: SymptomResponse):
#     print("📝 Received Answers:", data.answers)

#     confirmed_disease, severity = process_user_responses(data.answers)

#     print("✅ Confirmed Disease:", confirmed_disease)
#     print("⚠️ Severity:", severity)

#     return {
#         "disease": confirmed_disease,
#         "severity": severity,
#         "message": f"Disease: {confirmed_disease}, Severity: {severity}"
#     }
# @router.post("/get_disease_info")
# async def get_disease_info(
#     disease: str = Form(...),
#     severity: str = Form(...),
#     location: str = Form(...)
# ):
#     """
#     Returns symptoms, care instructions and nearby hospitals
#     based on disease and user location
#     """

#     # -------------------------------
#     # Symptoms & care instructions
#     # -------------------------------
#     symptoms_care = f"""
# ### Disease: {disease}

# **Severity Level:** {severity}

# **Recommended Care Instructions:**
# - Keep the affected area clean and dry
# - Avoid scratching or irritation
# - Use prescribed topical medication
# - Maintain good hygiene
# - Consult a dermatologist if symptoms worsen
# """

#     # -------------------------------
#     # Nearby hospitals (location-based)
#     # -------------------------------
#     hospitals = [
#         {
#             "name": "Apollo Hospital",
#             "location": location,
#             "maps_url": f"https://www.google.com/maps/search/{location}+hospital"
#         },
#         {
#             "name": "Fortis Healthcare",
#             "location": location,
#             "maps_url": f"https://www.google.com/maps/search/{location}+clinic"
#         }
#     ]

#     return {
#         "disease": disease,
#         "severity": severity,
#         "symptoms_care": symptoms_care,
#         "hospitals": hospitals
#     }

#------------------------------------------------------------------------------------------------------------------------------------
# from fastapi import APIRouter, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import Dict
# import requests

# from services.symptoms import confirm_disease_with_symptoms, process_user_responses
# from services.out_of_class import detect_unknown_disease

# router = APIRouter()

# # ✅ ML API root endpoint (your ML app uses POST "/")
# ML_API_URL = "http://127.0.0.1:8000/"


# # ===============================
# # IMAGE UPLOAD → ML PREDICTION
# # ===============================
# @router.post("/upload")
# async def upload_file(file: UploadFile = File(...)):

#     if not file:
#         raise HTTPException(status_code=400, detail="No file uploaded")

#     if file.filename == "":
#         raise HTTPException(status_code=400, detail="No selected file")

#     # --- Send image to ML API ---
#     try:
#         response = requests.post(
#             ML_API_URL,
#             files={
#                 "file": (
#                     file.filename,
#                     await file.read(),
#                     file.content_type
#                 )
#             },
#             timeout=30
#         )
#         response.raise_for_status()
#     except Exception as e:
#         print("❌ ML API ERROR:", str(e))
#         raise HTTPException(
#             status_code=500,
#             detail="ML processing failed"
#         )

#     # --- Parse ML Response ---
#     try:
#         data = response.json()
#         print("🔍 ML RAW RESPONSE:", data)
#     except Exception:
#         raise HTTPException(
#             status_code=500,
#             detail="Invalid response from ML model"
#         )

#     # --- Validate Predictions ---
#     if "predictions" not in data or not data["predictions"]:
#         raise HTTPException(
#             status_code=500,
#             detail="ML returned no predictions"
#         )

#     top_3_predictions = data["predictions"]
#     print("✅ Top 3 Predictions:", top_3_predictions)

#     # --- Out of class detection ---
#     if detect_unknown_disease(top_3_predictions):
#         return JSONResponse(content={"message": "Unknown disease detected."})

#     # --- Generate symptom questions ---
#     questions = confirm_disease_with_symptoms(top_3_predictions)
#     return JSONResponse(content={"questions": questions})


# # ===============================
# # SYMPTOM CONFIRMATION
# # ===============================
# class SymptomResponse(BaseModel):
#     answers: Dict[str, str]   # symptom -> '1' or '0'


# @router.post("/confirm_symptoms")
# async def confirm_symptoms(data: SymptomResponse):
#     print("📝 Received Answers:", data.answers)

#     confirmed_disease, severity = process_user_responses(data.answers)

#     print("✅ Confirmed Disease:", confirmed_disease)
#     print("⚠️ Severity:", severity)

#     return {
#         "disease": confirmed_disease,
#         "severity": severity,
#         "message": f"Disease: {confirmed_disease}, Severity: {severity}"
#     }


# # ===============================
# # FINAL DISEASE INFORMATION
# # ===============================
# class DiseaseInfoRequest(BaseModel):
#     disease: str
#     severity: str
#     location: str


# @router.post("/get_disease_info")
# async def get_disease_info(data: DiseaseInfoRequest):

#     disease = data.disease
#     severity = data.severity
#     location = data.location

#     print("📍 Location Received:", location)

#     # --- Symptoms & Care Instructions ---
#     symptoms_care = f"""
# ### Disease: {disease}

# **Severity Level:** {severity}

# **Recommended Care Instructions:**
# - Keep the affected area clean and dry  
# - Avoid scratching or irritation  
# - Use prescribed topical medication  
# - Maintain good hygiene  
# - Consult a dermatologist if symptoms worsen  
# """

#     # --- Nearby Hospitals (Location Based Dummy Data) ---
#     hospitals = [
#         {
#             "name": "Apollo Hospital",
#             "location": location,
#             "maps_url": f"https://www.google.com/maps/search/{location}+hospital"
#         },
#         {
#             "name": "Fortis Healthcare",
#             "location": location,
#             "maps_url": f"https://www.google.com/maps/search/{location}+clinic"
#         }
#     ]

#     return {
#         "disease": disease,
#         "severity": severity,
#         "symptoms_care": symptoms_care,
#         "hospitals": hospitals
#     }


#__________________________________________________________________________________________________________________

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict
import requests

from services.symptoms import confirm_disease_with_symptoms, process_user_responses
from services.out_of_class import detect_unknown_disease

router = APIRouter()

ML_API_URL = "http://127.0.0.1:8000/"


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

    top_3_predictions = data["predictions"]
    print("✅ Predictions:", top_3_predictions)

    if detect_unknown_disease(top_3_predictions):
        return JSONResponse(content={"message": "Unknown disease detected."})

    questions = confirm_disease_with_symptoms(top_3_predictions)
    return JSONResponse(content={"questions": questions})


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

    hospitals = [
        {
            "name": "Apollo Hospital",
            "location": location,
            "maps_url": f"https://www.google.com/maps/search/{location}+hospital"
        },
        {
            "name": "Fortis Healthcare",
            "location": location,
            "maps_url": f"https://www.google.com/maps/search/{location}+clinic"
        }
    ]

    return {
        "disease": disease,
        "severity": severity,
        "symptoms_care": symptoms_care,
        "hospitals": hospitals
    }
