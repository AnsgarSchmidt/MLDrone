from pymultiwii import MultiWii

serialPort = "/dev/ttyUSB0"
board = MultiWii(serialPort)
while True:
  print board.getData(MultiWii.ATTITUDE)
