'''
import multiprocessing
import time

import cv2

a =multiprocessing.Manager().list()
capture = cv2.VideoCapture("./video.mp4")
n = capture.get(cv2.CAP_PROP_FRAME_COUNT)
print(n)
while True:
    ret, image = capture.read()
    frame = capture.get(cv2.CAP_PROP_POS_FRAMES)
    print(frame)
    if frame >= n-1:
        break
    a.append([frame, image])

last_time = time.time()
a.sort()
this_time = time.time()
print(this_time - last_time)
'''
import time

'''
import queue
import random

q = queue.PriorityQueue()
for i in range(100):
    j = random.randint(0, 100)
    q.put([j,i])

for i in range(100):
    print(q.get())
'''

import multiprocessing
import queue
import time
from multiprocessing import Process
from threading import Thread


class T1(Process):
    def __init__(self, a):
        super(T1, self).__init__()
        self.a = a

    def run(self) -> None:
        while True:
            self.a.put("1")
            time.sleep(0.1)


class T2(Process):
    def __init__(self, a):
        super(T2, self).__init__()
        self.a = a

    def run(self) -> None:
        while True:
            if self.a.empty():
                print("Empty")
                continue
            print(self.a.empty())
            b = self.a.get()
            print(b)
            time.sleep(0.2)


if __name__ == "__main__":
    a = multiprocessing.Queue()
    # a=multiprocessing.Manager().Queue()
    t1 = T1(a)
    t2 = T2(a)
    t1.start()
    t2.start()
    # t1.join()
    t2.join()

'''
time.sleep(0.1)
a1 = time.time()
time.sleep(0.02-0.0015)
a2 = time.time()
print(a2 - a1)
'''
