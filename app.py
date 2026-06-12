import streamlit as st
import pandas as pd
import io
import re
from templates import TEMPLATES

# 1. SETTING LAYOUT (Tampilan Penuh)
st.set_page_config(page_title="Email Template Generator - FDS", layout="wide")

st.title("✉️ Email Template Generator - FDS ALTO")
st.write("Unggah data transaksi FDS untuk mengekstrak indikasi fraud dan membuat email secara otomatis. (Dalam bentuk CSV atau Excel)")

# Fungsi pembantu format tanggal
def format_date(dt):
    if pd.isnull(dt):
        return ""
    return f"{dt.month}/{dt.day}/{dt.year} {dt.strftime('%H:%M:%S')}"

# --- DATABASE KATEGORI PRODUK & FORMAT CASE LENGKAP (KATA "EMAIL" DIHAPUS) ---
PRODUCT_CASES = {
    "QR Domestik": [
        "ACQUIRER/MERCHANT, Produk QR",
        "MERCHANT LEBIH DARI 1, Produk QR",
        "NAMA MERCHANT ANOMALI (Acquirer), Produk QR",
        "NAMA MERCHANT ANOMALI (Issuer), Produk QR",
        "ISSUER LEBIH DARI 1 CPAN, Produk QR",
        "ISSUER/CUSTOMER, Produk QR",
        "ISSUER PROCODE 263000, Produk QR",
        "ISSUER SUSPECT RC 59, Produk QR",
        "ISSUER KENAIKAN MERCHANT RC 107, Produk QR",
        "ACQUIRER QR DOM APPROVE > 50 KALI, Produk QR",
        "ISSUER QR DOM APPROVE > 50 KALI, Produk QR"
    ],
    "QR Cross Border (QRCB)": [
        "ACQUIRER QRCB INBOUND, Produk QR CB",
        "ACQUIRER QRCB OUTBOUND, Produk QR CB",
        "ISSUER/CUSTOMER QRCB, Produk QR CB",
        "ISSUER QRCB OUTBOUND, Produk QR CB"
    ],
    "Disbursement": [
        "DISBURSEMENT SENDER, Produk Disbursement",
        "DISBURSEMENT 1 SENDER 1 BENEFICIARY, Produk Beneficiary",
        "DISBURSEMENT SENDER CV/PT, Produk Disbursement",
        "BENEFICIARY TRANSFER DISBURSEMENT, Produk Disbursement"
    ],
    "QR Transfer": [
        "QR TRANSFER BENEFICIARY, Produk QR Transfer",
        "QR TRANSFER 1 SENDER 1 BENEFICIARY, Produk QR Transfer"
    ],
    "ATM": [
        "ATM BEDA KOTA, Produk ATM",
        "ATM TRANSFER SENDER, Produk ATM",
        "ATM WITHDRAWAL, Produk ATM withdrawal"
    ]
}

# --- MENU DROPDOWN DI SIDEBAR ---
st.sidebar.header("⚙️ Pengaturan Global")

# 1. Dropdown Tingkat Pertama (Produk)
selected_product = st.sidebar.selectbox(
    "Pilih Kategori Produk:",
    options=list(PRODUCT_CASES.keys())
)

# 2. Dropdown Tingkat Kedua (Case)
chosen_case = st.sidebar.selectbox(
    "Pilih Jenis Case Investigasi:",
    options=PRODUCT_CASES[selected_product]
)

# 3. Logika Smart UI Bahasa (Hanya muncul jika memilih produk QRCB)
if selected_product == "QR Cross Border (QRCB)":
    actual_lang = st.sidebar.selectbox(
        "Pilih Bahasa Email (Khusus Produk QRCB):",
        options=["Bahasa Indonesia", "English"],
        help="Gunakan English untuk partner internasional, dan Bahasa Indonesia untuk partner lokal."
    )
else:
    actual_lang = "Bahasa Indonesia"

target_name = st.sidebar.text_input("Nama Instansi Target (cth: DANA / BCA / ShopeePay / Seabank)", value="DANA")

# --- KOMPONEN UPLOAD FILE ---
uploaded_file = st.file_uploader("Pilih file data transaksi (CSV atau Excel Workbook)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        
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

        dini_hari_found = False
        if 'Date_Time' in df.columns:
            dini_hari_trx = df[(df['Date_Time'].dt.hour >= 0) & (df['Date_Time'].dt.hour <= 4)]
            if len(dini_hari_trx) > 0:
                dini_hari_found = True

        # A. Pengkondisian Deteksi Nominal
        is_keriting = False
        formatted_top_nominal = "0"
        if 'Amount_Trx' in df.columns and not df['Amount_Trx'].empty:
            nominal_counts = df['Amount_Trx'].value_counts()
            if not nominal_counts.empty:
                top_nominal = nominal_counts.index[0]
                formatted_top_nominal = f"{int(top_nominal):,}".replace(",", ".")
                top_nominal_freq = nominal_counts.iloc[0]
                is_keriting = bool(re.search(r'(\d)\1\1', str(int(top_nominal))))
                
                if actual_lang == "Bahasa Indonesia":
                    if is_keriting and (top_nominal_freq / total_trx) > 0.4:
                        indikasi_nominal = f"Transaksi didominasi dengan angka keriting, seperti Rp{formatted_top_nominal}, dst"
                    elif (top_nominal_freq / total_trx) > 0.6:
                        indikasi_nominal = f"Transaksi didominasi dengan nominal yang sama yaitu Rp {formatted_top_nominal}"
                    else:
                        sample_amount = str(int(top_nominal))
                        if len(sample_amount) >= 7:
                            indikasi_nominal = f"Transaksi didominasi dengan nominal yang mirip/unik yaitu Rp {sample_amount[0]},{sample_amount[1:3]}xx,xxx"
                        else:
                            indikasi_nominal = f"Transaksi didominasi dengan angka unik, seperti Rp{formatted_top_nominal}, dst"
                else:
                    if is_keriting and (top_nominal_freq / total_trx) > 0.4:
                        indikasi_nominal = "Transactions are dominated by repetitive/patterned numbers (angka keriting)"
                    else:
                        indikasi_nominal = f"Transactions are dominated by the same amount, which is IDR {formatted_top_nominal}"
        else:
            indikasi_nominal = ""

        # B. Deteksi Unik CPAN & Merchant
        unique_cpans = df['CPAN_Masking'].nunique() if 'CPAN_Masking' in df.columns else 0
        unique_merchants = df['Merchant_Name'].nunique() if 'Merchant_Name' in df.columns else 0
        cpan_display = df['CPAN_Masking'].iloc[0] if unique_cpans > 0 else "[CPAN]"
        mpan_display = df['MPAN_Masking'].iloc[0] if 'MPAN_Masking' in df.columns and len(df) > 0 else "[MPAN]"
        m_name = df['Merchant_Name'].iloc[0] if unique_merchants > 0 else "[MERCHANT]"

        sender_bank = df['Sender_Bank'].iloc[0] if 'Sender_Bank' in df.columns else target_name
        sender_account = df['Sender_Account'].iloc[0] if 'Sender_Account' in df.columns else "[SENDER_ACCOUNT]"
        sender_name = df['Sender_Name'].iloc[0] if 'Sender_Name' in df.columns else "[SENDER_NAME]"

        if 'CPAN_Masking' in df.columns:
            cpan_list_string = ", ".join(df['CPAN_Masking'].unique().tolist())
        else:
            cpan_list_string = cpan_display

        if actual_lang == "Bahasa Indonesia":
            cpan_count_string = f"1 CPAN" if unique_cpans == 1 else f"{unique_cpans} CPAN berbeda"
            if "QR TRANSFER 1 SENDER 1 BENEFICIARY" in chosen_case:
                indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN yang sama pada 1 Benef PAN"
            else:
                indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN pada 1 Merchant yang sama yaitu {m_name}" if unique_cpans == 1 else "Transaksi dilakukan oleh CPAN yang sama pada merchant yang berbeda"
        else:
            cpan_count_string_en = f"1 CPAN" if unique_cpans == 1 else f"{unique_cpans} different CPANs"
            indikasi_cpan_merchant = "Repeated transactions conducted by the same CPANs at the same merchant"

        if unique_merchants > 1:
            all_merchants = df['Merchant_Name'].unique().tolist()
            merchant_list_string = " dan ".join([", ".join(all_merchants[:-1]), all_merchants[-1]]) if len(all_merchants) > 1 else all_merchants[0]
        else:
            merchant_list_string = m_name

        # C. Limit Akumulasi Per-CPAN
        indikasi_limit_cpan = ""
        if 'CPAN_Masking' in df.columns and 'Amount_Trx' in df.columns:
            cpan_grp = df.groupby('CPAN_Masking')['Amount_Trx'].sum()
            if len(cpan_grp[cpan_grp > 4000000]) > 0:
                indikasi_limit_cpan = "1 CPAN melakukan transaksi dengan total nominal > Rp 4 Juta" if actual_lang == "Bahasa Indonesia" else "1 CPAN performed transactions with total > IDR 4 Million"

        # D. Deteksi Response Code & Procode
        rc_61_count = rc_107_count = rc_59_count = rc_57_count = rc_96_count = 0
        if 'Response_Code' in df.columns:
            rc_61_count = len(df[df['Response_Code'].isin(['61', 'RC 61'])])
            rc_107_count = len(df[df['Response_Code'].isin(['107', 'RC 107'])])
            rc_59_count = len(df[df['Response_Code'].isin(['59', 'RC 59'])])
            rc_57_count = len(df[df['Response_Code'].isin(['57', 'RC 57'])])
            rc_96_count = len(df[df['Response_Code'].isin(['96', 'RC 96'])])

        if actual_lang == "Bahasa Indonesia":
            if rc_57_count > 0 and rc_96_count > 0:
                indikasi_decline = "Terdapat banyak transaksi Payment mendapatkan Response Code 57 dan Response Code 96"
            elif rc_59_count > 0:
                indikasi_decline = "Terdapat banyak transaksi yang mendapatkan Response Code 59 ”Suspected Fraud”"
            elif rc_61_count > 0:
                indikasi_decline = "Terdapat transaksi yang mendapatkan Response Code 61"
            else:
                indikasi_decline = "Transaksi secara berulang dalam kurun waktu yang berdekatan"
        else:
            indikasi_decline = "Repeated transactions occurred within a short time interval"

        indikasi_procode = "Transaksi dilakukan dengan Processing Code 263000" if (any(df['Procode'].astype(str).str.contains('263000')) if 'Procode' in df.columns else False) else ""
        indikasi_dini_hari = "Transaksi dilakukan pada waktu dini hari" if dini_hari_found else ""

        # =================================================================================

        # 3. INTERPRETER KUNCI KASUS (Mapping Exact String ke Template Key)
        case_map = {
            "ACQUIRER/MERCHANT, Produk QR": "case1",
            "MERCHANT LEBIH DARI 1, Produk QR": "case3",
            "ACQUIRER QRCB INBOUND, Produk QR CB": "case4",
            "NAMA MERCHANT ANOMALI (Acquirer), Produk QR": "case5",
            "NAMA MERCHANT ANOMALI (Issuer), Produk QR": "case5_issuer",
            "ACQUIRER QRCB OUTBOUND, Produk QR CB": "case6",
            "ISSUER/CUSTOMER QRCB, Produk QR CB": "case7",
            "ISSUER LEBIH DARI 1 CPAN, Produk QR": "case8",
            "ISSUER/CUSTOMER, Produk QR": "case9",
            "ISSUER PROCODE 263000, Produk QR": "case10",
            "ISSUER SUSPECT RC 59, Produk QR": "case11",
            "ISSUER QRCB OUTBOUND, Produk QR CB": "case12",
            "ISSUER KENAIKAN MERCHANT RC 107, Produk QR": "case13",
            "ACQUIRER QR DOM APPROVE > 50 KALI, Produk QR": "case14",
            "ISSUER QR DOM APPROVE > 50 KALI, Produk QR": "case15",
            "DISBURSEMENT SENDER, Produk Disbursement": "case16",
            "DISBURSEMENT 1 SENDER 1 BENEFICIARY, Produk Beneficiary": "case17",
            "DISBURSEMENT SENDER CV/PT, Produk Disbursement": "case18",
            "BENEFICIARY TRANSFER DISBURSEMENT, Produk Disbursement": "case19",
            "QR TRANSFER BENEFICIARY, Produk QR Transfer": "case20",
            "QR TRANSFER 1 SENDER 1 BENEFICIARY, Produk QR Transfer": "case21",
            "ATM BEDA KOTA, Produk ATM": "case22",
            "ATM TRANSFER SENDER, Produk ATM": "case23",
            "ATM WITHDRAWAL, Produk ATM withdrawal": "case24"
        }
        
        # Ambil key dari dictionary mapping. Default ke case1 jika tidak ditemukan (fallback)
        case_key = case_map.get(chosen_case, "case1")

        final_key = f"{case_key}_id" if actual_lang == "Bahasa Indonesia" else f"{case_key}_en"

        template_raw = TEMPLATES[final_key]
        email_text = template_raw.format(
            target_name=target_name, formatted_amount=formatted_amount, formatted_top_nominal=formatted_top_nominal,
            total_trx=total_trx, min_date=min_date, max_date=max_date, m_name=m_name, cpan_display=cpan_display,
            mpan_display=mpan_display, cpan_list_string=cpan_list_string, merchant_list_string=merchant_list_string,
            indikasi_nominal=indikasi_nominal, indikasi_cpan_merchant=indikasi_cpan_merchant, indikasi_decline=indikasi_decline,
            indikasi_procode=indikasi_procode, indikasi_limit_cpan=indikasi_limit_cpan, indikasi_dini_hari=indikasi_dini_hari,
            sender_bank=sender_bank, sender_account=sender_account, sender_name=sender_name, unique_merchants=unique_merchants,
            cpan_count_string=cpan_count_string if 'cpan_count_string' in locals() else "",
            cpan_count_string_en=cpan_count_string_en if 'cpan_count_string_en' in locals() else ""
        )

        email_text = "\n".join([line for line in email_text.split('\n') if line.strip() != ""])

        # --- TAMPILAN OUTPUT UTAMA ---
        st.subheader("📋 Hasil Ekstraksi Draf Teks Email")
        st.info(f"📁 **Produk:** {selected_product} | 🌐 **Bahasa:** {actual_lang} | 🎯 **Target Router:** `{final_key}`")
        st.text_area("Salin teks hasil otomatisasi di bawah ini:", value=email_text, height=500)
        
        st.download_button(
            label="📥 Download Teks Email (.txt)", data=email_text,
            file_name=f"Draf_FDS_{target_name}_{actual_lang[:2].lower()}.txt", mime="text/plain"
        )

        st.subheader("📊 Analitik Ringkasan Data Pendukung")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Frekuensi Transaksi", f"{total_trx} Trx")
        c2.metric("Total Nominal Terhitung", f"Rp {formatted_amount}")
        c3.metric("Jumlah Unik CPAN/Sender", f"{unique_cpans if unique_cpans > 0 else 1}")
        c4.metric("Deteksi RC Bermasalah", f"RC59: {rc_59_count} | RC57: {rc_57_count} | RC96: {rc_96_count}")

    except Exception as e:
        st.error(f"Terjadi kesalahan teknis pemrosesan: {e}")
