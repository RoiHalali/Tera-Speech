from opencvcoloredge import *
from face_landmark import *
from Data_Base import *
from tkinter import *
import tkinter as tk, threading
from Net import *
import glob
from PIL import ImageTk, Image
from scipy.io.wavfile import write
import time
import imageio
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import pandas as pd
import cv2
import multiprocessing as mp
import winsound
from googli import *
import os
from tkvideo import tkvideo
from threading import Thread


def btn_clicked():
    print("Button Clicked")

def show_frames(start,old_state,new_state,cap,label):

    date_time = datetime.now()
    df = []

    img = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)

    vert, hor = vertical_horizontal(img)
    # Get the latest frame and convert into Image
    if (vert and hor != None):
        new_state = face(vert, hor, "open_mouth")

    if new_state == "open" and old_state == "close":
        end = time.time()
        overall_time = end - start
        df.extend([date_time, 'open_mouth', vert, overall_time])
        #df = pd.Series(df, index=prog.columns)
        #prog = prog.append(df, ignore_index=True)
        #prog.to_csv(str(recipt) + '.csv', index=False)

        cv2.putText(img, "open mouth", (25, 100), 2, 1, (255, 255, 255))
        print(overall_time)
        old_state = "open"

    elif new_state == "close" and old_state == "open":
        overall_time = 0
        start = time.time()
        old_state = "close"

    # Get the latest frame and convert into Image
    image = Image.fromarray(img)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=image)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    # Repeat after an interval to capture continiously
    label.after(20, show_frames(start,old_state,new_state,cap,label))

def main(video_Label):


def show_motion(main_frame, motion,canvas, new_button, title, text, video_path, cap, vid_bg):
    # Pages setings:
    # open_mouth->smile
    if motion == "open_mouth":

        # delete the start button
        for idx, widget in enumerate(main_frame.winfo_children()):
            if isinstance(widget, Button) and idx == 3:
                widget.destroy()

        # Next page Definitions
        next_motion = "smile"
        next_text = "תרגול תנועת חיוך"
        next_video_path = "videos\smile.mp4"
        vid_bg = "videos\music_sub\introface.wav"
        new_button.configure(
            command=lambda: show_motion(main_frame, next_motion,canvas, new_button, title, next_text, next_video_path, cap,
                                        vid_bg))

    # smile->kiss
    if motion == "smile":
        # Next page Definitions
        next_motion = "kiss"
        next_text = "תרגול תנועת נשיקה"
        next_video_path = "videos\kiss.mp4"
        vid_bg = "videos\music_sub\introface.wav"
        new_button.configure(
            command=lambda: show_motion(main_frame, next_motion, new_button, title, next_text, next_video_path, cap,
                                        vid_bg))

    # kiss->tounge_down
    if motion == "kiss":
        # Next page Definitions
        next_motion = "tounge_down"
        next_text = "תרגול לשון למטה"
        next_video_path = "videos/tounge_down.mp4"
        vid_bg = "videos\music_sub\introface.wav"
        new_button.configure(
            command=lambda: show_motion(main_frame, next_motion, new_button, title, next_text, next_video_path, cap,
                                        vid_bg))

    # tounge_down->tounge_up
    if motion == "tounge_down":
        # Next page Definitions
        next_motion = "tounge_up"
        next_text = "תרגול לשון למעלה"
        next_video_path = "videos/tounge_up.mp4"
        vid_bg = "videos\music_sub\introface.wav"
        new_button.configure(
            command=lambda: show_motion(main_frame, next_motion, new_button, title, next_text, next_video_path, cap,
                                        vid_bg))

    # tounge_up->tounge_left
    if motion == "tounge_up":
        # Next page Definitions
        next_motion = "tounge_left"
        next_text = "תרגול לשון שמאלה"
        next_video_path = "videos/tounge_left.mp4"
        vid_bg = "videos\music_sub\introface.wav"
        new_button.configure(
            command=lambda: show_motion(main_frame, next_motion, new_button, title, next_text, next_video_path, cap,
                                        vid_bg))

    # tounge_left->tounge_right
    if motion == "tounge_left":
        # Next page Definitions
        next_motion = "tounge_right"
        next_text = "תרגול לשון ימינה"
        next_video_path = "videos/tounge_right.mp4"
        vid_bg = "videos\music_sub\introface.wav"
        new_button.configure(
            command=lambda: show_motion(main_frame, next_motion, new_button, title, next_text, next_video_path, cap,
                                        vid_bg))

    # tounge_right->finel
    if motion == "tounge_right":
        # Next page Definitions
        next_motion = "finel"
        next_text = "כל הכבוד! סיימת את התרגול בהצלחה"
        next_video_path = "videos\smile.mp4"
        vid_bg = "videos\music_sub\introface.wav"
        new_button.configure(
            command=lambda: show_motion(main_frame, next_motion, new_button, title, next_text, next_video_path, cap,
                                        vid_bg))

    # finel
    if motion == "finel":
        # Next page Definitions
        new_button.configure(command=lambda: (main_frame, username, recipt, user_id))

    sd.stop()  # stop the sound

    # Title
    canvas.itemconfig(title, text=text)

    # Explanation Video:
    # video lable
    video_Label = Label(main_frame)
    video_Label.place(
        x=524, y=87,
        width=428,
        height=354)

    player = tkvideo("videos/introface.mp4", video_Label, loop=1, size=(428, 354), hz=40)
    player.play()
    main(video_Label)
    # stream(video_Label, video_path)


    # Play video background sound
    data, fs = sf.read(vid_bg, dtype='float32')
    sd.play(data, fs)


    # Create a Label for camera video
    label = Label(main_frame)
    label.place(
        x=72, y=87,
        width=428,
        height=354)

    # Define function to show frame
    overall_time = 0
    reps = 0
    start = time.time()
    old_state = 'close'
    new_state = 'close'
    # prog = pd.read_csv(str(recipt) + '.csv')
    show_frames(start,old_state,new_state,cap,label)


    window.mainloop()
    cap.release()
    cv2.destroyAllWindows()


def face_motion_page(main_frame, username, recipt, user_id):

    main_frame.destroy()
    main_frame = Frame(window)
    main_frame.pack(fill=BOTH, expand=1)

    # Background:
    canvas = Canvas(
        main_frame,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)

    background_img = PhotoImage(file=f"background_face.png")
    background = canvas.create_image(
        491.0, 306.0,
        image=background_img)

    # Title
    title = canvas.create_text(
        490.5, 50.5,
        text="אימון תנועות פנים",
        fill="#00b2ff",
        font=("IstokWeb-Regular", int(30.0)))

    # Button- back to menu
    img0 = PhotoImage(file=f"back.png")
    b0 = Button(
        main_frame,
        image=img0,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:btn_clicked,
        relief="flat")

    b0.place(
        x=910, y=539,
        width=33,
        height=30)

    # Button- next
    img2 = PhotoImage(file=f"img2_face.png")
    b2 = Button(
        main_frame,
        image=img2,
        borderwidth=0,
        highlightthickness=0,
        command=btn_clicked,
        relief="flat")

    b2.place(
        x=346, y=454,
        width=111,
        height=37)

    # Capture web camera video
    cap = cv2.VideoCapture(0)
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(1)

    # Button- start
    img1 = PhotoImage(file=f"img1_face.png")
    b1 = Button(
        main_frame,
        image=img1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_motion(main_frame, "mouth_open",canvas, b2, title, "אימון פתיחת פה", "videos/open_mouth.mp4", cap,
                                    "videos/music_sub/introface.wav"))

    b1.place(
        x=200, y=454,
        width=111,
        height=37)

    # right rectangle
    canvas.create_rectangle(
        524, 87, 524 + 428, 87 + 354,
        fill="#e8e8ef",
        outline="")

    # left rectangle
    canvas.create_rectangle(
        72, 87, 72 + 428, 87 + 354,
        fill="#e8e8ef",
        outline="")

    # Intro Text
    im = cv2.imread("face_motion_introtext.png")
    im = cv2.resize(im, (428, 354))

    img3 = PhotoImage(file=f"face_motion_introtext.png")

    b3 = Label(
        main_frame,
        image=img3,
        borderwidth=0,
        highlightthickness=0,
        relief="flat")

    b3.place(
        x=72, y=87,
        width=428,
        height=354)

    # cap_vid = cv2.VideoCapture("videos/introface.mp4")
    show_motion(main_frame, None,canvas, b2, title, "אימון הבעות הפנים", "videos/introface.mp4", cap, "videos/music_sub/introface.wav")

    # window.protocol("WM_DELETE_WINDOW", lambda:on_closing(user_id, recipt))
    window.resizable(False, False)
    window.mainloop()

if __name__==  "__main__":
    # Window setings:
    window = Tk()  # window on the system
    window.geometry("1000x600")  # window shape
    window.configure(bg="#ffffff")  # Query or set the default value of the specified option(s) in style.
    window.title("Tera-Speech")  # window title
    window.iconbitmap('person.ico')  # window iconframe=Frame(window)

    # Create A Main Frame
    main_frame = Frame(window)
    main_frame.pack(fill=BOTH, expand=1)

    face_motion_page(main_frame, "רועי הללי", 123, 123)

























# def elegir_visualizar_video():
#     global cap
#     if cap is not None:
#         lblVideo.image = ""
#         cap.release()
#         cap = None
#     video_path = filedialog.askopenfilename(filetypes = [
#         ("all video format", ".mp4"),
#         ("all video format", ".avi")])
   
#     if len(video_path) > 0:
#         lblInfoVideoPath.configure(text=video_path)
#         cap = cv2.VideoCapture(video_path)
#         visualizar()
#     else:
#         lblInfoVideoPath.configure(text="Aún no se ha seleccionado un video")

# def visualizar():
#     global cap
#     if cap is not None:
#         ret, frame = cap.read()
#         if ret == True:
#                 # Sound player
#             # filename = 'videos\music_subed\introface.wav'
#             # data, fs = sf.read(filename, dtype='float32')  
#             # sd.play(data, fs)
#             frame = imutils.resize(frame, width=640)
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             im = Image.fromarray(frame)
#             img = ImageTk.PhotoImage(image=im)
#             lblVideo.configure(image=img)
#             lblVideo.image = img
#             lblVideo.after(25, visualizar)
#         else:
#             lblVideo.image = ""
#             cap.release()
            
# def finalizar():
#     global cap
#     cap.release()
    
# cap = None
# root = Tk()
# btnVisualizar = Button(root, text="Elegir y visualizar video", command=elegir_visualizar_video)
# btnVisualizar.grid(column=0, row=0, padx=5, pady=5, columnspan=2)

# lblInfo1 = Label(root, text="Video de entrada:")
# lblInfo1.grid(column=0, row=1)
# lblInfoVideoPath = Label(root, text="Aún no se ha seleccionado un video")
# lblInfoVideoPath.grid(column=1, row=1)

# lblVideo = Label(root)
# lblVideo.grid(column=0, row=2, columnspan=2)
# root.mainloop()