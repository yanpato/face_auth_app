"""
made by Tom0427 !!
"""
import cv2
import numpy
import base64
import hashlib

import os
from flask import Flask, render_template, request


# my modules
from face_detector import sampling_face_feature


# Flaskアプリケーションのインスタンスを作成
app = Flask(
    __name__,
    template_folder="../templates",  # テンプレートフォルダを指定
    static_folder="../static"       # 静的ファイルフォルダを指定
)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
- [POST] upload function
"""
@app.route('/login')
def login():
    return render_template("login.html")

# ルートエンドポイントにアクセスしたときの処理を定義
@app.route('/')
def home():
    data = {
        "title": "Welcome to 怪しい理科大の秘密サイトへ",
        "message": "会員制理科大のやばめの情報まとめサイト"
    }
    return render_template("index.jinja", **data)

# ユーザーの認証
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # 画像データを受け取る
        data = request.json.get('image')
        if not data:
            return "No image data", 400

        # Base64形式をデコード
        header, encoded = data.split(',', 1)
        image_data = base64.b64decode(encoded)

        sampling_face_feature(image_data)
        # ファイル保存
        file_hash_name = hashlib.sha256(image_data).hexdigest()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], '%s.png' % file_hash_name)
        with open(file_path, 'wb') as f:
            f.write(image_data)

        return "Image uploaded successfully", 200
    except Exception as e:
        print(e)
        return str(e), 500

# ユーザーの登録
@app.route('/register', methods=['POST'])
def register():
    try:
        # 画像データを受け取る
        data = request.json.get('image')
        if not data:
            return "No image data", 400
        # Base64形式をデコード
        header, encoded = data.split(',', 1)
        image_data = base64.b64decode(encoded)
        # ファイル保存
        file_hash_name = hashlib.sha256(image_data).hexdigest()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], '%s.png' % file_hash_name)
        with open(file_path, 'wb') as f:
            f.write(image_data)

        return "Image uploaded successfully", 200
    except Exception as e:
        return str(e), 500


def show_cv2_version():
    print(cv2.__version__)

# アプリケーションを実行
if __name__ == "__main__":
    app.run(debug=True)

