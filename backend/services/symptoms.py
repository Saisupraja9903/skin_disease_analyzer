
# # Define symptom equivalences
# equivalent_symptoms = {
#     #Systemic Symptoms
#     "fever": ["fever"],
#     "fatigue/tiredness": ["tiredness", "fatigue"],
#     "pain": ["pain", "burning pain", "nerve pain", "painful swelling"],
    
#     #Inside-skin Symptoms
#     "burning/itching": ["itching", "burning"],
    
#     #On-skin Symptoms
#     "sores": ["sores"],
#     "crusting": ["crusting"],
#     "swelling/inflammation": ["swelling", "painful swelling", "inflammation"],
#     "blisters": ["blisters", "fluid-filled blisters"],
#     "warm skin": ["warm skin"],
    
#     #Over-skin Symptoms
#     "redness": ["redness", "red ring-shaped patch"],
#     "thread/ring like pattern": ["red ring-shaped patch", "red lines on skin"],
#     "skin texture changes": ["peeling skin", "scaly skin", "cracks"],
#     "nail changes": ["thickened nails", "nail discoloration", "brittle nails"],
#     "bad odor": ["bad odor"]
# }

# def normalize_symptom(symptom):
#     for key, values in equivalent_symptoms.items():
#         if symptom in values:
#             return key
#     return symptom

# # Disease symptom mapping
# SYMPTOM_MAPPING = {

# "Cellulitis": ["redness", "swelling", "warm skin", "pain", "fever"],

# "Impetigo": ["sores", "itching", "blisters", "crusting"],

# "Ringworm": ["red ring-shaped patch", "itching", "scaly skin", "inflammation"],

# "Cutaneous_larva_migrans": ["itching", "red lines on skin", "painful swelling"],

# "Chickenpox": ["fever", "tiredness", "itching", "fluid-filled blisters"],

# "Shingles": ["burning pain", "itching", "blisters", "nerve pain"],

# "Athlete-foot": ["itching", "cracks", "burning", "peeling skin", "blisters"],

# "Nail-fungus": ["thickened nails", "nail discoloration", "brittle nails", "bad odor"],

# "Psoriasis": ["red patches", "silvery scales", "dry skin", "itching"],

# "Eczema": ["dry skin", "itching", "red rash", "skin inflammation"],

# "Acne": ["pimples", "blackheads", "whiteheads", "oily skin"],

# "Rosacea": ["facial redness", "visible blood vessels", "skin irritation"],

# "Warts": ["rough bumps", "skin growth", "thickened skin"],

# "Melanoma": ["dark mole", "irregular borders", "color changes", "bleeding mole"],

# "Basal_cell_carcinoma": ["pearly bump", "skin lesion", "bleeding sore"],

# "Contact_dermatitis": ["rash", "itching", "burning skin", "swelling"],

# "Heat_rash": ["tiny red bumps", "itching", "prickly sensation"],

# "Scabies": ["intense itching", "burrow lines", "skin rash"],

# "Vitiligo": ["white patches", "loss of skin color"],

# "Seborrheic_dermatitis": ["flaky skin", "scalp dandruff", "red skin"]
# }

# # Normalize disease symptoms
# SYMPTOM_MAPPING = {
#     disease: list(set(normalize_symptom(symptom) for symptom in symptoms))
#     for disease, symptoms in SYMPTOM_MAPPING.items()
# }

# # Store pending symptom checks
# pending_symptom_check = {}  

# def confirm_disease_with_symptoms(top_3_predictions):

#     print("TOP 3 PREDICTIONS RECEIVED:", top_3_predictions)
#     """
#     Sends symptom questions to the frontend for user input.
#     """
#     disease_keys = [pred[0] for pred in top_3_predictions]
    
#     for disease, symptoms in SYMPTOM_MAPPING.items():
#         print(disease," : ",symptoms)

#     # Collect unique symptoms from the top diseases
#     unique_symptoms = set()
#     for disease in disease_keys:
#         if disease in SYMPTOM_MAPPING:
#             unique_symptoms.update(SYMPTOM_MAPPING[disease])

#     # Convert unique symptoms into a dictionary with questions
#     questions = {symptom: f"Do you have {symptom}?" for symptom in unique_symptoms}

#     pending_symptom_check["diseases"] = disease_keys  # Store for later confirmation
#     return questions

# def process_user_responses(answers):
#     """
#     Processes user responses and confirms the most probable disease.
#     """
#     if "diseases" not in pending_symptom_check:
#         return "Unknown", "Out of Class"

#     symptom_scores = {disease: 0 for disease in pending_symptom_check["diseases"]}
    
#     print(answers)

#     for disease in pending_symptom_check["diseases"]:
#         if disease in SYMPTOM_MAPPING:
#             for symptom in SYMPTOM_MAPPING[disease]:
#                 if symptom in answers and answers[symptom] == "1":
#                     symptom_scores[disease] += 1  # Increase score if symptom matches
    
#     confirmed_disease = max(symptom_scores, key=symptom_scores.get)
#     confirmed_disease_tot_symptoms = len(SYMPTOM_MAPPING.get(confirmed_disease, []))
#     severity_percentage = symptom_scores[confirmed_disease]/confirmed_disease_tot_symptoms
    
#     if severity_percentage < 0.25:
#         severity = "Out of Class"
#     elif severity_percentage <= 0.50:
#         severity = "Mild"
#     elif severity_percentage < 0.75:
#         severity = "Moderate"
#     else:
#         severity = "Severe"
    
#     print("Disease Scores: ", symptom_scores)
#     print("Confirmed Disease Scores: ", symptom_scores[confirmed_disease])
#     print("Confirmed Disease Total Symptoms: ",confirmed_disease_tot_symptoms)
#     print("Confirmed Disease Severity Percentage: ", severity_percentage)
#     print("Confirmed Disease Severity: ", severity)
#     return confirmed_disease, severity

# ==============================
# Symptom Normalization
# ==============================

# Define symptom equivalences
equivalent_symptoms = {

    # Systemic Symptoms
    "fever": ["fever"],
    "fatigue/tiredness": ["tiredness", "fatigue"],
    "pain": ["pain", "burning pain", "nerve pain", "painful swelling"],

    # Inside-skin Symptoms
    "burning/itching": ["itching", "burning"],

    # On-skin Symptoms
    "sores": ["sores"],
    "crusting": ["crusting"],
    "swelling/inflammation": ["swelling", "painful swelling", "inflammation"],
    "blisters": ["blisters", "fluid-filled blisters"],
    "warm skin": ["warm skin"],

    # Over-skin Symptoms
    "redness": ["redness", "red ring-shaped patch"],
    "thread/ring like pattern": ["red ring-shaped patch", "red lines on skin"],
    "skin texture changes": ["peeling skin", "scaly skin", "cracks"],
    "nail changes": ["thickened nails", "nail discoloration", "brittle nails"],
    "bad odor": ["bad odor"]
}


def normalize_symptom(symptom):
    for key, values in equivalent_symptoms.items():
        if symptom in values:
            return key
    return symptom


# ==============================
# Disease Symptom Mapping
# ==============================

# NOTE FOR DEVELOPERS:
# The current ML model is trained to recognize only a limited set of diseases.
# Based on evidence in the codebase (e.g., services/out_of_class.py), this is likely
# the first 8 diseases listed below. The other diseases are included for future
# expansion when the model is updated.
#
# For now, only the top 8 diseases will be actively used for symptom checking
# as the model will not predict the others.
SYMPTOM_MAPPING = {
    # --- Diseases supported by the current ML model ---
    "Cellulitis": ["redness", "swelling", "warm skin", "pain", "fever"],
    "Impetigo": ["sores", "itching", "blisters", "crusting"],
    "Ringworm": ["red ring-shaped patch", "itching", "scaly skin", "inflammation"],
    "Cutaneous_larva_migrans": ["itching", "red lines on skin", "painful swelling"],
    "Chickenpox": ["fever", "tiredness", "itching", "fluid-filled blisters"],
    "Shingles": ["burning pain", "itching", "blisters", "nerve pain"],
    "Athlete-foot": ["itching", "cracks", "burning", "peeling skin", "blisters"],
    "Nail-fungus": ["thickened nails", "nail discoloration", "brittle nails", "bad odor"],

    # --- Diseases for future model versions ---
    # "Psoriasis": ["red patches", "silvery scales", "dry skin", "itching"],
    # "Eczema": ["dry skin", "itching", "red rash", "skin inflammation"],
    # "Acne": ["pimples", "blackheads", "whiteheads", "oily skin"],
    # "Rosacea": ["facial redness", "visible blood vessels", "skin irritation"],
    # "Warts": ["rough bumps", "skin growth", "thickened skin"],
    # "Melanoma": ["dark mole", "irregular borders", "color changes", "bleeding mole"],
    # "Basal_cell_carcinoma": ["pearly bump", "skin lesion", "bleeding sore"],
    # "Contact_dermatitis": ["rash", "itching", "burning skin", "swelling"],
    # "Heat_rash": ["tiny red bumps", "itching", "prickly sensation"],
    # "Scabies": ["intense itching", "burrow lines", "skin rash"],
    # "Vitiligo": ["white patches", "loss of skin color"],
    # "Seborrheic_dermatitis": ["flaky skin", "scalp dandruff", "red skin"]
}


# ==============================
# Normalize Disease Symptoms
# ==============================

SYMPTOM_MAPPING = {
    disease: list(set(normalize_symptom(symptom) for symptom in symptoms))
    for disease, symptoms in SYMPTOM_MAPPING.items()
}


# ==============================
# Store Pending Symptom Checks
# ==============================

pending_symptom_check = {}


# ==============================
# Ask Symptom Questions
# ==============================

def confirm_disease_with_symptoms(top_predictions):

    print("PREDICTIONS RECEIVED:", top_predictions)

    # Use more predictions instead of only 3
    disease_keys = [pred[0] for pred in top_predictions]

    unique_symptoms = set()

    for disease in disease_keys:
        if disease in SYMPTOM_MAPPING:
            unique_symptoms.update(SYMPTOM_MAPPING[disease])

    questions = {
        symptom: f"Do you have {symptom}?"
        for symptom in unique_symptoms
    }

    pending_symptom_check["diseases"] = disease_keys

    return questions


# ==============================
# Process User Answers
# ==============================

def process_user_responses(answers):

    if "diseases" not in pending_symptom_check:
        return "Unknown", "Out of Class"

    diseases = pending_symptom_check["diseases"]

    symptom_scores = {disease: 0 for disease in diseases}

    print("User Answers:", answers)

    for disease in diseases:
        if disease in SYMPTOM_MAPPING:
            for symptom in SYMPTOM_MAPPING[disease]:
                if symptom in answers and answers[symptom] == "1":
                    symptom_scores[disease] += 1

    print("Disease Scores:", symptom_scores)

    # Always choose the highest scoring disease
    confirmed_disease = max(symptom_scores, key=symptom_scores.get)

    total_symptoms = len(SYMPTOM_MAPPING.get(confirmed_disease, []))

    if total_symptoms == 0:
        return confirmed_disease, "Out of Class"

    severity_percentage = symptom_scores[confirmed_disease] / total_symptoms

    if severity_percentage < 0.25:
        severity = "Mild"
    elif severity_percentage <= 0.50:
        severity = "Moderate"
    elif severity_percentage < 0.75:
        severity = "Severe"
    else:
        severity = "Critical"

    print("Confirmed Disease:", confirmed_disease)
    print("Severity:", severity)

    return confirmed_disease, severity