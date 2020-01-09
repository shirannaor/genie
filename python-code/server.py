import eventlet
eventlet.monkey_patch()

import time
from threading import Thread
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import json
import face_recognition
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)
socket = SocketIO(app, cors_allowed_origins='*')

found_times = {}
frames_count_th = 5
persons_found = {}
time_th = 300

print('Initializing...')

known_face_encodings = np.load('encoding.npy', allow_pickle=False)
with open('names.json') as names:
    known_face_names = json.load(names)

def update_frames_count(person_id):
    if person_id not in persons_found:
        persons_found[person_id] = 1
    else:
        persons_found[person_id] += 1

def alert(person_id):
    name = 'Unknown' if person_id == -1 else known_face_names[person_id]
    socket.emit('newApprovedVisitor', name)
    print('{} located'.format(name))

def mark_as_found(person_id):
    if person_id not in found_times:
        found_times[person_id] = time.time()
        alert(person_id)
    else:
        found_time = found_times[person_id]
        if time.time() - found_time > time_th:
            alert(person_id)
        found_times[person_id] = time.time()

def update_results(results, result, frame_id):
    old_frame_results = results[frame_id]
    results[frame_id] = result
    for person_id in result:
        update_frames_count(person_id)
        if persons_found[person_id] >= frames_count_th:
            mark_as_found(person_id)

    for person_id in old_frame_results:
        persons_found[person_id] -= 1

def background_thread():
    video_capture = cv2.VideoCapture(0)

    frame_id = 0
    frames_memorized = 20
    results = [[]]*frames_memorized

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    scale = 2

    while True:
        time.sleep(1)

        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=1.0/scale, fy=1.0/scale)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            frame_results = set([])
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.52)
                name = ""

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    frame_results.add(best_match_index)
                else:
                    frame_results.add(-1)

                face_names.append(name)

            frame_id = (frame_id + 1) % frames_memorized
            update_results(results, frame_results, frame_id)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= scale
            right *= scale
            bottom *= scale
            left *= scale

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom), (right, bottom+35), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

thread = Thread(target=background_thread)
thread.daemon = True
thread.start()

@socket.on('connect')
def on_connect():
    print('user connected')

print('running server')
socket.run(app)