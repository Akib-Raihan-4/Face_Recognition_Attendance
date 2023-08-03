import tkinter as tk
import cv2
import face_recognition
import pickle
from datetime import datetime
import csv
from PIL import Image, ImageTk
import os
import numpy as np

def load_known_encodings(load_file):
    with open(load_file, "rb") as file:
        data = pickle.load(file)
    return data

def markAttendance(name, date):
    file_name = f'Attendance_Folder/Attendance_{date}.csv'
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Timestamp'])

    with open(file_name, 'r+') as f:
        myDataList = f.readlines()
        nameList = []

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
def marked_faces(name, date):
    current_date = datetime.now().strftime('%Y-%m-%d')

    file_name = f'Attendance_Folder/Attendance_{current_date}.csv'

    if not os.path.exists(file_name):
        return "Not Marked"

    else:
        with open(file_name, 'r+') as f:
            myDataList = f.readlines()
            nameList = []

            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])

            if name not in nameList:
                return "Not Marked"
            else:
                return "Marked"
def recognize_faces():
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 1, 1)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 , x2 , y2 , x1 

            current_date = datetime.now().strftime('%Y-%m-%d')

            marked = marked_faces(name,current_date)

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0),2)
            cv2.putText(img, marked, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 2, (245, 123, 26), 2)
            
            markAttendance(name, current_date)
            
            print(name)

    imgtk = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(imgtk))
    label_video.imgtk = imgtk
    label_video.configure(image=imgtk)
    label_video.after(10, recognize_faces)

def start_attendance():
    global cap,img
    cap = cv2.VideoCapture(0)
    recognize_faces()

def stop_attendance():
    # global cap
    # if cap is not None:
    #     cap.release()
    app.quit()

classNames_file = "classNames.pkl"
encodeListKnown_file = "encodeListKnown.pkl"

classNames = load_known_encodings(classNames_file)
encodeListKnown = load_known_encodings(encodeListKnown_file)

app = tk.Tk()
app.title("Face Recognition Attendance App")

label_video = tk.Label(app)
label_video.pack()

button_start = tk.Button(app, text="Start Attendance", command=start_attendance)
button_start.pack()

button_stop = tk.Button(app, text="Stop Attendance", command=stop_attendance)
button_stop.pack()

app.mainloop()
