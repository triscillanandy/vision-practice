from tkinter import *

from PIL import Image, ImageTk

from datetime import datetime

import sqlite3
import cv2



class Recog:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Student Management System")

        img = Image.open(r"blue.jpg")
        img = img.resize((1366, 128),
                         Image.Resampling.LANCZOS)  # resize and converting high level img to low level img.
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=1366, height=138)

        title_lbl = Label(f_lbl, text="Student Management System", font=("times new roman", 30, "bold"), bg="white",
                          fg="red")
        title_lbl.place(x=25, y=25, width=1300, height=90)

        # bg image.
        img2 = Image.open(r"blue.jpg")
        img2 = img2.resize((1366, 640),
                           Image.Resampling.LANCZOS)  # resize and converting high level img to low level img.
        self.photoimg2 = ImageTk.PhotoImage(img2)

        bg_img = Label(self.root, image=self.photoimg2)
        bg_img.place(x=0, y=130, width=1366, height=640)

        # main frame
        main_frame = Frame(bg_img)
        main_frame.place(x=25, y=0, width=1300, height=560)

        # bbuttons_frame
        btn_frame = Frame(main_frame, relief=RIDGE, bg="white")
        btn_frame.place(x=5, y=200, width=600, height=85)

        # delete button
        recognize_btn = Button(btn_frame, text="Recognize and take attendence", command=self.face_recog, width=27,
                            font=("times new roman", 12, "bold"), fg="white", bg="red")
        recognize_btn.grid(row=0, column=2, padx=2, pady=2, sticky=W)

        # =============Attendance===============

    def mark_attendance(self, i, r, n, d):
        with open("Attendance.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = []
            for line in myDataList:
                entry = line.split((","))
                name_list.append(entry[0])
            if ((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")

    # Face Recognization
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            # # Converting image to gray-scale
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # # detecting features in gray-scale image, returns coordinates, width and height of features
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord=[]

            for (x, y, w, h) in features:
                # drawing rectangle around the feature and labeling it
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                # # Predicting the id of the user
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                #is the confidence threshold, a scale that describes how certain a facial recognition system is that
                # a match it has produced is accurate.
                confidence = int((100 * (1 - predict / 300)))
                conn = sqlite3.connect('FR.db')
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT Name FROM Student where ID="+str(id))
                n = my_cursor.fetchone()


                my_cursor.execute("SELECT Roll FROM Student where ID="+str(id))
                r = my_cursor.fetchone()


                my_cursor.execute("SELECT Department FROM Student where ID="+str(id))
                d = my_cursor.fetchone()


                my_cursor.execute("SELECT ID FROM Student where ID="+str(id))
                i = my_cursor.fetchone()


                k=[i,r,n,d]



                if confidence > 77:
                    cv2.putText(img, f"ID:{str(k[0])}", (x, y - 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll:{str(k[1])}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name:{str(k[2])}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department:{str(k[3])}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendance(i,r,n, d)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coord = [x, y, w, h]

            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.yml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Welcome to Face Recognition", img)
            k = cv2.waitKey(30)
            if k == 27:
                break
        video_cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Recog(root)
    root.mainloop()
