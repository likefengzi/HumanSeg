import multiprocessing
import time
from threading import Thread
import cv2

from PyQt5.QtCore import QSize

from Image_Process import ProcessImageProcess
from HumanSeg import HumanSeg


# TypeError: can't pickle cv2.VideoCapture objects

class ThreadVideoGet(Thread):
    def __init__(self, my_thread_queue_image_read, my_process_queue_image_processing, my_process_queue_image_processed,
                 my_end):
        super(ThreadVideoGet, self).__init__()

        self.my_thread_queue_image_read = my_thread_queue_image_read
        self.my_process_queue_image_processing = my_process_queue_image_processing
        self.my_process_queue_image_processed = my_process_queue_image_processed
        self.my_end = my_end

        self.is_running = True
        self.w = None
        self.h = None
        self.size = None

        self.video_background = cv2.VideoCapture("./background.mp4")
        self.my_thread_queue_image_background = multiprocessing.Queue()

        self.my_process_list = []
        self.my_process_image_process = ProcessImageProcess(
            self.my_process_queue_image_processing,
            self.my_process_queue_image_processed, self.my_end, self.my_thread_queue_image_background)

        self.capture = cv2.VideoCapture("./video.mp4")
        self.humanseg = HumanSeg()

        self.frame = 0
        self.frame_change_flag = False

        self.time_sleep = 0.05
        self.time_sleep_min = 0.0015

    def frame_change(self, frame):
        self.frame = frame
        self.frame_change_flag = True

    def set_video(self, filename_fg, filename_bg):
        self.video_background = cv2.VideoCapture(filename_bg)
        self.capture = cv2.VideoCapture(filename_fg)
        frames_bg = self.video_background.get(cv2.CAP_PROP_FRAME_COUNT)
        frames_fg = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        print("frames:"+str(frames_fg))
        if frames_fg >= frames_bg:
            return frames_bg
        else:
            return frames_fg

    def run(self) -> None:
        self.process_start()
        while self.is_running:
            self.function()

    def stop(self):
        self.is_running = False
        for my_process in self.my_process_list:
            my_process.stop()

        self.my_process_list = []

    def function(self):
        if self.frame_change_flag:
            self.frame_change_flag = False
            print("change :" + str(self.frame))
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame)
            self.video_background.set(cv2.CAP_PROP_POS_FRAMES, self.frame)
            print("video get 2")
            while self.my_thread_queue_image_background.qsize() > 0:
                self.my_thread_queue_image_background.get()
            while self.my_process_queue_image_processing.qsize() > 0:
                self.my_process_queue_image_processing.get()
            print("video get 3")
        ret, image = self.capture.read()
        if ret:
            frame = self.capture.get(cv2.CAP_PROP_POS_FRAMES)
            if frame % 2 != 0:
                ret, image = self.video_background.read()
                return None
            image = cv2.resize(image, (480, 270))

            image = self.humanseg.segment(image)
            self.my_process_queue_image_processing.put([frame, image])
            ret, image = self.video_background.read()
            if ret:
                frame = self.video_background.get(cv2.CAP_PROP_POS_FRAMES)
                self.my_thread_queue_image_background.put([frame, image])

            '''
            # 跳帧大法
            if frame % 10 == 0:
                self.my_process_queue_image_processing.put([frame, image])
            '''

        elif not ret:
            self.is_running = False
            self.my_end.put("End")

    def set_size(self, w, h):
        if (w / self.w) * self.h < h:
            size = QSize(w, w * self.h / self.w)
        else:
            size = QSize(h * self.w / self.h, h)
        self.size = size
        return size

    def get_size(self):
        return self.size

    def process_start(self):
        self.w = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.h = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.my_process_list = []
        for i in range(10):
            my_process_image_process = ProcessImageProcess(
                self.my_process_queue_image_processing,
                self.my_process_queue_image_processed, self.my_end, self.my_thread_queue_image_background)
            self.my_process_list.append(my_process_image_process)

        time.sleep(self.time_sleep)

        for my_process in self.my_process_list:
            my_process.start()
