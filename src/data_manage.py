# for postgresql
import psycopg2
# .env manage
from dotenv import load_dotenv

import numpy as np
load_dotenv(".env")

import os

# database info
DBNAME = os.getenv("DBNAME")
DBUSER = os.getenv("DBUSER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")

"""
新しいuser_nameと、顔の特徴量データの情報を挿入
databaseには
人の名前と、特徴量とのペアの情報を入れる
"""
def register_face_feature(user_name:str, np_array:np.ndarray):
    # NumPy配列をバイナリデータに変換
    face_feature_binary = np_array.tobytes()

    try:
        with psycopg2.connect(
            dbname=DBNAME,
            user=DBUSER,
            password=PASSWORD,
            host=HOST,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (user_name, face_feature) VALUES (%s, %s)",
                    (user_name, psycopg2.Binary(face_feature_binary))
                )
                conn.commit()
    except Exception as e:
        print(f"Error: {e}")


"""
ユーザーネームで検索をかけて、見つかった顔の特徴量を返却する
"""
def get_user_face_feature_from_database(user_name):
    # データベース接続とクエリ実行
    try:
        with psycopg2.connect(
            dbname=DBNAME,
            user=DBUSER,
            password=PASSWORD,
            host=HOST,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT face_feature FROM users WHERE user_name = %s", (user_name,))
                result = cursor.fetchone()

                if result:
                    face_feature_binary = result[0]
                    face_feature_array = np.frombuffer(face_feature_binary, dtype=np.float32)
                    print(face_feature_array)
    except Exception as e:
        print(f"Error: {e}")



if __name__=="__main__":
    # face_feature_array = np.random.rand(128).astype(np.float32)
    # user_name = "John Doe"
    # register_face_feature(user_name, face_feature_array)
    print(DBNAME, DBUSER, PASSWORD, HOST)
    user_name = "John Doe"
    get_user_face_feature_from_database(user_name)


