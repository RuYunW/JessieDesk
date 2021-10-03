import tkinter as tk
import cv2
from PIL import Image, ImageTk  #图像控件
import numpy as np
import random

xmlfile_eye = 'haarcascade_eye.xml'
xmlfile_face = 'haarcascade_frontalface_default.xml'
eye_cascade = cv2.CascadeClassifier(xmlfile_eye)
face_cascade = cv2.CascadeClassifier(xmlfile_face)

window  = tk.Tk()
window.minsize(500, 500)
window.title('看与被看的艺术')

canvas = tk.Canvas(window, width=500, height=500)
canvas.pack()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
success, frame = cap.read()
# print(frame.shape)
# # exit()
# print(type(frame))  # <class 'numpy.ndarray'>
# print(frame)
# exit()
counter = 10
flag = 1
while(success):
    counter -= 1
    if counter == 0:
        flag += 1
        counter = 10

    eye_list = []
    success, frame = cap.read()
    # 检测人眼
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.15, minNeighbors=3, minSize=(50, 50), maxSize=(200, 200))
    if len(faces) > 0:  # 如果检测到人脸
        for (fx, fy, fw, fh) in faces:
            face_pic = frame[fy:fy+fh, fx:fx+fw]
            eyes = eye_cascade.detectMultiScale(face_pic, scaleFactor=1.15, minNeighbors=3, minSize=(50, 50), maxSize=(300, 300))
            if len(eyes) > 0:  # 如果检测到眼睛
                for (ex, ey, ew, eh) in eyes:
                    eye_list.append(cv2.resize(frame[fy+ey:fy+ey+eh, fx+ex:fx+ex+ew], (50, 50)))



    if flag == 1:  # 拓扑
        eye_pic = np.full((50, 100), 255, dtype=np.uint8)
        if len(eye_list) == 1:
            eye_pic = np.concatenate((eye_list[0], eye_list[0]), axis=1)
        elif len(eye_list) >= 2:  # 只要前两个
            eye_pic = np.concatenate((eye_list[0], eye_list[1]), axis=1)
        e4 = np.concatenate((eye_pic, eye_pic), axis=0)
        for i in range(3):
            new_frame = np.concatenate(((np.concatenate((e4, e4), axis = 1),(np.concatenate((e4, e4), axis = 1)))))
            e4 = new_frame

    elif flag == 2:  # 错位拓扑
        eye_pic = np.full((100, 100, 3), 255, dtype=np.uint8)
        if len(eye_list) == 0:
            pass
            # new_frame = np.full((100, 100, 3), 255, dtype=np.uint8)
        elif len(eye_list) == 1:
            # eye_pic = eye_list[0]
            eye_pic_1 = eye_list[0]
            eye_pic_2 = eye_list[0]
            eye_pic[0:25, 0:50] = eye_pic_1[25:50, :]
            eye_pic[25:75, 0:50] = eye_pic_1
            eye_pic[75:, 0:50] = eye_pic_1[0:25, :]
            eye_pic[0:50, 50:] = eye_pic_2
            eye_pic[50:, 50:] = eye_pic_2
        elif len(eye_list) >= 2:
            eye_pic_1 = eye_list[0]
            eye_pic_2 = eye_list[1]
            eye_pic[0:25, 0:50] = eye_pic_1[25:50, :]
            eye_pic[25:75, 0:50] = eye_pic_1
            eye_pic[75:, 0:50] = eye_pic_1[0:25, :]
            eye_pic[0:50, 50:] = eye_pic_2
            eye_pic[50:, 50:] = eye_pic_2
        for i in range(3):
            new_frame = np.concatenate(((np.concatenate((eye_pic, eye_pic), axis = 1),(np.concatenate((eye_pic, eye_pic), axis = 1)))))
            eye_pic = new_frame
    elif flag == 3:
        eye_pic = np.full((50, 50, 3), 255, dtype=np.uint8)
        if len(eye_list) == 0:
            pass
        elif len(eye_list) == 1:
            eye_pic_1 = eye_list[0]
            eye_pic_2 = eye_list[0]
            eye_pic[0:25, 0:25] = eye_pic_1[0:25, 0:25]
            eye_pic[0:25, 25:] = eye_pic_2[0:25, 25:]
            eye_pic[25:, 0:25] = eye_pic_2[25:, 0:25]
            eye_pic[25:, 25:] = eye_pic_1[25:, 25:]
        elif len(eye_list) >= 2:
            eye_pic_1 = eye_list[0]
            eye_pic_2 = eye_list[1]
            eye_pic[0:25, 0:25] = eye_pic_1[0:25, 0:25]
            eye_pic[0:25, 25:] = eye_pic_2[0:25, 25:]
            eye_pic[25:, 0:25] = eye_pic_2[25:, 0:25]
            eye_pic[25:, 25:] = eye_pic_1[25:, 25:]
        for i in range(4):
            new_frame = np.concatenate(((np.concatenate((eye_pic, eye_pic), axis = 1),(np.concatenate((eye_pic, eye_pic), axis = 1)))))
            eye_pic = new_frame
    else:
        flag = 1



    # new_frame = eye_pic
    # mouth_xyz.append(eclosion(
    #     cv2.resize(ori_frame[int(y + h * 0.4 + my):int(y + h * 0.4 + my + mh), x + mx:x + mx + mw],
    #                (2 * window_size, window_size), interpolation=cv2.INTER_AREA), top=int(window_size / 4),
    #     bottom=int(window_size / 4), left=int(window_size / 2), right=int(window_size / 2)))

    # white_matrix = np.full(frame.shape, 255, dtype=np.uint8)


    # new_frame = frame * zero_matrix

    cov = cv2.cvtColor(new_frame, cv2.COLOR_RGB2BGR)  # 初始图像是RGB格式，转换成BGR即可正常显示了
    img = Image.fromarray(cov)
    img = ImageTk.PhotoImage(img)

    canvas.create_image(0, 0, anchor='nw', image=img)
    window.update_idletasks()
    window.update()


