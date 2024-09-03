# import csv
# import os
# from tensorboardX import SummaryWriter

# # Set the path to your results.csv and the directory for TensorBoard logs
# results_csv_path = 'runs/train/exp/results.csv' 
# log_dir = 'runs/train/exp/tensorboard'

# # Initialize the TensorBoard writer
# writer = SummaryWriter(log_dir=log_dir)

# with open(results_csv_path, mode='r') as file:
#     csv_reader = csv.DictReader(file)

#     # print(csv_reader.fieldnames)
#     # next(csv_reader, None)

#     for epoch, row in enumerate(csv_reader):
        
#         # Extract the individual losses (train)
#         box_loss_train = float(row['      train/box_loss'])
#         obj_loss_train = float(row['      train/obj_loss'])
#         cls_loss_train = float(row['      train/cls_loss'])

#         # Calculate the total loss
#         total_loss_train = box_loss_train + obj_loss_train + cls_loss_train
#         mean_loss_train = total_loss_train / 3

#         # Extract the individual losses (validation)
#         box_loss_val = float(row['        val/box_loss'])
#         obj_loss_val = float(row['        val/obj_loss'])
#         cls_loss_val = float(row['        val/cls_loss'])

#         # Calculate the total loss 
#         total_loss_val = box_loss_val + obj_loss_val + cls_loss_val
#         mean_loss_val = total_loss_val / 3

#         lr = float(row['               x/lr0'])
#         precision = float(row['   metrics/precision'])
#         recall = float(row['      metrics/recall'])

#         # Log the desired metrics
#         writer.add_scalar('Result/Mean of Loss', mean_loss_train , epoch)
#         writer.add_scalar('Result/Objectness Loss', obj_loss_train , epoch)
#         writer.add_scalar('Result/Classification Loss', cls_loss_train , epoch)
#         writer.add_scalar('Result/Box Regression Loss', box_loss_train , epoch)

#         writer.add_scalar('Result/Mean of Loss', mean_loss_val , epoch)
#         writer.add_scalar('Result/Objectness Loss', obj_loss_val , epoch)
#         writer.add_scalar('Result/Classification Loss', cls_loss_val , epoch)
#         writer.add_scalar('Result/Box Regression Loss', box_loss_val , epoch)
        
#         # writer.add_scalars('Result/Scheduled Learning Rate', {
#         #     'lr0': float(row['               x/lr0'])
#         # }, epoch)
#         writer.add_scalar('Result/Scheduled Learning Rate', lr , epoch)
#         writer.add_scalar('Pricision', precision , epoch)
#         writer.add_scalar('Recall', recall , epoch)

# # Close the TensorBoard writer
# writer.close()







# import csv
# import os
# from tensorboardX import SummaryWriter
# import matplotlib.pyplot as plt

# # Set the path to your results.csv and the directory for TensorBoard logs
# results_csv_path = 'runs/train/exp/results.csv' 
# log_dir = 'runs/train/exp/tensorboard'

# # Initialize the TensorBoard writer
# writer = SummaryWriter(log_dir=log_dir)

# with open(results_csv_path, mode='r') as file:
#     csv_reader = csv.DictReader(file)

#     recall_values = []
#     precision_values = []

#     for epoch, row in enumerate(csv_reader):
        
#         # Extract the individual losses (train)
#         box_loss_train = float(row['      train/box_loss'])
#         obj_loss_train = float(row['      train/obj_loss'])
#         cls_loss_train = float(row['      train/cls_loss'])

#         # Calculate the total loss
#         total_loss_train = box_loss_train + obj_loss_train + cls_loss_train
#         mean_loss_train = total_loss_train / 3

#         # Extract the individual losses (validation)
#         box_loss_val = float(row['        val/box_loss'])
#         obj_loss_val = float(row['        val/obj_loss'])
#         cls_loss_val = float(row['        val/cls_loss'])

#         # Calculate the total loss 
#         total_loss_val = box_loss_val + obj_loss_val + cls_loss_val
#         mean_loss_val = total_loss_val / 3

#         lr = float(row['               x/lr0'])
#         precision = float(row['   metrics/precision'])
#         recall = float(row['      metrics/recall'])
#         recall_values.append(recall)
#         precision_values.append(precision)

#         map_05 = float(row['     metrics/mAP_0.5'])

#         # Log the desired metrics
#         writer.add_scalar('Result/Mean of Loss (Train)', mean_loss_train , epoch)
#         writer.add_scalar('Result/Objectness Loss (Train)', obj_loss_train , epoch)
#         writer.add_scalar('Result/Classification Loss (Train)', cls_loss_train , epoch)
#         writer.add_scalar('Result/Box Regression Loss (Train)', box_loss_train , epoch)

#         writer.add_scalar('Result/Mean of Loss (Validation)', mean_loss_val , epoch)
#         writer.add_scalar('Result/Objectness Loss (Validation)', obj_loss_val , epoch)
#         writer.add_scalar('Result/Classification Loss (Validation)', cls_loss_val , epoch)
#         writer.add_scalar('Result/Box Regression Loss (Validation)', box_loss_val , epoch)

#         writer.add_scalar('Result/Scheduled Learning Rate', lr , epoch)
#         writer.add_scalar('mAP@0.5', map_05 , epoch)
#         # Combine precision and recall into one graph
#         # writer.add_scalars('Result/Precision-Recall', {
#         #     'Precision': precision,
#         #     'Recall': recall
#         # })
#         # Plot precision vs recall
#         plt.figure()
#         plt.plot(recall_values, precision_values, marker='o')
#         plt.xlabel('Recall')
#         plt.ylabel('Precision')
#         plt.title('Precision vs Recall')
#         plt.grid(True)

#         # Save the plot to a tensorboardX image summary
#         writer.add_figure('Precision_vs_Recall', plt.gcf(), epoch)
#         plt.close()

# # Close the TensorBoard writer
# writer.close()


import tensorflow as tf
from tensorboardX import SummaryWriter
# from sklearn.metrics import precision_recall_curve
import csv

results_csv_path = 'runs/train/exp/results.csv' 
log_dir = 'runs/train/exp/tensorboard'

# Initialize the TensorBoard writer
writer = SummaryWriter(log_dir=log_dir)

with open(results_csv_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    recall_values = []
    precision_values = []
    for epoch, row in enumerate(csv_reader):
        precision2 = float(row['   metrics/precision'])
        recall2 = float(row['      metrics/recall'])
        recall_values.append(recall2)
        precision_values.append(precision2)

# Generate some sample data
# precision = [0, 0, 1, 1]  # Ground truth labels
# recall = [0.1, 0.4, 0.35, 0.8]  # Predicted probabilities
precision = precision_values
recall = recall_values

# Calculate precision and recall
# precision, recall, thresholds = precision_recall_curve(precision, recall)

# Convert to tensor format
precision = tf.convert_to_tensor(precision, dtype=tf.float32)
recall = tf.convert_to_tensor(recall, dtype=tf.float32)

# Create a summary writer
log_dir = 'runs/train/exp/tensorboard'
writer = tf.summary.create_file_writer(log_dir)

with writer.as_default():
    tf.summary.scalar("Precision", precision, step=0)
    tf.summary.scalar("Recall", recall, step=0)

    # Log the precision-recall curve
    tf.summary.scalar('precision_recall', (precision, recall), step=0)

# Close the writer
writer.close()
