import multiprocessing
import sys
import time
import queue

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QFileDialog

from UI import Ui_MainWindow
from Emit_Image import ThreadEmitImage


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.initUI()

        self.my_thread_queue_image_done = queue.PriorityQueue()
        self.my_thread_queue_image_read = queue.PriorityQueue()
        self.my_process_queue_image_processing = multiprocessing.Queue()
        self.my_process_queue_image_processed = multiprocessing.Queue()
        self.my_end = multiprocessing.Queue()

        self.my_thread = ThreadEmitImage(self.my_thread_queue_image_done, self.my_thread_queue_image_read,
                                         self.my_process_queue_image_processing, self.my_process_queue_image_processed,
                                         self.my_end)
        self.my_thread.my_signal_image.connect(self.show_image)
        self.my_thread.my_signal_frame.connect(self.my_slider_value)

        self.pushButton.clicked.connect(self.my_start)
        self.pushButton_bg.clicked.connect(self.select_bg)
        self.pushButton_fg.clicked.connect(self.select_fg)
        self.pushButton_export.clicked.connect(self.export_video)
        self.pushButton_stop.clicked.connect(self.stop)

        self.widget_slider.installEventFilter(self)
        self.horizontalSlider.sliderPressed.connect(self.my_slider_pressed)
        self.horizontalSlider.sliderMoved.connect(self.my_slider_moved)
        self.horizontalSlider.sliderReleased.connect(self.my_slider_released)

        self.last_time = time.time()
        self.filename_fg = "./video.mp4"
        self.filename_bg = "./background.mp4"
        self.frames = 0
        self.frame_changed = 0

        self.time_sleep = 0.05
        self.time_sleep_min = 0.0015

        self.export_flag = False

    def initUI(self):
        self.setWindowTitle("Video")
        self.setFixedSize(self.width(), self.height())
        # self.show()
        self.label.setVisible(False)
        self.widget_slider.setVisible(False)

    def eventFilter(self, object, event) -> bool:
        if event.type() == QEvent.Enter:
            self.horizontalSlider.show()
            return True
        elif event.type() == QEvent.Leave:
            self.horizontalSlider.hide()
            return False
        return False

    def show_image(self, image):
        this_time = time.time()
        last_time = self.last_time
        self.last_time = this_time
        try:
            self.label_fps.setText(str(round(1 * 2 / (this_time - last_time), 0)))
            print("fps:" + str(round(1 * 1 / (this_time - last_time), 0)))
            # self.label_fps.setText(str(round(1 / (this_time - last_time), 2)))
            # print(str(1 / (this_time - last_time)))
        except:
            pass
        self.label.setPixmap(image[0])
        self.label.setScaledContents(True)

    def my_start(self):
        self.label.setVisible(True)
        self.widget_slider.setVisible(True)
        self.frames = self.my_thread.set_video(self.filename_fg, self.filename_bg)
        self.my_slider_init()
        self.my_thread.start()

    def my_slider_init(self):
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.frames)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.hide()

    def my_slider_value(self, frame):
        self.horizontalSlider.setValue(frame[0])

    def my_slider_pressed(self):
        self.my_thread.pause(True)

    def my_slider_moved(self, value):
        self.frame_changed = value

    def my_slider_released(self):
        self.my_thread.frame_change(self.frame_changed)
        time.sleep(self.time_sleep*4)
        self.my_thread.pause(False)

    def select_fg(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "选取文件",
                                                         "./",
                                                         "* (*.*);;")  # 设置文件扩展名过滤,注意用双分号间隔
        self.filename_fg = filename

    def select_bg(self):
        filename, filetype = QFileDialog.getOpenFileName(self,

                                                         "选取文件",
                                                         "./",
                                                         "* (*.*);;")  # 设置文件扩展名过滤,注意用双分号间隔
        self.filename_bg = filename

    def export_video(self):
        if self.export_flag:
            self.pushButton_export.setStyleSheet("background-color: rgb(64, 158, 255);\n"
                                                 "border-radius: 20px;\n"
                                                 "font-size: 16px;\n"
                                                 "linr-height: 20px;\n"
                                                 "color: rgb(255, 255, 255);")
            self.export_flag = False
        else:
            self.pushButton_export.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                                 "border-radius: 20px;\n"
                                                 "font-size: 16px;\n"
                                                 "linr-height: 20px;\n"
                                                 "color: rgb(255, 255, 255);")
            self.export_flag = True
        self.my_thread.export_video()

    def stop(self):
        self.my_thread.stop()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MyUI = MyMainWindow()
    MyUI.show()
    sys.exit(app.exec_())
