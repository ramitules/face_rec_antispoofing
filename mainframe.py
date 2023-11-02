from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk
from biometric_register import BiometricRegister


class Mainframe(Tk):
    def __init__(self):
        super().__init__()
        # Main screen config
        self.title('Face Recognition')
        self.geometry('1362x768')

        # Load images
        self.img_background = ImageTk.PhotoImage(self.resize_image('background'))
        self.img_sign_up = ImageTk.PhotoImage(self.resize_image('sign_up'))
        self.img_sign_in = ImageTk.PhotoImage(self.resize_image('sign_in'))
        self.img_form_login = ImageTk.PhotoImage(self.resize_image('form_login'))
        self.img_form_reg = ImageTk.PhotoImage(self.resize_image('form_register'))
        self.img_send_button = ImageTk.PhotoImage(self.resize_image('send_button'))
        self.img_face_rec_button = ImageTk.PhotoImage(self.resize_image('face_rec_button'))

        # Load labels
        self.label_background = Label(self, image=self.img_background)
        self.label_sign_in = Label(self, image=self.img_sign_in)
        self.label_sign_up = Label(self, image=self.img_sign_up)
        self.label_register = Label(self, image=self.img_form_reg)
        self.label_form_login = Label(self, image=self.img_form_login)
        self.label_form_reg = Label(self, image=self.img_form_reg)

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
        self.button_face_rec = Button(self, text='Begin', fg='white', bg='grey')

        # Widget attributes
        self.config_widgets()

        # Widget position
        self.place_widgets()

    def resize_image(self, path: str):
        width_factor = 1.4056
        height_factor = 1.40625

        img = Image.open(f'./media/{path}.png')
        img = img.resize((int(img.width / width_factor), int(img.height / height_factor)))

        return img

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

        # Buttons
        self.button_send_up['command'] = self.send_signup
        self.button_send_in['command'] = self.send_signin
        self.button_send_face['command'] = self.face_login
        self.button_face_rec['command'] = self.face_register

    def place_widgets(self):
        # Background
        self.label_background.place(x=0, y=0, relheight=1, relwidth=1)

        # Sign up
        self.label_sign_up.place(relx=0.0984, rely=0.0875)
        self.label_form_reg.place(relx=0.0984, rely=0.2642)
        self.button_send_up.place(relx=0.1984, rely=0.5743)
        self.sign_up_name.place(relx=0.242, rely=0.321)
        self.sign_up_user.place(relx=0.242, rely=0.37)
        self.sign_up_pass.place(relx=0.242, rely=0.418)
        self.button_face_rec.place(relx=0.3172, rely=0.46)

        # Sign in
        self.label_sign_in.place(relx=0.6161, rely=0.0875)
        self.label_form_login.place(relx=0.6161, rely=0.2642)
        self.button_send_in.place(relx=0.645, rely=0.5743)
        self.button_send_face.place(relx=0.7573, rely=0.5743)

    def send_signup(self):
        if not self.sign_up_name.get() or \
                not self.sign_up_user.get() or \
                not self.sign_up_pass.get():
            mb.showerror('Error', 'Missing one or more fields')
            return

        if self.button_send_face['text'] == 'Begin':
            if not mb.askyesno('Warning', 'Are you sure you want to continue without biometric information?'):
                return

        if len(self.sign_up_name.get()) < 4:
            mb.showerror('Error', 'Name must be at least four characters long')
            return

        if len(self.sign_up_pass.get()) < 6:
            mb.showerror('Error', 'Password must be at least six characters long')
            return

        if self.sign_up_pass.get().isalpha():
            mb.showerror('Error', 'Password must have at least one number')
            return
        
        return

    def send_signin(self):
        pass

    def face_login(self):
        pass

    def face_register(self):
        BiometricRegister(self).biometric_log()
