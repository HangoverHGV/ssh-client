import subprocess
import wx
import os
import multiprocessing as mp
import json


class App(wx.Frame):
    def __init__(self, *args, **kw):
        super(App, self).__init__(*args, **kw)
        self.SetSize((600, 400))  # Set the initial size of the frame
        self.initUI()
        self.config_file = self.init_configs_paths()
        self.configs = self.load_configs(self.config_file)
        self.populate_configs_dropdown()

    @staticmethod
    def init_configs_paths():
        configs_folder = os.path.join(os.getcwd(), '.configs')
        if not os.path.exists(configs_folder):
            os.makedirs(configs_folder)
        config_file = os.path.join(configs_folder, 'config.json')
        if not os.path.exists(config_file):
            with open(config_file, 'w') as f:
                json.dump({}, f)
        return config_file

    @staticmethod
    def load_configs(config_file):
        with open(config_file, 'r') as f:
            configs = json.load(f)
        return configs

    @staticmethod
    def save_configs_json(config_file, configs):
        with open(config_file, 'w') as f:
            json.dump(configs, f)

    def initUI(self):
        self.create_menu_bar()

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

        # Fourth row
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.private_key_value_lbl = wx.StaticText(panel, label="Private Key Value:")
        hbox4.Add(self.private_key_value_lbl, flag=wx.RIGHT, border=8)
        self.private_key_value = wx.TextCtrl(panel, style=wx.TE_MULTILINE)  # Multi-line text box
        hbox4.Add(self.private_key_value, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.private_key_value.SetMinSize((400, 100))
        self.private_key_value.Disable()

        # Check button row
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.use_value_check = wx.CheckBox(panel, label="Use Private Key Value")
        self.use_value_check.Bind(wx.EVT_CHECKBOX, self.on_use_value_check)
        hbox5.Add(self.use_value_check, flag=wx.RIGHT, border=8)
        vbox.Add(hbox5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Configs dropdown row
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.configs_dropdown = wx.Choice(panel)
        hbox6.Add(self.configs_dropdown, flag=wx.RIGHT, border=8)
        vbox.Add(hbox6, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Save button row
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        self.save_setting = wx.Button(panel, label="Save Configs")
        hbox7.Add(self.save_setting, flag=wx.RIGHT, border=8)

        self.load_setting = wx.Button(panel, label="Load Configs")
        hbox7.Add(self.load_setting, flag=wx.RIGHT, border=8)
        vbox.Add(hbox7, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        panel.SetSizer(vbox)

    def create_menu_bar(self):
        menubar = wx.MenuBar()
        edit_menu = wx.Menu()
        theme_item = edit_menu.Append(wx.ID_ANY, 'Change Theme')
        settings_item = edit_menu.Append(wx.ID_ANY, 'Settings')
        menubar.Append(edit_menu, '&Edit')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.on_change_theme, theme_item)
        self.Bind(wx.EVT_MENU, self.on_settings, settings_item)

    def on_change_theme(self, event):
        wx.MessageBox('Change Theme clicked', 'Info', wx.OK | wx.ICON_INFORMATION)

    def on_settings(self, event):
        wx.MessageBox('Settings clicked', 'Info', wx.OK | wx.ICON_INFORMATION)

    def browse_file(self, event):
        with wx.FileDialog(self, "Select Private Key File", wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.private_key_path.SetValue(fileDialog.GetPath())

    def on_use_value_check(self, event):
        if self.use_value_check.IsChecked():
            self.private_key_path.Disable()
            self.browse_button.Disable()
            self.private_key_value.Enable()
            self.private_key_value.SetMinSize((400, 100))  # Increase the size of the text box
        else:
            self.private_key_path.Enable()
            self.browse_button.Enable()
            self.private_key_value.Disable()
            self.private_key_value.SetMinSize((200, 30))  # Reset the size of the text box

        self.Layout()  # Adjust the layout dynamically

    def populate_configs_dropdown(self):
        config_names = list(self.configs.keys())
        self.configs_dropdown.SetItems(config_names)

    def save_configs(self, event):
        self.configs['hostname'] = self.ip_input.GetValue()
        self.configs['port'] = self.port_input.GetValue()
        self.configs['private_key'] = self.private_key_path.GetValue()
        self.save_configs_json(self.config_file, self.configs)

    def ssh_connect(self, event):
        host = self.ip_input.GetValue()
        user = ''
        if '@' in host:
            user, host = host.split('@')
        port = self.port_input.GetValue() or '22'
        private_key = self.private_key_path.GetValue()

        if self.use_value_check.IsChecked():
            private_key_value = self.private_key_value.GetValue()
            private_key_path = os.path.expanduser('~/.ssh/id_rsa')
            with open(private_key_path, 'w') as f:
                f.write(private_key_value)
            os.chmod(private_key_path, 0o600)
            private_key = private_key_path

        self.open_terminal(host, user, port, private_key)

    @staticmethod
    def open_terminal(host, user, port, private_key):
        p = mp.Process(target=start_terminal, args=(host, user, port, private_key))
        p.start()
        p.join()


def start_terminal(host, user, port, private_key):
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
