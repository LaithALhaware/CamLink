import tkinter as tk
from tkinter import Entry, messagebox, Toplevel
import webbrowser
import os
import time
import cv2
from imutils.video import VideoStream
from PIL import Image, ImageTk

# إعداد النافذة الرئيسية
root = tk.Tk()
root.title('CamLink')
root.configure(bg='white')
root.geometry('800x600')
root.resizable(False, False)

# أيقونة البرنامج
icon_image = tk.PhotoImage(file='data/Img/icon.png')
root.iconphoto(True, icon_image)

# شعار البرنامج
logo = tk.PhotoImage(file='data/Img/Main-Logo.png')
tk.Label(root, image=logo, bg='white').pack(pady=20)

# عنوان البرنامج
tk.Label(root, text='CamLink', bg='white', font=('Times New Roman', 18, 'bold')).pack(pady=5)
tk.Label(root, text='Please Add Information of the Camera', bg='white', font=('Helvetica', 14)).pack(pady=10)

# إنشاء حقل إدخال
frame = tk.Frame(root, bg='white')
frame.pack(pady=10)

def create_labeled_entry(parent, text, is_password=False):
    container = tk.Frame(parent, bg='white')
    container.pack(fill='x', pady=5)
    tk.Label(container, text=text, bg='white', font=('Helvetica', 10)).pack(side='left', padx=10)
    entry = Entry(container, font=('Helvetica', 10), bd=2, relief='solid', bg='white', width=25)
    if is_password:
        entry.config(show='*')
    entry.pack(side='right', padx=10)
    return entry

# حقول الإدخال
Address = create_labeled_entry(frame, 'IP Address :')
User = create_labeled_entry(frame, 'User Name :')
Password = create_labeled_entry(frame, 'Password :', is_password=True)
PORT = create_labeled_entry(frame, 'PORT (554) :')

vs = None  # متغير لتخزين كائن VideoStream

def start_camera_feed():
    global vs
    rtsp_url = f"rtsp://{User.get()}:{Password.get()}@{Address.get()}:{PORT.get()}/stream"
    camera_window = Toplevel(root)
    camera_window.title('Live Camera Feed')
    camera_window.geometry('800x600')
    video_label = tk.Label(camera_window, bg='black')
    video_label.pack(pady=10, expand=True)
    vs = VideoStream(src=rtsp_url).start()
    time.sleep(2.0)
    update_frame(video_label)

def update_frame(video_label):
    global vs
    frame = vs.read()
    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.imgtk = img
        video_label.configure(image=img)
    video_label.after(10, update_frame, video_label)

def open_github():
    webbrowser.open('https://github.com/LaithAlHaware')

def open_license_file():
    try:
        with open('LICENSE.txt', 'r') as file:
            messagebox.showinfo("LICENSE.txt", file.read())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {e}")

# أزرار التحكم
button_frame = tk.Frame(root, bg='white')
button_frame.pack(pady=20)

button1 = tk.Button(button_frame, text='Connect', command=start_camera_feed, bg='#007BFF', fg='white', font=('helvetica', 10, 'bold'), padx=10, pady=5, borderwidth=0, cursor='hand2')
button1.pack(side='left', padx=5, pady=5)

if os.path.exists('LICENSE.txt'):
    open_license_button = tk.Button(button_frame, text='LICENSE', command=open_license_file, bg='#f4d03f', fg='white', font=('helvetica', 10, 'bold'), padx=10, pady=5, borderwidth=0, cursor='hand2')
    open_license_button.pack(side='left', padx=5, pady=5)

tk.Button(button_frame, text='Go to GitHub Profile', command=open_github, bg='#28A745', fg='white', font=('helvetica', 10, 'bold'), padx=10, pady=5, borderwidth=0, cursor='hand2').pack(side='left', padx=5, pady=5)

# تشغيل التطبيق
root.mainloop()