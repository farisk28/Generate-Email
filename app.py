import streamlit as st
import pandas as pd
import io

# 1. SETTING LAYOUT (Tampilan Penuh)
st.set_page_config(page_title="Email Template Generator - FDS", layout="wide")

st.title("✉️ Smart Email Template Generator - Fraud Analyst")
st.write("Unggah file CSV/Excel untuk menganalisis pola fraud dan membuat draf email FDS secara otomatis.")

# Fungsi pembantu untuk format tanggal yang aman di server Cloud
def format_date(dt):
    if pd.isnull(dt):
        return ""
    return f"{dt.month}/{dt.day}/{dt.year} {dt.strftime('%H:%M:%S')}"

# --- MENU PENGATURAN DI SIDEBAR ---
st.sidebar.header("⚙️ Pengaturan Dinamis")

email_mode = st.sidebar.selectbox(
    "Kirim Teks Email Ke:",
    options=["Deteksi Otomatis", "Issuer (Member)", "Acquirer (Merchant)"]
)

target_name = st.sidebar.text_input("Nama Target (cth: Seabank / Xendit)", value="Seabank")

# --- KOMPONEN UPLOAD FILE ---
uploaded_file = st.file_uploader("Pilih file CSV atau Excel", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Membaca data mentah sebagai bytes
        file_bytes = uploaded_file.read()
        
        # LOGIKA DETEKSI SUPER AMAN: Memeriksa isi jeroan file sesungguhnya
        try:
            # Mengintip 2000 karakter pertama file
            text_sample = file_bytes[:2000].decode('utf-8', errors='ignore')
            
            # Jika isinya mengandung format teks terpisah atau tag HTML spreadsheet bawaan export sistem
            if ',' in text_sample or ';' in text_sample or '\t' in text_sample or 'Date_Time' in text_sample or '<table' in text_sample:
                # Tentukan pemisah otomatis (koma atau titik koma)
                sep = ';' if ';' in text_sample and ',' not in text_sample else ','
                df = pd.read_csv(io.BytesIO(file_bytes), sep=sep)
            else:
                # Jika jeroannya biner (Excel asli)
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(io.BytesIO(file_bytes))
                else:
                    df = pd.read_excel(io.BytesIO(file_bytes))
        except Exception:
            # Cadangan terakhir jika deteksi otomatis gagal
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(file_bytes))
            else:
                try:
                    df = pd.read_excel(io.BytesIO(file_bytes))
                except Exception:
                    # Jika read_excel gagal karena OLE2 (Excel palsu), paksa baca sebagai teks/csv
                    df = pd.read_csv(io.BytesIO(file_bytes), on_bad_lines='skip')

        # Memastikan data berhasil dimuat ke tabel
        if df.empty:
            st.error("File kosong atau tidak dapat dibaca strateginya.")
            st.stop()

        st.success("File Microsoft Excel Workbook berhasil dimuat dan dianalisis!")

        # 2. Pembersihan Data Masukan (Data Cleaning)
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip("'").str.strip()
                
        if 'Merchant_Name' in df.columns:
            df['Merchant_Name'] = df['Merchant_Name'].apply(lambda x: " ".join(x.split()))

        if 'Amount_Trx' in df.columns:
            df['Amount_Trx'] = pd.to_numeric(df['Amount_Trx'], errors='coerce')
        if 'Date_Time' in df.columns:
            df['Date_Time'] = pd.to_datetime(df['Date_Time'], errors='coerce')

        # ================= LOGIKA OTOMATISASI DATA FRAUD =================
        
        total_trx = len(df)
        total_amount = int(df['Amount_Trx'].sum()) if 'Amount_Trx' in df.columns else 0
        formatted_amount = f"{total_amount:,}".replace(",", ".")

        min_date = format_date(df['Date_Time'].min()) if 'Date_Time' in df.columns else ""
        max_date = format_date(df['Date_Time'].max()) if 'Date_Time' in df.columns else ""

        if 'Amount_Trx' in df.columns and not df['Amount_Trx'].empty:
            nominal_counts = df['Amount_Trx'].value_counts()
            if not nominal_counts.empty:
                top_nominal = nominal_counts.index[0]
                top_nominal_freq = nominal_counts.iloc[0]
                
                if (top_nominal_freq / total_trx) > 0.5:
                    formatted_top_nominal = f"{int(top_nominal):,}".replace(",", ".")
                    indikasi_nominal = f"Transaksi didominasi dengan nominal Rp{formatted_top_nominal}"
                else:
                    indikasi_nominal = "Transaksi didominasi dengan pola angka unik"
            else:
                indikasi_nominal = "Transaksi didominasi dengan pola angka unik"
        else:
            indikasi_nominal = "Transaksi didominasi dengan pola angka unik"

        unique_cpans = df['CPAN_Masking'].nunique() if 'CPAN_Masking' in df.columns else 0
        unique_merchants = df['Merchant_Name'].nunique() if 'Merchant_Name' in df.columns else 0
        
        cpan_display = df['CPAN_Masking'].iloc[0] if unique_cpans > 0 else "[CPAN]"
        m_name = df['Merchant_Name'].iloc[0] if unique_merchants > 0 else "[MERCHANT]"

        if unique_cpans == 1 and unique_merchants == 1:
            indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN pada merchant yang sama yaitu {m_name}"
            auto_merchant_case = False
        elif unique_cpans == 1 and unique_merchants > 1:
            top_merchants = df['Merchant_Name'].value_counts().index[:3].tolist()
            merchants_str = ", ".join(top_merchants)
            indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN pada beberapa merchant yaitu {merchants_str}"
            auto_merchant_case = False
        elif unique_cpans > 1 and unique_merchants == 1:
            indikasi_cpan_merchant = "Transaksi Dilakukan oleh beberapa CPAN ke merchant yang sama secara berulang"
            auto_merchant_case = True
        else:
            if 'Merchant_Name' in df.columns and unique_merchants > 0:
                top_merchants = df['Merchant_Name'].value_counts().index[:3].tolist()
                merchants_str = ", ".join(top_merchants)
                indikasi_cpan_merchant = f"Transaksi dilakukan oleh beberapa CPAN pada beberapa merchant di antaranya {merchants_str}"
            else:
                indikasi_cpan_merchant = "Transaksi dilakukan oleh beberapa CPAN pada beberapa merchant"
            auto_merchant_case = True

        # =================================================================

        # Penentuan mode berdasarkan Dropdown
        if email_mode == "Issuer (Member)":
            is_merchant_case = False
            sumber_pilihan = "Manual (Dropdown)"
        elif email_mode == "Acquirer (Merchant)":
            is_merchant_case = True
            sumber_pilihan = "Manual (Dropdown)"
        else:
            is_merchant_case = auto_merchant_case
            sumber_pilihan = "Sistem (Otomatis)"

        # Pemilihan struktur template draf email
        if is_merchant_case:
            # --- TEMPLATE ACQUIRER / MERCHANTS ---
            email_text = f"""Dear Team {target_name},

Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai penyelenggara infrastruktur pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada Merchant {m_name}
 
Adapun indikasi yang kami temukan terkait transaksi tersebut :
1. Total nilai transaksi mencapai Rp{formatted_amount}
2. Transaksi dilakukan secara berulang sebanyak {total_trx} kali dalam kurun waktu berdekatan
3. {indikasi_cpan_merchant}
4. Transaksi terjadi dalam periode waktu {min_date} - {max_date}

Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:
1. Apakah dari sisi merchant terdapat indikasi abuse?
2. Barang / jasa apa yang ditawarkan merchant pada transaksi terlampir?
3. Apakah profil merchant sesuai dengan pola transaksinya?
4. Jika transaksi di merchant tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.
 
Password akan kami kirim dengan email terpisah. 
Jika ada pertanyaan lebih lanjut tentang terkait case ini.
Jangan ragu jika ingin menghubungi kami melalui email ini atau bisa menghubungi nomor operasional kami: 0851 7968 1636

Demikian yang dapat kami sampaikan,
atas perhatiannya kami ucapkan terima kasih
 
Simple Payment, Redefined.
Best Regards,
Fraud Analyst
Enterprise, Architecture & Cybersecurity
Hotline Whatsapp : 0851 7968 1636
PT. ALTO Network"""

        else:
            # --- TEMPLATE ISSUER / BANK ---
            email_text = f"""Dear Rekan {target_name},

Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN ({cpan_display}).

Adapun indikasi yang kami temukan terkait transaksi tersebut :
1. Total nilai transaksi mencapai Rp{formatted_amount}
2. Transaksi dilakukan secara berulang sebanyak {total_trx} kali dalam kurun waktu berdekatan
3. {indikasi_nominal}
4. {indikasi_cpan_merchant}
5. Transaksi terjadi dalam periode waktu {min_date} - {max_date}

Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:  
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ?
2. Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku?
3. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?

Mohon dapat menginformasikan kembali hasil pengecekannya, agar kami dapat meningkatkan akurasi pada FDS kami. Jika diperlukan kami juga dapat mendukung terkait kasus fraud yang terkonfirmasi sesuai dengan kewenangan yang diberikan kepada PT. ALTO Network.

Note: Password akan kami kirim dengan email terpisah.

Demikian yang dapat kami sampaikan,
atas perhatiannya kami ucapkan terima kasih
 
Simple Payment, Redefined.
Best Regards,
Fraud Analyst
Enterprise, Architecture & Cybersecurity
Hotline Whatsapp : 0851 7968 1636
PT. ALTO Network"""

        # --- TAMPILAN OUTPUT UTAMA ---
        st.subheader("📋 Hasil Generate Teks Email")
        status_template = "Acquirer (Merchant)" if is_merchant_case else "Issuer (Bank)"
        st.info(f"⚙️ **Mode Aktif:** Menggunakan template **{status_template}** berdasarkan pilihan **{sumber_pilihan}**.")

        st.text_area("Salin teks hasil otomatisasi di bawah ini:", value=email_text, height=480)
        
        st.download_button(
            label="📥 Download Teks Email (.txt)",
            data=email_text,
            file_name=f"Email_Fraud_{target_name}.txt",
            mime="text/plain"
        )

        st.subheader("📊 Metrik Ringkasan Pola Data")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Frekuensi Transaksi", f"{total_trx} Kali Trx")
        col2.metric("Total Nominal Terhitung", f"Rp {formatted_amount}")
        col3.metric("Jumlah Unik Kartu (CPAN)", f"{unique_cpans} Card")
        col4.metric("Jumlah Unik Merchant", f"{unique_merchants} Merchant")

    except Exception as e:
        st.error(f"Terjadi kesalahan teknis dalam pemrosesan logika file: {e}")
