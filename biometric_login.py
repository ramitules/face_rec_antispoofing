import os
import cv2
import numpy as np
import face_recognition as fr
from toplevel_video import BaseVideo


class BiometricLogin(BaseVideo):
    def __init__(self, master):
        super().__init__(master=master)

        self.title('Biometric sign in')

        # Variables
        self.id = ''
        self.path_faces = './database/faces'
        self.ids = []
        self.faces = os.listdir(self.path_faces)
        self.codifications = self.login()

    def step3(self):
        # Find faces
        faces_loc = fr.face_locations(self.frame_to_save)
        faces_cod = fr.face_encodings(self.frame_to_save, faces_loc)

        # Iter faces
        for codification, location in zip(faces_cod, faces_loc):
            # Matching
            match = fr.compare_faces(self.codifications, codification)

            # Similarity
            sim = fr.face_distance(self.codifications, codification)

            # Less errors
            minn = np.argmin(sim)

            if match[minn]:
                self.id = self.ids[minn]

                self.completed = True

    def login(self):
        images = []

        for face in self.faces:
            # Read img
            imgdb = cv2.imread(f'{self.path_faces}/{face}')
            # Save in memory
            images.append(imgdb)
            # Save name in memory
            self.ids.append(os.path.splitext(face)[0])

        return self.face_codification(images)

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

    def destroy(self):
        if self.completed:
            print(f'Hello {self.id}!')

        else:
            print('Abort.')

        super().destroy()
