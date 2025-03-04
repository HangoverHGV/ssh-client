import wx
import paramiko
import pyte
import threading
import traceback
import socket


class TerminalWindow(wx.Frame):
    def __init__(self, parent, title, host, user, port, private_key, size=(800, 600)):
        super(TerminalWindow, self).__init__(parent, title=title)
        self.host = host
        self.user = user
        self.port = port
        self.private_key = private_key
        self.connection = self.create_connection()
        self.running = False
        if self.connection:
            self.initUI()
            self.SetSize(size)
        else:
            wx.MessageBox('Failed to establish SSH connection', 'Error', wx.OK | wx.ICON_ERROR)
            self.Close()

    def create_connection(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            pkey = paramiko.RSAKey.from_private_key_file(self.private_key) if self.private_key else None
            client.connect(hostname=self.host, username=self.user, port=self.port, pkey=pkey)
            print("connected")
            return client
        except Exception as e:
            print("Exception in create_connection:", e)
            traceback.print_exc()
            return None

    def initUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.terminal_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.terminal_output, proportion=1, flag=wx.EXPAND)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR, self.on_key_press)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.start_ssh_session()

    def start_ssh_session(self):
        self.channel = self.connection.get_transport().open_session()
        self.channel.get_pty()
        self.channel.invoke_shell()
        self.channel.settimeout(1.0)  # Set a timeout on the channel
        self.screen = pyte.Screen(80, 24)
        self.stream = pyte.Stream(self.screen)
        self.running = True
        self.thread = threading.Thread(target=self.update_terminal)
        self.thread.daemon = True
        self.thread.start()

    def update_terminal(self):
        try:
            while self.running:
                try:
                    data = self.channel.recv(1024).decode('utf-8')
                    self.stream.feed(data)
                    if wx.GetApp():
                        wx.CallAfter(self.terminal_output.SetValue, '\n'.join(self.screen.display))
                    else:
                        break
                except socket.timeout:
                    continue
        except Exception as e:
            if self.running:
                print("Exception in update_terminal:", e)
                traceback.print_exc()

    def on_key_press(self, event):
        keycode = event.GetUnicodeKey()
        if keycode == wx.WXK_RETURN:
            self.channel.send('\n')
        else:
            self.channel.send(chr(keycode))
        event.Skip()

    def on_close(self, event):
        print("Closing connection")
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        if self.channel:
            print('closing channel')
            self.channel.close()
        if self.connection:
            print('closing connection')
            self.connection.close()
        print('Destroying window')
        event.Skip()
