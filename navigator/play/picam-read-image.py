import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1944)
    #camera.resolution = (1024, 768)
    #camera.capture("foo.jpg")
    camera.framerate = 30
    camera.iso = 800
    time.sleep(3)
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    camera.capture_sequence(['image%05d.png' % i for i in range(5000)])

