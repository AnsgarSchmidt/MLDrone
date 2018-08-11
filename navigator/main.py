import time
from   QRmamager    import QRmanager
from   Videomanager import Videomanager


class Main():

    def __init__(self):
        self._videomanager = Videomanager()
        self._qrmanager    = QRmanager()
        self._videomanager.start()
        self._qrmanager.start()

    def debug(self):
        #print(self._qrmanager.getLastDecodeTimeStamp())
        #print(self._qrmanager.getQRValue())
        #print(self._qrmanager.getQRSize())
        print(self._qrmanager.getHorizontalOffset())
        #print(self._qrmanager.getVerticalOffset())

    def shutdown(self):
        self._qrmanager.stop()
        self._videomanager.stop()

if __name__ == "__main__":
    m = Main()

    for i in range(42):
        m.debug()
        time.sleep(1)
    
    m.shutdown()
    time.sleep(3)
