import wx


class AppearanceDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Appearance Settings", size=(300, 250))
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Theme selection
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        theme_label = wx.StaticText(panel, label="Theme:")
        hbox1.Add(theme_label, flag=wx.RIGHT, border=8)
        self.theme_choice = wx.Choice(panel, choices=["light", "dark"])
        self.theme_choice.SetStringSelection(self.parent.settings.get('theme', 'light'))
        self.theme_choice.Bind(wx.EVT_CHOICE, self.on_theme_change)
        hbox1.Add(self.theme_choice, flag=wx.EXPAND)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=10)

        # Font size selection
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        font_size_label = wx.StaticText(panel, label="Font Size:")
        hbox2.Add(font_size_label, flag=wx.RIGHT, border=8)
        self.font_size_choice = wx.Choice(panel, choices=[str(i) for i in range(8, 25)])
        self.font_size_choice.SetStringSelection(str(self.parent.settings.get('font_size', 12)))
        hbox2.Add(self.font_size_choice, flag=wx.EXPAND)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.ALL, border=10)

        # Save button
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(panel, label="Save")
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        hbox3.Add(save_button, flag=wx.ALIGN_CENTER)
        vbox.Add(hbox3, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

    def on_theme_change(self, event):
        selected_theme = self.theme_choice.GetStringSelection()
        font_color = '#FFFFFF' if selected_theme == 'dark' else '#000000'
        self.parent.change_theme(selected_theme, font_color, int(self.font_size_choice.GetStringSelection()))

    def on_save(self, event):
        selected_theme = self.theme_choice.GetStringSelection()
        selected_font_size = int(self.font_size_choice.GetStringSelection())
        font_color = '#FFFFFF' if selected_theme == 'dark' else '#000000'
        self.parent.save_theme(selected_theme, font_color, selected_font_size)
        self.Close()
