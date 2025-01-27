# Python-KeyLogger

### A Discord-integrated Python Keylogger

This is a simple, Discord-integrated keylogger built using Python. The project includes two main scripts: one for the server that receives keystrokes (`tool_gui.py`) and another for the keylogger to be run on the target computer (`keylogger.py`).

---

## Features

- **Keystroke Logging**: Tracks keystrokes typed on the target computer.
- **Sentence Grouping**: Groups keystrokes into readable sentences, sent upon pressing `Enter`.
- **Discord Integration**: Sends captured sentences to a specified Discord webhook for easy remote access.
- **GUI Server**: The server script (`tool_gui.py`) includes a simple GUI to display real-time logs of captured keystrokes.

---

## Setup Instructions

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/Python-KeyLogger.git
cd Python-KeyLogger
