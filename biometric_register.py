
from toplevel_video import BaseVideo


class BiometricRegister(BaseVideo):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title('Biometric sign up')
