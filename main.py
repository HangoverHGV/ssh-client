import wx
from GUI.window import App

def main():
    app = wx.App(False)
    frame = App(None, title="SSH-Client")
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()