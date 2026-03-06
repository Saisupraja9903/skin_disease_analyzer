

import os
import torch
import torchvision.models as models
from torch.utils.data import DataLoader
from torchvision import transforms, datasets




# directory structure expected by the script: dataset/train_set/<class-name>/*.jpg
# You can change DATA_DIR to point at your own folder if necessary.
DATA_DIR = os.getenv("SKIN_DATA_DIR", "dataset/train_set")

if not os.path.isdir(DATA_DIR):
    raise FileNotFoundError(
        f"Training data directory '{DATA_DIR}' does not exist. "
        "Create it with one subdirectory per class (Cellulitis, Impetigo, etc.)."
    )

# Data augmentation transforms
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomRotation(20),
    transforms.RandomHorizontalFlip(),
    transforms.RandomZoom((0.9, 1.1)),
    transforms.ColorJitter(brightness=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

train_dataset = datasets.ImageFolder(root=DATA_DIR, transform=train_transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Model Training Function
def train_model(model, save_path, is_regression=False):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    # Choose loss function based on classification or regression
    criterion = torch.nn.CrossEntropyLoss() if not is_regression else torch.nn.MSELoss()

    for epoch in range(10):
        model.train()
        total_loss = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}")

    torch.save(model.state_dict(), save_path)  # Save state_dict instead of the full model

# Train EfficientNet
efficientnet = models.efficientnet_b0(pretrained=True)
efficientnet.classifier[1] = torch.nn.Linear(efficientnet.classifier[1].in_features, 8)
train_model(efficientnet, "models/efficientnet.pth")

# Train ResNet
resnet = models.resnet18(pretrained=True)
resnet.fc = torch.nn.Linear(resnet.fc.in_features, 8)
train_model(resnet, "models/resnet.pth")

# Train MobileNet
mobilenet = models.mobilenet_v3_small(pretrained=True)
mobilenet.classifier[3] = torch.nn.Linear(mobilenet.classifier[3].in_features, 8)
train_model(mobilenet, "models/mobilenet.pth")

# Severity Model (Regression)
severity_model = models.efficientnet_b0(pretrained=True)
severity_model.classifier[1] = torch.nn.Linear(severity_model.classifier[1].in_features, 1)  # Regression output
train_model(severity_model, "models/severity_model.pth", is_regression=True)

