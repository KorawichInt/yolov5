import csv
import os
from tensorboardX import SummaryWriter
from PIL import Image
import numpy as np

# Set the path to your results.csv and the directory for TensorBoard logs
results_csv_path = 'runs/train/exp/results.csv' 
log_dir = 'runs/train/exp/tensorboard'
image_path = 'runs/train/exp/PR_curve.png'

# Initialize the TensorBoard writer
writer = SummaryWriter(log_dir=log_dir)

with open(results_csv_path, mode='r') as file:
    csv_reader = csv.DictReader(file)

    # print(csv_reader.fieldnames)
    # next(csv_reader, None)

    for epoch, row in enumerate(csv_reader):
        
        # Extract the individual losses (train)
        box_loss_train = float(row['      train/box_loss'])
        obj_loss_train = float(row['      train/obj_loss'])
        cls_loss_train = float(row['      train/cls_loss'])

        # Calculate the total loss
        total_loss_train = box_loss_train + obj_loss_train + cls_loss_train
        mean_loss_train = total_loss_train / 3

        # Extract the individual losses (validation)
        box_loss_val = float(row['        val/box_loss'])
        obj_loss_val = float(row['        val/obj_loss'])
        cls_loss_val = float(row['        val/cls_loss'])

        # Calculate the total loss 
        total_loss_val = box_loss_val + obj_loss_val + cls_loss_val
        mean_loss_val = total_loss_val / 3

        lr = float(row['               x/lr0'])
        precision = float(row['   metrics/precision'])
        recall = float(row['      metrics/recall'])

        # Log the desired metrics
        writer.add_scalar('Train/Mean_Loss', mean_loss_train , epoch)
        writer.add_scalar('Train/Objectness_Loss', obj_loss_train , epoch)
        writer.add_scalar('Train/Classification_Loss', cls_loss_train , epoch)
        writer.add_scalar('Train/Box_Loss', box_loss_train , epoch)
        writer.add_scalar('Train/Scheduled_Learning_Rate', lr , epoch)

        writer.add_scalar('Validate/Mean_Loss', mean_loss_val , epoch)
        writer.add_scalar('Validate/Objectness_Loss', obj_loss_val , epoch)
        writer.add_scalar('Validate/Classification_Loss', cls_loss_val , epoch)
        writer.add_scalar('Validate/Box_Loss', box_loss_val , epoch)

        writer.add_scalar('Precision-Recall/Precision', precision , epoch)
        writer.add_scalar('Precision-Recall/Recall', recall , epoch)

        # Load the image and add it to TensorBoard
        if epoch == 0:  # Only log the image once at the first epoch
            image = Image.open(image_path)
            image_np = np.array(image)
            writer.add_image('Precision-Recall/Y1', image_np, epoch, dataformats='HWC')

# Close the TensorBoard writer
writer.close()
