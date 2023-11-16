import numpy as np
import paddlehub as hub


class HumanSeg:
    def __init__(self):
        # self.human_seg = hub.Module(name='humanseg_lite')
        self.human_seg = hub.Module(name='humanseg_mobile')
        # self.human_seg = hub.Module(name='humanseg_server')

    def segment(self, image):
        res = self.human_seg.segment(images=[image])
        i = 0
        rgba = np.concatenate((image, np.expand_dims(res[0]['data'], axis=2)), axis=2)
        return rgba
