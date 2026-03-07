# import logging
# from logging.handlers import RotatingFileHandler
# from fastapi import APIRouter, HTTPException, Request
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel, ValidationError
# from typing import Any

# from apis.city_coordinates_api import get_city_coordinates
# from apis.nearby_hospitals_api import get_nearby_hospitals
# from apis.gemini_api import gemini

# # Centralized logging setup
# handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=5)
# handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
# logger = logging.getLogger("info_logger")
# logger.setLevel(logging.INFO)
# logger.addHandler(handler)

# router = APIRouter()

# # Pydantic model
# class DiseaseRequest(BaseModel):
#     disease: str
#     severity: str
#     location: str

# @router.post("/get_disease_info")
# async def get_disease_info(request: Request):
#     try:
#         body: dict[str, Any] = await request.json()
#         try:
#             data = DiseaseRequest(**body)
#         except ValidationError as e:
#             logger.warning(f"Validation error: {e.errors()}")
#             return JSONResponse(
#                 status_code=400,
#                 content={"error": "Invalid request", "details": e.errors()}
#             )

#         if data.severity == "Out of Class":
#             logger.info(f"Out of Class severity: {data.disease}")
#             return {"out_of_class": True}

#         logger.info(f"Processing: {data.disease} in {data.location}")

#         query = (
#             f"Provide detailed information about the skin disease name present in the title {data.disease} ignoring the title itself. Include:\n"
#             "- External and internal symptoms (in bullet points)\n"
#             "- Steps to take care of it\n"
#         )

#         print(data.location)

#         try:
#             ai_response = gemini(query).text
#         except Exception as e:
#             logger.exception(f"Gemini API failed: {str(e)}")
#             raise HTTPException(status_code=500, detail="Failed to fetch disease info")

#         try:
#             print(data.location)
#             coords = get_city_coordinates(data.location)
#             print(coords)
#             hospitals = get_nearby_hospitals(coords)
#             print(hospitals)
#         except Exception:
#             logger.exception("Nearby hospital fetch failed.")
#             hospitals = []

#         hospital_infos = [
#             {
#                 "name": h.get("tags", {}).get("name", f"Hospital {i+1}"),
#                 "location": data.location,
#                 "maps_url": f"https://www.google.com/maps/search/?q={h['lat']},{h['lon']}"
#             }
#             for i, h in enumerate(hospitals)
#         ]
#         print(hospital_infos)

#         return {
#             "disease": data.disease,
#             "severity": data.severity,
#             "location": data.location,
#             "symptoms_care": ai_response,
#             "hospitals": hospital_infos,
#         }

#     except Exception:
#         logger.exception("Unhandled exception.")
#         raise HTTPException(status_code=500, detail="Internal server error")

import logging
from logging.handlers import RotatingFileHandler
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Any

from apis.city_coordinates_api import get_city_coordinates
from apis.nearby_hospitals_api import get_nearby_hospitals
from apis.gemini_api import gemini


# ==============================
# Logging Setup
# ==============================

handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

logger = logging.getLogger("info_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

router = APIRouter()


# ==============================
# Request Model
# ==============================

class DiseaseRequest(BaseModel):
    disease: str
    severity: str
    location: str


# ==============================
# API: Get Disease Info
# ==============================

@router.post("/get_disease_info")
async def get_disease_info(request: Request):

    try:
        body: dict[str, Any] = await request.json()

        try:
            data = DiseaseRequest(**body)

        except ValidationError as e:

            logger.warning(f"Validation error: {e.errors()}")

            return JSONResponse(
                status_code=400,
                content={
                    "error": "Invalid request",
                    "details": e.errors()
                }
            )

        # Handle out of class case
        if data.severity == "Out of Class":
            logger.info(f"Out of Class severity: {data.disease}")
            return {"out_of_class": True}

        logger.info(f"Processing disease: {data.disease} in {data.location}")


        # ==============================
        # Gemini AI Disease Info
        # ==============================

        query = (
            f"Provide detailed information about the skin disease named {data.disease}. "
            f"Include:\n"
            f"- External and internal symptoms (bullet points)\n"
            f"- Care instructions\n"
            f"- Other potential diseases with similar symptoms (Differential Diagnosis)\n"
        )

        try:
            ai_response = gemini(query).text

        except Exception as e:

            logger.exception(f"Gemini API failed: {str(e)}")

            raise HTTPException(
                status_code=500,
                detail="Failed to fetch disease info"
            )


        # ==============================
        # Get Nearby Hospitals
        # ==============================

        fallback_message = None
        hospitals = []

        try:

            coords = get_city_coordinates(data.location)
            print("City coordinates:", coords)

            # Step 1: Try dermatology clinics
            hospitals = get_nearby_hospitals(coords, specialty="dermatology")

            if not hospitals:

                fallback_message = (
                    "No dermatologists found in your area. "
                    "Showing nearby hospitals instead."
                )

                # Step 2: Try general hospitals
                hospitals = get_nearby_hospitals(coords)
                print("Hospitals found:", hospitals)

            if not hospitals:

                fallback_message = (
                    "No hospitals found in your location. "
                    "Showing hospitals from nearest city."
                )

                # Step 3: fallback city
                coords = get_city_coordinates("Hyderabad")

                hospitals = get_nearby_hospitals(coords)

        except Exception:

            logger.exception("Nearby hospital fetch failed.")

            hospitals = []
            fallback_message = "Unable to fetch nearby hospitals."


        # ==============================
        # Format Hospital Data
        # ==============================

        hospital_infos = []

        hospital_infos = []

        for i, h in enumerate(hospitals):

            hospital_infos.append({
                "name": h["name"],
                "location": data.location,
                "lat": h["lat"],
                "lon": h["lon"]
            })

        # If still no hospitals → create fallback hospital using Google search
        if len(hospital_infos) == 0:

            hospital_infos.append({
                "name": "Search Hospitals in " + data.location,
                "location": data.location,
                "lat": coords["lat"],
                "lon": coords["lon"]
            })


        # ==============================
        # API Response
        # ==============================

        return {
            "disease": data.disease,
            "severity": data.severity,
            "location": data.location,
            "symptoms_care": ai_response,
            "fallback_message": fallback_message,
            "hospitals": hospital_infos
        }


    except Exception:

        logger.exception("Unhandled exception.")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )