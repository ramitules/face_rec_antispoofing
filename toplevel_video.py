import time
from tkinter import Toplevel, Label
from PIL import Image, ImageTk
import mediapipe as mp
import cv2
import imutils
import math


class BaseVideo(Toplevel):
    def __init__(self, master):
        super().__init__(master=master)
        self.geometry('1280x720')

        # Label & video
        self.label_video = Label(self)
        self.cap = cv2.VideoCapture(0)

        self.configure_video()

        # Images
        self.img_step0 = cv2.imread('media/human_verification.png')
        self.img_step1 = cv2.imread('media/step_1.png')
        self.img_step2 = cv2.imread('media/step_2.png')
        self.img_check = cv2.imread('media/check.png')
        self.img_check_big = cv2.imread('media/check_big.png')

        # Some variables
        self.completed = False
        self.blink = False
        self.count = 0
        self.step = 1

        # Coordinates
        self.points_x = None
        self.points_y = None
        self.lengths = None

        # Picture of face recognition
        self.frame_to_save = None

        # Offset
        self.OFFSETY = 50
        self.OFFSETX = 20
        self.OFFSETY_UP = 65

        # Threshold
        self.THRESHOLD = 0.5

        # Draw tool
        self.mp_draw = mp.solutions.drawing_utils
        self.config_draw = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1)

        # Face Mesh object
        self.face_mesh_obj = mp.solutions.face_mesh
        self.facemesh = self.face_mesh_obj.FaceMesh(max_num_faces=1)

        # Face detector object
        self.face_obj = mp.solutions.face_detection
        self.detector = self.face_obj.FaceDetection(min_detection_confidence=0.5, model_selection=1)

    def biometric_log(self):
        if self.cap:
            ret, frame = self.cap.read()
            self.frame_to_save = frame.copy()

            # Resize image
            frame = imutils.resize(frame, width=1280)

            # Colour
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if ret:
                # Face Mask inference
                self.inference()

            # Video convertion
            img = Image.fromarray(self.frame)
            img = ImageTk.PhotoImage(image=img)

            # Show video
            self.label_video.configure(image=img)
            self.label_video.image = img
            self.label_video.after(10, self.biometric_log)

            if self.completed:
                self.destroy()

        else:
            self.cap.release()

    def inference(self):
        result = self.facemesh.process(self.frame)

        if result.multi_face_landmarks:
            self.extract_facemesh(result.multi_face_landmarks)

    def extract_facemesh(self, landmarks):
        # Extract Face Mesh
        for faces in landmarks:
            # Draw
            self.mp_draw.draw_landmarks(
                self.frame,
                faces,
                self.face_mesh_obj.FACEMESH_CONTOURS,
                self.config_draw,
                self.config_draw)

            self.extract_keypoints(faces)

    def extract_keypoints(self, faces):
        # Result list
        px, py, li = [], [], []

        for i, points in enumerate(faces.landmark):
            self.height, self.width, c = self.frame.shape
            x = int(points.x * self.width)
            y = int(points.y * self.height)
            px.append(x)
            py.append(y)
            li.append([i, x, y])

            if len(li) == 468:
                self.save_points(li)
                self.face_detect()

    def save_points(self, li):
        # Right eye
        x1, y1 = li[145][1:]
        x2, y2 = li[159][1:]
        length1 = math.hypot(x2 - x1, y2 - y1)

        # Left eye
        x3, y3 = li[374][1:]
        x4, y4 = li[386][1:]
        length2 = math.hypot(x4 - x3, y4 - y3)
        print(f'Ojo Izquierdo: {length1}\nOjo derecho: {length2}')

        # Parietal
        x5, y5 = li[139][1:]
        x6, y6 = li[368][1:]

        # Eyebrow
        x7, y7 = li[70][1:]
        x8, y8 = li[300][1:]

        self.points_x = [x1, x2, x3, x4, x5, x6, x7, x8]
        self.points_y = [y1, y2, y3, y4, y5, y6, y7, y8]
        self.lengths = [length1, length2]

    def face_detect(self):
        faces = self.detector.process(self.frame)

        if faces.detections:
            self.draw_box(faces)

    def draw_box(self, faces):
        for face in faces.detections:
            # Bbox: ID, BBOX, SCORE
            score = face.score[0]
            bbox = face.location_data.relative_bounding_box

            # Threshold
            self.threshold_offset(score, bbox)

    def threshold_offset(self, score, bbox):
        if score > self.THRESHOLD:
            # Pixels
            xi, yi = int(bbox.xmin * self.width), int(bbox.ymin * self.height)
            w, h = int(bbox.width * self.width), int(bbox.height * self.height)

            # Offset width
            offset_w = (self.OFFSETX / 100) * w
            xi = int(xi - int(offset_w / 2))
            w = int(w + offset_w)
            xf = xi + w

            # Offset height
            offset_y = (self.OFFSETY / 100) * h
            yi = int(yi - int(offset_y / 2)) - self.OFFSETY_UP
            h = int(h + offset_y)
            yf = yi + h

            # Coordinates to take picture of face
            self.my_position = [yi, yf, xi, xf]

            self.check_proximity()

    def check_proximity(self):
        distance_eyes = self.points_x[5] - self.points_x[4]

        # Draw recognition rectangle
        if 300 < distance_eyes < 340:
            self.load_images()
            self.steps()

        else:
            self.count = 0

    def load_images(self):
        # Img step 1
        h_step0, w_step0, c = self.img_step0.shape
        self.frame[50:50 + h_step0, 50:50 + w_step0] = self.img_step0

        # Img step 2
        h_step1, w_step1, c = self.img_step1.shape
        self.frame[50:50 + h_step1, 1030:1030 + w_step1] = self.img_step1

        # Img step 3
        h_step2, w_step2, c = self.img_step2.shape
        self.frame[330:330 + h_step2, 1030:1030 + w_step2] = self.img_step2

    def steps(self):
        self.step1()
        self.step2()

        if self.step == 3:
            self.step3()

    def step1(self):  # Face center
        if self.points_x[6] > self.points_x[4] and self.points_x[7] < self.points_x[5]:
            h_check, w_check, c = self.img_check.shape
            self.frame[200:200 + h_check, 1123:1123 + w_check] = self.img_check

            self.step = 2

        else:
            self.count = 0

    def step2(self):  # Blink counter
        text = f'Blinks: {int(self.count)}'
        coordinates = (1120, 500)
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        font_scale = 0.5
        white = (0, 0, 0)

        if self.lengths[0] <= 15 and self.lengths[1] <= 15 and not self.blink:
            self.count += 1
            self.blink = True

        elif self.lengths[0] > 15 and self.lengths[1] > 15 and self.blink:
            self.blink = False

        cv2.putText(self.frame, text, coordinates, font, font_scale, white, 1)

        if self.count > 2:
            # Img Check
            h_check, w_check, c = self.img_check_big.shape
            self.frame[478:478 + h_check, 1121:1121 + w_check] = self.img_check_big

            self.step = 3

    def step3(self):  # Take a picture
        yi, yf, xi, xf = self.my_position[:]

        # If eyes are opened
        if self.lengths[0] > 20 and self.lengths[1] > 20:
            # Cut
            cut = self.frame_to_save[yi:yf, xi:xf]

            # Save face
            cv2.imwrite('./database/faces/face.png', cut)

            self.completed = True

    def configure_video(self):
        self.label_video.place(x=0, y=0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

    def destroy(self):
        if self.completed:
            print('Picture saved. Registration completed.')

        else:
            print('Abort.')

        self.cap.release()
        super().destroy()
        print('Cam closed')
