import streamlit as st
import pandas as pd
import io
import re
from templates import TEMPLATES

# 1. SETTING LAYOUT (Tampilan Penuh)
st.set_page_config(page_title="Email Template Generator - FDS", layout="wide")

st.title("✉️ Email Template Generator")
st.write("Unggah data transaksi FDS untuk mengekstrak indikasi fraud dan membuat email secara otomatis. (Dalam bentuk CSV atau Excel)")

# Fungsi pembantu format tanggal
def format_date(dt):
    if pd.isnull(dt):
        return ""
    return f"{dt.month}/{dt.day}/{dt.year} {dt.strftime('%H:%M:%S')}"

# --- MENU DROPDOWN DI SIDEBAR ---
st.sidebar.header("⚙️ Pengaturan Global")

# Pilihan Bahasa Global (Mempengaruhi seluruh isi email)
email_lang = st.sidebar.selectbox(
    "Pilih Bahasa Email (Global Language):",
    options=["Bahasa Indonesia", "English"]
)

# Pilihan Kasus Router (Case 1 s.d Case 10)
chosen_case = st.sidebar.selectbox(
    "Pilih Jenis Case Investigasi:",
    options=[
        "Case 1: EMAIL ACQUIRER/MERCHANT, Produk QR",
        "Case 2: EMAIL MERCHANT KENAIKAN TPV RC 107 / RC 59, Produk QR",
        "Case 3: EMAIL MERCHANT LEBIH DARI 1, Produk QR",
        "Case 4: EMAIL ACQUIRER QRCB INBOUND, Produk QR CB",
        "Case 5: EMAIL NAMA MERCHANT ANOMALI (Acquirer), Produk QR",
        "Case 5: EMAIL NAMA MERCHANT ANOMALI  (Issuer), Produk QR",
        "Case 6: EMAIL ACQUIRER QRCB OUTBOUND, Produk QR CB",
        "Case 7: EMAIL ISSUER/CUSTOMER QRCB, Produk QR CB",
        "Case 8: EMAIL ISSUER LEBIH DARI 1, Produk QR",
        "Case 9: EMAIL ISSUER/CUSTOMER, Produk QR",
        "Case 10: EMAIL ISSUER PROCODE 263000, Produk QR"
    ]
)

target_name = st.sidebar.text_input("Nama Instansi Target (cth: NOBU / DANA / BCA / ShopeePay / Bank Jago)", value="DANA")

# --- KOMPONEN UPLOAD FILE ---
uploaded_file = st.file_uploader("Pilih file data transaksi (CSV atau Excel Workbook)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        
        # Penanganan Pembacaan File Pintar (Anti-Crash Biner & Teks)
        if uploaded_file.name.endswith('.csv'):
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), sep=',')
            except Exception:
                df = pd.read_csv(io.BytesIO(file_bytes), sep=';')
        else:
            try:
                df = pd.read_excel(io.BytesIO(file_bytes))
            except Exception as excel_err:
                try:
                    df = pd.read_csv(io.BytesIO(file_bytes), sep=',')
                except Exception:
                    df = pd.read_csv(io.BytesIO(file_bytes), sep=';')

        if df.empty:
            st.error("File tidak memiliki baris data.")
            st.stop()

        st.success("File data transaksi berhasil dimuat dan dianalisis!")

        # 2. Pembersihan Data Masukan
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip("'").str.strip()
                
        if 'Merchant_Name' in df.columns:
            df['Merchant_Name'] = df['Merchant_Name'].apply(lambda x: " ".join(x.split()))
        if 'Amount_Trx' in df.columns:
            df['Amount_Trx'] = pd.to_numeric(df['Amount_Trx'], errors='coerce')
        if 'Date_Time' in df.columns:
            df['Date_Time'] = pd.to_datetime(df['Date_Time'], errors='coerce')

        # ================= LOGIKA MATRIKS ATURAN (RULE-BASED REASONING) =================
        
        total_trx = len(df)
        total_amount = int(df['Amount_Trx'].sum()) if 'Amount_Trx' in df.columns else 0
        formatted_amount = f"{total_amount:,}".replace(",", ".")

        min_date = format_date(df['Date_Time'].min()) if 'Date_Time' in df.columns else ""
        max_date = format_date(df['Date_Time'].max()) if 'Date_Time' in df.columns else ""

        # A. Pengkondisian Deteksi Nominal & Pola Keriting vs Unik
        is_keriting = False
        formatted_top_nominal = "0"
        
        if 'Amount_Trx' in df.columns and not df['Amount_Trx'].empty:
            nominal_counts = df['Amount_Trx'].value_counts()
            if not nominal_counts.empty:
                top_nominal = nominal_counts.index[0]
                formatted_top_nominal = f"{int(top_nominal):,}".replace(",", ".")
                top_nominal_freq = nominal_counts.iloc[0]
                
                top_nominal_str = str(int(top_nominal))
                is_keriting = bool(re.search(r'(\d)\1\1', top_nominal_str))
                
                # Cek Pola Kelompok Nominal (Sama / Keriting / Unik)
                if email_lang == "Bahasa Indonesia":
                    if is_keriting and (top_nominal_freq / total_trx) > 0.4:
                        indikasi_nominal = "Transaksi didominasi dengan pola angka keriting"
                    elif (top_nominal_freq / total_trx) > 0.6:
                        indikasi_nominal = "Transaksi dilakukan dengan nominal yang sama"
                    else:
                        # Pola Unik Berdasarkan Range Digit Jutaan
                        sample_amount = str(int(top_nominal))
                        if len(sample_amount) >= 7:
                            indikasi_nominal = f"Transaksi didominasi dengan nominal yang besar dan unik yaitu Rp {sample_amount[0]},{sample_amount[1:3]}xx,xxx"
                        else:
                            indikasi_nominal = "Transaksi didominasi dengan nominal yang unik"
                else:
                    # English Term
                    if is_keriting and (top_nominal_freq / total_trx) > 0.4:
                        indikasi_nominal = "Transactions are dominated by repetitive/patterned numbers (angka keriting)"
                    elif (top_nominal_freq / total_trx) > 0.6:
                        indikasi_nominal = "Transactions were conducted with the same nominal value"
                    else:
                        sample_amount = str(int(top_nominal))
                        if len(sample_amount) >= 7:
                            indikasi_nominal = f"The transactions are dominated by the similar nominal value IDR {sample_amount[0]},{sample_amount[1:3]}xx,xxx"
                        else:
                            indikasi_nominal = "Transactions are dominated by unique/random nominal values"
        else:
            indikasi_nominal = ""

        # B. Deteksi Unik CPAN, MPAN & Nama Merchant
        unique_cpans = df['CPAN_Masking'].nunique() if 'CPAN_Masking' in df.columns else 0
        unique_merchants = df['Merchant_Name'].nunique() if 'Merchant_Name' in df.columns else 0
        
        cpan_display = df['CPAN_Masking'].iloc[0] if unique_cpans > 0 else "[CPAN]"
        mpan_display = df['MPAN_Masking'].iloc[0] if 'MPAN_Masking' in df.columns and len(df) > 0 else "[MPAN]"
        m_name = df['Merchant_Name'].iloc[0] if unique_merchants > 0 else "[MERCHANT]"

        # Menggabungkan nomor kartu CPAN jika ada lebih dari 1 untuk draf text
        if 'CPAN_Masking' in df.columns:
            cpans_list = df['CPAN_Masking'].unique().tolist()
            cpan_list_string = ", ".join(cpans_list)
        else:
            cpan_list_string = cpan_display

        # String Kondisi Kenaikan TPV atau Multi-Card
        if email_lang == "Bahasa Indonesia":
            cpan_count_string = f"1 CPAN" if unique_cpans == 1 else f"{unique_cpans} CPAN berbeda"
            if unique_cpans == 1 and unique_merchants == 1:
                indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN pada 1 Merchant yang sama yaitu {m_name}"
            elif unique_cpans == 1 and unique_merchants > 1:
                indikasi_cpan_merchant = "Transaksi dilakukan oleh 1 CPAN pada berbagai merchant berbeda-beda"
            else:
                indikasi_cpan_merchant = "Transaksi dilakukan secara berulang oleh beberapa CPAN pada merchant yang sama"
        else:
            # English
            cpan_count_string_en = f"1 CPAN" if unique_cpans == 1 else f"{unique_cpans} different CPANs"
            if unique_cpans == 1 and unique_merchants == 1:
                indikasi_cpan_merchant = f"Transactions were performed by 1 CPAN at the same 1 Merchant"
            elif unique_cpans == 1 and unique_merchants > 1:
                indikasi_cpan_merchant = "Transactions were performed by 1 CPAN at various different merchants"
            else:
                indikasi_cpan_merchant = "Repeated transactions conducted by the same CPANs at the same merchant"

        # Logika Gabungan Nama Merchant Banyak (Case 3)
        if unique_merchants > 1:
            all_merchants = df['Merchant_Name'].unique().tolist()
            if len(all_merchants) > 1:
                merchant_list_string = " dan ".join([", ".join(all_merchants[:-1]), all_merchants[-1]])
            else:
                merchant_list_string = all_merchants[0]
        else:
            merchant_list_string = m_name

        # D. Deteksi Limit Akumulasi Nominal Per-CPAN (> 50 Juta)
        indikasi_limit_cpan = ""
        if 'CPAN_Masking' in df.columns and 'Amount_Trx' in df.columns:
            cpan_grp = df.groupby('CPAN_Masking')['Amount_Trx'].sum()
            over_limit_count = len(cpan_grp[cpan_grp > 50000000])
            if over_limit_count > 0:
                if email_lang == "Bahasa Indonesia":
                    indikasi_limit_cpan = f"1 CPAN melakukan transaksi dengan total > Rp 50 Juta" if unique_cpans == 1 else f"Terdapat CPAN yang melakukan transaksi dengan akumulasi > Rp 50 Juta"
                else:
                    indikasi_limit_cpan = f"1 CPAN performed transactions with total > IDR 50 Million"
            else:
                if email_lang == "Bahasa Indonesia":
                    indikasi_limit_cpan = f"1 CPAN melakukan transaksi dengan total nilai Rp {formatted_amount}" if unique_cpans == 1 else f"Total keseluruhan transaksi adalah Rp {formatted_amount}"
                else:
                    indikasi_limit_cpan = f"1 CPAN conducted transactions with total value IDR {formatted_amount}" if unique_cpans == 1 else f"Total overall transaction value is IDR {formatted_amount}"

        # E. Deteksi Otomatis Response Code & Processing Code (RC 61, RC 107, Procode 263000)
        rc_61_count = 0
        rc_107_count = 0
        procode_263000_found = False
        
        if 'Response_Code' in df.columns:
            rc_61_count = len(df[df['Response_Code'].isin(['61', "'61'", 'RC 61'])])
            rc_107_count = len(df[df['Response_Code'].isin(['107', "'107'", 'RC 107'])])
        if 'Procode' in df.columns:
            procode_263000_found = any(df['Procode'].astype(str).str.contains('263000'))

        # Teks Status Decline
        if email_lang == "Bahasa Indonesia":
            if rc_61_count > 0:
                indikasi_decline = "Terdapat transaksi yang mendapatkan Response Code 61"
            elif rc_107_count > 0:
                indikasi_decline = "Terdapat transaksi yang mendapatkan Response Code 107"
            else:
                indikasi_decline = "Transaksi secara berulang dalam kurun waktu yang berdekatan"
        else:
            if rc_61_count > 0:
                indikasi_decline = "There are transactions that received Response Code 61"
            elif rc_107_count > 0:
                indikasi_decline = "There are transactions that received Response Code 107"
            else:
                indikasi_decline = "Repeated transactions occurred within a short time interval"

        # Teks Status Procode
        if email_lang == "Bahasa Indonesia":
            indikasi_procode = "Transaksi dilakukan dengan Processing Code 263000" if procode_263000_found else ""
        else:
            indikasi_procode = "Transactions were conducted using Processing Code 263000" if procode_263000_found else ""

        # =================================================================================

        # 3. MAPPING KUNCI KASUS BERDASARKAN PILIHAN USER
        if chosen_case.startswith("Case 1:"):
            case_key = "case1"
        elif chosen_case.startswith("Case 2:"):
            case_key = "case2"
        elif chosen_case.startswith("Case 3:"):
            case_key = "case3"
        elif chosen_case.startswith("Case 4:"):
            case_key = "case4"
        elif chosen_case.startswith("Case 5:"):
            case_key = "case5"
        elif chosen_case.startswith("Case 5-Issuer:"):
            case_key = "case5_issuer"
        elif chosen_case.startswith("Case 6:"):
            case_key = "case6"
        elif chosen_case.startswith("Case 7:"):
            case_key = "case7"
        elif chosen_case.startswith("Case 8:"):
            case_key = "case8"
        elif chosen_case.startswith("Case 9:"):
            case_key = "case9"
        else:
            case_key = "case10"

        # Gabungkan kode kasus dengan kode bahasa (_id atau _en)
        final_key = f"{case_key}_id" if email_lang == "Bahasa Indonesia" else f"{case_key}_en"

        # Memuat master draf teks dari templates.py
        template_raw = TEMPLATES[final_key]
        email_text = template_raw.format(
            target_name=target_name,
            formatted_amount=formatted_amount,
            formatted_top_nominal=formatted_top_nominal,
            total_trx=total_trx,
            min_date=min_date,
            max_date=max_date,
            m_name=m_name,
            cpan_display=cpan_display,
            mpan_display=mpan_display,
            cpan_list_string=cpan_list_string,
            merchant_list_string=merchant_list_string,
            indikasi_nominal=indikasi_nominal,
            indikasi_cpan_merchant=indikasi_cpan_merchant,
            indikasi_decline=indikasi_decline,
            indikasi_procode=indikasi_procode,
            indikasi_limit_cpan=indikasi_limit_cpan,
            cpan_count_string=cpan_count_string if 'cpan_count_string' in locals() else "",
            cpan_count_string_en=cpan_count_string_en if 'cpan_count_string_en' in locals() else ""
        )

        # --- TAMPILAN OUTPUT UTAMA ---
        st.subheader("📋 Hasil Ekstraksi Draf Teks Email")
        st.info(f"🌐 **Bahasa Aktif:** {email_lang} | **Target Router Aturan:** `{final_key}`")
        st.text_area("Salin teks hasil otomatisasi di bawah ini:", value=email_text, height=500)
        
        st.download_button(
            label="📥 Download Teks Email (.txt)",
            data=email_text,
            file_name=f"Draf_FDS_{target_name}_{email_lang[:2].lower()}.txt",
            mime="text/plain"
        )

        # Dashboard Summary Mini
        st.subheader("📊 Analitik Ringkasan Data Pendukung")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Frekuensi Transaksi", f"{total_trx} Trx")
        c2.metric("Total Nominal Terhitung", f"Rp {formatted_amount}")
        c3.metric("Jumlah Unik CPAN", f"{unique_cpans}")
        c4.metric("Status Procode 263000", "Terdeteksi (🚨)" if procode_263000_found else "Tidak Ada")

    except Exception as e:
        st.error(f"Terjadi kesalahan teknis pemrosesan: {e}")
