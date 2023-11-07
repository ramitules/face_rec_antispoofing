from toplevel_video import BaseVideo
from database_handler import last_user_id
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

                # Filename = new user ID
                path = last_user_id()

                # Save face
                cv2.imwrite(f'./database/faces/{path}.png', cut)

            except cv2.error:
                print('Error. Try again')

            self.completed = True

    def destroy(self):
        if self.completed:
            # Face recognition completed. Button not needed
            self.master.button_new_face['text'] = 'Completed'
            self.master.button_new_face['state'] = 'disabled'

            print('Picture saved. Registration completed.')

        else:
            print('Abort.')

        super().destroy()
