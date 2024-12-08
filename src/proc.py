from face_detector import sampling_face_feature

from data_manage import register_face_feature


"""
登録時の処理をする関数

"""
def register_proc(user_name:str, image_bin_data):
    try:
        face_feature = sampling_face_feature(image_bin_data)
    except Exception as e:
        return "some thing wrong with detecting proc"
    try:
        register_face_feature(user_name, face_feature)
    except Exception as e:
        return "some thing wrong with database proc"




