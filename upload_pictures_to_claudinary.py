import cloudinary
import cloudinary.uploader
import cloudinary.api
import tkinter as tk
from tkinter import filedialog
import json
import uuid
import os

# -----------------------------
# CONFIGURE CLOUDINARY
# -----------------------------
cloudinary.config(
    cloud_name="dag0mcbzj",
    api_key="574563425293112",       # add your key
    api_secret="2Cfc9bZwoMfIY1DYuerDu-yfwvY",    # add your secret
    secure=True
)

JSON_FILE = r"C:\Users\USER\OneDrive\CVTS\My Property Website\myProperties.json"

# -----------------------------
# FILE PICKER
# -----------------------------
def select_images():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.update()

    file_paths = filedialog.askopenfilenames(
        parent=root,
        title="Select images",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.webp *.gif"),
            ("All files", "*.*")
        ]
    )

    root.destroy()
    return list(file_paths)

# -----------------------------
# JSON HANDLING
# -----------------------------
def generate_unique_id():
    return uuid.uuid4().int >> 64

def add_property_to_json(property_data):
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                properties = json.load(f)
            except json.JSONDecodeError:
                properties = []
    else:
        properties = []

    properties.append(property_data)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(properties, f, indent=4)

# -----------------------------
# MAIN SCRIPT
# -----------------------------
def main():
    folder_name = input("Enter the Cloudinary folder name: ").strip()
    if not folder_name:
        print("Folder name cannot be empty.")
        return

    image_paths = select_images()
    if not image_paths:
        print("No images selected.")
        return

    uploaded_urls = []
    for image_path in image_paths:
        try:
            result = cloudinary.uploader.upload(
                image_path,
                folder=folder_name
            )
            uploaded_urls.append(result["secure_url"])
        except Exception as e:
            print(f"Failed to upload {image_path}: {e}")

    print("\nUploaded image links:\n")
    print(", ".join(uploaded_urls))

    # Collect property details
    property_data = {
        "ID": generate_unique_id(),
        "Property Type": input("Enter Property Type: "),
        "Price": int(input("Enter Price: ")),
        "Town": input("Enter Town: "),
        "Suburb": input("Enter Suburb: "),
        "Bedrooms": int(input("Enter Bedrooms: ")),
        "Bathrooms": int(input("Enter Bathrooms: ")),
        "Garages": int(input("Enter Garages: ")),
        "Carports": int(input("Enter Carports: ")),
        "Pool": input("Pool (true/false): ").lower() == "true",
        "Description": str(input("Enter Description: ")),
        "Pictures": ", ".join(uploaded_urls),
        "Floor size": int(input("Enter Floor size: ")),
        "Stand size": int(input("Enter Stand size: ")),
        "RNO": input("Enter RNO (or leave blank): ") or None
    }

    add_property_to_json(property_data)
    print("Property added successfully!")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()