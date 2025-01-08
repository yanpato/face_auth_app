import cv2
import numpy as np
import os

# https://github.com/ShiqiYu/libfacedetection.train/blob/master/onnx/yunet_n_640_640.onnx
PATH_TO_FACE_DETECTOR = os.path.join("models", "yunet_n_640_640.onnx")
# https://drive.google.com/file/d/1ClK9WiB492c5OZFKveF3XiHCejoOxINW/view
PATH_TO_FACE_RECOGNIZER = os.path.join("models", "face_recognizer_fast.onnx")

class NoFaceFoundError(BaseException):
    def __init__(self):
        self.message = "顔が検出できなかった場合のエラー"
        super().__init__(self.message)

class MultiFaceFoundError(BaseException):
    def __init__(self):
        self.message = "複数の顔を検出した場合のエラー"
        super().__init__(self.message)

"""
顔を見つけて、切り取る関数
"""
def detect_face_images(face_detector, face_recognizer,binary_data):
    image = create_cv2_image_from_binary(binary_data)
    # モデルを読み込む
    height, width, _ = image.shape
    face_detector.setInputSize((width, height))

    # 顔を検出する
    _, faces = face_detector.detect(image)
    faces = faces if faces is not None else []

    # 検出された顔を切り抜く
    aligned_faces = []
    if faces is not None:
        for face in faces:
            aligned_face = face_recognizer.alignCrop(image, face)
            aligned_faces.append(aligned_face)
    return aligned_faces

"""
`detector`と`recognizer`を返す関数
"""
def set_face_models():
    face_detector = cv2.FaceDetectorYN.create(PATH_TO_FACE_DETECTOR, "", (0, 0))
    face_recognizer = cv2.FaceRecognizerSF.create(PATH_TO_FACE_RECOGNIZER, "")
    return face_detector,face_recognizer


"""
# imageのバイナリデータを受け取って、特徴量を抽出する関数

画像に顔が写っていない場合は、顔が写っていないことを示すerrorを返す
画像に二人以上の人が写っているときもerrorを返す
"""
def sampling_face_feature(binary_data) -> np.ndarray:

    # 画像バイナリからnumpyのの形式に変換
    image = create_cv2_image_from_binary(binary_data)

    # 画像が3チャンネル以外の場合は3チャンネルに変換する
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # モデルを読み込む
    face_detector, face_recognizer = set_face_models()

    # 入力サイズを指定する
    height, width, _ = image.shape

    # 画像に写っていた人の顔の画像をすべて返します
    aligned_faces = detect_face_images(face_detector, face_recognizer, binary_data)
    if len(aligned_faces) == 1:
        pass
    elif len(aligned_faces) > 1:
        raise MultiFaceFoundError()
    else:
        raise NoFaceFoundError()

    # 特徴を抽出する
    for i, aligned_face in enumerate(aligned_faces):
        cv2.imwrite("uploads//face{:03}.jpg".format(i + 1), aligned_face)

    face_feature = face_recognizer.feature(aligned_face)
    # print(face_feature)
    return face_feature


"""
イメージバイナリデータから、cv2imageオブジェクトを作る
"""
def create_cv2_image_from_binary(binary_data):
    # バイナリデータをnumpy配列に変換
    nparr = np.frombuffer(binary_data, np.uint8)
    # OpenCVで画像をデコード
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

"""
顔の特徴量を比較する関数
"""
def compare_faces(feature1:np.ndarray, feature2:np.ndarray):
    face_recognizer = cv2.FaceRecognizerSF.create(PATH_TO_FACE_RECOGNIZER, "")
    score = face_recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
    return score


if __name__ == "__main__":
    main()
