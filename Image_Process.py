import time
from multiprocessing import Process
import cv2

from Merge_Alpha import Merge_Alpha


class ProcessImageProcess(Process):
    def __init__(self, my_process_queue_image_processing, my_process_queue_image_processed, my_end,
                 my_thread_queue_image_background):
        super(ProcessImageProcess, self).__init__()

        self.my_process_queue_image_processing = my_process_queue_image_processing
        self.my_process_queue_image_processed = my_process_queue_image_processed
        self.my_end = my_end

        self.is_running = True
        self.w = 960
        self.h = 540

        self.time_sleep = 0.05
        self.time_sleep_min = 0.0015

        self.my_thread_queue_image_background = my_thread_queue_image_background
        self.image_bg = None
        self.merge_alpha = Merge_Alpha()

    def run(self) -> None:
        time.sleep(self.time_sleep)
        while self.is_running:
            flag = self.function()
            if not flag:
                time.sleep(self.time_sleep_min)

    def stop(self):
        self.is_running = False

    def function(self):
        if self.my_process_queue_image_processing.empty():
            if not self.my_end.empty():
                self.is_running = False
            return False
        else:
            frame, image = self.my_process_queue_image_processing.get()
            bg_frame, image_bg = self.my_thread_queue_image_background.get()
            image_bg = cv2.resize(image_bg, (480, 270))
            image = self.video_process(image, image_bg)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            data = []

            self.my_process_queue_image_processed.put([frame, image, data])
            return True

    def video_process(self, image, image_bg):
        image = self.merge_alpha.merge(image, image_bg)
        return image
