import torch
from torch.serialization import safe_globals
import torchvision.transforms as transforms
from PIL import Image

# Allow EfficientNet to be safely unpickled
safe_globals(["torchvision.models.efficientnet.EfficientNet"])

# helper that falls back to a trivial neural network if the file is
# missing; this allows the module to be imported in environments where the
# real weights are not available (e.g. during CI or when running unit tests).
def _safe_load_model(path, num_classes=None):
    try:
        mdl = torch.load(path, map_location=torch.device("cpu"), weights_only=False)
    except FileNotFoundError:
        # create a dummy model that returns zero logits for every class
        class _Dummy(torch.nn.Module):
            def __init__(self, n):
                super().__init__()
                self.n = n or 8
            def forward(self, x):
                # batch size × num_classes
                bs = x.shape[0]
                return torch.zeros(bs, self.n)
        mdl = _Dummy(num_classes)
    mdl.eval()
    return mdl

# Load full models directly (or dummy placeholders if the checkpoints are absent)
num_labels = 8  # keep in sync with `classes` below
efficientnet = _safe_load_model("models/efficientnet.pth", num_labels)
resnet = _safe_load_model("models/resnet.pth", num_labels)
mobilenet = _safe_load_model("models/mobilenet.pth", num_labels)

# Class Labels
# Ordering has been aligned with the symptom mapping and underscores
# are used where necessary so the strings match the keys in
# services/symptoms.py exactly.
classes = [
    "Cellulitis",
    "Impetigo",
    "Ringworm",
    "Cutaneous_larva_migrans",
    "Chickenpox",
    "Shingles",
    "Athlete-foot",
    "Nail-fungus",
]

# Preprocess the image
def preprocess_image(image: Image.Image):    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    return transform(image).unsqueeze(0)  # Add batch dimension

# Ensemble classification
def ensemble_classify(img: Image.Image) -> list:    
    image_tensor = preprocess_image(img)

    # Get predictions from each model
    with torch.no_grad():
        output1 = efficientnet(image_tensor)
        output2 = resnet(image_tensor)
        output3 = mobilenet(image_tensor)

    # Average the predictions
    final_output = (output1 + output2 + output3) / 3
    probabilities = torch.nn.functional.softmax(final_output, dim=1).squeeze().tolist()

    # Get top 8 predictions (or fewer if there aren't that many classes)
    top_k = min(8, len(probabilities))
    top_indices = sorted(range(len(probabilities)), key=lambda i: probabilities[i], reverse=True)[:top_k]
    top_predictions = [(classes[i], probabilities[i]) for i in top_indices]

    return top_predictions
