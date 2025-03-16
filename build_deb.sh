#!/bin/bash

# Variables
APP_NAME="ssh-manager"
VERSION="v1.0.2"
ARCH="amd64"
MAINTAINER="Hangover <hangobogdan@gmail.com>"
DESCRIPTION="SSH Manager Application"
DEPENDENCIES="python3, python3-pip, python3-pyqt5"

# Create a temporary directory for the package
TEMP_DIR=$(mktemp -d)
INSTALL_DIR="$TEMP_DIR/usr/local/$APP_NAME"

# Create necessary directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$TEMP_DIR/usr/share/applications"
mkdir -p "$TEMP_DIR/usr/share/icons/hicolor/48x48/apps"

# Build the application using PyInstaller
pyinstaller --onefile --noconsole main.py

# Copy the built application
cp dist/main "$INSTALL_DIR/$APP_NAME"

# Create a desktop entry
cat <<EOF > "$TEMP_DIR/usr/share/applications/$APP_NAME.desktop"
[Desktop Entry]
Name=SSH Manager
Comment=$DESCRIPTION
Exec=/usr/local/$APP_NAME/$APP_NAME
Icon=/usr/local/$APP_NAME/icon.png
Terminal=false
Type=Application
Categories=Utility;
EOF

# Copy the icon
cp icon.png "$TEMP_DIR/usr/share/icons/hicolor/48x48/apps/icon.png"

# Build the .deb package
fpm -s dir -t deb -n "$APP_NAME" -v "$VERSION" -a "$ARCH" --description "$DESCRIPTION" \
    --maintainer "$MAINTAINER" --depends "$DEPENDENCIES" \
    -C "$TEMP_DIR" .

# Clean up
rm -rf "$TEMP_DIR"