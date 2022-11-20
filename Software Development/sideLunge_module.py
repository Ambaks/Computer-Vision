import datetime
from datetime import timedelta
import cv2
import numpy as np

import PoseEstimationModule
import PoseEstimationModule as pm
import matplotlib.pyplot as plt


plt.style.use('seaborn')

cap = cv2.VideoCapture("side_lunge.mp4")
detector = pm.poseDetector()
count = -.5
dir = 0
tlist = []
ylist = []


while True:
    success, img = cap.read()
    if success:
        img = detector.findPose(img, draw=False)
        lmlist = detector.findPosition(img, draw=False)


        if len(lmlist) != 0:
            angle = detector.find_angle(img, 24, 26, 28)
            per = np.interp(angle,(115, 170),(0, 100))

            # Check for squats
            if per >= 95:
                if dir == 0:
                    count += 0.5
                    dir = 1

            if per <= 7:
                if dir == 1:
                    count += 0.5
                    dir = 0

            ylist.append(int(per))
            tlist.append(datetime.datetime.now())

        cv2.putText(img, f'Reps: {str(int(count))}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    else:
        plt.plot_date(tlist, ylist)
        plt.title('Side lunge Range Of Motion / time')
        plt.gcf().autofmt_xdate()
        plt.show()
        rep_time = max(tlist) - min(tlist)
        pm.printResults(count, rep_time)
        PoseEstimationModule.poseDetector.printResults(count, rep_time)
        break

    cv2.imshow("Image", img)
    cv2.waitKey(1)

