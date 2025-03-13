from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox
                             , QDesktopWidget)
import requests
import json
import os
import random


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 400, 300)
        self.parent = parent
        self.center()
        self.init_ui()
        self.load_settings()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def init_ui(self):
        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        self.label = QLabel('API Key')
        hbox1.addWidget(self.label)
        self.text = QLineEdit()
        hbox1.addWidget(self.text)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        self.label_server = QLabel('Server')
        hbox2.addWidget(self.label_server)
        self.text_server = QLineEdit()
        hbox2.addWidget(self.text_server)
        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        self.sync_button = QCheckBox('Sync')
        hbox3.addWidget(self.sync_button)
        vbox.addLayout(hbox3)

        hbox4 = QHBoxLayout()
        self.test_connection_button = QPushButton('Test Connection')
        self.test_connection_button.clicked.connect(self.on_test_connection)
        hbox4.addWidget(self.test_connection_button)
        self.ok_button = QPushButton('Save')
        self.ok_button.clicked.connect(self.on_save)
        hbox4.addWidget(self.ok_button)
        self.get_config_button = QPushButton('Get Config')
        self.get_config_button.clicked.connect(self.on_get_config)
        hbox4.addWidget(self.get_config_button)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.on_cancel)
        hbox4.addWidget(self.cancel_button)
        vbox.addLayout(hbox4)

        hbox5 = QHBoxLayout()
        self.label_connection = QLabel('')
        hbox5.addWidget(self.label_connection)
        vbox.addLayout(hbox5)

        self.setLayout(vbox)

    def load_settings(self):
        settings = self.parent.load_configs(self.parent.settings_file)
        connection = settings.get('connection', {})
        self.text.setText(connection.get('api_key', ''))
        self.text_server.setText(connection.get('server', ''))
        self.sync_button.setChecked(connection.get('sync', False))

    def on_test_connection(self):
        api_key = self.text.text()
        server = self.text_server.text()
        try:
            response = requests.get(f'{server}/user/my/user', headers={'Authorization': f'Bearer {api_key}'})
        except:
            self.label_connection.setText('Connection failed')
            return
        if response.status_code == 200:
            self.label_connection.setText(f'Connection successful: {response.status_code}')
        else:
            self.label_connection.setText(f'Connection failed: {response.status_code}')

    def on_save(self):
        connection_dict = {
            'api_key': self.text.text(),
            'server': self.text_server.text(),
            'sync': self.sync_button.isChecked()
        }
        settings = self.parent.load_configs(self.parent.settings_file)
        settings['connection'] = connection_dict
        self.parent.sync = connection_dict['sync']

        with open(self.parent.settings_file, 'w') as f:
            json.dump(settings, f)

    def on_get_config(self):
        api_key = self.text.text()
        server = self.text_server.text()
        try:
            response = requests.post(f'{server}/user/config/data', headers={'Authorization': f'Bearer {api_key}'})
        except:
            self.label_connection.setText('Connection failed')
            return

        if response.status_code == 200:
            self.label_connection.setText(f'Config fetched successfully: {response.status_code}')
            fetched_configs = response.json()

            ssh_folder = os.path.join(os.path.expanduser('~'), '.ssh')
            if not os.path.exists(ssh_folder):
                os.makedirs(ssh_folder)

            for fetched_config in fetched_configs:
                private_key_value = fetched_config.get('private_key', '')
                private_key_path = None
                if private_key_value != '':
                    private_key_value = self.parent.decrypt_ssh(private_key_value)
                if os.path.exists(ssh_folder):
                    for file_name in os.listdir(ssh_folder):
                        file_path = os.path.join(ssh_folder, file_name)
                        if os.path.isfile(file_path):
                            with open(file_path, 'r') as f:
                                if f.read().strip() == private_key_value.strip():
                                    private_key_path = file_path
                                    break

                if not private_key_path:
                    random_suffix = random.randint(100, 999)
                    private_key_path = os.path.join(ssh_folder, f'key_{fetched_config["name"]}_{random_suffix}')
                    with open(private_key_path, 'w') as f:
                        f.write(private_key_value)

                try:
                    os.chmod(private_key_path, 0o600)
                except Exception as e:
                    self.label_connection.setText(f'Error changing permission of private key: {e}')

                fetched_config['private_key'] = private_key_path

            selected_config_name = self.parent.configs_dropdown.currentText()

            with open(self.parent.configs_file, 'w') as f:
                json.dump(fetched_configs, f)

            self.parent.configs = fetched_configs
            self.parent.populate_configs_dropdown()

            if selected_config_name != 'None':
                selected_config = next((conf for conf in fetched_configs if conf['name'] == selected_config_name), None)
                if selected_config:
                    self.parent.ip_input.setText(selected_config.get('hostname', ''))
                    self.parent.port_input.setText(selected_config.get('port', ''))
                    self.parent.private_key_path.setText(selected_config.get('private_key', ''))
                    self.parent.private_key_value.setText('')
                    self.parent.use_value_check.setChecked(False)
                    self.parent.private_key_value.setDisabled(True)
                    self.parent.private_key_path.setEnabled(True)
                    self.parent.browse_button.setEnabled(True)
                    self.parent.name_input.setText(selected_config.get('name', ''))
            self.parent.configs_dropdown.setCurrentText(selected_config_name)
            self.close()
        else:
            self.label_connection.setText(f'Config fetch failed: {response.status_code}')

    def on_cancel(self):
        self.close()
