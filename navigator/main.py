import time
from   QRmamager import QRmanager

class Main():

    def __init__(self):
        print ("INIT")
        self._qrmanager = QRmanager()
        self._qrmanager.start()

    def debug(self):
        print(self._qrmanager.getLastDecodeTimeStamp())
        print(self._qrmanager.getQRValue())
        print(self._qrmanager.getQRSize())
        print(self._qrmanager.getHorizontalOffset())
        print(self._qrmanager.getVerticalOffset())

if __name__ == "__main__":
    m = Main()
    for i in range(42):
        m.debug()
        time.sleep(1)
