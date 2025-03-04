import subprocess
import wx
import os


class App(wx.Frame):
    def __init__(self, *args, **kw):
        super(App, self).__init__(*args, **kw)
        self.initUI()

    def initUI(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # First row
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.label = wx.StaticText(panel, label="Hostname:")
        hbox1.Add(self.label, flag=wx.RIGHT, border=8)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Second row
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.ip_input = wx.TextCtrl(panel)
        hbox2.Add(self.ip_input, proportion=1)
        self.port_input = wx.TextCtrl(panel)
        hbox2.Add(self.port_input, flag=wx.LEFT, border=10)
        self.connect_button = wx.Button(panel, label='Connect')
        self.connect_button.Bind(wx.EVT_BUTTON, self.ssh_connect)
        hbox2.Add(self.connect_button, flag=wx.LEFT, border=10)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Third row
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.private_key_lbl = wx.StaticText(panel, label="Private Key:")
        hbox3.Add(self.private_key_lbl, flag=wx.RIGHT, border=8)
        self.private_key_path = wx.TextCtrl(panel)
        hbox3.Add(self.private_key_path, proportion=1)
        self.browse_button = wx.Button(panel, label='Browse')
        self.browse_button.Bind(wx.EVT_BUTTON, self.browse_file)
        hbox3.Add(self.browse_button, flag=wx.LEFT, border=10)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        panel.SetSizer(vbox)

    def browse_file(self, event):
        with wx.FileDialog(self, "Select Private Key File", wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.private_key_path.SetValue(fileDialog.GetPath())

    def ssh_connect(self, event):
        host = self.ip_input.GetValue()
        user = ''
        if '@' in host:
            user, host = host.split('@')
        port = self.port_input.GetValue() or '22'
        private_key = self.private_key_path.GetValue()

        self.start_terminal(host, user, port, private_key)

    def start_terminal(self, host, user, port, private_key):
        if host == '' or host.isspace() or host is None:
            wx.MessageBox('Hostname cannot be empty', 'Error', wx.OK | wx.ICON_ERROR)
            return
        connection = ["ssh"]
        if user:
            connection.extend([f"{user}@{host}"])
        else:
            connection.extend([f"{host}"])
        if port:
            connection.extend(["-p", port])
        if private_key:
            connection.extend(["-i", private_key])

        if os.name == 'nt':  # Windows
            subprocess.Popen(['start', 'cmd', '/k'] + connection, shell=True)
        else:  # Unix-based systems
            subprocess.Popen(['x-terminal-emulator', '-e'] + connection)

