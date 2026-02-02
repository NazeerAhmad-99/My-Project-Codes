import tkinter as tk
from tkinter import ttk
import socket
import threading
import struct
import queue
from cryptography.fernet import Fernet, InvalidToken
import time


def main():
    root = tk.Tk()
    root.title("Encryption App (LAN)(Nazeer Ahmad)")
    root.geometry("980x640")
    
    sock = None
    server_sock = None
    incoming_queue = queue.Queue()
    messages = {}
    
    
    main_frame = ttk.Frame(root, padding=12)
    main_frame.pack(fill="both", expand=True)
    
    #left side wala frame
    left_frame = ttk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", expand=True, padx=(0,8))
    
    
    #right side wala frame 
    right_frame = ttk.Frame(main_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=(8,0))
    
    #Connection wala section
    connection_frame = ttk.LabelFrame(left_frame, text="Connection", padding=10)
    connection_frame.pack(fill="x", pady=(0, 10))
    
    #Connection to the other guy
    ttk.Label(connection_frame, text="Listen IP").grid(row=0, column=0, sticky="w")
    listen_ip_entry = ttk.Entry(connection_frame, width = 18)
    listen_ip_entry.grid(row=0, column= 1, sticky="w", padx=(6,0))
    
    #port entry field wala section
    ttk.Label(connection_frame, text="Port:").grid(row=0, column=2, sticky="w", padx=(10,0))
    port_entry = ttk.Entry(connection_frame, width=8)
    port_entry.grid(row=0, column=3, sticky="w", padx=(6,0))

    status_label = ttk.Label(connection_frame, text="Status: Not connected")
    status_label.grid(row=3, column=0, columnspan=4, sticky="w", pady=(8,0))

    def set_status(text):
        status_label.config(text=f"Status: {text}")
        
    def start_server():
        nonlocal server_sock, sock
        host = listen_ip_entry.get().strip() or "0.0.0.0"
        port_text = port_entry.get().strip()
        
        if not port_text.isdigit():
            set_status("Invalid number")
            return
        
        port = int(port_text)
        
        def server_thread():
            nonlocal server_sock, sock
            try:
                server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                server_sock.bind((host, port))
                server_sock.listen(1)
                set_status(f"Listening on {host}:{port}")
                client, addr = server_sock.accept()
                sock = client
                set_status(f"Connected to {addr[0]}:{addr[1]}")
                start_reader_thread(sock)
            except Exception as e:
                set_status(f"Server error: {e}")
        threading.Thread(target=server_thread, daemon=True).start()
        
    def connect_to_peer():
        nonlocal sock
        host = connect_ip_entry.get().strip()
        port_text = port_entry.get().strip()
        
        if not host:
            set_status ("Enter peer IP")
            return
        if not port_text.isdigit():
            set_status("Invalid port ")
            return
        port = int (port_text)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host,port))
            set_status(f"Connected to {host}:{port}")
            start_reader_thread(sock)
        except Exception as e:
            set_status(f"Connection failed: {e}")
            
    def disconnect():
        nonlocal sock, server_sock
        try:
            if sock:
                sock.close()
        except Exception:
            pass
        try:
            if server_sock:
                server_sock.close()
        except Exception:
            pass
        sock = None
        server_sock = None
        set_status("Disconnected")
        
    def send_frame(sock_obj, payload):
        length = struct.pack("!I", len(payload))
        sock_obj.sendall(length + payload)
        
    def recv_exact(sock_obj, size):
        data = b""
        while len(data) < size:
            chunk = sock_obj.recv(size - len(data))
            if not chunk:
                raise ConnectionError("Socket closed")
            data += chunk
        return data
    def recv_frame(sock_obj):
        length_bytes = recv_exact(sock_obj, 4)
        msg_len = struct.unpack("!I", length_bytes)[0]
        if msg_len == 0:
            return b""
        return recv_exact(sock_obj, msg_len)
    
    def start_reader_thread(sock_obj):
        def reader():
            try:
                while True:
                    msg = recv_frame(sock_obj)
                    incoming_queue.put(msg)
            except Exception:
                incoming_queue.put(None)
        threading.Thread(target=reader, daemon=True).start()
    
    def get_fernet():
        key = key_entry.get().strip()
        if not key:
            set_status("Key REQUIRED")
            return None
        try:
            return Fernet(key.encode())
        except Exception:
            set_status("Invalid Key")
            return None
        
    def generate_key():
        key = Fernet.generate_key().decode()
        key_entry.delete(0,"end")
        key_entry.insert(0,key)
        
    def copy_key():
        key = key_entry.get().strip()
        if not key:
            return
        root.clipboard_clear()
        root.clipboard_append(key)
        
    def paste_key():
        try:
            text = root.clipboard_get()
        except Exception:
            return
        key_entry.delete(0,"end")
        key_entry.insert(0,text.strip())
        
    def encrypt_preview():
        f = get_fernet()
        if not f:
            return
        plaintext = input_text.get("1.0","end").strip()
        if not plaintext:
            set_status("Type a message first my guy")
            return
        ciphertext = f.encrypt(plaintext.encode()).decode()
        preview_text.config(state="normal")
        preview_text.delete("1.0","end")
        preview_text.insert("1.0",ciphertext)
        preview_text.config(state="disabled")
        
    def decrypt_selected():
        selection = history_tree.selection()
        if not selection:
            set_status("Select a message")
            return
        msg_id = selection[0]
        msg = messages.get(msg_id)
        if not msg:
            set_status("Message not found")
            return
        if msg["plaintext"]:
            detail_text.config(state="normal")
            detail_text.delete("1.0","end")
            detail_text.insert("1.0", msg["plaintext"])
            detail_text.config(state="disabled")
            return
        f = get_fernet()
        if not f:
            return
        try:
            plaintext = f.decrypt(msg["ciphertext"].encode()).decode()
        except InvalidToken:
            set_status("Wrong key")
            return
        msg["plaintext"] = plaintext
        history_tree.set(msg_id, "status", "decrypted")
        detail_text.config(state="normal")
        detail_text.delete("1.0","end")
        detail_text.insert("1.0", plaintext)
        detail_text.config(state="disabled")
        
    def add_history(direction, ciphertext, plaintext=None):
        timestamp = time.strftime("%H:%M:%S")
        preview = ciphertext[:48] + ("..." if len(ciphertext) > 48 else "")
        msg_id = str(time.time_ns())
        messages[msg_id] = {"ciphertext": ciphertext, "plaintext": plaintext}
        history_tree.insert("","end", iid=msg_id, values=(timestamp, direction, "encrypted", preview))
        return msg_id
    
    def clear_compose():
        input_text.delete("1.0","end")
        preview_text.config(state="normal")
        preview_text.delete("1.0","end")
        preview_text.config(state="disabled")
        
    def send_message():
        if not sock:
            set_status("Not connected")
            return
        plaintext = input_text.get("1.0","end").strip()
        ciphertext = preview_text.get("1.0","end").strip()
        if not ciphertext:
            set_status("Encrypt preview first")
            return
        try:
            send_frame(sock,ciphertext.encode())
        except Exception as e:
            set_status(f"send failed: {e}")
            return
        add_history("out", ciphertext, plaintext=plaintext if plaintext else None)
        clear_compose()

    def on_select_message(_event=None):
        selection = history_tree.selection()
        if not selection:
            return
        msg_id = selection[0]
        msg = messages.get(msg_id)
        if not msg:
            return
        text = msg["plaintext"] if msg["plaintext"] else msg["ciphertext"]
        detail_text.config(state="normal")
        detail_text.delete("1.0","end")
        detail_text.insert("1.0", text)
        detail_text.config(state="disabled")

    def show_ciphertext():
        selection = history_tree.selection()
        if not selection:
            return
        msg_id = selection[0]
        msg = messages.get(msg_id)
        if not msg:
            return
        detail_text.config(state="normal")
        detail_text.delete("1.0","end")
        detail_text.insert("1.0", msg["ciphertext"])
        detail_text.config(state="disabled")

    def copy_detail():
        text = detail_text.get("1.0","end").strip()
        if not text:
            return
        root.clipboard_clear()
        root.clipboard_append(text)
        
    def poll_incoming():
        try:
            while True:
                msg = incoming_queue.get_nowait()
                if msg is None:
                    set_status("Disconnected")
                    break
                add_history("in", msg.decode())
        except queue.Empty:
            pass
        root.after(150, poll_incoming)
    
    #Server start button
    start_server_button = ttk.Button(connection_frame, text="Start Server",command=start_server)
    start_server_button.grid(row=1, column=0, columnspan=2, sticky="w", pady=(8,0))

    ttk.Label(connection_frame, text="Connect to IP").grid(row=2, column=0, sticky="w", pady=(10,0))
    connect_ip_entry = ttk.Entry(connection_frame, width=18)
    connect_ip_entry.grid(row=2, column=1, sticky="w", padx=(6,0), pady=(10,0))
    
    #Connect button
    connect_button = ttk.Button(connection_frame, text="Connect",command=connect_to_peer)
    connect_button.grid(row=2, column=2, sticky="w", padx=(10,0), pady=(10,0))
    
    #disconnect button
    disconnect_button = ttk.Button(connection_frame, text="Disconnect",command=disconnect)
    disconnect_button.grid(row=1, column=2, columnspan=2, sticky="w", padx=(10,0), pady=(8,0))

    #Keys
    key_frame = ttk.LabelFrame(left_frame, text="Encryption keys", padding=10)
    key_frame.pack(fill="x", pady=(0, 10))
    
    key_entry = ttk.Entry(key_frame, width = 60)
    key_entry.grid(row=0, column=0, columnspan=3, sticky="we")
    
    generate_key_button = ttk.Button(key_frame, text="Generate Key", command=generate_key)
    generate_key_button.grid(row=1, column=0, sticky="w", pady=(8,0),)

    copy_key_button = ttk.Button(key_frame, text="Copy Key", command=copy_key)
    copy_key_button.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))
    
    paste_key_button = ttk.Button(key_frame, text="Paste Key", command=paste_key)
    paste_key_button.grid(row=1, column=2, sticky="w", padx=(8, 0), pady=(8, 0))
    
    #Message compose section wala section 
    
    compose_frame = ttk.LabelFrame(left_frame, text="Compose", padding= 10)
    compose_frame.pack(fill="both", expand=True)
    
    input_text = tk.Text(compose_frame, height=8, wrap='word')
    input_text.grid(row=0, column=0, columnspan=3, sticky="nsew")
    
    encrypt_preview_button = ttk.Button(compose_frame, text="Encrypt Preview ", command=encrypt_preview)
    encrypt_preview_button.grid(row=1, column=0, sticky="w", pady=(8,0))
    
    send_button = ttk.Button(compose_frame, text="Send Message", command=send_message)
    send_button.grid(row=1, column=1, sticky='w', padx=(8,0), pady=(8,0))
    
    clear_button = ttk.Button(compose_frame, text="Clear", command=clear_compose)
    clear_button.grid(row=1, column=2, sticky="w", padx=(8,0), pady=(8,0))
    
    ttk.Label(compose_frame, text="Encrypted preview").grid(row=2, column=0, sticky="w", pady=(8,0))
    preview_text = tk.Text(compose_frame, height=8, wrap="word", state="disabled", background="#f0f0f0")
    preview_text.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(4,0))
    
    compose_frame.grid_rowconfigure(0, weight=1)
    compose_frame.grid_rowconfigure(3, weight=1)
    compose_frame.grid_columnconfigure(0, weight=1)
    
    #History section wala section
    history_frame = ttk.LabelFrame(right_frame, text="Message History", padding=10)
    history_frame.pack(fill="both", expand=True, pady=(0,10))
    
    columns = ("time", "dir", "status", "preview")
    history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)
    history_tree.heading("time", text="Time")
    history_tree.heading("dir", text="Dir")
    history_tree.heading("status", text="Status")
    history_tree.heading("preview", text="Cipher preview")
    history_tree.column("time", width=90)
    history_tree.column("dir", width=50)
    history_tree.column("status", width=90)
    history_tree.column("preview", width=240)
    history_tree.pack(fill="both", expand=True)
    history_tree.bind("<<TreeviewSelect>>", on_select_message)
    
    #Message deatilas
    detail_frame = ttk.LabelFrame(right_frame, text="Selected message", padding=10)
    detail_frame.pack(fill="x")
    
    detail_text = tk.Text(detail_frame, height=6, wrap="word", state="disabled")
    detail_text.grid(row=0, column=0, columnspan=3, sticky="nsew")
    
    decrypt_button = ttk.Button(detail_frame, text="Decrypt Selected ", command=decrypt_selected)
    decrypt_button.grid(row=1, column=0, sticky="w",pady=(8,0))
    
    show_cipher_button = ttk.Button(detail_frame, text="Show Ciphertext", command=show_ciphertext)
    show_cipher_button.grid(row=1, column=1, sticky="w", padx=(8,0), pady=(8,0))
    
    copy_text_button = ttk.Button(detail_frame, text="Copy Text", command=copy_detail)
    copy_text_button.grid(row=1, column=2, sticky="w", padx=(8,0), pady=(8,0))
    
    
    poll_incoming()
    
    root.mainloop()


if __name__ == "__main__":
    main()
    
