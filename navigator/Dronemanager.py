from   Multiwii import MultiWii
from   sys      import stdout
import time

MAX_POWER      = 1999
CENTER_X       = 2.5      # bigger -> right
CENTER_Y       = -3.8   # bigger -> forkward
ALPHA          = 1
MAX_CORRECTION = 50

if __name__ == "__main__":
    board = MultiWii("/dev/ttyUSB0")

    try:

        start = time.time()
        state = 0
        data = [1500,1500,1500,1000,1500]

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
        board.disarm()
        time.sleep(1)
    except Exception as error:        
        print ("Error on Main: " + str(error))
        board.disarm()
        time.sleep(1)