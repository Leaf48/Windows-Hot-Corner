from src.trayIcon import Tray

if __name__ == "__main__":
    # top right keyInput
    keyInput = "win+d"

    # bottom right application
    app = "notepad"
    appProcess = "notepad++.exe"

    t = Tray(image="icon.png", keyInput=keyInput, app=app, appProcess=appProcess)
    t.runProgram()
