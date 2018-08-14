import time
from   QRmamager    import QRmanager
from   Videomanager import Videomanager
from   Dronemanager import Dronemanager

INIT    = 0
STARTED = 1

class Main():

    def __init__(self):
        self._videomanager = Videomanager()
        self._qrmanager    = QRmanager()
        self._dronemanager = Dronemanager()
        self._videomanager.start()
        self._qrmanager.start()
        self._state = INIT

    def debug(self):
        #print(self._qrmanager.getLastDecodeTimeStamp())
        #print(self._qrmanager.getQRValue())
        #print(self._qrmanager.getQRSize())
        #print(self._qrmanager.getHorizontalOffset())
        print(self._qrmanager.getVerticalOffset())

    def controll(self):

        if (time.time() - self._qrmanager.getLastDecodeTimeStamp()) < 1000:

            if self._state == INIT:
                self._state = STARTED
                m._dronemanager.start()

            if self._state == STARTED:
                if self._qrmanager.getVerticalOffset() > 0:
                    self._dronemanager.up()


    def shutdown(self):
        self._dronemanager.stop()
        self._qrmanager.stop()
        self._videomanager.stop()

if __name__ == "__main__":
    m = Main()

    try:
        for i in range(42):
            m.controll()
            m.debug()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Emergency landing")
        m.shutdown()
    except Exception as error:
        print("ERROR")
        m.shutdown()

    m.shutdown()
    time.sleep(3)
