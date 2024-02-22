from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import os
from dotenv import load_dotenv

load_dotenv()
user_name = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
port_stg = os.getenv("PORT_STG")
database = os.getenv("DATABASE")
database_stg = os.getenv("DATABASE_STG")


#MariaDB 연결할 때 쓰는 코드
DB_URL = f"mysql+pymysql://{user_name}:{password}@{host}:{port}/{database}?charset=utf8"
DB_STG_URL = f"mysql+pymysql://{user_name}:{password}@{host}:{port_stg}/{database_stg}?charset=utf8"

# 데이터베이스 설정
engine = create_engine(
    DB_URL, encoding='utf-8'

    # DB_STG_URL, encoding='utf-8'
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()