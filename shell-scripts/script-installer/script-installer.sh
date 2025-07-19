#!/bin/bash
# Usage: ./script-installer.sh /path/to/script [command-name]

set -e

SCRIPT_PATH="$1"
CMD_NAME="$2"

if [ -z "$SCRIPT_PATH" ]; then
    echo "Usage: $0 /path/to/script [command-name]"
    exit 1
fi

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Script '$SCRIPT_PATH' not found."
    exit 1
fi

# Default command name is the script filename
if [ -z "$CMD_NAME" ]; then
    CMD_NAME="$(basename "$SCRIPT_PATH")"
fi

# Choose install directory
INSTALL_DIR="$HOME/bin"
if [ ! -d "$INSTALL_DIR" ]; then
    mkdir -p "$INSTALL_DIR"
fi

# Make script executable
chmod +x "$SCRIPT_PATH"

# Create symlink
ln -sf "$SCRIPT_PATH" "$INSTALL_DIR/$CMD_NAME"
echo "✅ Installed '$CMD_NAME' as a command in $INSTALL_DIR."

# Add INSTALL_DIR to PATH if not already
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    SHELL_RC="$HOME/.bashrc"
    [ "$SHELL" = "/bin/zsh" ] && SHELL_RC="$HOME/.zshrc"
    echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$SHELL_RC"
    echo "🔔 Added $INSTALL_DIR to PATH in $SHELL_RC. Please restart your shell or run: source $SHELL_RC"
fi
