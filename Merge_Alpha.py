import cv2
import numpy as np


class Merge_Alpha:
    def __init__(self):
        pass

    def add_alpha_channel(self, img):
        """ 为jpg图像添加alpha通道 """

        b_channel, g_channel, r_channel = cv2.split(img)  # 剥离jpg图像通道
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道

        img_new = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))  # 融合通道
        return img_new

    def merge_img(self, jpg_img, png_img, y1, y2, x1, x2):
        """ 将png透明图像与jpg图像叠加
            y1,y2,x1,x2为叠加位置坐标值
        """

        # 判断jpg图像是否已经为4通道
        if jpg_img.shape[2] == 3:
            jpg_img = self.add_alpha_channel(jpg_img)

        '''
        当叠加图像时，可能因为叠加位置设置不当，导致png图像的边界超过背景jpg图像，而程序报错
        这里设定一系列叠加位置的限制，可以满足png图像超出jpg图像范围时，依然可以正常叠加
        '''
        yy1 = 0
        yy2 = png_img.shape[0]
        xx1 = 0
        xx2 = png_img.shape[1]

        if x1 < 0:
            xx1 = -x1
            x1 = 0
        if y1 < 0:
            yy1 = - y1
            y1 = 0
        if x2 > jpg_img.shape[1]:
            xx2 = png_img.shape[1] - (x2 - jpg_img.shape[1])
            x2 = jpg_img.shape[1]
        if y2 > jpg_img.shape[0]:
            yy2 = png_img.shape[0] - (y2 - jpg_img.shape[0])
            y2 = jpg_img.shape[0]

        # 获取要覆盖图像的alpha值，将像素值除以255，使值保持在0-1之间
        alpha_png = png_img[yy1:yy2, xx1:xx2, 3] / 255.0
        alpha_jpg = 1 - alpha_png

        # 开始叠加
        for c in range(0, 3):
            jpg_img[y1:y2, x1:x2, c] = (
                    (alpha_jpg * jpg_img[y1:y2, x1:x2, c]) + (alpha_png * png_img[yy1:yy2, xx1:xx2, c]))

        return jpg_img

    def merge(self, image_fg, image_bg):

        size1 = image_fg.shape
        h1, w1 = size1[0], size1[1]
        size2 = image_bg.shape
        h2, w2 = size2[0], size2[1]

        y0 = (h2 - h1) // 2
        y1 = y0 + h1
        x0 = (w2 - w1) // 2
        x1 = x0 + w1

        res_img = self.merge_img(image_bg, image_fg, y0, y1, x0, x1)
        return res_img
