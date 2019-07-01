import re
import os
import face_recognition

def get_foto_dict(path):
    foto_dict = {}
    for filename in os.listdir(path):
        if not filename.endswith(".jpg"):
            continue
        
        name = re.sub("\.jpg$", "", filename)
        print(name)
        foto_dict[name] = face_recognition.face_encodings(
            face_recognition.load_image_file(os.path.join(path, filename)))[0]
    return foto_dict

def test_face(filename, foto_dict):
    faces = face_recognition.face_encodings(
        face_recognition.load_image_file(filename))
    if not faces:
        return []
    face = faces[0]
    names = list(foto_dict.keys()) 
    res = face_recognition.compare_faces(list(foto_dict.values()), face)
    return [names[i] for i, r in enumerate(res) if r]