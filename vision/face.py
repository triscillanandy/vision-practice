from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from face_reg import Recog
from student import Student
class Face_reg:
    def __init__(self, root,):
        self.app = None
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("face recognition")

        img = Image.open(r"blue.jpg")
        img = img.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)


        bg_img=Label(self.root,image=self.photoimg)
        bg_img.place(x=0, y=0, width=1530, height=900)

        title_lbl=Label(bg_img  ,text="Face Recogntion Attendace System Software",font=("times new roman",35,"bold"),bg="white",fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=110)
        #Student button
        img1= Image.open(r"student.jpg")
        img1 = img1.resize((220, 220),Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        b1 = Button(bg_img,image=self.photoimg1,command=self.student_details,cursor="hand2")
        b1.place(x=200, y=220, width=220, height=220)

        b1_1 = Button(bg_img, text="Student details",command=self.student_details,font=("times new roman", 15, "bold"), bg="white", fg="red")
        b1_1.place(x=201, y=400, width=220, height=40)
        #Detect face button
        img2 = Image.open(r"student.jpg")
        img2 = img2.resize((220, 220), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        b1 = Button(bg_img, image=self.photoimg2, cursor="hand2")
        b1.place(x=500, y=220, width=220, height=220)

        b1_1 = Button(bg_img, text="Face Detactor", font=("times new roman", 15, "bold"), bg="white", fg="red")
        b1_1.place(x=500, y=400, width=220, height=40)

      # Attendeace face button
        img3 = Image.open(r"student.jpg")
        img3 = img3.resize((220, 220), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        b1 = Button(bg_img, image=self.photoimg3, cursor="hand2",command=self.Recog_app)
        b1.place(x=800, y=220, width=220, height=220)

        b1_1 = Button(bg_img, text="Attendance details", command=self.Recog_app,font=("times new roman", 15, "bold"), bg="white", fg="red")
        b1_1.place(x=800, y=400, width=220, height=40)

        # Train  face button
        img4 = Image.open(r"student.jpg")
        img4 = img4.resize((220, 220), Image.Resampling.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1 = Button(bg_img, image=self.photoimg4, cursor="hand2")
        b1.place(x=200, y=500, width=220, height=220)

        b1_1 = Button(bg_img, text="Train data details", font=("times new roman", 15, "bold"), bg="white", fg="red")
        b1_1.place(x =200, y=700, width=220, height=40)







        # functions button

    def open_images(self):
        os.startfile("data")

    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def Recog_app(self):
        self.new_window=Toplevel(self.root)
        self.app=Recog(self.new_window)



if __name__ == "__main__":
    root = Tk()
    obj=Face_reg(root)
    root.mainloop()