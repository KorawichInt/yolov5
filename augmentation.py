import os
from PIL import Image
from torchvision.transforms import v2
from torchvision import tv_tensors
import torch

# Define the paths
input_folder = 'dataset/train/images'
output_images_folder = 'dataset/train/images_augment'
output_labels_folder = 'dataset/train/labels_augment'

# Create the output folder if it does not exist
os.makedirs(output_images_folder, exist_ok=True)
os.makedirs(output_labels_folder, exist_ok=True)

def my_xywh2xyxy(yolo_label, size):
    # bbox = torch.tensor([center_x, center_y, width, height])
    # bbox = torch.tensor(yolo_label)
    CX, CY, W, H = yolo_label
    x_min = CX - (W / 2)
    y_min = CY - (H / 2)
    x_max = CX + (W / 2)
    y_max = CY + (H / 2)

    bbox_xyxy = [x_min*size, y_min*size, x_max*size, y_max*size]
    return bbox_xyxy

# Loop through each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        # Open the image file
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path)

        boxes_data = []

        with open(output_labels_folder+'/'+filename.replace('.jpg', 'txt'), 'r') as f:
            for line in f:
                components = line.split()[1:]  # Skip the first element
                box_data = [float(x) for x in components]
                size = image.size(1)
                box_xyxy = my_xywh2xyxy(box_data, size)  # Convert to XYXY format
                # dd_data.append(box_data)
                boxes_data.append(box_xyxy)
        
        # Create BoundingBoxes object
        boxes = tv_tensors.BoundingBoxes(
            torch.tensor(boxes_data),
            format='XYXY',
            # canvas_size=(img.shape[-2], img.shape[-1])
            canvas_size=image.shape[-2:]
        )

        ### Augmentation
        croped_img, croped_boxex = v2.RandomCrop(size=(224, 224))(image, boxes)
        blured_img, blured_boxex = v2.GaussianBlur(kernel_size=9, sigma=(0.8, 1.2))(image, boxes)
        brightnessed_img, brightnessed_boxex = v2.ColorJitter(brightness=(1.1,1.5))(image, boxes)
        darknessed_img, darknessed_boxex = v2.ColorJitter(brightness=(0.6,0.9))(image, boxes)

        # Save the resized image to the output folder
        augmented_images_path = os.path.join(output_images_folder, filename)
        augmented_labels_path = os.path.join(output_images_folder, filename)
        # croped.save(augmented_image_path)
        croped_img.save(augmented_images_path)
        blured_img.save(augmented_images_path)
        brightnessed_img.save(augmented_images_path)
        darknessed_img.save(augmented_images_path)

        croped_boxex.save(augmented_labels_path)
        blured_boxex.save(augmented_labels_path)
        brightnessed_boxex.save(augmented_labels_path)
        darknessed_boxex.save(augmented_labels_path)