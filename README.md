-   **Title**: Python-KeyLogger-   **Description**: A simple Discord-integrated keylogger using Python with two scripts:
    -   `tool_gui.py`: The server script to receive and log keystrokes.
    -   `keylogger.py`: The keylogger script to capture keystrokes on the target machine.-   **Features**:
    -   Logs and groups keystrokes.
    -   Sends logs to a Discord webhook.
    -   Includes a GUI for live monitoring.-   **Setup**:
    1.  Install Python and dependencies via `pip install -r requirements.txt`.
    2.  Configure IP, port, and webhook in `tool_gui.py` and `keylogger.py`.
    3.  Run `tool_gui.py` on your machine.
    4.  Compile `keylogger.py` to `.exe` using PyInstaller.
