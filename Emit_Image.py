import time

from PyQt5.QtCore import QThread, pyqtSignal

from Opencv_to_Qpixmap import ThreadOpencvToQpixmap
from Video_Get import ThreadVideoGet


class ThreadEmitImage(QThread):
    my_signal_image = pyqtSignal(list)
    my_signal_frame = pyqtSignal(list)

    def __init__(self, my_thread_queue_image_done, my_thread_queue_image_read, my_process_queue_image_processing,
                 my_process_queue_image_processed, my_end):
        super(ThreadEmitImage, self).__init__()

        self.my_thread_queue_image_done = my_thread_queue_image_done
        self.my_thread_queue_image_read = my_thread_queue_image_read
        self.my_process_queue_image_processing = my_process_queue_image_processing
        self.my_process_queue_image_processed = my_process_queue_image_processed
        self.my_end = my_end

        self.is_running = True
        self.pause_flag = False
        # self.fps = 20
        self.fps = 20
        self.time_sleep=0.05
        self.time_sleep_min=0.0015

        self.my_thread_record_screen = ThreadVideoGet(self.my_thread_queue_image_read,
                                                      self.my_process_queue_image_processing,
                                                      self.my_process_queue_image_processed, self.my_end)
        self.my_thread_list = []
        self.my_thread_opencv_to_qpixmap = ThreadOpencvToQpixmap(self.my_thread_queue_image_done,
                                                                 self.my_process_queue_image_processed, self.my_end)

    def set_video(self, filename_fg, filename_bg):
        frames = self.my_thread_record_screen.set_video(filename_fg, filename_bg)
        return frames

    def run(self) -> None:
        self.my_thread_record_screen.start()
        time.sleep(self.time_sleep)
        self.thread_start()
        time.sleep(self.time_sleep)
        while self.is_running:
            flag = self.function()
            if not flag:
                time.sleep(self.time_sleep_min)

    def stop(self):
        self.is_running = False
        self.my_thread_record_screen.stop()
        for my_thread in self.my_thread_list:
            my_thread.stop()

        self.my_thread_list = []

    def function(self):
        if self.my_thread_queue_image_done.empty():
            if not self.my_end.empty():
                self.is_running = False
            return False
        elif self.pause_flag:
            return False
        else:
            time.sleep((1 / self.fps) - self.time_sleep_min)
            frame, image, data = self.my_thread_queue_image_done.get()
            print("qsize:" + str(self.my_thread_queue_image_done.qsize()))
            print("frame:" + str(frame))
            self.my_signal_image.emit([image])
            self.my_signal_frame.emit([frame])
            return True

    def thread_start(self):
        self.my_thread_list = []
        for i in range(1):
            my_thread_opencv_to_qpixmap = ThreadOpencvToQpixmap(self.my_thread_queue_image_done,
                                                                self.my_process_queue_image_processed, self.my_end)
            self.my_thread_list.append(my_thread_opencv_to_qpixmap)

        time.sleep(self.time_sleep)

        for my_thread in self.my_thread_list:
            my_thread.start()

    def pause(self, flag):
        self.pause_flag = flag

    def frame_change(self, frame):
        self.my_thread_record_screen.frame_change(frame)
        for my_thread in self.my_thread_list:
            my_thread.frame_change(frame)

    def export_video(self):
        for my_thread in self.my_thread_list:
            my_thread.export_video()
