import os
import shutil

# Define source and destination paths
source_root = r"C:5"
destination = r"C:\UM"

# Ensure destination folder exists
os.makedirs(destination, exist_ok=True)

# Traverse the directory structure
for root, dirs, files in os.walk(source_root):
    for file in files:
        if file.lower().endswith(".ppm"):  # Check if file is a PPM copy
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination, file)

            # Copy the file to the destination
            shutil.copy2(source_file, destination_file)
            print(f"Copied: {source_file} -> {destination_file}")

print("All PPM copies have been successfully copied.")
