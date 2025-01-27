# Python-KeyLogger

## Description
Python-KeyLogger is a simple, Discord-integrated keylogger built using Python. It consists of two scripts:

- **`tool_gui.py`**: The server-side script to receive and log keystrokes.
- **`keylogger.py`**: The keylogger script that captures keystrokes on the target machine.

---

## Features
- Logs and groups keystrokes for easy analysis.
- Sends logs to a Discord webhook for remote monitoring.
- Includes a graphical user interface (GUI) for live monitoring.

---

## Setup
Follow these steps to set up and use Python-KeyLogger:

### 1. **Install Python and dependencies**
   - Make sure Python is installed on your system.
   - Install the required dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

### 2. **Configure the scripts**
   - Open `tool_gui.py` and `keylogger.py` in a text editor.
   - Set up the IP, port, and Discord webhook URL according to your requirements.

### 3. **Run the server script**
   - Start `tool_gui.py` on your machine to begin receiving logs.

### 4. **Compile the keylogger script**
   - Use [PyInstaller](https://www.pyinstaller.org/) to compile `keylogger.py` into a standalone `.exe` file:
     ```bash
     pyinstaller --onefile keylogger.py
     ```
   - Distribute the compiled `.exe` to the target machine.

---

## Disclaimer
This tool is intended for educational purposes only. Unauthorized use of keylogging software is illegal and unethical. Please use responsibly.

---

**Note:** Make sure to use this tool only with proper authorization and adhere to all applicable laws and regulations.
