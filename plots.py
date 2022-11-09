import PoseEstimationModule as pm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import cv2
import mediapipe as mp

cap = cv2.VideoCapture("squats.mp4")
detector = pm.poseDetector()
tlist = []
ylist = []
def getlists():
    while True:
        success, img = cap.read()
        img = detector.findPose(img, draw=False)
        lmlist, time, y = detector.findPosition(img, draw=False)
        print(time)
        tlist.append(time)
        ylist.append(y)
    return tlist, ylist
print(tlist)
# fig = plt.figure(figsize=(6, 3))
#
#  ln, = plt.plot(time, y, '-')
#         plt.axis([0, 100, 0, 10])
#
#
# def update(frame):
#     success, img = cap.read()
#     img = detector.findPose(img, draw=False)
#     lmlist, time, y = detector.findPosition(img, draw=False)
#
#     ln.set_data(time, y)
#     return ln,
#
#
# animation = FuncAnimation(fig, update, interval=500)
# plt.show()