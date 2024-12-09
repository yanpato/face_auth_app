from face_detector import sampling_face_feature,detect_face_images

from os import path

def test00():
    with open(path.join("uploads","face001.jpg"), mode="rb") as f:
        bin_image = f.read()
        image_feature = detect_face_images(bin_image)
        print(image_feature)
    return 

def main():
    test00()

if __name__ == "__main__":
    main()
