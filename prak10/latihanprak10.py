while True:

    # ======================================
    #   ELGAMAL – ASCII + MANUAL + PER HURUF
    # ======================================

    # input manual
    plaintext = input("\nMasukkan plaintext (huruf): ")

    p = int(input("Masukkan bilangan prima p (>255): "))
    g = int(input("Masukkan g (1 < g < p): "))
    x = int(input("Masukkan x, kunci privat (1 < x < p): "))
    k = int(input("Masukkan k (1 < k < p): "))

    # hitung y
    y = pow(g, x, p)

    print("\n=== KUNCI ===")
    print(f"Public key  = (y,g,p) = ({y},{g},{p})")
    print(f"Private key = (x,p)   = ({x},{p})")

    # ============================
    # ENKRIPSI
    # ============================

    print("\n=== PROSES ENKRIPSI ===")
    a = pow(g, k, p)
    print(f"Nilai a = g^k mod p = {a}")

    cipher = []

    for ch in plaintext:
        m = ord(ch)
        b = (m * pow(y, k, p)) % p

        cipher.append(b)

        print(f"Huruf {ch} -> ASCII {m} -> b = {b}")

    print("\nCiphertext:")
    print("a =", a)
    print("b =", cipher)

    # ============================
    # DEKRIPSI
    # ============================

    print("\n=== PROSES DEKRIPSI ===")
    inv = pow(a, p-1-x, p)
    print(f"Nilai inverse = a^(p-1-x) mod p = {inv}")

    hasil = ""

    for b in cipher:
        m = (b * inv) % p
        ch = chr(m)

        hasil += ch

        print(f"Cipher b = {b} -> m = {m} -> huruf = {ch}")

    print("\nHasil plaintext =", hasil)

    # ============================
    # TANYA MAU ULANG LAGI
    # ============================

    ulang = input("\nUlang lagi? (y/n) : ").lower()
    if ulang != "y":
        print("\nProgram selesai.")
        break
