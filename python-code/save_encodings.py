import face_recognition
import numpy as np
import os
import json

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
# Load a sample picture and learn how to recognize it.
#
# obama_image = face_recognition.load_image_file("test.png")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
# biden_image = face_recognition.load_image_file("biden.jpg")
# biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
]
known_face_names = [
]

images_dir = 'images'
files = os.listdir(images_dir)
for filename in files:
    image = face_recognition.load_image_file(images_dir+'/'+filename)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(filename.split('.')[0])

np.save('encoding.npy', np.asmatrix(known_face_encodings), allow_pickle=False)
with open('names.json', 'w') as names:
    json.dump(known_face_names, names)

#
# # Initialize some variables
# face_locations = []
# face_encodings = []
# face_names = []
# process_this_frame = True
# scale = 2
#
# print('Initialization complete')
