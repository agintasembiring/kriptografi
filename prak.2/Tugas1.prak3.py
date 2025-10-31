import tkinter as tk
from tkinter import ttk, messagebox

# ==========================
#  Fungsi Konversi Bilangan
# ==========================
def konversi():
    jenis = combo_pilihan.get()
    nilai = entry_nilai.get().strip().upper()

    if not nilai:
        messagebox.showwarning("Peringatan", "Masukkan nilai bilangan terlebih dahulu!")
        return

    try:
        # ===== 1. Biner ke Desimal & Hexadesimal =====
        if jenis == "Biner ke Desimal & Hexadesimal":
            desimal = int(nilai, 2)
            hasil = f"""
Nilai Biner     : {nilai}
Konversi Desimal: {desimal}
Konversi Hexa   : {hex(desimal)[2:].upper()}
"""
        # ===== 2. Oktal ke Desimal, Biner & Hexadesimal =====
        elif jenis == "Oktal ke Desimal, Biner & Hexadesimal":
            desimal = int(nilai, 8)
            hasil = f"""
Nilai Oktal     : {nilai}
Konversi Desimal: {desimal}
Konversi Biner  : {bin(desimal)[2:]}
Konversi Hexa   : {hex(desimal)[2:].upper()}
"""
        # ===== 3. Hexadesimal ke Desimal, Biner & Oktal =====
        elif jenis == "Hexadesimal ke Desimal, Biner & Oktal":
            desimal = int(nilai, 16)
            hasil = f"""
Nilai Hexa      : {nilai}
Konversi Desimal: {desimal}
Konversi Biner  : {bin(desimal)[2:]}
Konversi Oktal  : {oct(desimal)[2:]}
"""
        else:
            hasil = "Silakan pilih jenis konversi terlebih dahulu!"

        # Tampilkan hasil di label output
        output_label.config(text=hasil.strip())

    except ValueError:
        messagebox.showerror("Kesalahan", "Nilai bilangan tidak sesuai dengan jenis yang dipilih!")
        output_label.config(text="")

# ==========================
#  GUI Tkinter
# ==========================
root = tk.Tk()
root.title("Program Konversi Bilangan")
root.geometry("550x450")
root.resizable(False, False)
root.config(bg="#f0f0f0")

# --- Judul Program ---
judul = tk.Label(
    root,
    text="PROGRAM KONVERSI BILANGAN",
    font=("Arial", 16, "bold"),
    bg="#f0f0f0",
    fg="#333"
)
judul.pack(pady=15)

# --- Pilihan Konversi ---
frame_menu = tk.Frame(root, bg="#f0f0f0")
frame_menu.pack(pady=10)

tk.Label(frame_menu, text="Pilih Jenis Konversi:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10)
combo_pilihan = ttk.Combobox(frame_menu, font=("Arial", 11), width=40, state="readonly")
combo_pilihan["values"] = (
    "Biner ke Desimal & Hexadesimal",
    "Oktal ke Desimal, Biner & Hexadesimal",
    "Hexadesimal ke Desimal, Biner & Oktal"
)
combo_pilihan.grid(row=0, column=1)
combo_pilihan.current(0)

# --- Input Nilai Bilangan ---
frame_input = tk.Frame(root, bg="#f0f0f0")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Masukkan Nilai Bilangan:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10)
entry_nilai = tk.Entry(frame_input, font=("Arial", 12), width=30)
entry_nilai.grid(row=0, column=1)

# --- Tombol Konversi ---
tombol_konversi = tk.Button(
    root,
    text="Konversi",
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    width=15,
    command=konversi
)
tombol_konversi.pack(pady=15)

# --- Area Output ---
frame_output = tk.Frame(root, bg="#f0f0f0")
frame_output.pack(pady=10)

tk.Label(frame_output, text="Hasil Konversi:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
output_label = tk.Label(
    frame_output,
    text="",
    font=("Consolas", 12),
    bg="#ffffff",
    width=55,
    height=8,
    relief="sunken",
    anchor="nw",
    justify="left"
)
output_label.pack(pady=5)

# --- Tombol Keluar ---
tombol_keluar = tk.Button(
    root,
    text="Keluar",
    font=("Arial", 11, "bold"),
    bg="#f44336",
    fg="white",
    width=10,
    command=root.destroy
)
tombol_keluar.pack(pady=10)

root.mainloop()
