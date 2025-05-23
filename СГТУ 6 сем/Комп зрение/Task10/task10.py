import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os
import matplotlib.pyplot as plt
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", message="iCCP: known incorrect sRGB profile")

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Define the same model architecture as during training
class AnimalClassifier(nn.Module):
    def __init__(self, num_classes=10):
        super(AnimalClassifier, self).__init__()
        self.base_model = models.mobilenet_v2(pretrained=True)

        # Freeze base model parameters
        for param in self.base_model.parameters():
            param.requires_grad = False

        # Modify the classifier (must match training architecture)
        self.base_model.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(self.base_model.last_channel, 64),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.base_model(x)


# Load the trained model
def load_model(model_path, num_classes=10):
    model = AnimalClassifier(num_classes=num_classes).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model


# Define class names (replace with your actual class names)
class_names = ['cane', 'cavallo', 'elefante', 'farfalla', 'gallina',
               'gatto', 'mucca', 'pecora', 'ragno', 'scoiattolo']

# Image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


# Function to predict image class
def predict_image(image_path, model, transform, class_names):
    try:
        image = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None, None

    image_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        probability = torch.nn.functional.softmax(outputs, dim=1)[0] * 100

    return class_names[predicted.item()], probability[predicted.item()].item()


# Main function to process test images
def process_test_images(test_folder, model, transform, class_names, num_images=10):
    # Get list of image files in test folder
    image_files = [f for f in os.listdir(test_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Process each image
    for i, img_file in enumerate(image_files[:num_images]):
        img_path = os.path.join(test_folder, img_file)
        predicted_class, confidence = predict_image(img_path, model, transform, class_names)
        translate = {"cane": "dog", "cavallo": "horse", "elefante": "elephant", "farfalla": "butterfly", "ragno": "spider",
                     "gallina": "chicken", "gatto": "cat", "mucca": "cow", "pecora": "sheep", "scoiattolo": "squirrel",
                     "dog": "cane", "cavallo": "horse", "elephant": "elefante", "butterfly": "farfalla",
                     "chicken": "gallina", "cat": "gatto", "cow": "mucca",  "squirrel": "scoiattolo"}

        if predicted_class is not None:
            # Display the image with prediction
            plt.figure(figsize=(5, 5))
            image = Image.open(img_path)
            plt.imshow(image)
            plt.title(f"Predicted: {translate[predicted_class]}\nConfidence: {confidence:.2f}%")
            plt.axis('off')
            plt.show()


if __name__ == "__main__":
    # Paths configuration
    model_path = "best_model_weights.pth"  # Path to saved model weights
    test_folder = "test"  # Folder containing test images

    # Load the trained model
    model = load_model(model_path, num_classes=len(class_names))
    print("Model loaded successfully")

    # Process and display test images
    print(f"Processing images from {test_folder} folder...")
    process_test_images(test_folder, model, transform, class_names)