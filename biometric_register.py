from toplevel_video import BaseVideo
import cv2


class BiometricRegister(BaseVideo):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title('Biometric sign up')

    def step3(self):
        yi, yf, xi, xf = self.my_position[:]

        # If eyes are opened
        if self.lengths[0] > 20 and self.lengths[1] > 20:
            try:
                # Cut
                cut = self.frame_to_save[yi:yf, xi:xf]

                # Save face
                cv2.imwrite('./database/faces/face.png', cut)

            except cv2.error:
                print('Error. Try again')

            self.completed = True

    def destroy(self):
        if self.completed:
            # Face recognition completed. Button not needed
            self.master.button_face_rec['text'] = 'Completed'
            self.master.button_face_rec['state'] = 'disabled'

            print('Picture saved. Registration completed.')

        else:
            print('Abort.')

        super().destroy()
