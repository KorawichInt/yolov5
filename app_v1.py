# import os
# from flask import Flask, request, render_template, send_from_directory
# import subprocess

# app = Flask(__name__)

# # ตั้งค่าที่เก็บไฟล์อัปโหลด
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # กำหนด path สำหรับผลลัพธ์
# RESULTS_FOLDER = r'runs/detect/exp'

# @app.route('/')
# def upload_form():
#     return render_template('upload.html')

# @app.route('/', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return 'No file part'
#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file'
    
#     # บันทึกไฟล์ภาพที่อัปโหลด
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(file_path)

#     # รันคำสั่ง detect.py
#     model_path = r'C:\Y4T1\241_353_Art_Intell_Eco_Mod\yolov5\food16_weights\best.pt'
#     command = f'py detect.py --save-txt --save-conf --weights {model_path} --source {file_path}'
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)

#     # ตรวจสอบผลลัพธ์
#     if result.returncode == 0:
#         # อ่านผลลัพธ์จากไฟล์ที่บันทึกใน runs/detect/exp
#         output_folder = os.path.join(RESULTS_FOLDER, 'labels')
        
#         # แสดงผลลัพธ์จากไฟล์ .txt
#         results = []
#         try:
#             for file in os.listdir(output_folder):
#                 if file.endswith('.txt'):  # ตรวจสอบไฟล์ .txt ที่บันทึกข้อมูล
#                     with open(os.path.join(output_folder, file), 'r') as f:
#                         results.append(f.read())
#         except FileNotFoundError:
#             return "Output folder not found."
        
#         # กำหนดชื่อไฟล์รูปภาพผลลัพธ์
#         processed_image_filename = os.path.join(RESULTS_FOLDER, 'image.jpg')  # หรือชื่ออื่นๆ ที่ YOLOv5 สร้างไว้
#         # แสดงผลลัพธ์ในหน้า HTML
#         return render_template('result.html', results=results, processed_image=processed_image_filename)
#     else:
#         return f'Error: {result.stderr}'

# @app.route('/results/<path:filename>')
# def send_image(filename):
#     return send_from_directory(RESULTS_FOLDER, filename)

# if __name__ == '__main__':
#     app.run(debug=True)


import os
from flask import Flask, request, render_template, send_from_directory
import subprocess

app = Flask(__name__)

# ตั้งค่าที่เก็บไฟล์อัปโหลด
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# กำหนด path สำหรับผลลัพธ์
RESULTS_FOLDER = r'runs/detect/exp'

# กำหนด path สำหรับ cover.png
COVER_IMG = r'img_source/'

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Run the detection command
    model_path = r'D:\EcoSystem\yolov5_team\yolov5\food16_weights\best.pt'
    command = f'py detect.py --save-csv --weights {model_path} --source {file_path}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
        # Assuming the processed image name is derived from the uploaded file name
        processed_image_filename = f'{file.filename.split(".")[0]}.jpg'  # Update according to YOLOv5 output

        return render_template('result.html', processed_image=processed_image_filename)
    else:
        return f'Error: {result.stderr}'

@app.route('/results/<path:filename>')
def send_image(filename):
    return send_from_directory(RESULTS_FOLDER, filename)

@app.route('/img/<path:filename>')
def image(filename):
    return send_from_directory(COVER_IMG, filename)

if __name__ == '__main__':
    app.run(debug=True)


