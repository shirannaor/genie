import face_recognition
import cv2
import numpy as np
import os
import time

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

print('Initializing...')

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("test.png")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
# biden_image = face_recognition.load_image_file("biden.jpg")
# biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding
]
known_face_names = [
    "Barack Obama"
]

images_dir = '/home/nvidia/Desktop/images'
files = os.listdir(images_dir)
for filename in files:
    image = face_recognition.load_image_file(images_dir+'/'+filename)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(filename.split('.')[0])

frame_id = 0
frames_memorized = 20
frames_count_th = 5
persons_found = {}
found_times = {}
time_th = 300
results = [[]]*frames_memorized

def update_frames_count(person_id):
    if person_id not in persons_found:
        persons_found[person_id] = 1
    else:
        persons_found[person_id] += 1


def alert(person_id):
    name = 'Unknown' if person_id == -1 else known_face_names[person_id]
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

def update_results(result, frame_id):
    old_frame_results = results[frame_id]
    results[frame_id] = result
    for person_id in result:
        update_frames_count(person_id)
        if persons_found[person_id] >= frames_count_th:
            mark_as_found(person_id)

    for person_id in old_frame_results:
        persons_found[person_id] -= 1

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
scale = 2

print('Initialization complete')

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1.0/scale, fy=1.0/scale)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
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
        update_results(frame_results, frame_id)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
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

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()