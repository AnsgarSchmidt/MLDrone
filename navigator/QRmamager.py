import pyzbar.pyzbar as     pyzbar
import numpy         as     np
import threading
import time
import cv2

BEST_SIZE       =  450
BEST_SIZE_DELTA =   50
POSITION_DELTA  =  100
IMAGE_WIDTH     = 1920
IMAGE_HEIGHT    = 1080
DEBUG           = True

class QRmanager(threading.Thread):

    def __init__(self):
        print("INIT")
        super(QRmanager, self).__init__()
        self.setDaemon(True)
        self._cap = cv2.VideoCapture(0)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH,  IMAGE_WIDTH  )
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT )
        self._cap.set(cv2.CAP_PROP_AUTOFOCUS,    0            )
        self._qrvalue   = None
        self._qrcenterx = 0
        self._qrcentery = 0
        self._qrsize    = 0
        self._qrupdate  = 0

    def _decode(self, image):
        decodedObjects = pyzbar.decode(image)
        if DEBUG:
            cv2.imwrite("../../debugimages/test-%08d.png" % time.time(), image)

        for obj in decodedObjects:
        
            if "QRCODE" != obj.type:
                continue

            points = obj.polygon

            if len(points) > 4 : 
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else : 
                hull = points

            tx, ty, tw, th = cv2.boundingRect(np.array([point for point in points], dtype=np.float32))
            size           = np.average([tw, th])
            cx             = tx + (tw / 2.0)
            cy             = ty + (th / 2.0)

            if DEBUG:
                for j in range(0, len(hull)):
                    cv2.line(image, hull[j], hull[ (j+1) % len(hull)], (255,0,0), 3)
                cv2.imwrite("../../debugimages/%04d-%04d-%04d-%07d.png" % (size, cx, cy, time.time()), image)
        
            return obj.data, size, cx, cy

        return None, None, None, None

    def getLastDecodeTimeStamp(self):
        return self._qrupdate

    def getQRValue(self):
        if self._qrvalue:
            return self._qrvalue.decode("utf-8")
        else:
            return None

    def getQRSize(self):
        if self._qrsize:
            return 100 * ((self._qrsize * self._qrsize) / (IMAGE_HEIGHT * IMAGE_WIDTH)) 
        else:
            return None

    def getHorizontalOffset(self):
        if self._qrcenterx:
            return (IMAGE_WIDTH / 2.0) - self._qrcenterx # Left + / Right -
        else:
            return None

    def getVerticalOffset(self):
        if self._qrcentery:
            return (IMAGE_HEIGHT / 2.0) - self._qrcentery # Up + / Down -
        else:
            return None

    def run(self):

        while True:
            ret, image = self._cap.read()

            if ret:
                value, size, cx, cy = self._decode(image)

                if value and size and cx and cy:
                    self._qrvalue = value
                    self._qrsize  = size
                    self._qrcenterx = cx
                    self._qrcentery = cy
                    self._qrupdate  = time.time()
