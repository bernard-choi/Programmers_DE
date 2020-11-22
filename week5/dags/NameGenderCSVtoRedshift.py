from airflow import DAG
from airflow.operators import PythonOperator
from datetime import datetime # startdate지정 위해
import requests
import logging  ## print위해
import psycopg2 ## redshift에서 read, write위해

def get_Redshift_connection():
    host = "grepp-data.cduaw970ssvt.ap-northeast-2.redshift.amazonaws.com"
    redshift_user = ""  # 본인 ID 사용
    redshift_pass = ""  # 본인 Password 사용
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


def extract(url):
    logging.info("Extract started")
    f = requests.get(url)
    logging.info("Extract done")
    return (f.text)


def transform(text):
    logging.info("transform started")
    # ignore the first line - header
    lines = text.split("\n")[1:]
    logging.info("transform done")
    return lines


def load(lines):
    logging.info("load started")
    cur = get_Redshift_connection()
    sql = "BEGIN;DELETE FROM TABLE raw_data.name_gender;" ## truncate은 roll back이 안됨.
    for l in lines:
        if l != '':
            (name, gender) = l.split(",")
            sql += "INSERT INTO raw_data.name_gender VALUES ('{name}', '{gender}');"
    sql += "COMMIT;END;" ## 실행 결과에 문제가 있을때 이전으로 쉽게 들어가기위해 Blocking하는 목적
                  ## try except 는 에러를 잡을수는 있지만 어떤 에러인지 확인하기 힘들다.
    cur.execute(sql)
    logging.info(sql)
    logging.info("load done")


def etl():
    link = "https://s3-geospatial.s3-us-west-2.amazonaws.com/name_gender.csv"
    data = extract(link)
    lines = transform(data)
    load(lines)


dag_second_assignment = DAG(
	dag_id = 'second_assignment',
	start_date = datetime(2020,8,10), # 날짜가 미래인 경우 실행이 안됨
	schedule_interval = '0 2 * * *')  # UTC기준 오전 2시. local timezone도 사용 가능

task = PythonOperator(
	task_id = 'perform_etl',
	python_callable = etl,
	dag = dag_second_assignment) ## 다른 오퍼레이터는 다루지 않을 예정.
