# import os
# from PIL import Image

# # Define the paths
# input_folder = 'project_dataset'
# output_folder = 'project_dataset_resized'

# # Create the output folder if it does not exist
# os.makedirs(output_folder, exist_ok=True)

# # Loop through each file in the input folder
# for filename in os.listdir(input_folder):
#     if filename.endswith('.jpg') or filename.endswith('.png'):
#         # Open the image file
#         image_path = os.path.join(input_folder, filename)
#         image = Image.open(image_path)
        
#         # Resize the image
#         new_image = image.resize((224, 224))
        
#         # Save the resized image to the output folder
#         # new_image_path = os.path.join(output_folder, filename)
#         # new_image.save(new_image_path)
#         base_name = os.path.splitext(filename)
#         # เปิดภาพต้นฉบับ
#         with Image.open(filename) as img:
#             # แปลงและบันทึกเป็น JPG
#             img.convert('RGB').save(f"{base_name}.jpg", "JPEG")

# print("All images have been resized and saved.")

import os
from PIL import Image

# Define the paths
input_folder = 'project_dataset'
output_folder = 'project_dataset_resized'

# Create the output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Loop through each file in the input folder
for filename in os.listdir(input_folder):
# for filename in [input_folder+'/mama_5',
#                  input_folder+'/mama_7',
#                  input_folder+'/mama_8',
#                  input_folder+'/mama_9',
#                  input_folder+'/mama_10',]:
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Open the image file
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path)
        
        # Resize the image
        new_image = image.resize((224, 224))

        # Convert the image to RGB and save as .jpg
        base_name = os.path.splitext(filename)[0]  # Get the filename without extension
        new_image_path = os.path.join(output_folder, f"{base_name}.jpg")
        new_image.convert('RGB').save(new_image_path, "JPEG")

print("All images have been resized and saved as .jpg.")

