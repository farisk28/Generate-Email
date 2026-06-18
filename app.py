import streamlit as st
import pandas as pd
import io
import re
from templates import TEMPLATES

# 1. SETTING LAYOUT (Tampilan Penuh)
st.set_page_config(page_title="Email Template Generator - FDS", layout="wide")

st.title("✉️ Email Template Generator - FDS ALTO")
st.write("Unggah data transaksi FDS untuk mengekstrak indikasi fraud dan membuat email secara otomatis. (Bisa menggunakan file CSV atau Excel)")

# Fungsi pembantu format tanggal
def format_date(dt):
    if pd.isnull(dt):
        return ""
    return f"{dt.month}/{dt.day}/{dt.year} {dt.strftime('%H:%M:%S')}"

# --- DATABASE KATEGORI PRODUK & FORMAT CASE LENGKAP ---
PRODUCT_CASES = {
    "QR Domestik": [
        "MERCHANT",
        "ISSUER",
        "MERCHANT LEBIH DARI 1",
        "ISSUER LEBIH DARI 1",
        "NAMA MERCHANT ANOMALI (Acquirer)",
        "NAMA MERCHANT ANOMALI (Issuer)",
        "ACQUIRER QR APPROVE > 50 KALI",
        "ISSUER QR APPROVE > 50 KALI",
        "MERCHANT KENAIKAN TPV RC 107 / RC 59",
        "ISSUER KENAIKAN MERCHANT RC 107",
        "ISSUER SUSPECT RC 59",
        "ISSUER PROCODE 263000"
    ],
    "QR Cross Border (QRCB)": [
        "ACQUIRER QRCB INBOUND",
        "ACQUIRER QRCB OUTBOUND",
        "ISSUER/CUSTOMER QRCB",
        "ISSUER QRCB OUTBOUND"
    ],
    "Disbursement": [
        "DISBURSEMENT SENDER",
        "DISBURSEMENT 1 SENDER 1 BENEFICIARY",
        "DISBURSEMENT SENDER CV/PT",
        "BENEFICIARY TRANSFER DISBURSEMENT"
    ],
    "QR Transfer": [
        "QR TRANSFER BENEFICIARY",
        "QR TRANSFER 1 SENDER 1 BENEFICIARY"
    ],
    "ATM": [
        "ATM BEDA KOTA",
        "ATM TRANSFER SENDER",
        "ATM WITHDRAWAL"
    ],
    "Cardless": [
        "CARDLESS DECLINE"
    ],
    "Debit": [
        "PAN DEBIT"
    ]
}

# --- MENU DROPDOWN DI SIDEBAR ---
st.sidebar.header("⚙️ Pengaturan Investigasi")

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

# 3. Logika Smart UI Bahasa (Muncul khusus QRCB)
if selected_product == "QR Cross Border (QRCB)":
    actual_lang = st.sidebar.selectbox(
        "Pilih Bahasa Email (Khusus Produk QRCB):",
        options=["Bahasa Indonesia", "English"],
        help="Gunakan English untuk partner internasional, dan Bahasa Indonesia untuk partner lokal."
    )
else:
    actual_lang = "Bahasa Indonesia"

target_name = st.sidebar.text_input("Nama Instansi Target (cth: DANA / BCA / ShopeePay / Astrapay)", value="DANA")

# --- KOMPONEN UPLOAD FILE ---
uploaded_file = st.file_uploader("Pilih file data transaksi (CSV atau Excel Workbook)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        
        # Penanganan Pembacaan File
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

        # 2. Pembersihan Data Masukan & Pencegahan Error
        df.dropna(how='all', inplace=True)
        
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip("'").str.strip()
                
        if 'Merchant_Name' in df.columns:
            df['Merchant_Name'] = df['Merchant_Name'].apply(lambda x: " ".join(str(x).split()) if pd.notnull(x) and str(x).lower() != 'nan' else "")
            
        if 'Amount_Trx' in df.columns:
            df['Amount_Trx'] = pd.to_numeric(df['Amount_Trx'], errors='coerce')
            
        df.dropna(subset=['Amount_Trx'], inplace=True)
            
        if 'Date_Time' in df.columns:
            df['Date_Time'] = pd.to_datetime(df['Date_Time'], errors='coerce')

        # ================= LOGIKA MATRIKS ATURAN (RULE-BASED REASONING) =================
        
        total_trx = len(df)
        total_amount = int(df['Amount_Trx'].sum()) if 'Amount_Trx' in df.columns else 0
        formatted_amount = f"{total_amount:,}".replace(",", ".")

        min_date = format_date(df['Date_Time'].min()) if 'Date_Time' in df.columns else ""
        max_date = format_date(df['Date_Time'].max()) if 'Date_Time' in df.columns else ""

        # Deteksi Waktu Dini Hari (00:00 - 04:00)
        dini_hari_found = False
        if 'Date_Time' in df.columns:
            dini_hari_trx = df[(df['Date_Time'].dt.hour >= 0) & (df['Date_Time'].dt.hour <= 4)]
            if len(dini_hari_trx) > 0:
                dini_hari_found = True

        # =================================================================================
        # A. SMART ANALYTICS: ANGKA UNIK vs ANGKA KERITING
        # =================================================================================
        formatted_top_nominal = "0"
        indikasi_nominal = ""
        
        if 'Amount_Trx' in df.columns and not df['Amount_Trx'].empty:
            top_nominal = df['Amount_Trx'].mode()[0]
            top_nominal_freq = (df['Amount_Trx'] == top_nominal).sum()
            rasio_sama = top_nominal_freq / total_trx
            formatted_top_nominal = f"{int(top_nominal):,}".replace(",", ".")
            
            # Filter angka tidak bulat (sisa bagi 1000 tidak nol)
            df_non_round = df[df['Amount_Trx'] % 1000 != 0]
            rasio_non_round = len(df_non_round) / total_trx
            
            if rasio_sama > 0.6:
                if actual_lang == "Bahasa Indonesia":
                    indikasi_nominal = f"Transaksi didominasi dengan nominal yang sama yaitu Rp {formatted_top_nominal}"
                else:
                    indikasi_nominal = f"Transactions are dominated by the same amount, which is IDR {formatted_top_nominal}"
                    
            elif rasio_non_round > 0.3:
                # Ambil nilai-nilai yang tidak bulat
                unique_vals = df_non_round['Amount_Trx'].drop_duplicates()
                
                # Cek jumlah variasi "Base Ribuan"
                bases = (unique_vals // 1000).nunique()
                selisih_max_min = unique_vals.max() - unique_vals.min()
                
                sampel_unik = unique_vals.head(3).astype(int)
                sampel_str = ", ".join([f"Rp{x:,}".replace(",", ".") for x in sampel_unik])
                
                # LOGIKA RBR: Jika base ribuannya sama, atau rentang nilai sangat sempit = ANGKA UNIK
                if bases == 1 or selisih_max_min < 5000:
                    if actual_lang == "Bahasa Indonesia":
                        indikasi_nominal = f"Transaksi didominasi dengan angka unik, seperti {sampel_str}, dst"
                    else:
                        sampel_str_en = sampel_str.replace("Rp", "IDR ")
                        indikasi_nominal = f"Transactions are dominated by unique identifiers, such as {sampel_str_en}, etc."
                # LOGIKA RBR: Jika base ribuannya beda-beda dan rentangnya jauh = ANGKA KERITING
                else:
                    if actual_lang == "Bahasa Indonesia":
                        indikasi_nominal = f"Transaksi didominasi dengan angka keriting, seperti {sampel_str}, dst"
                    else:
                        sampel_str_en = sampel_str.replace("Rp", "IDR ")
                        indikasi_nominal = f"Transactions are dominated by non-round/patterned amounts (angka keriting), such as {sampel_str_en}, etc."
            else:
                if actual_lang == "Bahasa Indonesia":
                    indikasi_nominal = "Transaksi dilakukan dengan pola nominal yang bervariasi"
                else:
                    indikasi_nominal = "Transactions were conducted with varied amounts"

        # B. Deteksi Unik CPAN, MPAN & Nama Merchant/Sender
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

        # Kondisi CPAN & Merchant (Indonesia / English)
        if actual_lang == "Bahasa Indonesia":
            cpan_count_string = f"1 CPAN" if unique_cpans == 1 else f"{unique_cpans} CPAN berbeda"
            
            if "QR TRANSFER 1 SENDER 1 BENEFICIARY" in chosen_case:
                indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 CPAN yang sama pada 1 Benef PAN"
            elif "CARDLESS" in chosen_case:
                indikasi_cpan_merchant = f"Transaksi dilakukan oleh {unique_cpans} customer berbeda pada masing-masing merchant yang berbeda" if unique_cpans > 1 else "Transaksi dilakukan pada masing-masing merchant yang berbeda"
            else:
                indikasi_cpan_merchant = f"Transaksi dilakukan oleh 1 PAN pada 1 Merchant yang sama yaitu {m_name}" if unique_cpans == 1 else "Transaksi dilakukan oleh PAN yang sama pada merchant yang berbeda"
        else:
            cpan_count_string_en = f"1 CPAN" if unique_cpans == 1 else f"{unique_cpans} different CPANs"
            indikasi_cpan_merchant = "Repeated transactions conducted by the same CPANs at the same merchant"

        # Gabungan Multi Merchant
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
            else:
                indikasi_limit_cpan = f"1 CPAN melakukan transaksi dengan total nilai Rp {formatted_amount}" if actual_lang == "Bahasa Indonesia" else f"1 CPAN conducted transactions with total value IDR {formatted_amount}"

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

        # 3. INTERPRETER KUNCI KASUS (Mapping Exact String)
        case_map = {
            "MERCHANT": "case1",
            "MERCHANT KENAIKAN TPV RC 107 / RC 59": "case2",
            "MERCHANT LEBIH DARI 1": "case3",
            "ACQUIRER QRCB INBOUND": "case4",
            "NAMA MERCHANT ANOMALI (Acquirer)": "case5",
            "NAMA MERCHANT ANOMALI (Issuer)": "case5_issuer",
            "ACQUIRER QRCB OUTBOUND": "case6",
            "ISSUER/CUSTOMER QRCB": "case7",
            "ISSUER LEBIH DARI 1 CPAN": "case8",
            "ISSUER": "case9",
            "ISSUER PROCODE 263000": "case10",
            "ISSUER SUSPECT RC 59": "case11",
            "ISSUER QRCB OUTBOUND": "case12",
            "ISSUER KENAIKAN MERCHANT RC 107": "case13",
            "ACQUIRER QR DOM APPROVE > 50 KALI": "case14",
            "ISSUER QR DOM APPROVE > 50 KALI": "case15",
            "DISBURSEMENT SENDER": "case16",
            "DISBURSEMENT 1 SENDER 1 BENEFICIARY": "case17",
            "DISBURSEMENT SENDER CV/PT": "case18",
            "BENEFICIARY TRANSFER DISBURSEMENT": "case19",
            "QR TRANSFER BENEFICIARY": "case20",
            "QR TRANSFER 1 SENDER 1 BENEFICIARY": "case21",
            "ATM BEDA KOTA": "case22",
            "ATM TRANSFER SENDER": "case23",
            "ATM WITHDRAWAL": "case24",
            "CARDLESS DECLINE": "case25",
            "PAN DEBIT": "case26"
        }
        
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

        # === PEMBERSIH PINTAR (SMART CLEANER) ===
        cleaned_lines = []
        for line in email_text.split('\n'):
            if re.match(r'^\d+\.\s*$', line.strip()):
                continue 
            cleaned_lines.append(line)
            
        email_text = "\n".join(cleaned_lines)

        # --- TAMPILAN OUTPUT UTAMA ---
        st.subheader("📋 Hasil Ekstraksi Draf Teks Email")
        st.info(f"📁 **Produk:** {selected_product} | 🌐 **Bahasa:** {actual_lang} | 🎯 **Target Router:** `{final_key}`")
        st.text_area("Salin teks hasil otomatisasi di bawah ini:", value=email_text, height=500)
        
        st.download_button(
            label="📥 Download Teks Email (.txt)", data=email_text,
            file_name=f"Draf_FDS_{target_name}_{actual_lang[:2].lower()}.txt", mime="text/plain"
        )

        # --- SUMMARY ANALYTICS ---
        st.subheader("📊 Analitik Ringkasan Data Pendukung")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Frekuensi Transaksi", f"{total_trx} Trx")
        c2.metric("Total Nominal Terhitung", f"Rp {formatted_amount}")
        c3.metric("Jumlah Unik CPAN/Sender", f"{unique_cpans if unique_cpans > 0 else 1}")
        c4.metric("Deteksi RC Bermasalah", f"RC59: {rc_59_count} | RC57: {rc_57_count} | RC96: {rc_96_count}")

    except Exception as e:
        st.error(f"Terjadi kesalahan teknis pemrosesan: {e}")
