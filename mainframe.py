from tkinter import *
import cv2
from PIL import ImageTk, Image
import imutils
from biometric_register import BiometricRegister
from biometric_login import BiometricLogin
from database_handler import *
import re
import os


class Mainframe(Tk):
    def __init__(self):
        super().__init__()
        # Main screen config
        self.title('Face Recognition')
        self.geometry('1366x768')

        # Load images
        self.img_background = PhotoImage(file='./media/background_768.png')
        self.img_background_e = PhotoImage(file='./media/background_720_empty.png')
        self.img_face_rec_signup = PhotoImage(file='./media/button.png')
        self.img_send_button = PhotoImage(file='./media/send_button.png')
        self.img_face_rec_button = PhotoImage(file='./media/face_rec_button.png')

        # Load labels
        self.label_background = Label(self, image=self.img_background)

        # Load inputs
        self.sign_up_name = Entry(self)
        self.sign_up_user = Entry(self)
        self.sign_up_pass = Entry(self, show='*')
        self.sign_in_user = Entry(self)
        self.sign_in_pass = Entry(self, show='*')

        # Load buttons
        self.button_send_up = Button(self, image=self.img_send_button)
        self.button_send_in = Button(self, image=self.img_send_button)
        self.button_send_face = Button(self, image=self.img_face_rec_button)
        self.button_new_face = Button(self, image=self.img_face_rec_signup)

        # Widget attributes
        self.config_widgets()

        # Widget position
        self.place_widgets()

    def config_widgets(self):
        for widget in self.winfo_children():
            widget['borderwidth'] = 0
            widget['border'] = 0

            if isinstance(widget, Entry):
                widget['bg'] = '#292929'
                widget['fg'] = 'lightgrey'
                widget['highlightbackground'] = 'black'

            if isinstance(widget, Button):
                widget['bg'] = 'black'
                widget['highlightthickness'] = 0
                widget['activeforeground'] = 'grey'
                widget['activebackground'] = 'black'

        self.button_new_face.configure(text='Begin', fg='white', compound='center')

        # Input command when 'ENTER' is pressed
        self.sign_up_pass.bind('<Return>', lambda x: self.send_signup())
        self.sign_in_pass.bind('<Return>', lambda x: self.send_signin())

        # Buttons command
        self.button_send_up['command'] = self.send_signup
        self.button_send_in['command'] = self.send_signin
        self.button_send_face['command'] = self.face_login
        self.button_new_face['command'] = self.face_register

    def place_widgets(self):
        # Background
        self.label_background.place(x=0, y=0, relheight=1, relwidth=1)

        # Sign up
        self.sign_up_name.place(x=397, y=248)
        self.sign_up_user.place(x=397, y=288)
        self.sign_up_pass.place(x=397, y=328)
        self.button_send_up.place(x=303, y=448)
        self.button_new_face.place(x=423, y=360)

        # Sign in
        self.sign_in_user.place(x=1050, y=288)
        self.sign_in_pass.place(x=1050, y=328)
        self.button_send_in.place(x=802, y=448)
        self.button_send_face.place(x=1011, y=436)

    def send_signup(self):
        name = self.sign_up_name.get()
        user = self.sign_up_user.get()
        password = self.sign_up_pass.get()

        if not name or not user or not password:
            mb.showerror('Error', 'Missing one or more fields')
            return

        if len(name) < 4:
            mb.showerror('Error', 'Name must be at least four characters long')
            return

        if len(user) < 4:
            mb.showerror('Error', 'Username must be at least four characters long')
            return

        if len(password) < 6:
            mb.showerror('Error', 'Password must be at least six characters long')
            return

        if not re.search(r'[A-Z]+', password):
            mb.showerror('Error', 'Password must have at least one capital letter')
            return

        if not re.search(r'\d+', password):
            mb.showerror('Error', 'Password must have at least one number')
            return

        if self.button_new_face['state'] != 'disabled':
            if not mb.askyesno('Warning', 'Are you sure you want to continue without biometric information?'):
                return

        # User creation with SQLite3 custom function
        if new_user(name=name, user=user, pas=password):
            # Empty Entries
            self.sign_up_name.delete(0, END)
            self.sign_up_user.delete(0, END)
            self.sign_up_pass.delete(0, END)

            return mb.showinfo('Success', 'User created successfully')

    def send_signin(self):
        user = self.sign_in_user.get()
        password = self.sign_in_pass.get()

        credentials = fetch_user(user, password)

        # If user exists, change the main window
        if credentials:
            self.change_background()
            self.show_user_info(credentials)

        else:
            mb.showerror('Not found', 'User not found')

    def change_background(self):
        self.label_background['image'] = self.img_background_e
        self.geometry('1280x720')

        # Destroy everything except background and images
        for widget in self.winfo_children():
            if isinstance(widget, Label) or isinstance(widget, PhotoImage):
                continue

            widget.destroy()

    def show_user_info(self, credentials: tuple):
        id = f'ID:\t{credentials[0]}'
        name = f'Name:\t{credentials[1]}'
        user = f'User:\t{credentials[2]}'

        path_face_img = f'{credentials[0]}.png'

        if path_face_img in os.listdir('./database/faces'):
            img = cv2.imread(f'./database/faces/{path_face_img}')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = imutils.resize(img, width=150)
            img = Image.fromarray(img)

            self.img_face = ImageTk.PhotoImage(image=img)
            label_face = Label(self, image=self.img_face)
            label_face.place(x=600, y=180)

        label_welcome = Label(self, text='Welcome!', fg='white', bg='black')
        label_id = Label(self, text=id, fg='white', bg='black')
        label_name = Label(self, text=name, fg='white', bg='black')
        label_user = Label(self, text=user, fg='white', bg='black')

        label_welcome.place(x=427, y=210)
        label_id.place(x=427, y=240)
        label_name.place(x=427, y=270)
        label_user.place(x=427, y=300)

    def face_login(self):
        face_rec_frame = BiometricLogin(self)

        face_rec_frame.biometric_log()

        id = face_rec_frame.id

        if not id:
            mb.showerror('Not found', 'This user doesn\'t have biometric information')
            return

        credentials = fetch_user_id(id)

        if credentials:
            self.change_background()
            self.show_user_info(credentials)

        else:
            mb.showerror('Not found', 'User not found')

    def face_register(self):
        face_rec_frame = BiometricRegister(self)

        face_rec_frame.biometric_log()
