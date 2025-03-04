import wx
import requests


class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(None, title='Settings', size=(300, 200))
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.label = wx.StaticText(panel, label='API Key')
        hbox1.Add(self.label, flag=wx.RIGHT, border=8)
        self.text = wx.TextCtrl(panel)
        hbox1.Add(self.text, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_server = wx.StaticText(panel, label='Server')
        hbox2.Add(self.label_server, flag=wx.RIGHT, border=8)
        self.text_server = wx.TextCtrl(panel)
        hbox2.Add(self.text_server, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sync_button = wx.CheckBox(panel, label='Sync')
        hbox3.Add(self.sync_button)
        vbox.Add(hbox3, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        vbox.Add((-1, 10))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.test_connectio_button = wx.Button(panel, label='Test Connection')
        self.test_connectio_button.Bind(wx.EVT_BUTTON, self.on_test_connection)
        hbox4.Add(self.test_connectio_button)
        self.ok_button = wx.Button(panel, label='OK')
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        hbox4.Add(self.ok_button)
        self.cancel_button = wx.Button(panel, label='Cancel')
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox4.Add(self.cancel_button, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox4, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_consection = wx.StaticText(panel, label='')
        hbox5.Add(self.label_consection)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        panel.SetSizer(vbox)

    def on_test_connection(self, event):
        api_key = self.text.GetValue()
        server = self.text_server.GetValue()
        response = requests.get(f'{server}/api/v1/test', headers={'Authorization': f'Bearer {api_key}'})
        if response.status_code == 200:
            self.label_consection.SetLabel('Connection successful')

    def on_ok(self, event):
        self.Close()

    def on_cancel(self, event):
        self.Close()
