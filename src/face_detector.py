import cv2
import numpy as np
import os

# https://github.com/ShiqiYu/libfacedetection.train/blob/master/onnx/yunet_n_320_320.onnx
PATH_TO_FACE_DETECTOR = os.path.join("models", "yunet_n_320_320.onnx")
# https://drive.google.com/file/d/1ClK9WiB492c5OZFKveF3XiHCejoOxINW/view
PATH_TO_FACE_RECOGNIZER = os.path.join("models", "face_recognizer_fast.onnx")

def main():
    # 入力サイズを指定する
    # 画像が3チャンネル以外の場合は3チャンネルに変換する
    image = cv2.imread("./uploads/captured_image.png")
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    # モデルを読み込む
    face_detector = cv2.FaceDetectorYN.create(PATH_TO_FACE_DETECTOR, "", (0, 0))
    face_recognizer = cv2.FaceRecognizerSF.create(PATH_TO_FACE_RECOGNIZER, "")
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
    for i, aligned_face in enumerate(aligned_faces):
        cv2.imwrite("uploads//face{:03}.jpg".format(i + 1), aligned_face)

def sampling_face_feature(binary_data):
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
    face_detector = cv2.FaceDetectorYN.create(PATH_TO_FACE_DETECTOR, "", (0, 0))
    face_recognizer = cv2.FaceRecognizerSF.create(PATH_TO_FACE_RECOGNIZER, "")
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
    # 特徴を抽出する
    for i, aligned_face in enumerate(aligned_faces):
        cv2.imwrite("uploads//face{:03}.jpg".format(i + 1), aligned_face)

    # face_feature = face_recognizer.feature(aligned_face)


def create_cv2_image_from_binary(binary_data):
    # バイナリデータをnumpy配列に変換
    nparr = np.frombuffer(binary_data, np.uint8)
    # OpenCVで画像をデコード
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)


if __name__ == "__main__":
    main()
