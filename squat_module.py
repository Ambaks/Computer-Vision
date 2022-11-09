import datetime
import cv2
import numpy as np
import PoseEstimationModule as pm
import matplotlib.pyplot as plt


class Squat():
    def __init__(self, tlist = [], ylist = [], dir = 0, count = -.5, detector = pm.poseDetector()):
        self.ylist = ylist
        self.tlist = tlist
        self.dir = dir
        self.count = count
        self.detector = detector

    def doSquat(self):

        plt.style.use('fivethirtyeight')

        cap = cv2.VideoCapture('squats.mp4')
        # detector = pm.poseDetector()
        # count = -.5
        # dir = 0
        # tlist = []
        # ylist = []


        while True:
            success, img = cap.read()
            if success:
                img = self.detector.findPose(img, draw=False)
                lmlist = self.detector.findPosition(img, draw=False)


                if len(lmlist) != 0:
                    self.angle = self.detector.find_angle(img, 24, 26, 28)
                    self.per = np.interp(self.angle,(55, 180),(0, 100))

                    # Check for squats
                    if self.per >= 95:
                        if self.dir == 0:
                            self.count += 0.5
                            self.dir = 1

                    if self.per <= 7:
                        if self.dir == 1:
                            self.count += 0.5
                            self.dir = 0

                    self.ylist.append(int(self.per))
                    self.tlist.append(datetime.datetime.now())

                cv2.putText(img, f'Reps: {str(int(self.count))}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            else:
                plot = pm.poseDetector.plotTimeSeries(self.tlist, self.ylist, 'Squat')
                rep_time, set_length, av_rep_length = pm.poseDetector.printResults(self.count, self.tlist)
                break

            cv2.imshow("Image", img)
            cv2.waitKey(1)
        return self.count, rep_time, plot, set_length, av_rep_length


def main():
    perform = Squat()
    perform.doSquat()

if __name__ == '__main__':
    main()