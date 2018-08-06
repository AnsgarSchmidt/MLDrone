from __future__      import print_function
import pyzbar.pyzbar as     pyzbar
import numpy         as     np
import time
import glob
import cv2

BEST_SIZE       = 450
BEST_SIZE_DELTA = 50
POSITION_DELTA  = 100
IMAGE_WIDTH     = 1920
IMAGE_HEIGHT    = 1080

def decode(image, filenumber):
  decodedObjects = pyzbar.decode(image)
  #cv2.imwrite("neu/test-%08d.png" % filenumber, image)

  for obj in decodedObjects:
        
    if "QRCODE" != obj.type:
          continue

    points = obj.polygon

    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points

    for j in range(0, len(hull)):
      cv2.line(im, hull[j], hull[ (j+1) % len(hull)], (255,0,0), 3)

    tx, ty, tw, th = cv2.boundingRect(np.array([point for point in points], dtype=np.float32))
    size           = np.average([tw, th])
    cx             = tx + (tw / 2.0)
    cy             = ty + (th / 2.0)

    cv2.imwrite("neu/%04d-%04d-%04d-%07d%s" % (size, cx, cy, filenumber, ".png"), im)
    return obj.data, size, cx, cy

  return None, None, None, None

if __name__ == '__main__':
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  IMAGE_WIDTH  )
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT )
    cap.set(cv2.CAP_PROP_AUTOFOCUS,    0            )
    
    for i in range(30):
   
      ret, im = cap.read()
      
      if not ret:
        continue

      id, size, cx, cy = decode(im, time.time())
      print("done")
      MOVETO = [0, 0, 0] # Z, X, Y

      if id and size and cx and cy:

        dx = cx - (IMAGE_WIDTH  / 2.0)
        dy = cy - (IMAGE_HEIGHT / 2.0)

        if size > (BEST_SIZE + BEST_SIZE_DELTA):
          MOVETO[0] = -1
        
        if size < (BEST_SIZE - BEST_SIZE_DELTA):
          MOVETO[0] = 1
      
        if dx < (-1 * POSITION_DELTA):
          MOVETO[1] = -1
   
        if dx > POSITION_DELTA:
          MOVETO[1] = 1

        if dy < (-1 * POSITION_DELTA):
          MOVETO[2] = -1
        
        if dy > POSITION_DELTA:
          MOVETO[2] = 1

        print(MOVETO)