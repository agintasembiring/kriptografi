import tkinter as tk
from tkinter import messagebox

# Dictionary untuk menyimpan aturan substitusi
aturan = {}

# Fungsi menambahkan aturan
def tambah_aturan():
    asli = entry_asli.get().upper()
    ganti = entry_ganti.get().upper()

    if not asli or not ganti:
        messagebox.showwarning("Peringatan", "Isi huruf asli dan huruf pengganti!")
        return

    if len(asli) != 1 or len(ganti) != 1 or not asli.isalpha() or not ganti.isalpha():
        messagebox.showerror("Kesalahan", "Masukkan hanya 1 huruf alfabet untuk masing-masing kolom!")
        return

    aturan[asli] = ganti
    entry_asli.delete(0, tk.END)
    entry_ganti.delete(0, tk.END)
    update_daftar()

# Fungsi untuk memperbarui daftar aturan di GUI
def update_daftar():
    daftar.delete(1.0, tk.END)
    for k, v in aturan.items():
        daftar.insert(tk.END, f"{k} → {v}\n")

# Fungsi untuk enkripsi
def enkripsi():
    plaintext = entry_plain.get().upper()
    if not plaintext:
        messagebox.showwarning("Peringatan", "Masukkan plaintext terlebih dahulu!")
        return

    hasil = ""
    for huruf in plaintext:
        hasil += aturan.get(huruf, huruf)  # jika tidak ada di aturan, biarkan

    entry_hasil.delete(0, tk.END)
    entry_hasil.insert(0, hasil)

# Fungsi reset
def reset():
    aturan.clear()
    daftar.delete(1.0, tk.END)
    entry_plain.delete(0, tk.END)
    entry_hasil.delete(0, tk.END)

# GUI utama
root = tk.Tk()
root.title("Substitusi Cipher (Aturan Manual)")
root.geometry("550x500")
root.config(bg="#F8F9FA")

tk.Label(root, text="SUBSTITUSI CIPHER", font=("Arial", 16, "bold"), bg="#F8F9FA", fg="#333").pack(pady=10)

# Input plaintext
tk.Label(root, text="Masukkan Plaintext:", font=("Arial", 11), bg="#F8F9FA").pack()
entry_plain = tk.Entry(root, font=("Arial", 11), width=40)
entry_plain.pack(pady=5)

# Bagian aturan
frame = tk.Frame(root, bg="#F8F9FA")
frame.pack(pady=10)

tk.Label(frame, text="Huruf Asli:", font=("Arial", 11), bg="#F8F9FA").grid(row=0, column=0, padx=5)
entry_asli = tk.Entry(frame, font=("Arial", 11), width=5, justify="center")
entry_asli.grid(row=0, column=1, padx=5)

tk.Label(frame, text="→", font=("Arial", 11, "bold"), bg="#F8F9FA").grid(row=0, column=2)

tk.Label(frame, text="Huruf Pengganti:", font=("Arial", 11), bg="#F8F9FA").grid(row=0, column=3, padx=5)
entry_ganti = tk.Entry(frame, font=("Arial", 11), width=5, justify="center")
entry_ganti.grid(row=0, column=4, padx=5)

tk.Button(frame, text="Tambahkan Aturan", font=("Arial", 10, "bold"), bg="#28A745", fg="white", command=tambah_aturan).grid(row=0, column=5, padx=10)

# Daftar aturan
tk.Label(root, text="Daftar Aturan:", font=("Arial", 11, "bold"), bg="#F8F9FA").pack()
daftar = tk.Text(root, width=40, height=7, font=("Consolas", 11))
daftar.pack(pady=5)

# Tombol Enkripsi dan Reset
tk.Button(root, text="Enkripsi", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", width=12, command=enkripsi).pack(pady=5)
tk.Button(root, text="Reset", font=("Arial", 11), bg="#FFC107", fg="black", width=10, command=reset).pack(pady=5)

# Hasil
tk.Label(root, text="Hasil Cipher:", font=("Arial", 11, "bold"), bg="#F8F9FA").pack()
entry_hasil = tk.Entry(root, font=("Consolas", 12), width=45)
entry_hasil.pack(pady=5)

# Tombol keluar
tk.Button(root, text="Keluar", font=("Arial", 11), bg="#DC3545", fg="white", width=10, command=root.destroy).pack(pady=10)

root.mainloop()
