import os
import base64
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

SALT_SIZE = 16
ITERATIONS = 200_000


def get_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)


def save_encrypted():
    text = text_box.get("1.0", tk.END).rstrip("\n")
    password = simpledialog.askstring("PASSWORD", "ENTER PASSWORD TO ENCRYPT:", show="*")
    if not password:
        return
    salt = os.urandom(SALT_SIZE)
    key = get_key(password, salt)
    f = Fernet(key)
    data = salt + f.encrypt(text.encode())

    path = filedialog.asksaveasfilename(defaultextension=".enc",
                                        filetypes=[("Encrypted files", "*.enc")])
    if path:
        with open(path, "wb") as file_out:
            file_out.write(data)
        messagebox.showinfo("SAVED", "ENCRYPTED & SAVED")


def open_encrypted():
    path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
    if not path:
        return
    password = simpledialog.askstring("PASSWORD", "ENTER PASSWORD TO DECRYPT:", show="*")
    if not password:
        return
    with open(path, "rb") as file_in:
        data = file_in.read()
    salt, ciphertext = data[:SALT_SIZE], data[SALT_SIZE:]
    key = get_key(password, salt)
    f = Fernet(key)
    try:
        text = f.decrypt(ciphertext).decode()
        text_box.delete("1.0", tk.END)
        text_box.insert("1.0", text)
        messagebox.showinfo("OPENED", "FILE DECRYPTED")
    except InvalidToken:
        messagebox.showerror("ERROR", "WRONG PASSWORD")


root = tk.Tk()
root.title("PBKDF2 + Fernet")
root.geometry("600x400")

text_box = tk.Text(root, wrap="word")
text_box.pack(fill="both", expand=True)

menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=False)
file_menu.add_command(label="OPEN (ENCRYPTED)", command=open_encrypted)
file_menu.add_command(label="SAVE (DECRYPTED)", command=save_encrypted)
file_menu.add_separator()
file_menu.add_command(label="EXIT", command=root.quit)
menu.add_cascade(label="FILE", menu=file_menu)

root.mainloop()