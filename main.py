from figure import Figure
import cv2

class Main:
    def __init__(self):
        figure = Figure('okamura.png')
        figure.saveJSON('out.json')
        while True:
            figure.draw()
            key = cv2.waitKey(33)
            if key == ord('q'):
                break



if __name__ == '__main__':
    Main()

