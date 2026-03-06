# import requests

# def get_nearby_hospitals(coords):
#     """Finds hospitals near given (lat, lon) using OpenStreetMap Overpass API."""

#     if not coords or coords == (None, None):
#         return []

#     lat, lon = coords

#     overpass_url = "https://overpass-api.de/api/interpreter"
#     query = f"""
#     [out:json];
#     node["amenity"="hospital"](around:10000,{lat},{lon});
#     out body;
#     """

#     headers = {"User-Agent": "Mozilla/5.0"}

#     try:
#         response = requests.post(overpass_url, data=query, headers=headers, timeout=10)
#         response.raise_for_status()

#         hospitals = response.json().get("elements", [])[:5]  # Take up to 5 hospitals
#         return hospitals

#     except requests.exceptions.RequestException:
#         return []

import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def get_nearby_hospitals(coords, specialty=None):

    lat = coords["lat"]
    lon = coords["lon"]

    # Dermatology search
    if specialty == "dermatology":
        query = f"""
        [out:json][timeout:25];
        (
          node["healthcare:speciality"="dermatology"](around:10000,{lat},{lon});
          node["healthcare"="dermatologist"](around:10000,{lat},{lon});
          node["amenity"="clinic"](around:10000,{lat},{lon});
        );
        out body;
        """

    # General hospitals fallback
    else:
        query = f"""
        [out:json][timeout:25];
        (
          node["amenity"="hospital"](around:15000,{lat},{lon});
          node["amenity"="clinic"](around:15000,{lat},{lon});
          way["amenity"="hospital"](around:15000,{lat},{lon});
          way["amenity"="clinic"](around:15000,{lat},{lon});
        );
        out center;
        """

    response = requests.post(OVERPASS_URL, data=query)

    data = response.json()

    elements = data.get("elements", [])

    hospitals = []

    for h in elements:

        lat = h.get("lat") or h.get("center", {}).get("lat")
        lon = h.get("lon") or h.get("center", {}).get("lon")

        if not lat or not lon:
            continue

        name = h.get("tags", {}).get("name", "Unnamed Hospital")

        hospitals.append({
            "name": name,
            "lat": lat,
            "lon": lon
        })

    return hospitals[:5]   # return top 5 hospitals