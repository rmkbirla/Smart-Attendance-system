import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle
import pandas as pd

path = 'images'

semester = int(input('Enter Semester: '))
branch = input("Enter Branch: ").upper()

images = []
classNames = []
mylist = os.listdir(path)
attendance_list = pd.read_excel(f'./Attendance_{semester}_{branch}.xlsx')
date = datetime.now().strftime('%d-%B-%Y')
attendance_list[date] = 'A'

for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])


def findEncodings(images):
    encodeList = []
    # count = 0
    for img in images:
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ef = face_recognition.face_encodings(img)
            if len(ef) > 0:
                encoded_face = ef[0]
            else:
                continue
            encodeList.append(encoded_face)
        # if count % 10 == 0:
        #     print(count)
        # count += 1
    return encodeList


encoded_face_train = findEncodings(images)


def markAttendance(name):
    # with open('Attendance.csv','r+') as f:
    #     attendanceList = [line.split(',')[0] for line in f]
    #     if name not in attendanceList:
    #         now = datetime.now()
    #         time = now.strftime('%I:%M:%S:%p')
    #         date = now.strftime('%d-%B-%Y')
    #         f.write(f'{name}, {time}, {date}\n')
    # print(name)
    attendance_list[date].loc[attendance_list['Name'] == name.upper()] = 'P'


# cap  = cv2.VideoCapture(0)
imgs = ['./1.jpg']
for i in imgs:
    img = cv2.imread(i)
    # success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(imgS)
    # print(faces_in_frame)
    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
    for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
        matchIndex = np.argmin(faceDist)
        # print(matchIndex)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper().lower()
            y1, x2, y2, x1 = faceloc
            # since we scaled down by 4 times
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
attendance_list.to_excel(f"./Attendance_{semester}_{branch}.xlsx", index=False)
