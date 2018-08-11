from pywultiwii import MultiWii
from sys import stdout

if __name__ == "__main__":
    board = MultiWii("/dev/ttyUSB0")
    try:
        while True:
            board.getData(MultiWii.ATTITUDE)
            print board.attitude 
    except Exception,error:
        print "Error on Main: "+str(error)
