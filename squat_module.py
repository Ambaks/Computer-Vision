import datetime
import math

import cv2
import numpy as np

import PoseEstimationModule as pm
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class Squat():
    def __init__(self):
        self.ylist = []
        self.tlist = []
        self.dir = 0
        self.count = -.5
        self.detector = pm.poseDetector()
        self.rep_start = datetime.datetime.now()
        self.repTimes = []
        self.previous_count = -0.5

    def doSquat(self):

        plt.style.use('fivethirtyeight')

        cap = cv2.VideoCapture('squats.mp4')


        while True:
            success, img = cap.read()
            if success:
                img = self.detector.findPose(img, draw=False)
                lmlist = self.detector.findPosition(img, draw=False)


                if len(lmlist) != 0:

                    angle = self.detector.find_angle(img, 24, 26, 28)
                    per = np.interp(angle,(55, 180),(0, 100))


                    # Check for squats
                    if per >= 95:
                        if self.dir == 0:
                            self.count += 0.5
                            self.dir = 1



                    if per <= 7:
                        if self.dir == 1:
                            self.count += 0.5
                            self.dir = 0

                    # Get repetition length
                    if self.count.is_integer() is True and self.count != self.previous_count:
                        self.rep_time = datetime.datetime.now() - self.rep_start
                        self.repTimes.append(int(self.rep_time.seconds) + round(float(self.rep_time.microseconds * 10**-6), 2))
                        self.rep_start = datetime.datetime.now()
                        self.previous_count = self.count



                    self.ylist.append(lmlist[24][2])
                    self.tlist.append(datetime.datetime.now())


                cv2.putText(img, f'Reps: {str(int(self.count))}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            else:
                plot = pm.poseDetector.plotTimeSeries(self.tlist, self.ylist, 'Squat')
                rep_time, set_length, av_rep_length = pm.poseDetector.printResults(self.count, self.tlist)
                self.repTimes.pop(0)
                break

            cv2.imshow("Image", img)
            cv2.waitKey(1)

        return self.count, rep_time, plot, set_length, av_rep_length, print(self.repTimes)


def main():
    perform = Squat()
    perform.doSquat()

if __name__ == '__main__':
    main()