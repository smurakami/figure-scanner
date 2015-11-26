from figure import Figure
import cv2
import commands

class Main:
    def __init__(self):
        figure = Figure('okamura.png')
        figure.saveJSON('out.json')
        figure.saveTestPNG('okamura_test.png')
        commands.getoutput('open okamura_test.png')

if __name__ == '__main__':
    Main()

