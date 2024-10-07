
import numpy as np
import pandas as pd
import base64
import subprocess
import os
import uuid
import glob
import dash
from dash import dcc, html, Input, Output
# Path ของโมเดล
model_path = r'C:\Y4T1\241_353_Art_Intell_Eco_Mod\yolov5\food16_weights\best.pt'
results_dir = r'C:\Y4T1\241_353_Art_Intell_Eco_Mod\yolov5\runs\detect'  # Path ของ results directory
food16_dict = {
    "basil": [0.45, 0.45, 0.1],
    "curry": [0.5, 0.3, 0.2],
    "fried_rice": [0.6, 0.3, 0.1],
    "grilled_pork": [0.2, 0.8, 0],
    "hy_fried_chicken": [0.2, 0.8, 0],
    "mama": [0.9, 0.05, 0.05],
    "noodles": [0.5, 0.35, 0.15],
    "omelet": [0.5, 0.45, 0.05],
    "papaya_salad": [0, 0.1, 0.9],
    "pizza": [0.8, 0.15, 0.05],
    "porridge": [0.7, 0.25, 0.05],
    "red_crispy_pork": [0.5, 0.4, 0.1],
    "sandwich": [0.8, 0.1, 0.1],
    "sashimi": [0, 1, 0],
    "steak": [0.2, 0.6, 0.2],
    "stir_fried_veg": [0, 0.2, 0.8]
}
food_class_names = list(food16_dict.keys())
# สร้างแอป Dash
app = dash.Dash(__name__)
# Layout ของแอป
app.layout = html.Div([
    html.Div(className="header", children=[
        html.H2("Food Recommendation for Next Meal")
    ]),
    html.Img(src='/assets/cov.png', alt='Description of image', style={'width': '300px', 'height': '250px'}),
    html.Div(className="upload-container", style={
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'padding': '20px',
        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
        'backgroundColor': '#ffffff',
        'margin': '15px 0',
        'width': '550px'  # หรือขนาดที่คุณต้องการ
    }, children=[
        html.H1("Upload an Image", style={'textAlign': 'center'}),  # ทำให้ข้อความอยู่กลาง
        # html.P("Meal", style={'textAlign': 'left'}),  # ทำให้ข้อความอยู่ชิดซ้าย
        dcc.Upload(
            id='upload-image',
            children=html.Button('Upload Image', style={
                'width': '100%',
                'background-color': '#28a745',
                'color': 'white',
                'border': 'none',
                'padding': '10px',
                'border-radius': '5px',
                'cursor': 'pointer'
            }),
            multiple=False
        ),
        html.Div(id='output-data-upload', style={'marginTop': '10px'}),
    ]),
], style={
    'fontFamily': 'cursive',
    'backgroundColor': '#f4f4f4',
    'display': 'flex',
    'justifyContent': 'center',
    'alignItems': 'center',
    'flexDirection': 'column',
    'margin': '0',
    'padding': '30px'
})
# Callback เพื่อประมวลผลภาพ
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-image', 'contents')
)
def upload_image(contents):
    if contents:
        # บันทึกไฟล์ภาพที่ผู้ใช้อัปโหลด
        image_name = f'uploaded_image_{uuid.uuid4()}.jpg'  # สร้างชื่อไฟล์แบบสุ่ม
        image_data = contents.split(',')[1]  # แยกข้อมูลภาพ
        with open(image_name, 'wb') as f:
            f.write(base64.b64decode(image_data))  # แก้ไขให้ใช้ base64.b64decode()
        # รันคำสั่งเพื่อประมวลผลภาพ
        command = f'py detect.py --device cuda:0 --save-csv --weights {model_path} --source {image_name}'
        subprocess.run(command, shell=True)
        # ค้นหาไฟล์ predictions.csv ล่าสุด
        latest_csv = max(glob.glob(os.path.join(results_dir, 'exp*/predictions.csv')), key=os.path.getmtime)
        # อ่านผลลัพธ์จาก CSV ล่าสุด
        df = pd.read_csv(latest_csv, header=None, names=['image_name', 'food_class', 'confidence'])
        df.to_csv(r"src\spark\assets\data\detection_log.csv")
        
        # df_spark = pd.read_csv(r"src\spark\assets\data\output_postgres\last_detection_form_db.csv", header=None, names=['image_name', 'food_class', 'confidence'])
        
        # แสดงผลลัพธ์ล่าสุด
        if not df.empty:
            latest_result = df.iloc[-1]  # ใช้แค่ผลล่าสุด
            img_name = latest_result['image_name']  # ชื่อไฟล์ภาพ
            food_class = latest_result['food_class']  # ชนิดอาหาร
            confidence = latest_result['confidence']  # ความมั่นใจ
            
            # หา ratio จาก food_class
            food_ratio = food16_dict.get(food_class, [0, 0, 0])  # ดึงข้อมูล ratio
            # แนะนำมื้อถัดไป
            if 'meals' not in upload_image.__dict__:
                upload_image.meals = []  # initialize meals list
            upload_image.meals.append(food_ratio)  # เก็บค่า ratio
            results = []
            if len(upload_image.meals) == 1:
                # แนะนำมื้อที่ 2
                recommended_second_meal = recommend_next_meal(food_ratio)
                component, top_foods = map_recommendation_to_foods(recommended_second_meal)
                results.append(html.Div([
                    html.P(f"Recommended ratio for 2nd meal: {recommended_second_meal}"),
                    *[html.P(f"{food[0]} (Carb: {food[1][0]}, Protein: {food[1][1]}, Vegge: {food[1][2]})") for food in top_foods],
                    html.Hr()
                ]))
            elif len(upload_image.meals) == 2:
                # แนะนำมื้อที่ 3
                avg_meal = calculate_average(upload_image.meals)
                recommended_third_meal = recommend_next_meal(avg_meal)
                component, top_foods = map_recommendation_to_foods(recommended_third_meal)
                results.append(html.Div([
                    html.P(f"Recommended ratio for 3rd meal: {recommended_third_meal}"),
                    *[html.P(f"{food[0]} (Carb: {food[1][0]}, Protein: {food[1][1]}, Vegge: {food[1][2]})") for food in top_foods],
                    html.Hr()
                ]))
            return html.Div([
                html.H5('Detection Results:'),
                html.P(f"Image Name: {img_name}"),
                html.P(f"Food Class: {food_class}"),
                html.P(f"Confidence: {confidence:.2f}"),
                *results
            ])
    return "No image uploaded."
# ฟังก์ชันการคำนวณอัตราส่วนเฉลี่ย
def calculate_average(meal_history):
    return [np.float16(x) for x in list(np.mean(meal_history, axis=0))]
# ฟังก์ชันแนะนำมื้อถัดไป
def recommend_next_meal(current_avg_ratio):
    target_ratio = [1/3, 1/3, 1/3]  # อัตราส่วนเป้าหมาย
    recommend_ratio = [
        np.float16(2 * target_ratio[0] - current_avg_ratio[0]),
        np.float16(2 * target_ratio[1] - current_avg_ratio[1]),
        np.float16(2 * target_ratio[2] - current_avg_ratio[2])
    ]
    return recommend_ratio
# ฟังก์ชันการแมพคำแนะนำไปยังอาหาร
def map_recommendation_to_foods(recommend_ratio):
    dominant_index = np.argmax(recommend_ratio)
    component_name = ["carb", "protein", "vegge"][dominant_index]
    sorted_foods = sorted(food16_dict.items(), key=lambda item: item[1][dominant_index], reverse=True)
    top_3_foods = sorted_foods[:3]
    return component_name, top_3_foods
if __name__ == '__main__':
    app.run_server(debug=True)

# import numpy as np
# import pandas as pd
# import base64
# import subprocess
# import os
# import uuid
# import glob
# import dash
# from dash import dcc, html, Input, Output
# import requests


# import requests
# from requests.auth import HTTPBasicAuth

# # ข้อมูลการเชื่อมต่อ Airflow
# AIRFLOW_BASE_URL = "http://localhost:8085/api/v1"  # เปลี่ยนเป็น URL ของ Airflow Webserver ของคุณ
# DAG_ID = "yolo"  # ชื่อ DAG ที่ต้องการ trigger
# AIRFLOW_USERNAME = "airflow2"  # ชื่อผู้ใช้ Airflow ของคุณ
# AIRFLOW_PASSWORD = "airflow2"  # รหัสผ่าน Airflow ของคุณ

# def trigger_airflow_dag():
#     url = f"{AIRFLOW_BASE_URL}/dags/{DAG_ID}/dagRuns"
#     payload = {
#         "conf": {}  # ส่งพารามิเตอร์เพิ่มเติมได้หากต้องการ
#     }
#     response = requests.post(url, json=payload, auth=HTTPBasicAuth(AIRFLOW_USERNAME, AIRFLOW_PASSWORD))
#     if response.status_code == 200 or response.status_code == 201:
#         dag_run_id = response.json().get("dag_run_id")
#         print(f"Triggered DAG {DAG_ID} with run ID: {dag_run_id}")
#         return dag_run_id
#     else:
#         print(f"Failed to trigger DAG {DAG_ID}: {response.text}")
#         return None

# def wait_for_dag_completion(dag_run_id, timeout=300):
#     import time

#     url = f"{AIRFLOW_BASE_URL}/dags/{DAG_ID}/dagRuns/{dag_run_id}"
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         response = requests.get(url, auth=HTTPBasicAuth(AIRFLOW_USERNAME, AIRFLOW_PASSWORD))
#         if response.status_code == 200:
#             state = response.json().get("state")
#             if state in ["success", "failed", "running"]:
#                 print(f"DAG run {dag_run_id} state: {state}")
#                 if state == "success":
#                     return True
#                 elif state == "failed":
#                     return False
#         time.sleep(5)  # รอ 5 วินาทีก่อนตรวจสอบสถานะอีกครั้ง
#     print(f"DAG run {dag_run_id} did not complete within {timeout} seconds")
#     return False

# # Path ของโมเดล
# model_path = r'C:\Y4T1\241_353_Art_Intell_Eco_Mod\yolov5\food16_weights\best.pt'
# results_dir = r'C:\Y4T1\241_353_Art_Intell_Eco_Mod\yolov5\runs\detect'  # Path ของ results directory

# food16_dict = {
#     "basil": [0.45, 0.45, 0.1],
#     "curry": [0.5, 0.3, 0.2],
#     "fried_rice": [0.6, 0.3, 0.1],
#     "grilled_pork": [0.2, 0.8, 0],
#     "hy_fried_chicken": [0.2, 0.8, 0],
#     "mama": [0.9, 0.05, 0.05],
#     "noodles": [0.5, 0.35, 0.15],
#     "omelet": [0.5, 0.45, 0.05],
#     "papaya_salad": [0, 0.1, 0.9],
#     "pizza": [0.8, 0.15, 0.05],
#     "porridge": [0.7, 0.25, 0.05],
#     "red_crispy_pork": [0.5, 0.4, 0.1],
#     "sandwich": [0.8, 0.1, 0.1],
#     "sashimi": [0, 1, 0],
#     "steak": [0.2, 0.6, 0.2],
#     "stir_fried_veg": [0, 0.2, 0.8]
# }

# food_class_names = list(food16_dict.keys())

# # สร้างแอป Dash
# app = dash.Dash(__name__)

# # Layout ของแอป
# app.layout = html.Div([
#     html.Div(className="header", children=[
#         html.H2("Food Recommendation for Next Meal")
#     ]),
#     html.Img(src='/assets/cov.png', alt='Description of image', style={'width': '300px', 'height': '250px'}),
#     html.Div(className="upload-container", style={
#         'border': '1px solid #ddd',
#         'borderRadius': '5px',
#         'padding': '20px',
#         'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
#         'backgroundColor': '#ffffff',
#         'margin': '15px 0',
#         'width': '550px'
#     }, children=[
#         html.H1("Upload an Image", style={'textAlign': 'center'}),
#         dcc.Upload(
#             id='upload-image',
#             children=html.Button('Upload Image', style={
#                 'width': '100%',
#                 'background-color': '#28a745',
#                 'color': 'white',
#                 'border': 'none',
#                 'padding': '10px',
#                 'border-radius': '5px',
#                 'cursor': 'pointer'
#             }),
#             multiple=False
#         ),
#         html.Div(id='output-data-upload', style={'marginTop': '10px'}),
#     ]),
# ], style={
#     'fontFamily': 'cursive',
#     'backgroundColor': '#f4f4f4',
#     'display': 'flex',
#     'justifyContent': 'center',
#     'alignItems': 'center',
#     'flexDirection': 'column',
#     'margin': '0',
#     'padding': '30px'
# })

# # Callback เพื่อประมวลผลภาพ
# @app.callback(
#     Output('output-data-upload', 'children'),
#     Input('upload-image', 'contents')
# )
# def upload_image(contents):
#     if contents:
#         # บันทึกไฟล์ภาพที่ผู้ใช้อัปโหลด
#         image_name = f'uploaded_image_{uuid.uuid4()}.jpg'
#         image_data = contents.split(',')[1]
#         with open(image_name, 'wb') as f:
#             f.write(base64.b64decode(image_data))

#         # รันคำสั่งเพื่อประมวลผลภาพ
#         command = f'py detect.py --device cuda:0 --save-csv --weights {model_path} --source {image_name}'
#         subprocess.run(command, shell=True)

#         # ค้นหาไฟล์ predictions.csv ล่าสุด
#         latest_csv = max(glob.glob(os.path.join(results_dir, 'exp*/predictions.csv')), key=os.path.getmtime)

#         # อ่านผลลัพธ์จาก CSV ล่าสุด
#         df = pd.read_csv(latest_csv, header=None, names=['image_name', 'food_class', 'confidence'])

#         df.to_csv(r"src\spark\assets\data\detection_log.csv")
#         print("save detection loc")
#              # Trigger Airflow DAG ก่อนที่จะทำการแนะนำ
#         dag_run_id = trigger_airflow_dag()
#         print("dag")
#         if dag_run_id:
#             print("dag run")
#             if not wait_for_dag_completion(dag_run_id):
#                 return "DAG failed to complete successfully."
        
#         df_spark = pd.read_csv(r"src\spark\assets\data\output_postgres\last_detection_form_db.csv", header=None, names=['image_name', 'food_class', 'confidence'])
        
        
#         # แสดงผลลัพธ์ล่าสุด
#         if not df_spark.empty:
#             latest_result = df_spark.iloc[-1]
#             img_name = latest_result['image_name']
#             food_class = latest_result['food_class']
#             confidence = latest_result['confidence']

#             # หา ratio จาก food_class
#             food_ratio = food16_dict.get(food_class, [0, 0, 0])

#             # แนะนำมื้อถัดไป
#             if 'meals' not in upload_image.__dict__:
#                 upload_image.meals = []

#             upload_image.meals.append(food_ratio)
#             results = []

#             if len(upload_image.meals) == 1:
#                 recommended_second_meal = recommend_next_meal(food_ratio)
#                 component, top_foods = map_recommendation_to_foods(recommended_second_meal)
#                 results.append(html.Div([
#                     html.P(f"Recommended ratio for 2nd meal: {recommended_second_meal}"),
#                     *[html.P(f"{food[0]} (Carb: {food[1][0]}, Protein: {food[1][1]}, Vegge: {food[1][2]})") for food in top_foods],
#                     html.Hr()
#                 ]))

#             elif len(upload_image.meals) == 2:
#                 avg_meal = calculate_average(upload_image.meals)
#                 recommended_third_meal = recommend_next_meal(avg_meal)
#                 component, top_foods = map_recommendation_to_foods(recommended_third_meal)
#                 results.append(html.Div([
#                     html.P(f"Recommended ratio for 3rd meal: {recommended_third_meal}"),
#                     *[html.P(f"{food[0]} (Carb: {food[1][0]}, Protein: {food[1][1]}, Vegge: {food[1][2]})") for food in top_foods],
#                     html.Hr()
#                 ]))

#             return html.Div([
#                 html.H5('Detection Results:'),
#                 html.P(f"Image Name: {img_name}"),
#                 html.P(f"Food Class: {food_class}"),
#                 html.P(f"Confidence: {confidence:.2f}"),
#                 *results
#             ])

#     return "No image uploaded."

# # ฟังก์ชันการคำนวณอัตราส่วนเฉลี่ย
# def calculate_average(meal_history):
#     return [np.float16(x) for x in list(np.mean(meal_history, axis=0))]

# # ฟังก์ชันแนะนำมื้อถัดไป
# def recommend_next_meal(current_avg_ratio):
#     target_ratio = [1/3, 1/3, 1/3]
#     recommend_ratio = [
#         np.float16(2 * target_ratio[0] - current_avg_ratio[0]),
#         np.float16(2 * target_ratio[1] - current_avg_ratio[1]),
#         np.float16(2 * target_ratio[2] - current_avg_ratio[2])
#     ]
#     return recommend_ratio

# # ฟังก์ชันการแมพคำแนะนำไปยังอาหาร
# def map_recommendation_to_foods(recommend_ratio):
#     dominant_index = np.argmax(recommend_ratio)
#     component_name = ["carb", "protein", "vegge"][dominant_index]

#     sorted_foods = sorted(food16_dict.items(), key=lambda item: item[1][dominant_index], reverse=True)

#     top_3_foods = sorted_foods[:3]
#     return component_name, top_3_foods

# if __name__ == '__main__':
#     app.run_server(debug=True)
