import csv
import os
from tensorboardX import SummaryWriter

# Set the path to your results.csv and the directory for TensorBoard logs
results_csv_path = 'runs/train/exp8/results.csv' 
log_dir = 'runs/train/exp8/tensor_data'

# Initialize the TensorBoard writer
writer = SummaryWriter(log_dir=log_dir)

with open(results_csv_path, mode='r') as file:
    csv_reader = csv.DictReader(file)

    # print(csv_reader.fieldnames)
    # next(csv_reader, None)

    for epoch, row in enumerate(csv_reader):
        
        # Extract the individual losses
        box_loss = float(row['      train/box_loss'])
        obj_loss = float(row['      train/obj_loss'])
        cls_loss = float(row['      train/cls_loss'])

        # Calculate the total loss
        total_loss = box_loss + obj_loss + cls_loss
        mean_loss = total_loss / 3

        # Log the desired metrics
        writer.add_scalar('Result/Mean of Loss', mean_loss, epoch)
        writer.add_scalar('Result/Objectness Loss', obj_loss, epoch)
        writer.add_scalar('Result/Classification Loss', cls_loss, epoch)
        writer.add_scalar('Result/Box Regression Loss', box_loss, epoch)

        writer.add_scalars('Result/Scheduled Learning Rate', {
            'lr0': float(row['               x/lr0']),
            'lr1': float(row['               x/lr1']),
            'lr2': float(row['               x/lr2'])
        }, epoch)

        # writer.add_scalar('Learning Rate/lr0', float(row['               x/lr0']), epoch)
        # writer.add_scalar('Learning Rate/lr1', float(row['               x/lr1']), epoch)
        # writer.add_scalar('Learning Rate/lr2', float(row['               x/lr2']), epoch)

# Close the TensorBoard writer
writer.close()