import os
import csv
from flask import Flask, request, render_template, send_from_directory, jsonify
import subprocess
from recommend import recommend_meals, simulate_monthly_meals  # นำเข้า recommend_meals จาก recommend.py

app = Flask(__name__)

# ตั้งค่าที่เก็บไฟล์อัปโหลด
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# กำหนด path สำหรับผลลัพธ์
RESULTS_FOLDER = os.path.join('runs', 'detect', 'exp')
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# ฟังก์ชันเพื่อเขียน header ลงใน CSV ถ้ายังไม่มีไฟล์
def write_csv_header(csv_file_path):
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Food Class Index", "Recommended Foods"])

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
    model_path = r'C:\Y4T1\241_353_Art_Intell_Eco_Mod\yolov5\food16_weights\best.pt'  # แก้ไขตามที่อยู่ของโมเดลคุณ
    command = f'py detect.py --device cuda:0 --save-txt --save-conf --weights "{model_path}" --source "{file_path}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        # อ่านผลลัพธ์จากไฟล์ที่บันทึกใน runs/detect/exp/labels
        output_folder = os.path.join(RESULTS_FOLDER, 'labels')
        
        # แปลงไฟล์ .txt เป็น .csv และดึงค่า food_class_index
        results = []
        food_class_index = None  # กำหนดตัวแปร food_class_index

        try:
            csv_file_path = os.path.join(RESULTS_FOLDER, 'results.csv')
            write_csv_header(csv_file_path)  # เขียน header ถ้ายังไม่มีไฟล์

            for file in os.listdir(output_folder):
                if file.endswith('.txt'):  # ตรวจสอบไฟล์ .txt ที่บันทึกข้อมูล
                    txt_file_path = os.path.join(output_folder, file)
                    with open(txt_file_path, 'r') as f:
                        result_data = f.readlines()
                        results.append(result_data)
                        if result_data:
                            # เอาค่าแรกใน list มาใช้เป็น food_class_index
                            first_line = result_data[0].strip().split()
                            if len(first_line) > 0:
                                food_class_index = int(first_line[0])
                    
                    # เขียนผลลัพธ์ลงในไฟล์ CSV
                    with open(csv_file_path, mode='a', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        for line in result_data:
                            data = line.strip().split()
                            writer.writerow(data)  # เขียนข้อมูลลง CSV

        except FileNotFoundError:
            return "Output folder not found."

        if food_class_index is not None:
            # เรียกใช้ recommend_meals จาก recommend.py โดยส่งค่า food_class_index
            recommended_foods = recommend_meals(food_class_index)
        else:
            recommended_foods = []

        # กำหนดชื่อไฟล์รูปภาพผลลัพธ์
        processed_image_filename = 'image.jpg'  # หรือชื่ออื่นๆ ที่ YOLOv5 สร้างไว้

        return render_template(
            'result.html',
            results=results,
            processed_image=processed_image_filename,
            food_class_index=food_class_index,
            recommended_foods=recommended_foods
        )
    else:
        return f'Error: {result.stderr}'

@app.route('/results/<path:filename>')
def send_image(filename):
    return send_from_directory(RESULTS_FOLDER, filename)

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        # สมมติว่าคุณต้องการเรียกใช้ฟังก์ชัน simulate_monthly_meals() เมื่อมีการเรียก API นี้
        simulate_monthly_meals()  # เรียกใช้ฟังก์ชันจาก recommend.py
        return jsonify({"message": "Simulation completed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
