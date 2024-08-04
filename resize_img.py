# from PIL import Image
# import os

# image = Image.open('dataset/images_no_resize/00001.jpg')
# new_image = image.resize((640, 640))
# new_image.save('dataset/images/00001.jpg')

import os
from PIL import Image

# Define the paths
input_folder = 'dataset/images_no_resize'
output_folder = 'dataset/images'

# Create the output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Loop through each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        # Open the image file
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path)
        
        # Resize the image
        new_image = image.resize((640, 640))
        
        # Save the resized image to the output folder
        new_image_path = os.path.join(output_folder, filename)
        new_image.save(new_image_path)

print("All images have been resized and saved.")
