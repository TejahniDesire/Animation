import matplotlib.pyplot as plt
import sys
import os
import subprocess
import numpy as np


def animate(update_func, max_frame, dir_path="./", name="movie.mp4",init_func=None,speed=15):
    if init_func is not None:
        init_func()
    temporary_path = dir_path + "animate_frames/"
    isDir = os.path.exists(temporary_path)
    if isDir:
        print("removing previously existing temp folder")
        subprocess.run(["rm -r " + temporary_path], shell=True)
    subprocess.run(["mkdir " + temporary_path],shell=True)

    if os.path.exists(temporary_path):
        print("subdirectory '{}' made".format(temporary_path))
    else: 
        raise RuntimeError("subdirectory '{}' failed to manifest".format(temporary_path))

    for i in range(max_frame):
        frame = i
        if frame % 10 == 0:
            print("Making Frame: ", frame)
        update_func(frame)
        plt.savefig(temporary_path + "frame_" + str(frame) + ".jpeg",bbox_inches='tight')

    name = dir_path + name
    if os.path.isfile(name):
        subprocess.run(['rm ' + name], shell=True)

    subprocess.run(["ffmpeg -r " + str(speed) + " -i " + temporary_path +
                    "frame_%d.jpeg -vf 'pad=ceil(iw/2)*2:ceil(ih/2)*2' -vcodec "
                    "libx264 -crf 10 -pix_fmt yuv420p " + name], shell=True)

    subprocess.run(["rm -r " + temporary_path], shell=True)
