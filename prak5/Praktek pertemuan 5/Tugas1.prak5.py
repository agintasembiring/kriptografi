import tkinter as tk
from tkinter import messagebox, scrolledtext

# ==============================
# Fungsi Pendukung Vigenere Cipher
# ==============================

def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt(text, key, output_box):
    encrypted_text = []
    key = generate_key(text, key)
    output_box.insert(tk.END, "\n=== PROSES ENKRIPSI ===\n")
    output_box.insert(tk.END, f"Teks Asli   : {text}\n")
    output_box.insert(tk.END, f"Kunci       : {key}\n\n")

    for i in range(len(text)):
        if text[i].isalpha():
            x = (ord(text[i].upper()) + ord(key[i].upper())) % 26
            x += ord('A')
            encrypted_char = chr(x)
            encrypted_text.append(encrypted_char)
            output_box.insert(
                tk.END,
                f"[{i+1}] Huruf: {text[i]} + {key[i]} → "
                f"({ord(text[i].upper()) - 65} + {ord(key[i].upper()) - 65}) % 26 = "
                f"{x - 65} → {encrypted_char}\n"
            )
        else:
            encrypted_text.append(text[i])

    cipher_result = "".join(encrypted_text)
    output_box.insert(tk.END, f"\nHasil Enkripsi: {cipher_result}\n")
    return cipher_result

def decrypt(cipher_text, key, output_box):
    decrypted_text = []
    key = generate_key(cipher_text, key)
    output_box.insert(tk.END, "\n=== PROSES DEKRIPSI ===\n")
    output_box.insert(tk.END, f"Teks Terenkripsi : {cipher_text}\n")
    output_box.insert(tk.END, f"Kunci            : {key}\n\n")

    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            x = (ord(cipher_text[i].upper()) - ord(key[i].upper()) + 26) % 26
            x += ord('A')
            decrypted_char = chr(x)
            decrypted_text.append(decrypted_char)
            output_box.insert(
                tk.END,
                f"[{i+1}] Huruf: {cipher_text[i]} - {key[i]} → "
                f"({ord(cipher_text[i].upper()) - 65} - {ord(key[i].upper()) - 65} + 26) % 26 = "
                f"{x - 65} → {decrypted_char}\n"
            )
        else:
            decrypted_text.append(cipher_text[i])

    plain_result = "".join(decrypted_text)
    output_box.insert(tk.END, f"\nHasil Dekripsi: {plain_result}\n")
    return plain_result

# ==============================
# FUNGSI EVENT HANDLER
# ==============================

def proses_enkripsi():
    text = entry_text.get().upper()
    key = entry_key.get().upper()
    if not text or not key:
        messagebox.showwarning("Peringatan", "Teks dan kunci tidak boleh kosong!")
        return
    output_box.delete(1.0, tk.END)
    encrypt(text, key, output_box)

def proses_dekripsi():
    cipher_text = entry_text.get().upper()
    key = entry_key.get().upper()
    if not cipher_text or not key:
        messagebox.showwarning("Peringatan", "Teks dan kunci tidak boleh kosong!")
        return
    output_box.delete(1.0, tk.END)
    decrypt(cipher_text, key, output_box)

def clear_all():
    entry_text.delete(0, tk.END)
    entry_key.delete(0, tk.END)
    output_box.delete(1.0, tk.END)

# ==============================
# ANTARMUKA GUI TKINTER
# ==============================

root = tk.Tk()
root.title("🔐 Vigenere Cipher - Enkripsi & Dekripsi")
root.geometry("650x520")
root.resizable(False, False)
root.config(bg="#f2f4f8")

# Judul
label_title = tk.Label(root, text="VIGENERE CIPHER", font=("Segoe UI", 18, "bold"), bg="#f2f4f8", fg="#333")
label_title.pack(pady=10)

# Frame input
frame_input = tk.Frame(root, bg="#f2f4f8")
frame_input.pack(pady=5)

tk.Label(frame_input, text="Plaintext:", bg="#7ca8ff", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
entry_text = tk.Entry(frame_input, width=50, font=("Segoe UI", 10))
entry_text.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Masukkan Kunci:", bg="#7ca8ff", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
entry_key = tk.Entry(frame_input, width=50, font=("Segoe UI", 10))
entry_key.grid(row=1, column=1, padx=10, pady=5)

# Tombol aksi
frame_button = tk.Frame(root, bg="#f2f4f8")
frame_button.pack(pady=10)

btn_encrypt = tk.Button(frame_button, text="🔒 Enkripsi", width=15, bg="#00ffd5", fg="black",
                        font=("Segoe UI", 10, "bold"), command=proses_enkripsi)
btn_encrypt.grid(row=0, column=0, padx=10)

btn_decrypt = tk.Button(frame_button, text="🔓 Dekripsi", width=15, bg="#4cfe00", fg="black",
                        font=("Segoe UI", 10, "bold"), command=proses_dekripsi)
btn_decrypt.grid(row=0, column=1, padx=10)

btn_clear = tk.Button(frame_button, text="🧹 Bersihkan", width=15, bg="#ff0000", fg="black",
                      font=("Segoe UI", 10, "bold"), command=clear_all)
btn_clear.grid(row=0, column=2, padx=10)

# Output box
output_box = scrolledtext.ScrolledText(root, width=75, height=15, font=("Consolas", 9))
output_box.pack(pady=10)

# Jalankan GUI
root.mainloop()
