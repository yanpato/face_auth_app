# face auth up

## 必要な学習済みモデル

以下のモデルをダウンロードして、`models`ディレクトリ内に配置する必要がある

- [detector](https://github.com/ShiqiYu/libfacedetection.train/blob/master/onnx/yunet_n_320_320.onnx)

- [recognizer](https://drive.google.com/file/d/1ClK9WiB492c5OZFKveF3XiHCejoOxINW/view)

## 必要なデータベースの設定

### postgresqlをインストールする

[postgresql公式](https://www.postgresql.org/)

### データベースの作成と設定

#### データーベースを作成する

```sql
CREATE DATABASE face_auth_app;
```

#### データーベース内にテーブルを作成する

`database/up.sql`の内容を実行する

#### データーベースの設定を`.env`に書く

`.env`という名前のファイルを作成して、中に設定を書く

上からdatabaseの名前(今回は`face_auth_app`)

データベースのユーザー名(デフォルトでpostgres)

パスワード(自分のやつ)

ホスト名(hostnameのままでok)

```
DBNAME='face_auth_app'
DBUSER='postgres'
PASSWORD='your password'
HOST='localhost'
```

## 実行

実行するときは
```bash
uv run src/app.py
```

[http://127.0.0.1:5000/register](http://127.0.0.1:5000/register)にアクセスする

