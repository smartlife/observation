import os
import sys
import shutil
import subprocess
import requests
from flask import Flask, request


try:
    import pyaudio
    import wave
    PLAY_SOUND = True
except:
    PLAY_SOUND = False
    print('No sound available')

import face_detection
from motion_detection import MotionDetector

ADDR = "::"
PORT = 8087
DEBUG = True

path_to_archive = "фото2.0"
path_to_sound = "звуки"
face_dict = face_detection.get_foto_dict("faces")
motion_detector = MotionDetector()


def play_sound(filename):
    if not PLAY_SOUND:
        return
    print("ps>", filename)
    CHUNK = 1024
 
    with wave.open(filename, 'rb') as wf:

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()

        p.terminate()

def upload_image(filename="photo.jpg"):
    with open(filename, "rb") as fr:
        r = requests.post('https://thiord.com/camera/upload.php', files={'image': fr})
    print(r)
    print(r.text)
# upload_image(); exit()

html_index = """Hello
"""

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return html_index

faces_welcomed = set()

@app.route("/", methods=["POST"])
def process_photo():
    global faces_welcomed
    # shutil.move("photo.jpg")
    filename = "photo.jpg"
    in_filename = request.files["userfile"].filename
    if in_filename.endswith(".jpg"):
        print(request.files["userfile"].save(filename))
        shutil.copy(filename, os.path.join(path_to_archive, in_filename))
        upload_image(filename)
        motion = motion_detector.observe(filename)

        faces = face_detection.test_face(filename, face_dict)
        print(">>>>>", faces)
        for name in faces:
            if name in faces_welcomed:
                continue
            faces_welcomed.add(name)
            try:
                play_sound(os.path.join(path_to_sound,
                                    name + ".wav"))
            except FileNotFoundError as e:
                print(e)
        
        print("motion =", motion)
        if not faces:
            if motion>15:
                play_sound(os.path.join(path_to_sound, "ой.wav"))
            else:
                faces_welcomed = set()
        # print(request.files.save(filename))
    return html_index

app.run(port=PORT, host=ADDR, debug=DEBUG)