# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from datetime import datetime
# import pandas as pd
# import os

# # ฟังก์ชันในการโหลด CSV เข้า PostgreSQL
# def load_csv_to_postgres(**kwargs):
#     # ดึงค่า path ของไฟล์ CSV จาก dag parameters
#     csv_file = kwargs['dag_run'].conf.get('csv_file', '/usr/local/spark/assets/data/meal_log.csv')

#     # อ่านไฟล์ CSV
#     df = pd.read_csv(csv_file)
    
#     # เชื่อมต่อกับ PostgreSQL
#     # pg_hook = PostgresHook(postgres_conn_id='spark_default')
#     # pg_conn = pg_hook.get_conn()
#     # cursor = pg_conn.cursor()
    
#     pg_conn = os.environ.get("spark_default", "spark_default") 
#     pg_hook = "spark://spark:7077"
#     spark_app_name = "food"
#     cursor = pg_conn.cursor()
    
#     # ลบข้อมูลเดิมถ้าต้องการ หรือปรับตามความต้องการ
#     cursor.execute("DELETE FROM meal_log;")
#     pg_conn.commit()
    
#     # แทรกข้อมูลใหม่
#     for index, row in df.iterrows():
#         cursor.execute(
#             """
#             INSERT INTO meal_log (day, meal, food_class, food_class_index, carb, protein, vegge)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#             """,
#             (row['Day'], row['Meal'], row['Food Class'], row['Food Class Index'], row['Carb'], row['Protein'], row['Vegge'])
#         )
    
#     pg_conn.commit()
#     cursor.close()
#     pg_conn.close()

# # ตั้งค่า DAG
# default_args = {
#     'owner': 'airflow',
#     'start_date': datetime(2024, 1, 1)
# }

# with DAG(
#     'load_meal_log',
#     default_args=default_args,
#     schedule_interval='@daily',  # กำหนดเวลาในการรัน DAG
#     catchup=False,
# ) as dag:
    
#     load_meal_log = PythonOperator(
#         task_id='load_csv_to_postgres',
#         python_callable=load_csv_to_postgres,
#         provide_context=True,
#     )
    
#     load_meal_log

import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

###############################################
# Parameters
###############################################

spark_conn = os.environ.get("spark_default", "spark_default") 
spark_master = "spark://spark:7077"
postgres_driver_jar = "/usr/local/spark/assets/jars/postgresql-42.2.6.jar"

# movies_file = "/usr/local/spark/assets/data/movies.csv" 
# ratings_file = "/usr/local/spark/assets/data/ratings.csv"
gpt_prompt_file = "/usr/local/spark/assets/data/detection_log.csv"
postgres_db = "jdbc:postgresql://postgres:5432/airflow"
postgres_user = "airflow"
postgres_pwd = "airflow"

###############################################
# DAG Definition
###############################################
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    dag_id="yolo",
    description="This DAG is a sample of integration between Spark and DB. It reads CSV files, load them into a Postgres DB and then read them from the same Postgres DB.",
    default_args=default_args,
    schedule_interval=timedelta(1)
)

start = DummyOperator(task_id="start", dag=dag)


spark_job_load_postgres = SparkSubmitOperator( 
    task_id="spark_job_load_postgres",
    application="/usr/local/spark/applications/load-postgres.py",
    name="load-postgres",
    conn_id=spark_conn,
    verbose=1,
    conf={"spark.master": spark_master}, 
    application_args=[gpt_prompt_file,
                      postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag)

spark_job_read_postgres = SparkSubmitOperator(
    task_id="spark_job_read_postgres",
    application="/usr/local/spark/applications/read-postgres.py",
    name="read-postgres",
    conn_id= spark_conn,
    verbose=1,
    conf={"spark.master": spark_master},
    application_args=[postgres_db, postgres_user, postgres_pwd],
    jars=postgres_driver_jar,
    driver_class_path=postgres_driver_jar,
    dag=dag)

end = DummyOperator(task_id="end", dag=dag)

start >> spark_job_load_postgres >> spark_job_read_postgres >> end
