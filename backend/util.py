import cv2
from mtcnn.mtcnn import MTCNN
import numpy as np
from face_pose import predict_gaze
from eye_pose import get_eye_frame, get_eye_pose
import dlib
import matplotlib.pyplot as plt
import cv2

detector = MTCNN()
INTERVAL = 3

def distance(p1,p2):
    assert len(p1) == len(p2), "Dimension of points are not equal"
    return sum([(p1_i- p2_i)** 2 for p1_i,p2_i in zip(p1,p2)]) ** 0.5

def get_attention(frame,face):
    nose = np.array(face["keypoints"]["nose"])
    x,y,w,h = face["box"]
    centroid = np.array((frame.shape[1] // 2,frame.shape[0] // 2))
    centroid_face = np.array((x + w //2, y + h//2))
    nose_distance = distance(centroid_face,centroid)
    nose_face_distance = distance(nose,centroid_face)

    nose_face_score = (1 - (nose_face_distance / distance((x,y),centroid_face)))
    nose_frame_score = (1 - (nose_distance / distance((0,0),centroid)))
    score = min(nose_frame_score,nose_face_score)

    return score

def extract_attention(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(frame_rgb)
    if len(faces) == 0:
        return 0
    box_sizes = [face["box"][2] * face["box"][3] for face in faces]
    top_index = list(sorted(enumerate(box_sizes),key=lambda el : -el[1]))[0][0]
    face = faces[top_index]
    return get_attention(frame,face)



def extract_attention_video(video_path):
    numbers = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    counter = 0
    while cap.isOpened():
        ret,frame = cap.read()
        if ret:
            attention_score = extract_attention(frame) 
            numbers.append(attention_score)
            print(f"yo {counter} {attention_score*100:.3f}")

        else:
            break

        cap.set(cv2.CAP_PROP_POS_MSEC,INTERVAL * 1000 * counter)
        counter += 1
    
    cap.release()
    return numbers
