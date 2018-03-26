import numpy as np


class CameraParameters:
    def __init__(self):
        self.CameraMatrix = np.array([[1.3176839301649577e+03, 0., 7.5837802536116862e+02],
                                     [0., 1.3214149385977262e+03, 6.0096549808629777e+02],
                                     [0., 0., 1.]], dtype=np.double)

        self.Distorsion = np.array([7.6841235027641105e-02, -2.7839587019402939e-01,
                                    -1.2307309195164124e-03, 1.1727733173366706e-04,
                                    1.7689633573292043e-01], dtype=np.double)
