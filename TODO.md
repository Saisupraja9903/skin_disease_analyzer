# Skin Disease Diagnosis System - TODO

## ✅ Completed Tasks

### 1. Configuration Fixes
- [x] Fixed ML_API_URL in backend/routes/diagnosis_routes.py (changed from port 8000 to 7860)

### 2. Documentation
- [x] Updated README.md with complete running instructions
- [x] Documented API endpoints
- [x] Documented project structure

### 3. Verification
- [x] Verified test images exist (18 test images in SkinNet-Analyzer-Test-Images/)
- [x] Verified model files exist (efficientnet.pth, resnet.pth, mobilenet.pth, severity_model.pth)
- [x] Tested ML classification - runs successfully

## ⚠️ Note on Model Weights

The ML model test showed uniform predictions (equal probability for all classes). This indicates:
- The model files exist with proper sizes (16-45MB each)
- The classification layer was initialized but not trained on the skin disease dataset
- **To get accurate predictions, the model needs to be trained on the dataset**

## Training the Model

To train the model with accurate weights:

1. Download the dataset from Kaggle:
   https://www.kaggle.com/datasets/subirbiswas19/skin-disease-dataset

2. Organize the dataset as:
   ```
   dataset/
   ├── Cellulitis/
   ├── Impetigo/
   ├── Ringworm/
   ├── Cutaneous_larva_migrans/
   ├── Chickenpox/
   ├── Shingles/
   ├── Athlete-foot/
   └── Nail-fungus/
   ```

3. Run training:
   ```bash
   cd ml
   python train.py
   ```

4. The trained weights will be saved to ml/models/

## Running the System

### Terminal 1 - ML API (Port 7860):
```bash
cd ml
python app.py
```

### Terminal 2 - Backend API (Port 8080):
```bash
cd backend
python main.py
```

### Terminal 3 - Frontend (Port 3000):
```bash
cd frontend
npm start
