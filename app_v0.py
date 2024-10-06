import os
from flask import Flask, request, render_template, send_from_directory
import subprocess
from recommend import recommend_meals  # นำเข้า recommend_meals จาก recommend.py

app = Flask(__name__)

# ตั้งค่าที่เก็บไฟล์อัปโหลด
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# กำหนด path สำหรับผลลัพธ์
RESULTS_FOLDER = r'runs/detect/exp'

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # บันทึกไฟล์ภาพที่อัปโหลด
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # รันคำสั่ง detect.py
    model_path = r'C:\Y4T1\241_353_Art_Intell_Eco_Mod\yolov5\food16_weights\best.pt'
    command = f'py detect.py --save-txt --save-conf --weights "{model_path}" --source "{file_path}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # ตรวจสอบผลลัพธ์
    if result.returncode == 0:
        # อ่านผลลัพธ์จากไฟล์ที่บันทึกใน runs/detect/exp/labels
        output_folder = os.path.join(RESULTS_FOLDER, 'labels')
        results = []
        classes = []
        try:
            for file in os.listdir(output_folder):
                if file.endswith('.txt'):  # ตรวจสอบไฟล์ .txt ที่บันทึกข้อมูล
                    with open(os.path.join(output_folder, file), 'r') as f:
                        lines = f.readlines()
                        results.append(f.read())
                        if lines:  # ตรวจสอบว่าไฟล์มีข้อมูล
                            class_info = lines[0].strip().split()  # แบ่งข้อมูลในบรรทัดแรก
                            if len(class_info) > 0:  # ตรวจสอบว่ามีข้อมูลมากกว่า 0
                                classes.append(class_info[0])  # เก็บค่า Class แรก
        except FileNotFoundError:
            return "Output folder not found."
        
        # เรียกใช้ recommend_meals จาก recommend.py โดยส่งค่า classes
        avg_ratio, component, top_foods = recommend_meals(classes)
        
        # เตรียมข้อมูลสำหรับการแสดงผลในหน้า HTML
        recommended_foods = top_foods  # List ของ tuples (ชื่ออาหาร, อัตราส่วน)

        # กำหนดชื่อไฟล์รูปภาพผลลัพธ์
        processed_image_filename = 'image.jpg'  # หรือชื่ออื่นๆ ที่ YOLOv5 สร้างไว้

        # แสดงผลลัพธ์ในหน้า HTML
        return render_template(
            'result.html',
            results=results,
            processed_image=processed_image_filename,
            classes=classes,
            avg_ratio=avg_ratio,
            component=component,
            recommended_foods=recommended_foods
        )
    else:
        return f'Error: {result.stderr}'

@app.route('/results/<path:filename>')
def send_image(filename):
    return send_from_directory(RESULTS_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
