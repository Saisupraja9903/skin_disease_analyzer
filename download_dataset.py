


import os
import shutil


print(f"Dataset downloaded to: {path}")

# List contents
print("\nContents of downloaded dataset:")
for item in os.listdir(path):
    print(f"  - {item}")

# Create dataset directory in project root
dataset_dir = "dataset"
train_dir = os.path.join(dataset_dir, "train_set")

if os.path.exists(train_dir):
    print(f"\nDataset already exists at {train_dir}")
else:
    os.makedirs(train_dir, exist_ok=True)
    
    # Check if the downloaded path contains train directly
    source_train = os.path.join(path, "train")
    if os.path.exists(source_train):
        print(f"\nCopying from {source_train} to {train_dir}...")
        shutil.copytree(source_train, train_dir, dirs_exist_ok=True)
    else:
        # Maybe the structure is different
        print(f"\nLooking for image folders in {path}...")
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print(f"  Found folder: {item}")

print("\nDataset download complete!")
print(f"Dataset location: {os.path.abspath(dataset_dir)}")

