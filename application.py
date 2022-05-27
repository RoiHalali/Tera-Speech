import tkinter as tk
import pandas as pd
from PIL import ImageTk, Image
from face_landmark import face
from opencvcoloredge import tounge
import cv2
### sound libraries
import sounddevice as sd
import speech_recognition as sr 
import playsound
import os # to save/open files 
import winsound
from gtts import gTTS # google text to speech 
from scipy.io.wavfile import write
import wavio as wv


 

def login():
    
    ############# Create sign in screen #############
    # Create a new window with the title "Address Entry Form"
    window = tk.Tk()
    # window.geometry("300x300")
    window.title("כניסה")
    window.iconbitmap('person.ico')
    # Create a new frame `frm_form` to contain the Label
    # and Entry widgets for entering address information.
    frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
    # Pack the frame into the window
    frm_form.pack()
    
    # List of field labels
    labels = [
            "מייל:",     
            "סיסמא:",     
    ]
    
    # Loop over the list of field labels
    for idx, text in enumerate(labels):
        # Create a Label widget with the text from the labels list
        label = tk.Label(master=frm_form, text=text)
        # Create an Entry widget
        entry = tk.Entry(master=frm_form, width=50)
        # Use the grid geometry manager to place the Label and
        # Entry widgets in the row whose index is idx
        label.grid(row=idx, column=0, sticky="e")
        entry.grid(row=idx, column=1)
    
    # Create a new frame `frm_buttons` to contain the
    # Submit and Clear buttons. This frame fills the
    # whole window in the horizontal direction and has
    # 5 pixels of horizontal and vertical padding.
    frm_buttons = tk.Frame()
    frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
    
    # Create the "Submit" button and pack it to the
    # right side of `frm_buttons`
    btn_submit = tk.Button(window, text="התחברות", command=lambda: check_fields(x,frm_form,window))
    btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)
    
    # Create the "Clear" button and pack it to the
    # right side of `frm_buttons`
    btn_clear = tk.Button(window, text="הרשמה", command=lambda: register(window))
    btn_clear.pack(side=tk.RIGHT, ipadx=10)
    
    # Start the application
    window.mainloop()
    
def register(window_close):
    window_close.destroy()
    window = tk.Tk()
    # window.geometry("300x300")
    window.title("הרשמה")
    window.iconbitmap('person.ico')

    # Create a new frame `frm_form` to contain the Label
    # and Entry widgets for entering address information.
    frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
    # Pack the frame into the window
    frm_form.pack()
    
    # List of field labels
    labels = [
       "מייל:",     
     "סיסמא:",     
            "שם פרטי:",     
            "שם משפחה:",     
            "כתובת:",     
            "עיר:",     
            "מיקוד:",     
    ]
    
    # Loop over the list of field labels
    for idx, text in enumerate(labels):
        # Create a Label widget with the text from the labels list
        label = tk.Label(master=frm_form, text=text)
        # Create an Entry widget
        entry = tk.Entry(master=frm_form, width=50)
        # Use the grid geometry manager to place the Label and
        # Entry widgets in the row whose index is idx
        label.grid(row=idx, column=0, sticky="e")
        entry.grid(row=idx, column=1)
    
    # Create a new frame `frm_buttons` to contain the
    # Submit and Clear buttons. This frame fills the
    # whole window in the horizontal direction and has
    # 5 pixels of horizontal and vertical padding.
    frm_buttons = tk.Frame()
    frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
    
    # Create the "Submit" button and pack it to the
    # right side of `frm_buttons`
    btn_submit = tk.Button(window, text="אישור", command=lambda: save_fields(x,frm_form,window))
    btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)
    
    # Create the "Clear" button and pack it to the
    # right side of `frm_buttons`
    btn_clear = tk.Button(window, text="ניקוי", command=lambda: clear_fields(frm_form))
    btn_clear.pack(side=tk.RIGHT, ipadx=10)
    
    # Start the application
    window.mainloop()    

def save_fields(x,frm_form,window):
    global y
    df2 = []
    for idx, widget in enumerate(frm_form.winfo_children()):
        if isinstance(widget, tk.Entry):
            df2.append(widget.get())
    df2 = pd.Series(df2, index = x.columns)
    x = x.append(df2, ignore_index=True)
    y=x
    # check_fields()
    window.destroy()    
    
def clear_fields(frm_form):
    [widget.delete(0, tk.END) for widget in frm_form.winfo_children() if isinstance(widget, tk.Entry)]  

    
def check_fields(x, frm_form, window):
    Flag = True
    for idx, widget in enumerate(frm_form.winfo_children()):
        if isinstance(widget, tk.Entry):
            if widget.get() not in x.values:
                Flag = False
    if Flag is True:
        label = tk.Label(master=frm_form, text='Welcome')
        label.grid(row=2, column=0, sticky="e")
        # dkdwindow.destroy()
    else: 
        label = tk.Label(master=frm_form, text='user or email is invalid')
        label.grid(row=2, column=0, sticky="e")
        
def face_motion():
    # Create an instance of TKinter Window or frame
    win = tk.Tk()
    win.title("תנועות פנים")
    win.iconbitmap('person.ico')
    
    # Create a Label to capture the Video frames
    label = tk.Label(win)
    label.grid(row=0, column=0)
    cap= cv2.VideoCapture(0)
    
    # Define function to show frame
    def show_frames1():
       # Get the latest frame and convert into Image
       cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
       img_face = face(cv2image)
       img = Image.fromarray(img_face)
       # Convert image to PhotoImage
       imgtk = ImageTk.PhotoImage(image = img)
       label.imgtk = imgtk
       label.configure(image=imgtk)
       # Repeat after an interval to capture continiously
       label.after(20, show_frames1)
    
    show_frames1()
    win.mainloop()
    cap.release()
    cv2.destroyAllWindows() 
    
def tounge_motion():
    # Create an instance of TKinter Window or frame
    win = tk.Tk()
    win.title("תנועות לשון")
    win.iconbitmap('person.ico')
    
    # Create a Label to capture the Video frames
    label = tk.Label(win)
    label.grid(row=0, column=0)
    cap= cv2.VideoCapture(0)
    
    # Define function to show frame
    def show_frames2():
       # Get the latest frame and convert into Image
       cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
       img_face = tounge(cv2image)
       img = Image.fromarray(img_face)
       # Convert image to PhotoImage
       imgtk = ImageTk.PhotoImage(image = img)
       label.imgtk = imgtk
       label.configure(image=imgtk)
       # Repeat after an interval to capture continiously
       label.after(20, show_frames2)
       
    
    show_frames2()
    win.mainloop()
    cap.release()
    cv2.destroyAllWindows() 
    
def get_audio(win): 
    # Sampling frequency
    freq = 16600
      
    # Recording duration
    duration = 3
    
    label = tk.Label(master = win, text  ='Speak Now...')
    label.grid(row=2, column=0, sticky="e")
    # winsound.Beep(1000,500)
    
    # Start recorder with the given values 
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq), 
                       samplerate=freq, channels=2)
      
    # Record audio for the given number of seconds
    # sd.wait()
      
    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    # write("recording0.wav", freq, recording)
    i = 1
    # Convert the NumPy array to audio file
    wv.write('recording-' + str(i) + '.wav', recording, freq, sampwidth=2)
    
    return recording
        
    
def sound():
    # Create an instance of TKinter Window or frame
    win = tk.Tk()
    win.title("זיהוי סאונד")
    win.iconbitmap('person.ico')
    
    # Create a Label to capture the Video frames
    label = tk.Label(win)
    label.grid(row=0, column=0)
    cap= cv2.VideoCapture(0)
    i = 0
    
    # Define function to show frame
    def show_frames2():
       # Get the latest frame and convert into Image
       cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
       img = Image.fromarray(cv2image)
       # Convert image to PhotoImage
       imgtk = ImageTk.PhotoImage(image = img)
       label.imgtk = imgtk
       label.configure(image=imgtk)

       audio = get_audio(win)

       # Repeat after an interval to capture continiously
       label.after(20, show_frames2)
    
    show_frames2()
    win.mainloop()
    cap.release()
    cv2.destroyAllWindows() 
    
# data=[('dkd@hotmail.com','password','Dor', 'Kershberg', 'Pinkas 9', 'qiryat ono',55060)]
x = pd.DataFrame(columns=['mail','password','first', 'last', 'adress', 'city', 'zipcode'])
# login()
# face_motion()
# tounge_motion()
sound()