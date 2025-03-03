import os
import shutil

# Define source and destination paths
source_root = r"C:"
destination = r"C:PM"

# Ensure destination folder exists
os.makedirs(destination, exist_ok=True)

# Traverse the directory structure
for root, dirs, files in os.walk(source_root):
    # Check if the current directory is inside an employee folder (i.e., has files)
    if any(file.lower().endswith(".pdf") for file in files):  
        for file in files:
            if file.lower().endswith(".pdf"):  # Process only PDF files
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination, file)

                # Copy the file to the destination
                shutil.copy2(source_file, destination_file)
                print(f"Copied: {source_file} -> {destination_file}")

print("All PPM copies (PDFs) have been successfully copied.")
