"""
made by Tom0427 !!
"""
import cv2

from flask import Flask, render_template

# Flaskアプリケーションのインスタンスを作成
app = Flask(
    __name__,
    template_folder="../templates",  # テンプレートフォルダを指定
    static_folder="../static"       # 静的ファイルフォルダを指定
)


@app.route('/login')
def login():
    return "Hello, World!"


# ルートエンドポイントにアクセスしたときの処理を定義
@app.route('/')
def home():
    data = {
        "title": "Welcome to Flask with Jinja2",
        "message": "This page is rendered using Jinja2!"
    }
    return render_template("index.jinja", **data)


def show_cv2_version():
    print(cv2.__version__)

# アプリケーションを実行
if __name__ == "__main__":
    app.run(debug=True)


