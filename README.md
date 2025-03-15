# ssh-Manager

## Windows Installation
```bat
pyinstaller --onefile --noconsole main.py
```

## Linux Installation
```bash
pyinstaller --onefile --noconsole main.py
cd ..
dpkg-deb --build ssh-client
sudo dpkg -i ssh-client.deb
```
