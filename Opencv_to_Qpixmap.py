import time
from threading import Thread
import cv2

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage, QPixmap


# pickle QPixmap

class ThreadOpencvToQpixmap(Thread):
    def __init__(self, my_thread_queue_image_done, my_process_queue_image_processed, my_end):
        super(ThreadOpencvToQpixmap, self).__init__()

        self.my_thread_queue_image_done = my_thread_queue_image_done
        self.my_process_queue_image_processed = my_process_queue_image_processed
        self.my_end = my_end

        self.is_running = True
        self.w = 1440
        self.h = 810

        self.time_sleep = 0.05
        self.time_sleep_min = 0.0015

        self.export_flag = False
        self.export_video_cap = None

    def run(self) -> None:
        time.sleep(self.time_sleep)
        while self.is_running:
            flag = self.function()
            if not flag:
                time.sleep(self.time_sleep_min)

    def stop(self):
        self.is_running = False
        if self.export_video_cap:
            self.export_video_cap.release()

    def function(self):
        if self.my_process_queue_image_processed.empty():
            if not self.my_end.empty():
                self.is_running = False
            return False
        else:
            frame, image, data = self.my_process_queue_image_processed.get()
            if self.export_flag:
                self.export_video_cap.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                self.export_video_cap.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

            size = QSize(480, 270)
            image = QImage(image.data.tobytes(), image.shape[1], image.shape[0], image.shape[1] * 3,
                           QImage.Format_RGB888)
            image = QPixmap.fromImage(image.scaled(size, Qt.IgnoreAspectRatio))
            self.my_thread_queue_image_done.put([frame, image, data])
            return True

    def frame_change(self, frame):
        while self.my_process_queue_image_processed.qsize() > 0:
            self.my_process_queue_image_processed.get()
        while self.my_thread_queue_image_done.qsize() > 0:
            self.my_thread_queue_image_done.get()

    def export_video(self):
        if self.export_flag:
            self.export_video_cap.release()
            self.export_flag = False
        else:
            fps = 30
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.export_video_cap = cv2.VideoWriter('export.avi', fourcc, fps, (480, 270))
            self.export_flag = True
