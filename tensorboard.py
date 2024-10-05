import csv
from tensorboardX import SummaryWriter

# Paths to your CSV files and TensorBoard log directories
results_csv_path_y1 = 'runs/train/exp8/results.csv' 
results_csv_path_y2 = 'runs/train/exp8/results.csv' 
log_dir_y1 = 'tensorboard/Y1'
log_dir_y2 = 'tensorboard/Y2'

# Function to log results from a CSV file
def log_results(csv_reader, writer):
    for epoch, row in enumerate(csv_reader):
        
        # Extract and calculate losses for training
        box_loss_train = float(row['      train/box_loss'])
        obj_loss_train = float(row['      train/obj_loss'])
        cls_loss_train = float(row['      train/cls_loss'])
        total_loss_train = box_loss_train + obj_loss_train + cls_loss_train
        mean_loss_train = total_loss_train / 3

        # Extract and calculate losses for validation
        box_loss_val = float(row['        val/box_loss'])
        obj_loss_val = float(row['        val/obj_loss'])
        cls_loss_val = float(row['        val/cls_loss'])
        total_loss_val = box_loss_val + obj_loss_val + cls_loss_val
        mean_loss_val = total_loss_val / 3

        # Extract learning rate, precision, and recall
        lr = float(row['               x/lr0'])
        precision = float(row['   metrics/precision'])
        recall = float(row['      metrics/recall'])

        # Log the desired metrics to TensorBoard using the same scalar names
        writer.add_scalar('Train/Mean_Loss', mean_loss_train, epoch)
        writer.add_scalar('Train/Objectness_Loss', obj_loss_train, epoch)
        writer.add_scalar('Train/Classification_Loss', cls_loss_train, epoch)
        writer.add_scalar('Train/Box_Loss', box_loss_train, epoch)
        writer.add_scalar('Train/Scheduled_Learning_Rate', lr, epoch)

        writer.add_scalar('Validate/Mean_Loss', mean_loss_val, epoch)
        writer.add_scalar('Validate/Objectness_Loss', obj_loss_val, epoch)
        writer.add_scalar('Validate/Classification_Loss', cls_loss_val, epoch)
        writer.add_scalar('Validate/Box_Loss', box_loss_val, epoch)

        writer.add_scalar('Precision-Recall/Precision', precision, epoch)
        writer.add_scalar('Precision-Recall/Recall', recall, epoch)

# Log results from Y1
with open(results_csv_path_y1, mode='r') as file1:
    csv_reader1 = csv.DictReader(file1)
    writer_y1 = SummaryWriter(log_dir=log_dir_y1)
    log_results(csv_reader1, writer_y1)
    writer_y1.close()

# Log results from Y2
with open(results_csv_path_y2, mode='r') as file2:
    csv_reader2 = csv.DictReader(file2)
    writer_y2 = SummaryWriter(log_dir=log_dir_y2)
    log_results(csv_reader2, writer_y2)
    writer_y2.close()
