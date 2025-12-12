#!/usr/bin/env python3
# AES-128 Demonstrator (Versi lengkap untuk tugas)
# - Semua input dimasukkan MANUAL oleh user
# - Tidak memakai default sama sekali
# - Menampilkan semua proses: ASCII, HEX, BIN, Key Expansion, dan langkah enkripsi

from copy import deepcopy

# =============== SBOX HEX (seperti pada file PDF) ===============
SBOX = [
0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
]

RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]


# ====================== FUNGSI UTILITAS ===========================
def to_hex_list(b): return ' '.join(f"{x:02X}" for x in b)
def to_bin_list(b): return ' '.join(f"{x:08b}" for x in b)

def pad_pkcs7(bs):
    pad = 16 - (len(bs) % 16)
    return bs + [pad]*pad

def bytes_from_str(s):
    return [ord(c) for c in s]


# ======================== AES STATE ===============================
def bytes_to_matrix(b):  
    return [[b[c*4+r] for c in range(4)] for r in range(4)]

def matrix_to_bytes(m):
    return [m[r][c] for c in range(4) for r in range(4)]

def print_state(title, s):
    print(title)
    for r in range(4):
        print(" ", " ".join(f"{s[r][c]:02X}" for c in range(4)))
    print()


# ====================== KEY EXPANSION ==============================
def rot_word(w):
    return w[1:] + w[:1]

def sub_word(w):
    return [SBOX[x] for x in w]

def key_expansion_verbose(key_bytes):
    print("\n=== KEY EXPANSION (DETAIL) ===")
    w = []

    # w0..w3 dari key awal
    for i in range(4):
        w.append(key_bytes[4*i:4*i+4])
        print(f"w[{i:02d}] = {to_hex_list(w[i])}")

    # w4..w43
    for i in range(4, 44):
        temp = w[i-1].copy()
        print(f"\nMenghitung w[{i}]:")

        if i % 4 == 0:
            print(" i%4 = 0 → RotWord → SubWord → XOR RCON")
            t1 = rot_word(temp)
            print("  RotWord :", to_hex_list(t1))
            t2 = sub_word(t1)
            print("  SubWord :", to_hex_list(t2))
            t2[0] ^= RCON[(i//4)-1]
            print(f"  XOR RCON ({RCON[(i//4)-1]:02X}):", to_hex_list(t2))
            temp = t2
        else:
            print(" i%4 ≠ 0 → temp = w[i-1]")
            print("  temp    :", to_hex_list(temp))

        w_new = [x ^ y for x, y in zip(w[i-4], temp)]
        w.append(w_new)

        print("  w[i-4] :", to_hex_list(w[i-4]))
        print("  w[i]   :", to_hex_list(w_new))

    print("\n=== SELESAI KEY EXPANSION ===\n")
    return w

def words_to_round_keys(w):
    rks = []
    for i in range(11):
        block = []
        for j in range(4):
            block += w[4*i + j]
        rks.append(block)
    return rks


# ================= AES ROUND OPERATIONS ============================
def sub_bytes(s):
    return [[SBOX[s[r][c]] for c in range(4)] for r in range(4)]

def shift_rows(s):
    out = [[]]*4
    out[0] = s[0]
    out[1] = s[1][1:] + s[1][:1]
    out[2] = s[2][2:] + s[2][:2]
    out[3] = s[3][3:] + s[3][:3]
    return out

def xtime(a):
    return (((a << 1) & 0xFF) ^ 0x1B) if a & 0x80 else (a << 1)

def mix_single_column(col):
    a = col
    b = [xtime(x) for x in a]
    return [
        b[0]^a[3]^a[2]^b[1]^a[1],
        b[1]^a[0]^a[3]^b[2]^a[2],
        b[2]^a[1]^a[0]^b[3]^a[3],
        b[3]^a[2]^a[1]^b[0]^a[0]
    ]

def mix_columns(s):
    cols = [[s[r][c] for r in range(4)] for c in range(4)]
    mixed = [mix_single_column(c) for c in cols]
    return [[mixed[c][r] for c in range(4)] for r in range(4)]

def add_round_key(s, rk):
    keym = bytes_to_matrix(rk)
    return [[s[r][c] ^ keym[r][c] for c in range(4)] for r in range(4)]


# ================= AES ENCRYPTION (VERBOSE) =======================
def aes_encrypt_verbose(block, round_keys):
    print("\n=== PROSES ENKRIPSI BLOK 16 BYTE ===")
    state = bytes_to_matrix(block)

    print_state("State awal:", state)

    # AddRoundKey awal
    state = add_round_key(state, round_keys[0])
    print_state("Setelah AddRoundKey(K0):", state)

    # Ronde 1–9
    for r in range(1, 10):
        print(f"--- RONDE {r} ---")

        state = sub_bytes(state)
        print_state(" Setelah SubBytes:", state)

        state = shift_rows(state)
        print_state(" Setelah ShiftRows:", state)

        state = mix_columns(state)
        print_state(" Setelah MixColumns:", state)

        state = add_round_key(state, round_keys[r])
        print_state(f" Setelah AddRoundKey(K{r}):", state)

    # Ronde 10 (tanpa MixColumns)
    print("--- RONDE 10 (final) ---")
    state = sub_bytes(state)
    print_state(" Setelah SubBytes:", state)

    state = shift_rows(state)
    print_state(" Setelah ShiftRows:", state)

    state = add_round_key(state, round_keys[10])
    print_state(" Setelah AddRoundKey(K10):", state)

    return matrix_to_bytes(state)


# ========================= MAIN PROGRAM ===========================
def main():

    # -------- Input manual (tidak boleh kosong) --------
    plaintext = ""
    key = ""

    while plaintext.strip() == "":
        plaintext = input("Masukkan PLAINTEXT: ")

    while key.strip() == "":
        key = input("Masukkan CIPHERKEY (minimal 1 karakter): ")

    # -------- Konversi --------
    pt_bytes = bytes_from_str(plaintext)
    key_bytes = bytes_from_str(key)

    # Key harus 16 byte → pad/truncate
    if len(key_bytes) < 16:
        key_bytes += [0]*(16-len(key_bytes))
    key_bytes = key_bytes[:16]

    # Plaintext → pad PKCS7
    pt_padded = pad_pkcs7(pt_bytes)
    first_block = pt_padded[:16]

    print("\n=== KONVERSI PLAINtext ===")
    print("ASCII :", pt_bytes)
    print("HEX   :", to_hex_list(pt_bytes))
    print("BIN   :", to_bin_list(pt_bytes))

    print("\n=== KONVERSI KEY ===")
    print("ASCII :", key_bytes)
    print("HEX   :", to_hex_list(key_bytes))

    # -------- Key Expansion --------
    w = key_expansion_verbose(key_bytes)
    round_keys = words_to_round_keys(w)

    for i, rk in enumerate(round_keys):
        print(f"K{i}: {to_hex_list(rk)}")

    # -------- Enkripsi blok pertama --------
    print("\n=== ENKRIPSI BLOK 16 BYTE PERTAMA ===")
    print("Blok plaintext (hex):", to_hex_list(first_block))

    cipher_block = aes_encrypt_verbose(first_block, round_keys)

    print("\n=== HASIL AKHIR CIPHERTEXT (HEX) ===")
    print(to_hex_list(cipher_block))


# Jalankan
main()
