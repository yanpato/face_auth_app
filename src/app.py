"""
made by Tom0427 !!
"""
import cv2
import numpy
import base64
import hashlib

import os
from flask import Flask, render_template, request, session, redirect, url_for
from flask_cors import CORS

# my modules
from face_detector import sampling_face_feature, compare_faces
from data_manage import register_face_feature, get_user_face_feature_from_database

from dotenv import load_dotenv
load_dotenv(".env")

# Flaskアプリケーションのインスタンスを作成
app = Flask(
    __name__,
    template_folder="../templates",  # テンプレートフォルダを指定
    static_folder="../static"       # 静的ファイルフォルダを指定
)
CORS(app)


app.secret_key = os.getenv("SECRET_KEY")

# 必要な定数郡
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# request head type
RQHEADER_REGISTER="register" 
RQHEADER_LOGIN="login" 

"""
- [POST] upload function
"""
@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.jinja")


# ルートエンドポイントにアクセスしたときの処理を定義
@app.route('/')
def home():
    data = {
        "title": "Welcome to 怪しい理科大の秘密サイトへ",
        "message": "会員制理科大のやばめの情報まとめサイト"
    }
    return render_template("index.jinja", **data)


@app.route('/login_failed', methods=["GET"])
def login_failed():
    data = {
        "title": "Welcome to 怪しい理科大の秘密サイトへ",
        "message": "もう一度お試しください"
    }
    return render_template("index.jinja", **data)


@app.route('/user', methods=["GET"])
def user():
    data = {
        "title": "Welcome to 怪しい理科大の秘密サイトへ",
        "message": "ようこそ %s さん" % session["user_name"]
    }
    return render_template("user.html", **data)


# POST requestを受け取る

## ユーザーの認証
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # requestデータを受け取る
        data = request.json.get('image')
        request_head = request.json.get('request_head')
        user_name = request.json.get('user_name')
        # Base64形式をデコード
        image_data = base64_to_bin_image(data)

        print("userの名前", user_name)
        if not data:
            return "No image data", 400

        if request_head == RQHEADER_REGISTER:
            # 新しくユーザー登録する場合
            print("user tried to login register")
        elif request_head == RQHEADER_LOGIN:
            # ログインする場合
            print("user tried to login")
        else:
            # invalid operation
            return str("不正なヘッダーです！"), 500

        sampling_face_feature(image_data)
        # ファイル保存
        file_hash_name = hashlib.sha256(image_data).hexdigest()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], '%s.png' % file_hash_name)

        with open("uploads/face001.jpg", mode="rb") as f:
            print(compare_faces(sampling_face_feature(image_data), sampling_face_feature(f.read())))
        with open(file_path, 'wb') as f:
            f.write(image_data)

        return "Image uploaded successfully", 200
    except Exception as e:
        print(e)
        return str(e), 500

@app.route('/login_user', methods=["POST", "GET"])
def login_user():
    print("login_user".center(100,"="))
    try:
        # requestデータを受け取る
        data = request.json.get('image')
        request_head = request.json.get('request_head')
        user_name = request.json.get('user_name')
        # Base64形式をデコード
        image_data = base64_to_bin_image(data)

        print("userの名前", user_name)
        if not data:
            return "No image data", 400

        if check_user_face(user_name, image_data):
            # 本人の場合
            print("本人です")
            session["user_name"] = user_name
            return redirect(url_for("user"))
        else:
            # 本人でない場合
            print("本人ではないです")
            return redirect(url_for("login_failed"))
    except Exception as e:
       print(e)
       return str(e), 500


@app.route('/register_user', methods=["POST"])
def register_user():
    try:
        # requestデータを受け取る
        data = request.json.get('image')
        request_head = request.json.get('request_head')
        user_name = request.json.get('user_name')
        # Base64形式をデコード
        if not data:
            return "No image data", 400
        else:
            image_data = base64_to_bin_image(data)
        print("userの名前", user_name)

        try:
            # 新しく登録される顔の特徴量を抽出する
            face_feature =  sampling_face_feature(image_data)
            # データベースにアクセスして、名前と特徴量のペアの情報を登録
            register_face_feature(user_name, face_feature)
        except Exception(e) as e:
            data = {
                "title": "Welcome to 怪しい理科大の秘密サイトへ",
                "message": "登録できませんでした"
            }
            return render_template("index.jinja", **data)


        return "Image uploaded successfully", 200
    except Exception as e:
        print(e)
        return str(e), 500


"""
user_nameと、顔画像から
ログインできるか否かを判定する
"""
def check_user_face(user_name:str, image_data) -> bool:
    unknown_face_feature = sampling_face_feature(image_data)[0]
    base_face_feature = get_user_face_feature_from_database(user_name)
#    print("face_feature_array", base_face_feature)
#    print("unknown_face_feature",unknown_face_feature)
    score = compare_faces(unknown_face_feature, base_face_feature)
    if 95 < score:
        # 本人の場合
        return True
    else:
        # 本人ではない場合
        return False


def base64_to_bin_image(b64_data):
    header, encoded = b64_data.split(',', 1)
    image_data = base64.b64decode(encoded)
    return image_data


# アプリケーションを実行
if __name__ == "__main__":
    app.run(debug = True)

