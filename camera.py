import cv2
import tkinter as tk
from tkinter import filedialog#文件控件
from PIL import Image, ImageTk#图像控件
import threading#多线程

#---------------创建窗口
window = tk.Tk()
window.title('摄像头')
sw = window.winfo_screenwidth()#获取屏幕宽
sh = window.winfo_screenheight()#获取屏幕高
wx = 600
wh = 800
window.geometry("%dx%d+%d+%d" %(wx,wh,(sw-wx)/2,(sh-wh)/2-100))#窗口至指定位置
canvas = tk.Canvas(window,bg='#c4c2c2',height=wh,width=wx)#绘制画布
canvas.pack()

#---------------打开摄像头获取图片
def video_demo():
    def cc():
        capture = cv2.VideoCapture(0)
        while True:
            ret, frame = capture.read()#从摄像头读取照片
            frame = cv2.flip(frame, 1)#翻转 0:上下颠倒 大于0水平颠倒
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            image_file=ImageTk.PhotoImage(img)
            canvas.create_image(0,0,anchor='nw',image=image_file)
    t=threading.Thread(target=cc)
    t.start()

bt_start = tk.Button(window,text='打开摄像头',height=2,width=15,command=video_demo)
bt_start.place(x=230,y=600)
