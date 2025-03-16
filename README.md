# ssh-Manager

## Windows Installation
```bat
pyinstaller --onefile --noconsole main.py
```

## Linux Installation

In etc/ssh-client run:
```bash
pyinstaller --onefile --noconsole main.py```
```

Then:

```bash
cd ../../..
dpkg-deb --build ssh-client
sudo dpkg -i ssh-client.deb
```
