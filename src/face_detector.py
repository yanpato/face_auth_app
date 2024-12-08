import cv2
import numpy as np
import os
import face_recognition


# https://github.com/ShiqiYu/libfacedetection.train/blob/master/onnx/yunet_n_320_320.onnx
PATH_TO_FACE_DETECTOR = os.path.join("models", "yunet_n_640_640.onnx")
# https://drive.google.com/file/d/1ClK9WiB492c5OZFKveF3XiHCejoOxINW/view
PATH_TO_FACE_RECOGNIZER = os.path.join("models", "face_recognizer_fast.onnx")

"""
# imageのバイナリデータを受け取って、128次元の特徴を抽出する関数

画像に顔が写っていない場合は、顔が写っていないことを示すerrorを返す
画像に二人以上の人が写っているときもerrorを返す

"""
def sampling_face_feature(binary_data) -> np.ndarray:
    # 入力サイズを指定する
    # 画像が3チャンネル以外の場合は3チャンネルに変換する
    print("loading image data")
    image = create_cv2_image_from_binary(binary_data)
    print("loading image data... done")
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    # モデルを読み込む
    face_detector = cv2.FaceDetectorYN.create(PATH_TO_FACE_DETECTOR,  "", (640, 640), 0.6, 0.3, 5000, cv2.dnn.DNN_BACKEND_DEFAULT, target_id=cv2.dnn.DNN_TARGET_CPU)
    face_recognizer = cv2.FaceRecognizerSF.create(PATH_TO_FACE_RECOGNIZER, "")
    height, width, _ = image.shape
    face_detector.setInputSize((width, height))
    # 顔を検出する
    _, faces = face_detector.detect(image)
    faces = faces if faces is not None else []
    # 検出された顔を切り抜く
    print("faces.shape", faces.shape)
    aligned_faces = []
    if faces is not None:
        for face in faces:
            aligned_face = face_recognizer.alignCrop(image, face)
            aligned_faces.append(aligned_face)
    # 特徴を抽出する
    for i, aligned_face in enumerate(aligned_faces):
        cv2.imwrite("uploads//face{:03}.jpg".format(i + 1), aligned_face)

    print(aligned_face.shape)
    face_feature = face_recognizer.feature(aligned_face)
    _, faces = face_detector.detect(image)
    print(faces.shape)

    return face_feature

"""
画像に含まれているすべての顔を返す
"""
def find_all_face_in_image(bin_image):
    # 入力サイズを指定する
    # 画像が3チャンネル以外の場合は3チャンネルに変換する
    print("loading image data")
    image = create_cv2_image_from_binary(bin_image)
    print("loading image data... done")
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    # モデルを読み込む
    face_detector = cv2.FaceDetectorYN.create(PATH_TO_FACE_DETECTOR,  "", (320, 320), 0.6, 0.3, 5000, cv2.dnn.DNN_BACKEND_DEFAULT, target_id=cv2.dnn.DNN_TARGET_CPU)
    face_recognizer = cv2.FaceRecognizerSF.create(PATH_TO_FACE_RECOGNIZER, "")
    height, width, _ = image.shape
    face_detector.setInputSize((width, height))
    # 顔を検出する
    _, faces = face_detector.detect(image)
    faces = faces if faces is not None else []
    # 検出された顔を切り抜く
    print("faces.shape", faces.shape)
    aligned_faces = []
    if faces is not None:
        for face in faces:
            aligned_face = face_recognizer.alignCrop(image, face)
            aligned_faces.append(aligned_face)
    # 特徴を抽出する
    if len(aligned_faces) == 1:
        return aligned_faces[0]
    else:
        raise BaseException("人が見つかりませんでした")


"""
一枚の顔画像から、特徴を抽出する
"""
def sampling_face_feature2(npimage):
    return face_recognition.face_encodings(npimage)[0]


"""
２つのイメージを比較して一致した人物かどうかをチェックする
"""
def match_faces(enc1, enc2):
    # 2つの顔のエンコーディングを比較する
    results = face_recognition.compare_faces([enc1], enc2)

    dis = face_recognition.face_distance([enc1], enc2)
    print("dis",dis)
    # 結果の出力
    print("結果の出力",results)
    if results[0]:
        print("同じ人物です！")
    else:
        print("違う人物です。")


"""
イメージバイナリデータから、cv2imageオブジェクトを作る
"""
def create_cv2_image_from_binary(binary_data):
    # バイナリデータをnumpy配列に変換
    nparr = np.frombuffer(binary_data, np.uint8)
    image =cv2.imdecode(nparr, cv2.IMREAD_COLOR) 
    print("image shape", image.shape)
    # OpenCVで画像をデコード
    return image

"""
顔の特徴量を比較する関数
"""
def compare_faces(feature1:np.ndarray, feature2:np.ndarray):
    COSINE_THRESHOLD = 0.363
    face_recognizer = cv2.FaceRecognizerSF.create(PATH_TO_FACE_RECOGNIZER, "")
    score = face_recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
    return score
    # if score > COSINE_THRESHOLD:
    #     return True, (user_id, cos_score)
    # return False, ("", 0.0)


if __name__ == "__main__":
    main()
