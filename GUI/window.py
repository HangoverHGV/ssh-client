import sys
import os
import json
import base64
import copy
import requests
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QCheckBox, QComboBox, QFileDialog, QMessageBox, QAction, QTextEdit,
                             QDesktopWidget)
from cryptography.fernet import Fernet, InvalidToken
from GUI.settings_dialog import SettingsDialog
from GUI.config_dialog import ConfigDialog


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SSH Manager')
        self.setGeometry(100, 100, 1000, 700)
        self.center()
        self.init_ui()
        self.configs_file = self.init_configs_paths('configs.json', [])
        self.configs = self.load_configs(self.configs_file)
        self.settings_file = self.init_configs_paths('settings.json')
        self.settings = self.load_configs(self.settings_file)
        self.key = self.generate_key()
        self.cipher = Fernet(self.key)
        self.sync = self.settings.get('connection', {}).get('sync', False)
        self.populate_configs_dropdown()
        self.load_theme()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def init_ui(self):
        self.create_menu()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox = QVBoxLayout()

        # First row
        hbox1 = QHBoxLayout()
        self.label = QLabel("Hostname:")
        # hbox1.addWidget(self.label)
        vbox.addLayout(hbox1)

        # Second row
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.label)
        self.ip_input = QLineEdit()
        hbox2.addWidget(self.ip_input)
        self.port_label = QLabel("Port:")
        hbox2.addWidget(self.port_label)
        self.port_input = QLineEdit()
        hbox2.addWidget(self.port_input)
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.ssh_connect)
        hbox2.addWidget(self.connect_button)
        vbox.addLayout(hbox2)

        # Third row
        hbox3 = QHBoxLayout()
        self.private_key_lbl = QLabel("Private Key:")
        hbox3.addWidget(self.private_key_lbl)
        self.private_key_path = QLineEdit()
        hbox3.addWidget(self.private_key_path)
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_file)
        hbox3.addWidget(self.browse_button)
        vbox.addLayout(hbox3)

        # Fourth row
        hbox4 = QHBoxLayout()
        self.private_key_value_lbl = QLabel("Private Key Value:")
        hbox4.addWidget(self.private_key_value_lbl)
        self.private_key_value = QTextEdit()
        self.private_key_value.setMinimumSize(600, 300)
        hbox4.addWidget(self.private_key_value)
        self.private_key_value.setDisabled(True)
        vbox.addLayout(hbox4)

        # Check button row
        hbox5 = QHBoxLayout()
        self.use_value_check = QCheckBox("Use Private Key Value")
        self.use_value_check.stateChanged.connect(self.on_use_value_check)
        hbox5.addWidget(self.use_value_check)
        vbox.addLayout(hbox5)

        # Configs dropdown row
        hbox6 = QHBoxLayout()
        self.configs_dropdown = QComboBox()
        self.configs_dropdown.currentIndexChanged.connect(self.on_config_selected)
        hbox6.addWidget(self.configs_dropdown)
        vbox.addLayout(hbox6)

        # Save button row
        hbox7 = QHBoxLayout()
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        hbox7.addWidget(self.name_label)
        hbox7.addWidget(self.name_input)
        self.save_configs_button = QPushButton("Save Configs")
        self.save_configs_button.clicked.connect(self.on_save_configs_click)
        hbox7.addWidget(self.save_configs_button)
        self.delete_config_button = QPushButton("Delete Config")
        self.delete_config_button.clicked.connect(self.on_delete_config)
        hbox7.addWidget(self.delete_config_button)
        vbox.addLayout(hbox7)

        central_widget.setLayout(vbox)

    def create_menu(self):
        menubar = self.menuBar()
        edit = menubar.addMenu('Edit')

        open_settings_action = QAction('Settings', self)
        open_settings_action.triggered.connect(self.open_settings_dialog)
        edit.addAction(open_settings_action)

        open_config_action = QAction('Appearance', self)
        open_config_action.triggered.connect(self.open_config_dialog)
        edit.addAction(open_config_action)

    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def open_config_dialog(self):
        config_dialog = ConfigDialog(self)
        config_dialog.exec_()

    def generate_key(self):
        configs_folder = os.path.join(os.getcwd(), '.configs')
        key_file = os.path.join(configs_folder, 'key.key')
        if not os.path.exists(key_file):
            key = b'Qnbde_-ONcSIOP6fTG8OSYHCaiQ572o7MjjBavvmJRw='
            with open(key_file, 'wb') as f:
                f.write(key)
        else:
            with open(key_file, 'rb') as f:
                key = f.read()
        return key

    def init_configs_paths(self, file_name='settings.json', init_obj=None):
        if init_obj is None:
            init_obj = {'appearance': {'theme': 'Light', 'font_color': '#000000', 'font_size': 12}}
        configs_folder = os.path.join(os.getcwd(), '.configs')
        if not os.path.exists(configs_folder):
            os.makedirs(configs_folder)
        config_file = os.path.join(configs_folder, file_name)
        if not os.path.exists(config_file):
            with open(config_file, 'w') as f:
                json.dump(init_obj, f)
        return config_file

    def load_configs(self, config_file):
        with open(config_file, 'r') as f:
            configs = json.load(f)
        return configs

    def save_configs_json(self, config_file, configs, setting_key=None):
        if setting_key is None:
            with open(config_file, 'w') as f:
                json.dump(configs, f)
        else:
            settings = self.load_configs(config_file)
            settings[setting_key] = configs
            with open(config_file, 'w') as f:
                json.dump(settings, f)

    def apply_theme(self, theme):
        if theme == 'Dark':
            self.centralWidget().setStyleSheet("""
                QWidget {
                    background-color: #2D2D30;
                    color: #FFFFFF;
                }
                QLineEdit, QComboBox, QPushButton, QTextEdit {
                    background-color: #3E3E42;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                }
            """)
        else:
            self.centralWidget().setStyleSheet("""
                QWidget {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                QLineEdit, QComboBox, QPushButton, QTextEdit {
                    background-color: #F0F0F0;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                }
            """)

    def apply_font_size(self, font_size):
        self.setStyleSheet(f"""
            QWidget {{
                font-size: {font_size}px;
            }}
        """)

    def load_theme(self):
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)
        appearance = settings.get('appearance', {})
        theme = appearance.get('theme', 'Light')
        font_size = appearance.get('font_size', 12)
        self.apply_theme(theme)
        self.apply_font_size(font_size)

    def on_delete_config(self):
        selected_config = self.configs_dropdown.currentText()
        if selected_config:
            self.delete_config(selected_config)

    def delete_config(self, config_name):
        self.configs = [conf for conf in self.configs if conf['name'] != config_name]
        self.save_configs_json(self.configs_file, self.configs)
        self.populate_configs_dropdown()
        self.configs_dropdown.setCurrentIndex(0)
        self.clear_all_fields()

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Private Key File", "",
                                                   "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            self.private_key_path.setText(file_name)

    def on_use_value_check(self):
        if self.use_value_check.isChecked():
            self.private_key_path.setDisabled(True)
            self.browse_button.setDisabled(True)
            self.private_key_value.setEnabled(True)
        else:
            self.private_key_path.setEnabled(True)
            self.browse_button.setEnabled(True)
            self.private_key_value.setDisabled(True)

    def populate_configs_dropdown(self):
        config_names = [conf['name'] for conf in self.configs]
        config_names.insert(0, 'None')
        self.configs_dropdown.clear()
        self.configs_dropdown.addItems(config_names)
        self.configs_dropdown.setCurrentIndex(0)

    def on_config_selected(self):
        selected_config_name = self.configs_dropdown.currentText()
        if selected_config_name == 'None':
            self.clear_all_fields()
        else:
            selected_config = next((conf for conf in self.configs if conf['name'] == selected_config_name), None)
            if selected_config:
                self.ip_input.setText(selected_config.get('hostname', ''))
                self.port_input.setText(selected_config.get('port', ''))
                self.private_key_path.setText(selected_config.get('private_key', ''))
                self.private_key_value.setText('')
                self.use_value_check.setChecked(False)
                self.private_key_value.setDisabled(True)
                self.private_key_path.setEnabled(True)
                self.browse_button.setEnabled(True)
                self.name_input.setText(selected_config.get('name', ''))

    def clear_all_fields(self):
        self.ip_input.clear()
        self.port_input.clear()
        self.private_key_path.clear()
        self.private_key_value.clear()
        self.use_value_check.setChecked(False)
        self.private_key_value.setDisabled(True)
        self.private_key_path.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.name_input.clear()

    def encrypt_ssh(self, ssh_key):
        encrypted_key = self.cipher.encrypt(ssh_key.encode('utf-8'))
        return encrypted_key

    def decrypt_ssh(self, ssh_key):
        try:
            decrypted_key = self.cipher.decrypt(base64.urlsafe_b64decode(ssh_key)).decode('utf-8')
            return decrypted_key
        except InvalidToken:
            QMessageBox.critical(self, 'Error', 'Failed to decrypt the SSH key. The token is invalid.')
            return None

    def _format_config(self, config):
        config_to_return = []
        for c in config:
            if 'private_key' in c:
                if os.path.exists(c['private_key']):
                    with open(c['private_key'], 'r') as f:
                        encrypted_key = self.encrypt_ssh(f.read())
                        c['private_key'] = base64.urlsafe_b64encode(encrypted_key).decode('utf-8')
            config_to_return.append(c)
        return config_to_return

    def sync_config(self, config):
        url = self.settings.get('connection', {}).get('server', '')
        api_key = self.settings.get('connection', {}).get('api_key', '')
        if url and api_key:
            conf = copy.deepcopy(config)
            conf = self._format_config(conf)
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            try:
                response = requests.post(f'{url}/user/config', headers=headers, json=conf)
                if response.status_code == 200:
                    QMessageBox.information(self, 'Info', 'Configurations synced successfully')
                else:
                    QMessageBox.critical(self, 'Error', f'Failed to sync configurations: {response.json()["detail"]}')
            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, 'Error', f'Failed to sync configurations: {str(e)}')

    def on_save_configs_click(self):
        config_name = self.name_input.text()
        if config_name:
            reply = QMessageBox.question(self, 'Confirm Save',
                                         f"Do you want to save the configuration '{config_name}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save_configs(config_name)
                self.configs_dropdown.setCurrentText(config_name)
        else:
            QMessageBox.critical(self, 'Error', 'Config name cannot be empty')

    def save_to_ssh_folder(self, private_key_value, file_name):
        ssh_folder = os.path.join(os.path.expanduser('~'), '.ssh')
        if not os.path.exists(ssh_folder):
            os.makedirs(ssh_folder)
        file_path = os.path.join(ssh_folder, file_name)
        with open(file_path, 'w') as f:
            f.write(private_key_value)
        try:
            os.chmod(file_path, 0o600)
        except PermissionError:
            QMessageBox.critical(self, 'Error', 'Failed to change the permission of the private key file')
        return file_path

    def save_configs(self, config_name):
        save_config = {}
        save_config['name'] = config_name
        save_config['hostname'] = self.ip_input.text()
        save_config['port'] = self.port_input.text()

        if not self.use_value_check.isChecked():
            save_config['private_key'] = self.private_key_path.text()
        elif self.use_value_check.isChecked():
            if self.private_key_value.toPlainText() != '' or not self.private_key_value.toPlainText().isspace():
                private_key_file = self.save_to_ssh_folder(self.private_key_value.toPlainText(), config_name)
                save_config['private_key'] = private_key_file
                QMessageBox.information(self, 'Info', f'Saved private key to {private_key_file}')
        else:
            save_config['private_key'] = None

        existing_config = next((conf for conf in self.configs if conf['name'] == config_name), None)
        if existing_config:
            existing_config.update(save_config)
        else:
            self.configs.append(save_config)

        self.save_configs_json(self.configs_file, self.configs)
        self.configs = self.load_configs(self.configs_file)
        self.populate_configs_dropdown()
        if self.sync:
            self.sync_config(self.configs)

    def ssh_connect(self):
        host = self.ip_input.text()
        user = ''
        if '@' in host:
            user, host = host.split('@')
        port = self.port_input.text() or '22'
        private_key = self.private_key_path.text()

        if self.use_value_check.isChecked():
            private_key_value = self.private_key_value.toPlainText()
            temp_private_key_path = os.path.expanduser(f'~/.ssh/temp_key_{host}')
            with open(temp_private_key_path, 'w') as f:
                f.write(private_key_value)
            os.chmod(temp_private_key_path, 0o600)
            private_key = temp_private_key_path

        self.open_terminal(host, user, port, private_key)

    def open_terminal(self, host, user, port, private_key):
        if host == '' or host.isspace() or host is None:
            QMessageBox.critical(None, 'Error', 'Hostname cannot be empty')
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
            os.system('start cmd /k ' + ' '.join(connection))
        else:  # Unix-based systems
            os.system('x-terminal-emulator -e ' + ' '.join(connection))

        if 'temp_key' in private_key:
            import time
            time.sleep(5)
            if private_key and os.path.exists(private_key):
                os.remove(private_key)
            self.clear_all_fields()
