import streamlit as st
import random
import time

# --- 1. LOGIKA INTI GAME (Hampir Sama dengan Versi Terminal) ---

def hitung_cows_bulls(tebakan, rahasia):
    """Menghitung jumlah Bulls dan Cows."""
    bulls = 0
    cows = 0
    tebakan_list = list(tebakan)
    rahasia_list = list(rahasia)

    # Hitung Bulls dan Tandai
    for i in range(4): 
        if tebakan_list[i] == rahasia_list[i]:
            bulls += 1
            rahasia_list[i] = tebakan_list[i] = None 

    # Hitung Cows
    tebakan_sisa = [char for char in tebakan_list if char is not None]
    rahasia_sisa = [char for char in rahasia_list if char is not None]
    
    for char in tebakan_sisa:
        if char in rahasia_sisa:
            cows += 1
            rahasia_sisa.remove(char)
            
    return bulls, cows

def generate_kata_kunci_acak(mode):
    """Membuat kunci rahasia 4 karakter unik."""
    TARGET_LENGTH = 4
    if mode == "angka":
        digits = list("0123456789")
        random.shuffle(digits)
        kata_kunci = "".join(digits[:TARGET_LENGTH])
        validasi = "Angka Unik"
    elif mode == "kata":
        unique_words = ["love", "park", "fire", "hope", "jump", "talk", "many", "rule", "sink", "read"]
        kata_kunci = random.choice(unique_words)
        validasi = "Huruf Unik"
        
    return kata_kunci, validasi

# --- 2. FUNGSI MANAJEMEN STATE STREAMLIT ---

def inisialisasi_state():
    """Mengatur semua variabel yang dibutuhkan di st.session_state (Memori Aplikasi Web)."""
    # st.session_state adalah analogi dari 'self' di OOP untuk aplikasi Streamlit
    if 'kata_kunci_rahasia' not in st.session_state:
        st.session_state.kata_kunci_rahasia = None
    if 'mode' not in st.session_state:
        st.session_state.mode = None
    if 'validasi_tipe' not in st.session_state:
        st.session_state.validasi_tipe = ""
    if 'tebakan_ke' not in st.session_state:
        st.session_state.tebakan_ke = 0
    if 'riwayat_sesi' not in st.session_state:
        st.session_state.riwayat_sesi = []
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False

def mulai_game(mode_pilihan):
    """Meriset state dan memulai game baru."""
    st.session_state.mode = mode_pilihan
    kunci, tipe = generate_kata_kunci_acak(mode_pilihan)
    
    st.session_state.kata_kunci_rahasia = kunci
    st.session_state.validasi_tipe = tipe
    st.session_state.tebakan_ke = 1
    st.session_state.riwayat_sesi = []
    st.session_state.game_active = True

def proses_tebakan(tebakan):
    """Memproses tebakan pengguna dan memperbarui state."""
    
    tebakan = tebakan.lower().strip()
    
    # Validasi Unik dan Panjang
    if len(tebakan) != 4 or len(set(tebakan)) != 4:
        st.error(f"Tebakan harus 4 {st.session_state.validasi_tipe} unik!")
        return
    # Validasi Tipe Karakter (Angka/Huruf)
    if st.session_state.mode == "angka" and not tebakan.isdigit():
        st.error("Hanya boleh angka!")
        return
    if st.session_state.mode == "kata" and not tebakan.isalpha():
        st.error("Hanya boleh huruf!")
        return


    # Hitung Hasil
    bulls, cows = hitung_cows_bulls(tebakan, st.session_state.kata_kunci_rahasia)

    # Cek Kemenangan
    if tebakan == st.session_state.kata_kunci_rahasia:
        st.session_state.riwayat_sesi.append(f"({st.session_state.tebakan_ke}) {tebakan.upper()} | 🎉 MENANG! 🎉")
        st.balloons()
        st.success(f"🥳 SELAMAT! Anda menang dalam {st.session_state.tebakan_ke} kali percobaan!")
        st.session_state.game_active = False 
        return

    # Update Riwayat dan State
    st.session_state.riwayat_sesi.append(f"({st.session_state.tebakan_ke}) {tebakan.upper()} | Bulls: {bulls} | Cows: {cows}")
    st.session_state.tebakan_ke += 1
    
    # Feedback Instan
    if bulls > 0 or cows > 0:
        st.info(f"Umpan Balik: Bulls: {bulls} | Cows: {cows}")
    else:
        st.warning("Umpan Balik: Tidak ada yang benar.")
    
    # Reset input field setelah tebakan
    st.session_state.input_tebakan = "" # Menggunakan 'key' dari text_input

# --- 3. TAMPILAN UTAMA STREAMLIT ---

def main_app():
    
    inisialisasi_state()
    
    st.title("🐂 Cows and Bulls - Web App")
    st.markdown("---")
    
    # Tampilan Pilihan Mode (Menu Utama)
    if not st.session_state.game_active:
        st.header("Pilih Mode Permainan")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Mode Angka (4 Digit)", on_click=mulai_game, args=("angka",), type="primary")
        with col2:
            st.button("Mode Kata (4 Huruf)", on_click=mulai_game, args=("kata",), type="secondary")
        
        st.markdown("*Aplikasi ini menggunakan `st.session_state` sebagai 'memori' permainan.*")

    # Tampilan Game Aktif
    else:
        st.subheader(f"Mode: {st.session_state.mode.upper()} | Tebak {st.session_state.validasi_tipe} 4 karakter unik!")
        
        col_game, col_history = st.columns([1, 1])

        # A. Input Tebakan
        with col_game:
            # Gunakan key untuk mengontrol nilai input
            tebakan_input = st.text_input(
                f"Tebakan ke-{st.session_state.tebakan_ke}", 
                max_chars=4, 
                key="input_tebakan", 
                placeholder="Masukkan 4 karakter unik"
            )
            
            st.button(
                "TEBAK!", 
                on_click=proses_tebakan, 
                args=(tebakan_input,), 
                disabled=len(tebakan_input) != 4, # Tombol hanya aktif jika input 4 karakter
                type="primary"
            )
            
            # Button untuk memulai ulang game dengan mode yang sama
            st.button("Reset Game", on_click=mulai_game, args=(st.session_state.mode,))


        # B. Riwayat Permainan
        with col_history:
            st.markdown("### Riwayat")
            if st.session_state.riwayat_sesi:
                # Menampilkan riwayat dalam format list yang rapi
                riwayat_string = "\n".join(st.session_state.riwayat_sesi)
                st.code(riwayat_string, language="text")
            else:
                st.info("Mulai tebak untuk melihat riwayat.")

# --- JALANKAN APLIKASI ---
if __name__ == "__main__":
    main_app()