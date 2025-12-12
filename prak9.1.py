import tkinter as tk
from tkinter import scrolledtext
from math import gcd

# =========================
# Utility Functions
# =========================
def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    r = int(n**0.5)
    for i in range(3, r+1, 2):
        if n % i == 0:
            return False
    return True

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (g, x, y)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception("Invers modular tidak ada")
    return x % m

def chunk_message_to_ints(message, n):
    b = message.encode("utf-8")
    max_block = (n.bit_length() - 1) // 8
    if max_block < 1:
        return [ord(ch) for ch in message], 1

    blocks = []
    for i in range(0, len(b), max_block):
        blocks.append(int.from_bytes(b[i:i+max_block], "big"))
    return blocks, max_block

def ints_to_message(ints):
    result = b""
    for x in ints:
        length = (x.bit_length() + 7) // 8
        result += x.to_bytes(length, "big")
    return result.decode("utf-8", errors="replace")

# =========================
# Step 1: Hitung RSA dulu
# =========================
def hitung_rsa():
    textbox.delete(1.0, tk.END)

    try:
        p = int(entry_p.get())
        q = int(entry_q.get())
        e = int(entry_e.get())
    except:
        textbox.insert(tk.END, "ERROR: p, q, e harus berupa angka!\n")
        return

    if not is_prime(p) or not is_prime(q):
        textbox.insert(tk.END, "ERROR: p dan q harus bilangan prima!\n")
        return

    if p == q:
        textbox.insert(tk.END, "ERROR: p dan q tidak boleh sama!\n")
        return

    n = p * q
    phi = (p - 1) * (q - 1)

    if gcd(e, phi) != 1:
        textbox.insert(tk.END, f"ERROR: e = {e} tidak coprime dengan φ(n) = {phi}\n")
        return

    try:
        d = modinv(e, phi)
    except:
        textbox.insert(tk.END, "ERROR: Tidak dapat menghitung invers modular!\n")
        return

    # Simpan hasil untuk dipakai enkripsi
    globals()["g_p"] = p
    globals()["g_q"] = q
    globals()["g_e"] = e
    globals()["g_d"] = d
    globals()["g_n"] = n
    globals()["g_phi"] = phi

    # Tampilkan debug RSA terlebih dahulu
    textbox.insert(tk.END, "=== RSA BERHASIL DIBANGUN ===\n")
    textbox.insert(tk.END, f"p = {p}\n")
    textbox.insert(tk.END, f"q = {q}\n")
    textbox.insert(tk.END, f"n = p * q = {n}\n")
    textbox.insert(tk.END, f"phi = (p-1)(q-1) = {phi}\n")
    textbox.insert(tk.END, f"e = {e}\n")
    textbox.insert(tk.END, f"d = {d}\n")

    textbox.insert(tk.END, "\nSilakan masukkan plaintext untuk dienkripsi.\n")

    # Aktifkan input plaintext
    entry_plain.config(state="normal")
    btn_encrypt.config(state="normal")

# =========================
# Step 2: Enkripsi & Dekripsi setelah RSA siap
# =========================
def proses_enkripsi():
    plaintext = entry_plain.get()

    if plaintext.strip() == "":
        textbox.insert(tk.END, "\nPlaintext masih kosong!\n")
        return

    p, q = g_p, g_q
    e, d = g_e, g_d
    n, phi = g_n, g_phi

    textbox.insert(tk.END, "\n=== ENCODING PLAIN TEXT ===\n")

    blocks, block_size = chunk_message_to_ints(plaintext, n)
    textbox.insert(tk.END, f"Block size = {block_size} bytes\n")
    for i, b in enumerate(blocks):
        textbox.insert(tk.END, f"  M[{i}] = {b}\n")

    # Encrypt
    textbox.insert(tk.END, "\n=== ENCRYPTION ===\n")
    cipher = [pow(m, e, n) for m in blocks]
    for i, c in enumerate(cipher):
        textbox.insert(tk.END, f"  C[{i}] = {c}\n")

    textbox.insert(tk.END, "\nCiphertext:\n")
    textbox.insert(tk.END, " ".join(map(str, cipher)) + "\n")

    # Decrypt
    textbox.insert(tk.END, "\n=== DECRYPTION ===\n")
    dec = [pow(c, d, n) for c in cipher]
    for i, m in enumerate(dec):
        textbox.insert(tk.END, f"  Mdec[{i}] = {m}\n")

    # Recover text
    recovered = ints_to_message(dec)

    textbox.insert(tk.END, "\nRecovered Plaintext:\n")
    textbox.insert(tk.END, recovered + "\n")

    if recovered == plaintext:
        textbox.insert(tk.END, "\n✔ SUKSES! plaintext cocok.\n")
    else:
        textbox.insert(tk.END, "\n✘ GAGAL! plaintext tidak cocok.\n")


# =========================
# GUI LAYOUT
# =========================
root = tk.Tk()
root.title("RSA Manual (p, q, e) → Lanjut ke Plaintext")
root.geometry("760x650")

tk.Label(root, text="Masukkan p (prima):").pack()
entry_p = tk.Entry(root, width=30)
entry_p.pack()

tk.Label(root, text="Masukkan q (prima):").pack()
entry_q = tk.Entry(root, width=30)
entry_q.pack()

tk.Label(root, text="Masukkan e (coprime dengan φ):").pack()
entry_e = tk.Entry(root, width=30)
entry_e.pack()

btn_rsa = tk.Button(root, text="Bangun RSA", command=hitung_rsa)
btn_rsa.pack(pady=10)

tk.Label(root, text="Plaintext (aktif setelah RSA siap):").pack()
entry_plain = tk.Entry(root, width=50, state="disabled")
entry_plain.pack()

btn_encrypt = tk.Button(root, text="Enkripsi & Dekripsi", state="disabled", command=proses_enkripsi)
btn_encrypt.pack(pady=10)

textbox = scrolledtext.ScrolledText(root, width=90, height=28)
textbox.pack()

root.mainloop()
