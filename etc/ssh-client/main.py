import wx
from GUI.window import App

def main():
    app = wx.App(False)
    frame = App(None, title="SSH-Manager")
    icon = wx.Icon('icon.png', wx.BITMAP_TYPE_PNG)
    frame.SetIcon(icon)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()