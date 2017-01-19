import logging
logging.basicConfig(level=logging.INFO)

import time
import numpy as np
import cv2
import pyrealsense as pyrs


pyrs.start()
dev = pyrs.Device()

dev.set_device_option(30, 10)
dev.set_device_option(31, 0)

cnt = 0
last = time.time()
smoothing = 0.9
fps_smooth = 30

count = 0
while True:

    cnt += 1
    if (cnt % 10) == 0:
        now = time.time()
        dt = now - last
        fps = 10 / dt
        fps_smooth = (fps_smooth * smoothing) + (fps * (1.0 - smoothing))
        last = now

    dev.wait_for_frame()

    count = str(int(time.time()*1000))


    ir = dev.ir

    c = dev.colour
    c = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)

    d = dev.depth * dev.depth_scale * 1000
    d = cv2.applyColorMap(d.astype(np.uint8), cv2.COLORMAP_RAINBOW)

    #Note: OpenCV uses BGR color order
    b,g,r = cv2.split(c)
    cv2.imwrite("red/"+count+".png",r)
    cv2.imwrite("green/"+count+".png",b)
    cv2.imwrite("blue/"+count+".png",g)
    cv2.imwrite("ir/"+count+".png",ir)

    cv2.imshow('', ir)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('e'):
        exposure = input("Enter Exposure")
        dev.set_device_option(30, float(exposure))
