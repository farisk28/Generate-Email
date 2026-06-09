import streamlit as st
import pandas as pd

# 1. SETTING LAYOUT 
st.set_page_config(page_title="Email Template Generator - FDS", layout="wide")

st.title("✉️ Smart Email Template Generator - Fraud Analyst")
st.write("Unggah file CSV/Excel untuk menganalisis pola fraud dan membuat draf email FDS secara otomatis.")

# Fungsi pembantu untuk format tanggal yang aman di server Linux (Streamlit Cloud)
def format_date(dt):
    if pd.isnull(dt):
        return ""
    return f"{dt.month}/{dt.day}/{dt.year} {dt.strftime('%H:%M:%S')}"

# --- MENU PENGATURAN DI SIDEBAR ---
st.sidebar.header("⚙️ Pengaturan Dinamis")
# Input dinamis untuk nama tujuan (Bisa Bank / Acquirer seperti Xendit, dll)
target_name = st.sidebar.text_input("Nama Target (Bank / Acquirer)", value="Seabank")

# --- KOMPONEN UPLOAD FILE ---
uploaded_file = st.file_uploader("Pilih file CSV atau Excel", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 1. Proses Pembacaan File (Mendukung CSV dan Excel)
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("File berhasil diunggah dan dianalisis secara otomatis!")

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
        
        # A. Otomatisasi Hitung Total Nominal & Total Baris Transaksi
        total_trx = len(df)
        total_amount = int(df['Amount_Trx'].sum()) if 'Amount_Trx' in df.columns else 0
        formatted_amount = f"{total_amount:,}".replace(",", ".")

        # B. Otomatisasi Deteksi Rentang Waktu (Terawal dan Terakhir)
        min_date = format_date(df['Date_Time'].min()) if 'Date_Time' in df.columns else ""
        max_date = format_date(df['Date_Time'].max()) if 'Date_Time' in df.columns else ""

        # C. Otomatisasi Deteksi Dominasi Nominal vs Pola Angka Unik
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

        # D. Otomatisasi Analisis Hubungan Kondisional CPAN & Merchant (Case a, b, c)
        unique_cpans = df['CPAN_Masking'].nunique() if 'CPAN_Masking' in df.columns else 0
        unique_merchants = df['Merchant_Name'].nunique() if 'Merchant_Name' in df.columns else 0
        
        cpan_display = df['CPAN_Masking'].iloc[0] if unique_cpans > 0 else "[CPAN]"
        m_name = df['Merchant_Name'].iloc[0] if unique_merchants > 0 else "[MERCHANT]"

        # Variabel penentu alur / template email
        is_merchant_case = False

        if unique_cpans == 1 and unique_merchants == 1:
            # Case a: 1 CPAN ke 1 Merchant
            indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN pada merchant yang sama yaitu {m_name}"
            is_merchant_case = False
            
        elif unique_cpans == 1 and unique_merchants > 1:
            # Case b: 1 CPAN ke beberapa Merchant
            top_merchants = df['Merchant_Name'].value_counts().index[:3].tolist()
            merchants_str = ", ".join(top_merchants)
            indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN pada beberapa merchant yaitu {merchants_str}"
            is_merchant_case = False
            
        elif unique_cpans > 1 and unique_merchants == 1:
            # Case c: Beberapa CPAN ke 1 Merchant (🚨 MASUK KE TEMPLATE ACQUIRER/MERCHANT 🚨)
            indikasi_cpan_merchant = "Transaksi Dilakukan oleh beberapa CPAN ke merchant yang sama secara berulang"
            is_merchant_case = True
            
        else:
            # Banyak CPAN ke Banyak Merchant
            if 'Merchant_Name' in df.columns and unique_merchants > 0:
                top_merchants = df['Merchant_Name'].value_counts().index[:3].tolist()
                merchants_str = ", ".join(top_merchants)
                indikasi_cpan_merchant = f"Transaksi dilakukan oleh beberapa CPAN pada beberapa merchant di antaranya {merchants_str}"
            else:
                indikasi_cpan_merchant = "Transaksi dilakukan oleh beberapa CPAN pada beberapa merchant"
            is_merchant_case = True

        # =================================================================

        # 3. PEMILIHAN TEMPLATE EMAIL SECARA OTOMATIS
        if is_merchant_case:
            # --- TEMPLATE CASE C (BEBERAPA CPAN KE 1 MERCHANT - CONTOH XENDIT) ---
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
            # --- TEMPLATE CASE A & B (1 CPAN KE BANK ISSUER) ---
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

        # --- TAMPILAN OUTPUT UTAMA PADA LAYOUT ---
        st.subheader("📋 Hasil Generate Teks Email")
        
        # Penanda tipe template yang sedang aktif agar kamu tau jalurnya
        if is_merchant_case:
            st.info(f"💡 Jalur Deteksi: **Template Investigasi Merchant (Acquirer)** aktif karena terdeteksi {unique_cpans} CPAN berbeda.")
        else:
            st.info(f"💡 Jalur Deteksi: **Template Investigasi Kartu (Issuer)** aktif karena terdeteksi tunggal 1 CPAN.")

        st.text_area("Salin teks hasil otomatisasi di bawah ini:", value=email_text, height=480)
        
        st.download_button(
            label="📥 Download Teks Email (.txt)",
            data=email_text,
            file_name=f"Email_Fraud_{target_name}.txt",
            mime="text/plain"
        )

        # Dashboard Metrik Tambahan
        st.subheader("📊 Metrik Ringkasan Pola Data")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Frekuensi Transaksi", f"{total_trx} Kali Trx")
        col2.metric("Total Nominal Terhitung", f"Rp {formatted_amount}")
        col3.metric("Jumlah Unik Kartu (CPAN)", f"{unique_cpans} Card")
        col4.metric("Jumlah Unik Merchant", f"{unique_merchants} Merchant")

    except Exception as e:
        st.error(f"Terjadi kesalahan teknis dalam pemrosesan logika file: {e}")
        st.info("💡 Tips Cloud: Pastikan nama-nama kolom pada file masukan Anda sudah sesuai seperti 'Date_Time', 'Amount_Trx', 'CPAN_Masking', dan 'Merchant_Name'.")
