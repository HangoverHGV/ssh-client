import wx

class SaveConfigDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Save Configuration", size=(300, 150))
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, label="Config Name:")
        hbox1.Add(label, flag=wx.RIGHT, border=8)
        self.config_name_input = wx.TextCtrl(panel)
        hbox1.Add(self.config_name_input, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(panel, label="Save")
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        hbox2.Add(save_button, flag=wx.ALIGN_CENTER)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

    def on_save(self, event):
        config_name = self.config_name_input.GetValue()
        parent_configs_name = [confs['name'] for confs in self.parent.configs]
        if config_name:
            if config_name in parent_configs_name:
                wx.MessageBox('Config name already exists', 'Error', wx.OK | wx.ICON_ERROR)
            else:
                self.parent.save_configs(config_name)
                self.Close()
        else:
            wx.MessageBox('Config name cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)