import tkinter as tk
from tkinter import ttk, messagebox

# --- Fungsi Konversi ---
def konversi():
    jenis = combo_pilihan.get()
    nilai = entry_nilai.get().strip().upper()

    if not nilai:
        messagebox.showwarning("Peringatan", "Masukkan nilai bilangan terlebih dahulu!")
        return

    try:
        if jenis == "Biner ke Desimal & Hexadesimal":
            desimal = int(nilai, 2)
            hasil = f"Desimal: {desimal}\nHexadesimal: {hex(desimal)[2:].upper()}"
        elif jenis == "Oktal ke Desimal, Biner & Hexadesimal":
            desimal = int(nilai, 8)
            hasil = f"Desimal: {desimal}\nBiner: {bin(desimal)[2:]}\nHexadesimal: {hex(desimal)[2:].upper()}"
        elif jenis == "Hexadesimal ke Desimal, Biner & Oktal":
            desimal = int(nilai, 16)
            hasil = f"Desimal: {desimal}\nBiner: {bin(desimal)[2:]}\nOktal: {oct(desimal)[2:]}"
        else:
            hasil = "Silakan pilih jenis konversi terlebih dahulu!"
        
        output_label.config(text=hasil)
    except ValueError:
        messagebox.showerror("Kesalahan", "Nilai bilangan tidak sesuai dengan jenis yang dipilih!")
        output_label.config(text="")

# --- Membuat Jendela Utama ---
root = tk.Tk()
root.title("Program Konversi Bilangan")
root.geometry("500x400")
root.config(bg="#f0f0f0")

# --- Judul ---
judul = tk.Label(root, text="PROGRAM KONVERSI BILANGAN", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333")
judul.pack(pady=15)

# --- Pilihan Menu ---
frame_menu = tk.Frame(root, bg="#f0f0f0")
frame_menu.pack(pady=10)

tk.Label(frame_menu, text="Pilih Jenis Konversi:", font=("Arial", 11), bg="#f0f0f0").grid(row=0, column=0, padx=10)

combo_pilihan = ttk.Combobox(frame_menu, font=("Arial", 11), width=35, state="readonly")
combo_pilihan["values"] = (
    "Biner ke Desimal & Hexadesimal",
    "Oktal ke Desimal, Biner & Hexadesimal",
    "Hexadesimal ke Desimal, Biner & Oktal"
)
combo_pilihan.grid(row=0, column=1)
combo_pilihan.current(0)

# --- Input Nilai ---
frame_input = tk.Frame(root, bg="#f0f0f0")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Masukkan Nilai:", font=("Arial", 11), bg="#f0f0f0").grid(row=0, column=0, padx=10)
entry_nilai = tk.Entry(frame_input, font=("Arial", 11), width=30)
entry_nilai.grid(row=0, column=1)

# --- Tombol Konversi ---
tombol = tk.Button(root, text="Konversi", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15, command=konversi)
tombol.pack(pady=15)

# --- Output ---
frame_output = tk.Frame(root, bg="#f0f0f0")
frame_output.pack(pady=10)

tk.Label(frame_output, text="Hasil Konversi:", font=("Arial", 11, "bold"), bg="#f0f0f0").pack()
output_label = tk.Label(frame_output, text="", font=("Consolas", 12), bg="#fff", width=45, height=6, relief="sunken", anchor="nw", justify="left")
output_label.pack(pady=5)

# --- Tombol Keluar ---
tk.Button(root, text="Keluar", font=("Arial", 11), bg="#f44336", fg="white", width=10, command=root.destroy).pack(pady=10)

root.mainloop()
