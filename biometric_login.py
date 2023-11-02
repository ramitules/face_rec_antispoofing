import os
import cv2
import face_recognition as fr
from toplevel_video import BaseVideo


class BiometricLogin(BaseVideo):
    def __init__(self, master, user: str, password: str):
        super().__init__(master=master)

        self.title('Biometric sign in')

        # Variables
        self.user = user
        self.password = password
        self.path_faces = './database/faces'

    def login(self):
        # DB faces
        images = []
        names = []
        faces = os.listdir(self.path_faces)

        for face in faces:
            # Read img
            imgdb = cv2.imread(f'{self.path_faces}/{face}')
            # Save in memory
            images.append(imgdb)
            # Save name in memory
            names.append(os.path.splitext(face)[0])

        FaceCode = self.face_codification(images)

    def face_codification(self, images: list):
        code_list = []

        for img in images:
            # Color conversion
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Img code
            cod = fr.face_encodings(img)[0]

            # Save list
            code_list.append(cod)

        return code_list
