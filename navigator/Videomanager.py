import os
import time
import shutil
import picamera
import datetime 
import threading

TEMP_FOLDER  = "/tmp"
VIDEO_FOLDER = "/mnt/drone/videos"


class Videomanager(threading.Thread):

    def __init__(self):
        super(Videomanager, self).__init__()
        self.setDaemon(True)
        self._shouldrun = False
        self._camera    = picamera.PiCamera()
    
    def run(self):
        self._shouldrun = True
        filename        = "%s/video-%06d.h264" % (TEMP_FOLDER, time.time())
        self._camera.start_recording(filename)
        
    def stop(self):
        self._shouldrun = False
        try:
            self._camera.stop_recording()
        except:
            pass
        now = datetime.datetime.now()
        directory = "%s/%04d-%02d-%02d" % (VIDEO_FOLDER, now.year, now.month, now.day)
        if not os.path.exists(directory):
            os.makedirs(directory)
        files = os.listdir(TEMP_FOLDER)
        for f in files:
            if f.endswith(".h264"):
                shutil.move(TEMP_FOLDER + "/" + f, directory)

if __name__ == "__main__":
    v = Videomanager()
    v.start()
    time.sleep(5)
    v.stop()
