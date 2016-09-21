import ctypes
import os, time

delay = 1 / 10
imax = 100
i = 0
while True:
    start_clock = time.clock()
    img_name = "images/" + str(i) + ".bmp"
    img_path = os.path.abspath(img_name)
    ctypes.windll.user32.SystemParametersInfoW(0x14, 0, img_path, 3)
    end_clock = time.clock()
    time.sleep(max(0, delay - (end_clock - start_clock)))
    i = (i + 1) % (imax + 1)
