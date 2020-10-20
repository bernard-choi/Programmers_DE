from airflow import DAG
from airflow.operators import PythonOperator
from datetime import datetime
import requests
import psycopg2


dag_second_assignment = DAG(
	dag_id = 'second_assignment',
	start_date = datetime(2020,8,11), # 적당히 조절
	schedule_interval = '5 10 * * *')  # 적당히 조절

def extract(url):
    f = requests.get(link)
    return (f.text)

def transform(text):
    lines = text.split("\n")
    return lines

def load(lines):
    # BEGIN과 END를 사용해서 SQL 결과를 트랜잭션으로 만들어주는 것이 좋음
    # BEGIN;TRUNCATE TABLE;INSERT INTO TABLE VALUES ('KEEYONG', 'MALE');END;
    cur = get_Redshift_connection()
    sql = 'Truncate gafield8785.name_gender'
    print(sql)
    cur.execute(sql)
    for r in lines:
        if r != '':
            (name, gender) = r.split(",")
            if (name=='name')&(gender =='gender'): ## 변수명을 담고 있으면 pass
              continue
            print(name, "-", gender)
            sql = "INSERT INTO gafield8785.name_gender VALUES ('{name}', '{gender}')".format(name=name, gender=gender)
            print(sql)
            cur.execute(sql)

def get_Redshift_connection():
    host = "grepp-data.cduaw970ssvt.ap-northeast-2.redshift.amazonaws.com"
    redshift_user = "gafield8785"
    redshift_pass = "Gafield87851!"
    port = 5439
    dbname = "dev"
    conn = psycopg2.connect("dbname={dbname} user={user} host={host} password={password} port={port}".format(
        dbname=dbname,
        user=redshift_user,
        password=redshift_pass,
        host=host,
        port=port
    ))
    conn.set_session(autocommit=True)
    return conn.cursor()


def etl():
    link = "https://s3-geospatial.s3-us-west-2.amazonaws.com/name_gender.csv"
    data = extract(link)
    lines = transform(data)
    load(lines)

	 # 여기에 코드를 기록



task = PythonOperator(
	task_id = 'perform_etl',
	python_callable = etl,
	dag = dag_second_assignment)

# task가 하나 밖에 없는 경우 아무 것도 하지 않아도 그냥 실행됨
