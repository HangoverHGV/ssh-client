import wx
import paramiko
import pyte
import threading
import traceback

class TerminalWindow(wx.Frame):
    def __init__(self, parent, title, host, user, port, private_key):
        super(TerminalWindow, self).__init__(parent, title=title)
        self.host = host
        self.user = user
        self.port = port
        self.private_key = private_key
        self.connection = self.create_connection()
        self.initUI()

    def create_connection(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        pkey = paramiko.RSAKey.from_private_key_file(self.private_key) if self.private_key else None
        client.connect(hostname=self.host, username=self.user, port=self.port, pkey=pkey)
        print("connected")
        return client

    def initUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.terminal_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.terminal_output, proportion=1, flag=wx.EXPAND)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)
        self.start_ssh_session()

    def start_ssh_session(self):
        self.channel = self.connection.get_transport().open_session()
        self.channel.get_pty()
        self.channel.invoke_shell()
        self.screen = pyte.Screen(80, 24)
        self.stream = pyte.Stream(self.screen)
        self.thread = threading.Thread(target=self.update_terminal)
        self.thread.daemon = True
        self.thread.start()

    def update_terminal(self):
        try:
            while True:
                data = self.channel.recv(1024).decode('utf-8')
                self.stream.feed(data)
                wx.CallAfter(self.terminal_output.SetValue, '\n'.join(self.screen.display))
        except Exception as e:
            print("Exception in update_terminal:", e)
            traceback.print_exc()

    def on_key_press(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN:
            self.channel.send('\n')
        else:
            self.channel.send(chr(keycode))
        event.Skip()

    def closeEvent(self, event):
        self.channel.close()
        self.connection.close()
        event.Skip()