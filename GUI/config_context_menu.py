import wx

class ConfigContextMenu(wx.Menu):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        delete_item = wx.MenuItem(self, wx.ID_ANY, 'Delete')
        self.Append(delete_item)
        self.Bind(wx.EVT_MENU, self.on_delete, delete_item)

    def on_delete(self, event):
        selected_config = self.parent.configs_dropdown.GetStringSelection()
        if selected_config:
            self.parent.delete_config(selected_config)