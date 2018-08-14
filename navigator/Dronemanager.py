from   Multiwii import MultiWii
from   sys      import stdout
import time
import threading

MAX_POWER      = 1999
MIN_POWER      = 1000
POWER_DELTA    = 30
CENTER_X       = 0      # bigger -> right
CENTER_Y       = -2.2   # bigger -> forkward
ALPHA          = 1
MAX_CORRECTION = 100


class Dronemanager(threading.Thread):

    def __init__(self):
        super(Dronemanager, self).__init__()
        self.setDaemon(True)
        self._shouldrun = False
        self._center_x  = CENTER_X
        self._center_y  = CENTER_Y
        self._board     = MultiWii("/dev/ttyUSB0")
        self._rc        = [1500,1500,1500,1000,1500]

    def stop(self):
        self._shouldrun = False

    def up(self):
        val = self._rc[3]
        if val < (MAX_POWER - POWER_DELTA):
            self._rc[3] = val + POWER_DELTA
        else:
            self._rc[3] = MAX_POWER

    def down(self):
        val = self._rc[3]
        if val > (MIN_POWER + POWER_DELTA):
            self._rc[3] = val - POWER_DELTA
        else:
            self._rc[3] = MIN_POWER

    def left(self):
        pass

    def right(self):
        pass

    def run(self):
        self._shouldrun = True
        self._board.arm()
        self._rc = [1500,1500,1500,1000,1500]

        while self._shouldrun:
            self._board.getData(MultiWii.ATTITUDE)
            print ("Th:%04d - Roll:%04d - Pitch:%04d - X:%0.1f - Y:%0.1f" % (self._rc[3], self._rc[0], self._rc[1], self._board.attitude['angx'], self._board.attitude['angy'])) 
            angx = self._board.attitude['angx']
            angy = self._board.attitude['angy']
            
            # drifting right -> move left
            if angx < (CENTER_X - ALPHA):   # right
                self._rc[0] = 1500 + MAX_CORRECTION
                self._board.sendCMD(10, MultiWii.SET_RAW_RC, self._rc)
            elif angx > (CENTER_X + ALPHA): # left
                self._rc[0] = 1500 - MAX_CORRECTION
                self._board.sendCMD(10, MultiWii.SET_RAW_RC, self._rc)
            else:
                self._rc[0] = 1500
                self._board.sendCMD(10, MultiWii.SET_RAW_RC, self._rc)

            if angy < CENTER_Y - ALPHA: 
                self._rc[1] = 1500 + MAX_CORRECTION
                self._board.sendCMD(10, MultiWii.SET_RAW_RC, self._rc)
            elif angy > CENTER_Y + ALPHA:
                self._rc[1] = 1500 - MAX_CORRECTION
                self._board.sendCMD(10, MultiWii.SET_RAW_RC, self._rc)
            else:
                self._rc[1] = 1500
                self._board.sendCMD(10, MultiWii.SET_RAW_RC, self._rc)

        print("Shutting down")
        self._board.disarm()

if __name__ == "__main__":

    try:

        while True:

            # Arm
            if state == 0 and time.time() > start + 1:
                board.arm()
                state = 1

            if state == 1 and time.time() > start + 3:
                data[3] = 1300
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
                state = 2

            if state == 2 and time.time() > start + 5:
                data[3] = 1600
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
                state = 3

            # Max power
            if state == 3 and time.time() > start + 7:
                data[3] = MAX_POWER  # 1670 lifoff
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
                state = 4

            if state == 4 and time.time() > start + 17:
                data[3] = 1800
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
                state = 5

            if state == 5 and time.time() > start + 19:
                data[3] = 1700
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
                state = 6

            if state == 6 and time.time() > start + 21:
                data[3] = 1600
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
                state = 7

            if state == 7 and time.time() > start + 22:
                board.disarm()
                state = 8

            if state == 8 and time.time() > start + 23:
                break            

            board.getData(MultiWii.ATTITUDE)
            print ("Th:%04d - Roll:%04d - Pitch:%04d - X:%0.1f - Y:%0.1f" % (data[3], data[0], data[1], board.attitude['angx'], board.attitude['angy'])) 
            angx = board.attitude['angx']
            angy = board.attitude['angy']
            
            # drifting right -> move left
            if angx < (CENTER_X - ALPHA):   # right
                data[0] = 1500 + MAX_CORRECTION
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
            elif angx > (CENTER_X + ALPHA): # left
                data[0] = 1500 - MAX_CORRECTION
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
            else:
                data[0] = 1500
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)

            if angy < CENTER_Y - ALPHA: 
                data[1] = 1500 + MAX_CORRECTION
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
            elif angy > CENTER_Y + ALPHA:
                data[1] = 1500 - MAX_CORRECTION
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)
            else:
                data[1] = 1500
                board.sendCMD(10, MultiWii.SET_RAW_RC,data)

            #   angx  = -links   +rechts
            #   angy  = +vor     -zurueck
            # 0 ROLL  = rechts-links
            # 1 PITCH = vor-zurueck
            # 2 YAW   = cw-ccw
            # 3 THROTTLE
            
    except KeyboardInterrupt:
        data[3] = 1600
        board.sendCMD(10, MultiWii.SET_RAW_RC,data)
        time.sleep(1)
        data[3] = 1500
        board.sendCMD(10, MultiWii.SET_RAW_RC,data)
        time.sleep(1)
        time.sleep(1)
    except Exception as error:        
        print ("Error on Main: " + str(error))
        board.disarm()
        time.sleep(1)