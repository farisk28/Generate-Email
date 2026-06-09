import streamlit as st
import pandas as pd

st.set_page_config(page_title="Email Template Generator - FDS", layout="padded")
st.title("✉️ Smart Email Template Generator - Fraud Analyst")
st.write("Unggah file CSV/Excel untuk menganalisis pola fraud dan membuat email secara otomatis.")

# Fungsi format tanggal yang aman
def format_date(dt):
    if pd.isnull(dt):
        return ""
    return f"{dt.month}/{dt.day}/{dt.year} {dt.strftime('%H:%M:%S')}"

# Pengaturan Sidebar
st.sidebar.header("⚙️ Pengaturan")
bank_name = st.sidebar.text_input("Nama Bank Target", value="Seabank")
switching_name = st.sidebar.text_input("Nama Pihak/Switching", value="PT. ALTO Network")

uploaded_file = st.file_uploader("Pilih file CSV atau Excel", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 1. Baca File
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("File berhasil dianalisis!")

        # 2. Pembersihan Data Bawaan
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip("'")
                
        if 'Merchant_Name' in df.columns:
            df['Merchant_Name'] = df['Merchant_Name'].str.replace(r'\s+', ' ', regex=True).str.strip()

        df['Amount_Trx'] = pd.to_numeric(df['Amount_Trx'], errors='coerce')
        df['Date_Time'] = pd.to_datetime(df['Date_Time'], errors='coerce')

        # ================= LOGIKA OTOMATISASI =================
        
        # A. Hitung Total Transaksi & Nominal
        total_trx = len(df)
        total_amount = int(df['Amount_Trx'].sum())
        formatted_amount = f"{total_amount:,}".replace(",", ".")

        # B. Deteksi Waktu Terawal & Terakhir
        min_date = format_date(df['Date_Time'].min())
        max_date = format_date(df['Date_Time'].max())

        # C. Deteksi Dominasi Nominal vs Pola Unik
        # Mencari nominal yang paling sering muncul
        nominal_counts = df['Amount_Trx'].value_counts()
        if not nominal_counts.empty:
            top_nominal = nominal_counts.index[0]
            top_nominal_freq = nominal_counts.iloc[0]
            
            # Jika nominal teratas muncul lebih dari 50% dari seluruh transaksi, dianggap dominan
            if (top_nominal_freq / total_trx) > 0.5:
                formatted_top_nominal = f"{int(top_nominal):,}".replace(",", ".")
                indikasi_nominal = f"Transaksi didominasi dengan nominal Rp{formatted_top_nominal}"
            else:
                indikasi_nominal = "Transaksi didominasi dengan pola angka unik"
        else:
            indikasi_nominal = "Transaksi didominasi dengan pola angka unik"

        # D. Logika Kondisional CPAN & Merchant
        unique_cpans = df['CPAN_Masking'].nunique() if 'CPAN_Masking' in df.columns else 0
        unique_merchants = df['Merchant_Name'].nunique() if 'Merchant_Name' in df.columns else 0
        
        # Ambil sampel masker CPAN untuk di text
        cpan_display = df['CPAN_Masking'].iloc[0] if unique_cpans > 0 else "[CPAN]"

        indikasi_cpan_merchant = ""
        if unique_cpans == 1 and unique_merchants == 1:
            # Case a: 1 CPAN ke 1 Merchant
            m_name = df['Merchant_Name'].iloc[0]
            indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN pada merchant yang sama yaitu {m_name}"
            
        elif unique_cpans == 1 and unique_merchants > 1:
            # Case b: 1 CPAN ke beberapa Merchant (Maksimal ambil 3)
            top_merchants = df['Merchant_Name'].value_counts().index[:3].tolist()
            merchants_str = ", ".join(top_merchants)
            indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN pada beberapa merchant yaitu {merchants_str}"
            
        elif unique_cpans > 1 and unique_merchants == 1:
            # Case c: Beberapa CPAN ke 1 Merchant
            m_name = df['Merchant_Name'].iloc[0]
            indikasi_cpan_merchant = f"Transaksi dilakukan oleh beberapa CPAN pada merchant yang sama yaitu {m_name}"
            cpan_display = "beberapa CPAN terlampir"
            
        else:
            # Case Tambahan: Beberapa CPAN ke Beberapa Merchant
            top_merchants = df['Merchant_Name'].value_counts().index[:3].tolist()
            merchants_str = ", ".join(top_merchants)
            indikasi_cpan_merchant = f"Transaksi dilakukan oleh beberapa CPAN pada beberapa merchant di antaranya {merchants_str}"
            cpan_display = "beberapa CPAN terlampir"

        # ======================================================

        # 3. Susun Teks Email Berdasarkan Hasil Analisis Otomatis
        email_text = f"""Dear Rekan {bank_name},

Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN ({cpan_display}).

Adapun indikasi yang kami temukan terkait transaksi tersebut :
Total nilai transaksi mencapai Rp{formatted_amount}
Transaksi dilakukan secara berulang sebanyak {total_trx} kali dalam kurun waktu berdekatan
{indikasi_nominal}
{indikasi_cpan_merchant}
Transaksi terjadi dalam periode waktu {min_date} - {max_date}

Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:  
Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ?
Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku?
Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?

Mohon dapat menginformasikan kembali hasil pengecekannya, agar kami dapat meningkatkan akurasi pada FDS kami. Jika diperlukan kami juga dapat mendukung terkait kasus fraud yang terkonfirmasi sesuai dengan kewenangan yang diberikan kepada {switching_name}.

Note: Password akan kami kirim dengan email terpisah.

Demikian yang dapat kami sampaikan,
atas perhatiannya kami ucapkan terima kasih
 
Simple Payment, Redefined.
Best Regards,
Fraud Analyst
Enterprise, Architecture & Cybersecurity
Hotline Whatsapp : 0851 7968 1636
{switching_name}"""

        # 4. Tampilkan di UI Streamlit
        st.subheader("📋 Hasil Generate Teks Email")
        st.text_area("Salin teks di bawah ini:", value=email_text, height=480)
        
        st.download_button(
            label="📥 Download Teks Email (.txt)",
            data=email_text,
            file_name=f"Email_Fraud_{bank_name}.txt",
            mime="text/plain"
        )

        # Tampilkan metrik singkat untuk mempermudah cross-check kerjaanmu
        st.subheader("📊 Metrik Hasil Analisis Otomatis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Transaksi", f"{total_trx} Trx")
        col2.metric("Total Nilai", f"Rp {formatted_amount}")
        col3.metric("Pola Nominal", "Dominan Pecahan" if "nominal" in indikasi_nominal.lower() else "Angka Unik")

    except Exception as e:
        st.error(f"Terjadi kesalahan pemrosesan logika: {e}")
