import os
from PIL import Image
from torchvision.transforms import v2
from torchvision import tv_tensors
import torch

# Define the paths
# input_images_folder = 'dataset/train/images'
# input_labels_folder = 'dataset/train/labels'
# output_images_folder = 'dataset/train/images_augment'
# output_labels_folder = 'dataset/train/labels_augment'

input_images_folder = 'dataset/test/images'
input_labels_folder = 'dataset/test/labels'
output_images_folder = 'dataset/test_Y2/images'
output_labels_folder = 'dataset/test_Y2/labels'

# Create the output folder if it does not exist
os.makedirs(output_images_folder, exist_ok=True)
os.makedirs(output_labels_folder, exist_ok=True)

def my_xywh2xyxy(yolo_label, size):
    CX, CY, W, H = yolo_label
    x_min = CX - (W / 2)
    y_min = CY - (H / 2)
    x_max = CX + (W / 2)
    y_max = CY + (H / 2)

    # Convert to absolute coordinates
    x_min *= size[0]
    y_min *= size[1]
    x_max *= size[0]
    y_max *= size[1]
    return [x_min, y_min, x_max, y_max]

# Define transformations
transformations = {
    'croped': v2.RandomCrop(size=(224, 224)),
    'blured': v2.GaussianBlur(kernel_size=9, sigma=(0.8, 1.2)),
    'brightnessed': v2.ColorJitter(brightness=(1.1, 1.5)),
    'darknessed': v2.ColorJitter(brightness=(0.6, 0.9)),
}

# Loop through each file in the input folder
for filename in os.listdir(input_images_folder):
    if filename.endswith('.jpg'):
        # Open the image file
        image_path = os.path.join(input_images_folder, filename)
        image = Image.open(image_path).convert("RGB")

        # Load bounding boxes
        boxes_data = []
        label_file = os.path.join(input_labels_folder, filename.replace('.jpg', '.txt'))
        with open(label_file, 'r') as f:
            for line in f:
                components = line.split()[1:]  # Skip the first element
                box_data = [float(x) for x in components]
                box_xyxy = my_xywh2xyxy(box_data, image.size)  # Convert to XYXY format
                boxes_data.append(box_xyxy)

        # Create BoundingBoxes object
        boxes = tv_tensors.BoundingBoxes(
            torch.tensor(boxes_data),
            format='XYXY',
            canvas_size=image.size[::-1]  # (height, width) for canvas_size
        )

        # Apply transformations and save results
        for key, transform in transformations.items():
            # Apply transformation
            augmented_img, augmented_boxes = transform(image, boxes)

            # Save the transformed image
            augmented_image_path = os.path.join(output_images_folder, f"{filename.replace('.jpg', f'_{key}.jpg')}")
            augmented_img.save(augmented_image_path)

            # Save the transformed bounding boxes
            augmented_label_path = os.path.join(output_labels_folder, f"{filename.replace('.jpg', f'_{key}.txt')}")
            with open(augmented_label_path, 'w') as f:
                for bbox in augmented_boxes:
                    # Convert back to YOLO format for saving
                    width, height = augmented_img.size
                    bcx = (bbox[0] + bbox[2]) / 2 / width
                    bcy = (bbox[1] + bbox[3]) / 2 / height
                    bw = (bbox[2] - bbox[0]) / width
                    bh = (bbox[3] - bbox[1]) / height
                    f.write(f"0 {bcx} {bcy} {bw} {bh}\n")  # Assuming single class (class 0)

print("Augmentation completed.")
