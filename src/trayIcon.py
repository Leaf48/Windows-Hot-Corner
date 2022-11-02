from pystray import Icon, MenuItem, Menu
from PIL import Image
from pynput.mouse import Controller
import keyboard
from time import sleep
from win32api import GetSystemMetrics
from AppOpener import run
import psutil
from threading import Thread

isExit = False


def getProcessByName(psName):
    for proc in psutil.process_iter():
        if proc.name() == psName:
            print(proc.name())
            proc.kill()


class HotCorner:
    def __init__(self, keyInput, app, appProcess):
        self.mouse = Controller()
        self.isOpened = False

        self.keyInput = keyInput
        self.app = app
        self.appProcess = appProcess

    def hotCorner(self):
        while True:
            if isExit:
                break

            position = self.mouse.position

            x = position[0]
            y = position[1]
            # print(x, y)

            topRight = GetSystemMetrics(0) - 1
            bottomRight = GetSystemMetrics(1) - 1

            if x == topRight and y == 0:
                keyboard.press_and_release(self.keyInput)
                sleep(1)

            elif x == topRight and y == bottomRight:
                if not self.isOpened:
                    self.isOpened = True
                    run(self.app)
                    sleep(0.5)
                    keyboard.press_and_release("ctrl+n")
                    sleep(1)
                else:
                    self.isOpened = False
                    getProcessByName(self.appProcess)
                    sleep(1)

            sleep(0.2)


class Tray:
    def __init__(self, image, keyInput, app, appProcess):
        image = Image.open(image)

        menu = Menu(
            MenuItem("Exit", self.exit)
        )

        self.icon = Icon(name="Hot Corner", title="HotCorner", icon=image, menu=menu)

        self.keyInput = keyInput
        self.app = app
        self.appProcess = appProcess

    def exit(self):
        global isExit
        isExit = True

        self.icon.stop()

    def runProgram(self):
        hc = HotCorner(keyInput=self.keyInput, app=self.app, appProcess=self.appProcess)
        tsk = Thread(target=hc.hotCorner)
        tsk.start()

        self.icon.run()
