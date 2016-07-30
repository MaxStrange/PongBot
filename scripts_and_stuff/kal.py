import cv2
import numpy as np

# Drawing canvas
frame = np.zeros((400, 400, 3), np.uint8)

# Measurement
meas = []
mp = np.array((2, 1), np.float32)

# Tracked/Prediction
pred = []
tp = np.zeros((2, 1), np.float32)

def onmouse(k, x, y, p):
    '''
    Call-back function for mouse movement?
    '''
    global mp, meas
    mp = np.array([
                    [np.float32(x)],
                    [np.float32(y)]
                    ])
    meas.append((x, y))

def paint():
    global frame, meas, pred
    for i in range(len(meas) - 1):
        cv2.line(frame, meas[i], meas[i + 1], (0, 100, 0))
    for i in range(len(pred) - 1):
        cv2.line(frame, pred[i], pred[i + 1], (0, 0, 200))

def reset():
    global frame, meas, pred
    meas = []
    pred = []
    frame = np.zeros((400, 400, 3), np.uint8)

cv2.namedWindow("kalman")
cv2.setMouseCallback("kalman", onmouse)

kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([
                                    [1, 0, 0, 0],
                                    [0, 1, 0, 0]
                                    ], np.float32)
kalman.transitionMatrix = np.array([
                                    [1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [0, 0, 0, 1]
                                    ], np.float32)
kalman.processNoiseCov = np.array([
                                    [1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]
                                    ], np.float32) * 0.03
#kalman.measurementNoiseCov = np.array([
#                                    [1, 0],
#                                    [0, 1]
#                                    ], np.float32) * 0.00003

while True:
    kalman.correct(mp)
    tp = kalman.predict()
    
    pred.append(int(tp[0]), int(tp[1]))
    
    paint()
    cv2.imshow("kalman", frame)
    
    k = cv2.waitKey(30) & 0xFF
    if k is 27:
        break
    elif k is 32:
        reset()
