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
database = os.getenv("DATABASE")

print(user_name, password, host, port, database)

#MySQL 연결할 때 쓰는 코드
## print(__file__) #이 파일의 상대경로
# BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #이 파일의 절대경로
# SECRET_FILE = os.path.join(BASE_DIR, 'secrets.json')
# secrets = json.loads(open(SECRET_FILE).read())
# DB = secrets["DB"]

# DB_URL = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset=utf8"

#MariaDB 연결할 때 쓰는 코드
DB_URL = f"mysql+pymysql://{user_name}:{password}@{host}:{port}/{database}?charset=utf8"
# DB_URL = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset=utf8"

# 데이터베이스 설정
# DB_URL = "sqlite:///./google_chatgpt.db?check_same_thread=False"
engine = create_engine(
    DB_URL, encoding='utf-8'
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()