import streamlit as st
# (Semua import lainnya tetap sama)
import random
import pandas as pd
import numpy as np


# --- FUNGSI TAMPILAN HEALTH BAR (SAMA DENGAN SEBELUMNYA) ---

def tampilkan_health_bar(current_bulls):
    """
    Menampilkan progress bar kustom yang meniru health bar.
    current_bulls adalah jumlah Bulls dari tebakan terakhir.
    """
    # Pastikan tidak ada pembagian dengan nol jika max_bulls_tertinggi masih 0
    persen = int((current_bulls / 4) * 100) if current_bulls > 0 else 0
    
    # Menentukan warna berdasarkan persentase
    if persen == 100:
        warna = "#2ecc71"  # Hijau (Penuh/Menang)
    elif persen >= 50:
        warna = "#f1c40f"  # Kuning (Sedang)
    else:
        warna = "#e74c3c"  # Merah (Rendah)
        
    # Menggunakan HTML/CSS kustom untuk bar
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


# (Semua fungsi lain: hitung_cows_bulls, generate_kata_kunci_acak, inisialisasi_state, mulai_game, proses_tebakan tetap sama)


# --- FUNGSI UTAMA (HANYA BAGIAN TAMPILAN YANG BERUBAH) ---

def main_app():
    
    # Panggil inisialisasi
    if 'game_active' not in st.session_state:
        inisialisasi_state()
    
    st.set_page_config(page_title="Cows and Bulls", layout="wide")
    st.title("🐂 Cows and Bulls - Web App")
    st.markdown("---")
    
    # --- Pilihan Mode (Menu Utama) ---
    # (Tetap Sama)
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
            
            # --- LOGIKA BARU UNTUK HEALTH BAR RESPONSIVE ---
            bulls_terakhir = 0
            if st.session_state.riwayat_sesi:
                # Ambil nilai Bulls dari item terakhir di list riwayat (Dictionary)
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
    # (Fungsi ini menjalankan keseluruhan aplikasi)
    # (As
