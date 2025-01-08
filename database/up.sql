-- テーブルの作成
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,             -- 自動増分のプライマリキー
    user_name VARCHAR(255) NOT NULL UNIQUE,        -- ユーザー名（必須）
    face_feature BYTEA NOT NULL             -- NumPy形式の128次元のバイナリデータ
);

-- ユーザーデータの挿入例
-- INSERT INTO users (user_name, face_feature) VALUES ('John Doe', '\\x...');
