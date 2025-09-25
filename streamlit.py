import streamlit as st
import random
import pandas as pd
import numpy as np

# --- 0. FUNGSI UTILITY KHUSUS STREAMLIT ---

def tampilkan_health_bar(current_bulls):
    """
    Menampilkan progress bar kustom yang meniru health bar.
    current_bulls adalah jumlah Bulls dari tebakan terakhir.
    """
    # Menghitung persentase berdasarkan Bulls saat ini (maksimal 4)
    persen = int((current_bulls / 4) * 100) if current_bulls > 0 else 0
    
    # Menentukan warna berdasarkan persentase
    if persen == 100:
        warna = "#2ecc71"  # Hijau (Penuh/Menang)
    elif persen >= 50:
        warna = "#f1c40f"  # Kuning (Sedang)
    else:
        warna = "#e74c3c"  # Merah (Rendah)
        
    # Menggunakan HTML/CSS kustom
    st.markdown(f"""
        <div style="font-weight: bold; font-size: 1.1em; margin-bottom: 5px;">
            PROGRESS TEBAKAN TERAKHIR (4 BULLS):
        </div>
        <div style="background-color: #ddd; border: 2px solid #333; border-radius: 5px; height: 35px; margin-bottom: 15px;">
            <div style="
                background-color: {warna}; 
                height: 100%; 
                width: {persen}%; 
                border-radius: 3px; 
                text-align: right; 
                line-height: 35px; 
                color: #222; 
                font-weight: bold;
                padding-right: 10px;
                transition: width 0.5s;">
                {persen}% ({current_bulls}/4 Bulls)
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 1. LOGIKA INTI GAME ---

def hitung_cows_bulls(tebakan, rahasia):
    """Menghitung jumlah Bulls dan Cows."""
    bulls = 0
    cows = 0
    tebakan_list = list(tebakan)
    rahasia_list = list(rahasia)

    # Hitung Bulls dan Tandai dengan None
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
        MAX_GUESSES = 12
    elif mode == "kata":
        unique_words = ["love", "park", "fire", "hope", "jump", "talk", "many", "rule", "sink", "read"]
        kata_kunci = random.choice(unique_words)
        validasi = "Huruf Unik"
        MAX_GUESSES = 10 
        
    return kata_kunci, validasi, MAX_GUESSES

# --- 2. MANAJEMEN STATE STREAMLIT ---

def inisialisasi_state(mode_setelah_reset=None):
    """Mengatur semua variabel di st.session_state (Memori Aplikasi Web)."""
    st.session_state.kata_kunci_rahasia = None
    st.session_state.mode = mode_setelah_reset
    st.session_state.validasi_tipe = ""
    st.session_state.tebakan_ke = 0
    st.session_state.riwayat_sesi = []
    st.session_state.game_active = False
    st.session_state.max_guesses = 0
    st.session_state.input_tebakan = "" 

def mulai_game(mode_pilihan):
    """Meriset state dan memulai game baru."""
    kunci, tipe, batas_tebakan = generate_kata_kunci_acak(mode_pilihan)
    
    st.session_state.kata_kunci_rahasia = kunci
    st.session_state.validasi_tipe = tipe
    st.session_state.max_guesses = batas_tebakan
    st.session_state.mode = mode_pilihan
    st.session_state.tebakan_ke = 1
    st.session_state.riwayat_sesi = []
    st.session_state.game_active = True
    st.session_state.input_tebakan = "" 

def proses_tebakan(tebakan):
    """Memproses tebakan pengguna dan memperbarui state."""
    
    tebakan = tebakan.lower().strip()
    
    # 1. Validasi Input
    if len(tebakan) != 4 or len(set(tebakan)) != 4:
        st.error(f"Tebakan harus 4 {st.session_state.validasi_tipe} unik!")
        return
    if st.session_state.mode == "angka" and not tebakan.isdigit():
        st.error("Hanya boleh angka!")
        return
    if st.session_state.mode == "kata" and not tebakan.isalpha():
        st.error("Hanya boleh huruf!")
        return

    # 2. Hitung Hasil
    bulls, cows = hitung_cows_bulls(tebakan, st.session_state.kata_kunci_rahasia)
    
    # 3. Update Riwayat
    st.session_state.riwayat_sesi.append({
        'No.': st.session_state.tebakan_ke,
        'Tebakan': tebakan.upper(),
        'Bulls': bulls,
        'Cows': cows
    })
    
    # 4. Cek Kemenangan
    if tebakan == st.session_state.kata_kunci_rahasia:
        st.balloons()
        st.success(f"🥳 SELAMAT! Anda menang dalam {st.session_state.tebakan_ke} kali percobaan!")
        st.session_state.game_active = False 
        return

    # 5. Cek Batas Tebakan
    st.session_state.tebakan_ke += 1
    if st.session_state.tebakan_ke > st.session_state.max_guesses:
        st.error(f"❌ Anda kalah! Kunci rahasianya adalah: **{st.session_state.kata_kunci_rahasia.upper()}**")
        st.session_state.game_active = False
        return

    # 6. Feedback Instan
    if bulls > 0 or cows > 0:
        st.info(f"Umpan Balik: Bulls: {bulls} | Cows: {cows}")
    else:
        st.warning("Umpan Balik: Tidak ada yang benar.")
    
    # Kosongkan input
    st.session_state.input_tebakan = "" 

# --- 3. TAMPILAN UTAMA STREAMLIT ---

def main_app():
    
    # Inisialisasi State jika belum ada
    if 'game_active' not in st.session_state:
        inisialisasi_state()
    
    st.set_page_config(page_title="Cows and Bulls", layout="wide")
    st.title("🐂 Cows and Bulls - Web App")
    st.markdown("---")
    
    # --- Pilihan Mode (Menu Utama) ---
    if not st.session_state.game_active:
        st.header("Pilih Mode Permainan")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("1️⃣ Mode Angka (12x Coba)", on_click=mulai_game, args=("angka",), type="primary")
        with col2:
            st.button("🔠 Mode Kata (10x Coba)", on_click=mulai_game, args=("kata",), type="secondary")
        
        st.markdown("---")
        with st.expander("❓ Aturan Main (Wajib Baca!)"):
            st.write("""
            **Tujuan:** Menebak 4 karakter unik (angka/huruf) rahasia.
            * **BULLS 🐂:** Jumlah karakter yang **benar dan posisinya juga benar**.
            * **COWS 🐄:** Jumlah karakter yang **benar, tetapi posisinya salah**.
            """)
            
    # --- Tampilan Game Aktif ---
    else:
        st.subheader(f"Mode: {st.session_state.mode.upper()}")
        st.caption(f"Tebak {st.session_state.validasi_tipe} 4 karakter unik! Anda punya **{st.session_state.max_guesses - st.session_state.tebakan_ke + 1}** kesempatan lagi.")

        col_game, col_history = st.columns([1, 1])

        # A. Game Control & Input
        with col_game:
            
            # Progress Bar Batas Tebakan
            progress_val = (st.session_state.tebakan_ke - 1) / st.session_state.max_guesses
            st.progress(progress_val, text=f"Progress Sesi: {st.session_state.tebakan_ke - 1} dari {st.session_state.max_guesses} tebakan.")
            
            st.markdown("---")
            
            # Input Tebakan
            tebakan_input = st.text_input(
                f"Tebakan ke-{st.session_state.tebakan_ke}", 
                max_chars=4, 
                key="input_tebakan", 
                placeholder="Masukkan 4 karakter unik"
            )
            
            # Tombol Tebak
            st.button(
                "TEBAK!", 
                on_click=proses_tebakan, 
                args=(tebakan_input,), 
                disabled=len(tebakan_input) != 4 or st.session_state.tebakan_ke > st.session_state.max_guesses,
                type="primary"
            )
            
            # Tombol Reset
            st.button("Kembali ke Menu Utama", on_click=inisialisasi_state, args=(None,))


        # B. Riwayat Permainan dan Health Bar
        with col_history:
            
            # --- LOGIKA HEALTH BAR RESPONSIVE (Sudah Diperbaiki) ---
            bulls_terakhir = 0
            
            # Pengecekan aman (Perbaikan error Line 146)
            if st.session_state.riwayat_sesi: 
                # Ambil nilai Bulls dari item terakhir
                bulls_terakhir = st.session_state.riwayat_sesi[-1].get('Bulls', 0) 
            
            tampilkan_health_bar(bulls_terakhir)
            
            st.markdown("### Tabel Detail Riwayat")
            
            if st.session_state.riwayat_sesi:
                # Mengubah List of Dict menjadi DataFrame (Pemanfaatan Pandas)
                df_history = pd.DataFrame(st.session_state.riwayat_sesi)
                df_history.set_index('No.', inplace=True)
                
                # Menampilkan Tabel Riwayat Mentah
                st.dataframe(df_history, use_container_width=True)
            else:
                st.info("Mulai tebak untuk melihat detail.")

# --- JALANKAN APLIKASI ---
if __name__ == "__main__":
    main_app()
