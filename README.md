# Skin Disease Diagnosis System

A full-stack AI-powered web application for skin disease diagnosis using deep learning (EfficientNet, ResNet, MobileNet ensemble) and FastAPI.

---

## Features

- **Image-based Diagnosis**: Upload skin images for disease prediction using deep learning ensemble
- **Symptom Confirmation**: Interactive symptom questions to improve accuracy
- **Disease Info**: AI-generated disease explanations and care instructions
- **Hospital Finder**: Locates nearby hospitals using OpenStreetMap
- **PDF Reports**: Downloadable diagnosis reports
- **Location-aware**: Enter your city for localized hospital recommendations

---

## Supported Diseases

The model classifies the following 8 skin diseases:

1. Cellulitis
2. Impetigo
3. Ringworm
4. Cutaneous Larva Migrans
5. Chickenpox
6. Shingles
7. Athlete Foot
8. Nail Fungus

---

## Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   React UI      │──────│  Backend API    │──────│   ML API        │
│   (Port 3000)   │      │  (Port 8080)    │      │  (Port 7860)    │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                │                         │
                                ▼                         ▼
                         ┌─────────────┐          ┌─────────────┐
                         │   Hospital  │          │   Ensemble  │
                         │     API     │          │    Models   │
                         │ (OSM/Nominatim)         │ (PyTorch)   │
                         └─────────────┘          └─────────────┘
```

---

## Prerequisites

- Python 3.8+
- Node.js & npm
- pip

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SkinNet-Analyzer-main
```

### 2. Backend Setup

Navigate to the backend directory and install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 3. ML Service Setup

Navigate to the ml directory and install ML dependencies:

```bash
cd ml
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

---

## Running the Application

You need to run **three services** in separate terminals:

### Terminal 1: ML API (Port 7860)

```bash
cd ml
python app.py
```

Or using uvicorn:
```bash
cd ml
uvicorn app:app --host 0.0.0.0 --port 7860
```

### Terminal 2: Backend API (Port 8080)

```bash
cd backend
python main.py
```

Or using uvicorn:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8080
```

### Terminal 3: Frontend (Port 3000)

```bash
cd frontend
npm start
```

---

## API Endpoints

### ML API (Port 7860)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/` | POST | Predict disease from image |

**Request:**
```bash
curl -X POST -F "file=@image.jpg" http://127.0.0.1:7860/
```

**Response:**
```json
{
  "predictions": [
    ["Ringworm", 0.78],
    ["Cellulitis", 0.12],
    ["Impetigo", 0.05],
    ["Shingles", 0.03],
    ["Athlete-foot", 0.02]
  ]
}
```

### Backend API (Port 8080)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Server status |
| `/api/upload` | POST | Upload image, get predictions & symptom questions |
| `/api/confirm_symptoms` | POST | Confirm disease based on symptoms |
| `/api/get_disease_info` | POST | Get disease info, care instructions, hospitals |

---

## Testing with Sample Images

Test images are available in `SkinNet-Analyzer-Test-Images/`:

- `ringworm.jpg` - Ringworm sample
- `cellulitis.jpg` - Cellulitis sample
- `impetigo.jpg` - Impetigo sample
- `shingles.jpg` - Shingles sample
- `Athlete-foot.jpeg` - Athlete Foot sample
- And more...

---

## Project Structure

```
SkinNet-Analyzer-main/
├── backend/                    # FastAPI Backend
│   ├── main.py                 # Main backend server
│   ├── routes/                 # API routes
│   │   ├── diagnosis_routes.py
│   │   ├── info_routes.py
│   │   └── status_routes.py
│   ├── services/               # Business logic
│   │   ├── symptoms.py
│   │   ├── out_of_class.py
│   │   └── severity.py
│   ├── apis/                   # External APIs
│   │   ├── city_coordinates_api.py
│   │   ├── nearby_hospitals_api.py
│   │   └── gemini_api.py
│   └── requirements.txt
│
├── ml/                         # ML Service
│   ├── app.py                  # FastAPI ML server
│   ├── classify.py            # Classification logic
│   ├── train.py                # Training script
│   ├── models/                 # Trained models
│   │   ├── efficientnet.pth
│   │   ├── resnet.pth
│   │   ├── mobilenet.pth
│   │   └── severity_model.pth
│   └── requirements.txt
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   └── components/
│   │       └── Upload.js       # Main upload component
│   └── package.json
│
├── SkinNet-Analyzer-Test-Images/  # Test images
├── tests/                      # Test files
└── README.md
```

---

## Model Details

- **Architecture**: Ensemble of EfficientNetB0, ResNet18, MobileNetV3
- **Input Size**: 224x224
- **Preprocessing**: ImageNet normalization
- **Training**: Transfer learning with pretrained weights

---

## Disease Symptom Mapping

| Disease | Symptoms |
|---------|----------|
| Cellulitis | redness, swelling, warm skin, pain, fever |
| Impetigo | sores, itching, blisters, crusting |
| Ringworm | red ring-shaped patch, itching, scaly skin, inflammation |
| Cutaneous Larva Migrans | itching, red lines on skin, painful swelling |
| Chickenpox | fever, tiredness, itching, fluid-filled blisters |
| Shingles | burning pain, itching, blisters, nerve pain |
| Athlete Foot | itching, cracks, burning, peeling skin, blisters |
| Nail Fungus | thickened nails, nail discoloration, brittle nails, bad odor |

---

## Hospital Finder

Uses OpenStreetMap APIs:
- **Nominatim**: Convert city name to coordinates
- **Overpass API**: Find nearby hospitals/clinics

---

## License

**Disclaimer**: This system is for demonstration and educational purposes only. Not intended for real medical diagnosis. Always consult a healthcare professional for medical advice.

---

## References

- [Skin Disease Dataset (Kaggle)](https://www.kaggle.com/datasets/subirbiswas19/skin-disease-dataset)
- [IJIRT Journal Paper](https://ijirt.org/Article?manuscript=174480)

