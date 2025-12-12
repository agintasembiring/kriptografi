import tkinter as tk
from tkinter import scrolledtext
import random
from math import gcd

# ----------------------------
# Utility Functions
# ----------------------------
def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    r = int(n ** 0.5)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

def primes_in_range(low, high):
    return [x for x in range(low, high + 1) if is_prime(x)]

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (g, x, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("Inverse tidak ada")
    return x % m

# Konversi plaintext jadi blok integer < n
def chunk_message_to_ints(message, n):
    b = message.encode('utf-8')
    max_block_size = (n.bit_length() - 1) // 8

    if max_block_size < 1:
        return [ord(ch) for ch in message], 1

    blocks = []
    for i in range(0, len(b), max_block_size):
        part = b[i:i + max_block_size]
        blocks.append(int.from_bytes(part, "big"))

    return blocks, max_block_size

def ints_to_message(int_list):
    result = b""
    for x in int_list:
        length = (x.bit_length() + 7) // 8
        result += x.to_bytes(length, "big")
    return result.decode("utf-8", errors="replace")

# ----------------------------
# RSA Random Key Generation
# ----------------------------
def generate_keys():
    primes = primes_in_range(50, 200)
    p = random.choice(primes)
    q = random.choice(primes)
    while q == p:
        q = random.choice(primes)

    n = p * q
    phi = (p - 1) * (q - 1)

    # pilih e random yang coprime
    while True:
        e = random.randint(3, phi - 1)
        if gcd(e, phi) == 1:
            break

    d = modinv(e, phi)

    return p, q, n, phi, e, d

# ----------------------------
# Main GUI Functions
# ----------------------------
def run_rsa():
    plaintext = entry_plain.get()
    if plaintext == "":
        textbox.insert(tk.END, "Masukkan plaintext!\n")
        return

    textbox.delete(1.0, tk.END)

    # Generate RSA keys
    p, q, n, phi, e, d = generate_keys()

    textbox.insert(tk.END, "=== RANDOM RSA DEBUG ===\n")
    textbox.insert(tk.END, f"p = {p}\nq = {q}\n")
    textbox.insert(tk.END, f"n = p*q = {n}\n")
    textbox.insert(tk.END, f"phi = (p-1)(q-1) = {phi}\n")
    textbox.insert(tk.END, f"e = {e}\n")
    textbox.insert(tk.END, f"d = e^-1 mod phi = {d}\n")
    textbox.insert(tk.END, "\n=== ENCODING ===\n")

    blocks, block_size = chunk_message_to_ints(plaintext, n)
    textbox.insert(tk.END, f"Block size: {block_size} bytes\n")
    textbox.insert(tk.END, "Blok plaintext:\n")
    for i, b in enumerate(blocks):
        textbox.insert(tk.END, f"  M[{i}] = {b}\n")

    # Encryption
    textbox.insert(tk.END, "\n=== ENCRYPTION ===\n")
    cipher_blocks = [pow(m, e, n) for m in blocks]

    for i, c in enumerate(cipher_blocks):
        textbox.insert(tk.END, f"  C[{i}] = {c}\n")

    textbox.insert(tk.END, "\nCiphertext (angka):\n")
    textbox.insert(tk.END, " ".join(map(str, cipher_blocks)) + "\n")

    # Decryption
    textbox.insert(tk.END, "\n=== DECRYPTION ===\n")
    decrypted_blocks = [pow(c, d, n) for c in cipher_blocks]
    for i, m in enumerate(decrypted_blocks):
        textbox.insert(tk.END, f"  Mdec[{i}] = {m}\n")

    # Reconstruct message
    recovered = ints_to_message(decrypted_blocks)
    textbox.insert(tk.END, "\nRecovered plaintext:\n")
    textbox.insert(tk.END, recovered + "\n")

    textbox.insert(tk.END, "\n=== STATUS ===\n")
    if recovered == plaintext:
        textbox.insert(tk.END, "✔ Berhasil: plaintext cocok!\n")
    else:
        textbox.insert(tk.END, "✘ WARNING: plaintext TIDAK cocok!\n")

# ----------------------------
# GUI
# ----------------------------
root = tk.Tk()
root.title("RSA Random (50-200) + Debug Lengkap")
root.geometry("700x600")

tk.Label(root, text="Plaintext:").pack()
entry_plain = tk.Entry(root, width=50)
entry_plain.pack()

btn = tk.Button(root, text="Generate RSA & Encrypt", command=run_rsa)
btn.pack(pady=10)

textbox = scrolledtext.ScrolledText(root, width=80, height=30)
textbox.pack()

root.mainloop()
