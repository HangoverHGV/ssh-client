import wx
from GUI.window import App
import os

def main():
    app = wx.App(False)
    frame = App(None, title="SSH-Manager")
    app_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(app_dir, 'icon.png')
    icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
    frame.SetIcon(icon)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()