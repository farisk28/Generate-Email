# templates.py

# ================= BAGIAN PENUTUP STANDAR (FOOTER) =================
FOOTER_ID = """

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

FOOTER_EN = """

Please inform us of the results of your review so that we may enhance the accuracy of our Fraud Detection System (FDS). If required, we are also able to provide support for confirmed fraud cases in accordance with the authority granted to PT. ALTO Network.

Note: The password will be sent in a separate email.

This concludes the information we would like to convey.
Thank you for your kind attention.

Simple Payment, Redefined.
Best Regards,
Fraud Analyst
Enterprise, Architecture & Cybersecurity
Hotline Whatsapp : 0851 7968 1636
PT. ALTO Network"""


# ================= KAMUS TEMPLATE LENGKAP (24 CASE FDS) =================
TEMPLATES = {
    # -----------------------------------------------------------------
    # KELOMPOK DOMESTIK (HANYA BAHASA INDONESIA)
    # -----------------------------------------------------------------
    
    "case1_id": """Dear Rekan {target_name}, 

Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada MPAN ({mpan_display}) Acquirer {target_name} Merchant {m_name} 

Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Total nilai transaksi Rp {formatted_amount} 
2. {indikasi_nominal} 
3. {indikasi_decline} 
4. Transaksi dilakukan pada merchant {m_name} 
5. Transaksi terjadi pada periode {min_date} - {max_date}
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah dari sisi merchant terdapat indikasi abuse? 
2. Barang / jasa apa yang ditawarkan merchant pada transaksi terlampir? 
3. Apakah profil merchant sesuai dengan pola transaksinya? 
4. Apakah merchant merupakan merchant online, jika iya apakah ada link web merchant/transaksi-nya ? 
5. Jika transaksi di merchant tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.""" + FOOTER_ID,

    "case2_id": """Dear Rekan {target_name}, 

Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada MPAN ({mpan_display}) Acquirer {target_name} Merchant {m_name} 

Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Terdapat kenaikan transaksi yang mendapat Response Code 107 (Suspected Fraud) pada 1 Merchant yaitu {m_name} 
2. Transaksi terjadi pada periode waktu {min_date} - {max_date} 
3. Transaksi dilakukan oleh {cpan_count_string} dengan beberapa transaksi pertama mendapatkan Response Code 001 (Approved) kemudian transaksi selanjutnya mendapatkan Response Code 107 (Suspected Fraud) 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah dari sisi merchant terdapat indikasi abuse? Jika iya, mohon memberikan penjelasannya. 
2. Mengapa transaksi-transaksi tersebut mendapatkan Response Code 107 ”Suspected Fraud” ? 
3. Barang / jasa apa yang ditawarkan merchant pada transaksi terlampir? 
4. Apakah profil merchant sesuai dengan pola transaksinya? 
5. Jika transaksi di merchant tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.""" + FOOTER_ID,

    "case3_id": """Dear Rekan {target_name}, 

Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada Acquirer {target_name} dengan merchant sebagai berikut : {merchant_list_string}.

Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Total nilai transaksi Rp {formatted_amount} 
2. Terjadi transaksi berulang dalam interval waktu yang singkat 
3. {indikasi_nominal} 
4. {indikasi_cpan_merchant} 
5. Transaksi terjadi pada periode {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah dari sisi merchant terdapat indikasi abuse? 
2. Barang / jasa apa yang ditawarkan merchant pada transaksi terlampir? 
3. Apakah profil merchant sesuai dengan pola transaksinya? 
4. Apakah merchant merupakan merchant online, jika iya apakah ada link web merchant/transaksi-nya ? 
5. Jika transaksi di merchant tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.""" + FOOTER_ID,

    "case5_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada MPAN ({mpan_display}) Acquirer {target_name} Merchant {m_name}. 
 
Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Transaksi dilakukan kepada merchant dengan nama yang terdeteksi tidak wajar, yaitu {m_name} 
2. Nama tersebut tidak menyerupai merchant resmi pada umumnya. 
3. Transaksi dilakukan dalam periode waktu {min_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Barang atau jasa apa yang ditawarkan oleh merchant pada transaksi terlampir? 
2. Apakah profil merchant sesuai dengan pola transaksinya? 
3. Apakah nama merchant sesuai dengan bidang usahanya? 
4. Jika transaksi pada merchant tersebut merupakan transaksi genuine, mohon berikan penjelasannya.""" + FOOTER_ID,

    "case5_issuer_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN ({cpan_list_string}). 
 
Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Transaksi dilakukan kepada merchant dengan nama yang terdeteksi tidak wajar, yaitu {m_name} 
2. Nama tersebut tidak menyerupai merchant resmi pada umumnya. 
3. Transaksi dilakukan dalam periode waktu {min_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Apakah nasabah menerima tautan atau pesan mencurigakan sebelum transaksi terjadi? 
3. Apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
4. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case8_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN {cpan_list_string}

Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. Total keseluruhan transaksi adalah Rp {formatted_amount} 
2. {indikasi_limit_cpan} 
3. {indikasi_nominal} 
4. {indikasi_procode} 
5. {indikasi_cpan_merchant} 
6. Transaksi terjadi pada periode {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:   
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case9_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN {cpan_list_string}. 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. {indikasi_limit_cpan} 
2. Transaksi secara berulang dalam kurun waktu yang berdekatan dan singkat 
3. {indikasi_nominal} 
4. Transaksi dilakukan pada berbagai merchant berbeda-beda 
5. Transaksi terjadi pada periode {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:   
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case10_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN {cpan_list_string}. 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. {indikasi_limit_cpan} 
2. Transaksi secara berulang dalam kurun waktu yang berdekatan dan singkat 
3. {indikasi_nominal} 
4. {indikasi_procode} 
5. Transaksi dilakukan pada 1 Merchant yaitu {m_name} 
6. Transaksi dilakukan pada waktu {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:   
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case11_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN {cpan_list_string}. 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. Total nilai transaksi keseluruhan Rp {formatted_amount} 
2. {indikasi_limit_cpan} 
3. Transaksi secara berulang dalam kurun waktu yang berdekatan 
4. {indikasi_nominal} 
5. {indikasi_cpan_merchant} 
6. {indikasi_decline} 
7. Transaksi dilakukan dalam periode waktu {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:   
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case13_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN {cpan_list_string}. 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. {indikasi_limit_cpan} 
2. Transaksi secara berulang dalam kurun waktu yang berdekatan dan singkat 
3. {indikasi_nominal} 
4. Transaksi dilakukan pada 1 Merchant yaitu {m_name} 
5. Transaksi pertama mendapatkan Response Code 001 (Approved) kemudian transaksi selanjutnya mendapatkan Response Code 107 (Suspected Fraud) 
6. Transaksi terjadi pada periode {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:   
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case14_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada MPAN ({mpan_display}) Acquirer {target_name} Merchant {m_name}. 
 
Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Transaksi dilakukan secara berulang pada kurun waktu berdekatan 
2. {indikasi_nominal} 
3. {indikasi_cpan_merchant} 
4. {indikasi_dini_hari} 
5. Transaksi dilakukan dalam periode waktu {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah dari sisi merchant terdapat indikasi abuse? 
2. Apakah sedang dilakukan pameran? 
3. Barang / jasa apa yang ditawarkan merchant pada transaksi terlampir? 
4. Apakah profil merchant sesuai dengan pola transaksinya? 
5. Apakah merchant tersebut beroperasi selama 24 jam? 
6. Apakah merchant merupakan merchant online, jika iya apakah ada link web merchant/transaksi-nya ? 
7. Jika transaksi di merchant tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.""" + FOOTER_ID,

    "case15_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN ({cpan_list_string}). 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. Transaksi dilakukan secara berulang pada kurun waktu berdekatan 
2. {indikasi_dini_hari} 
3. {indikasi_nominal} 
4. {indikasi_cpan_merchant} 
5. Transaksi dilakukan dalam periode waktu {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:   
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case16_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi anomali berpotensi fraud yang terjadi pada Sender {sender_bank} dengan Sender Account {sender_account} ({sender_name}) 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. Total nilai transaksi yang dilakukan adalah Rp {formatted_amount} 
2. Terdapat 1 Sender Account yang melakukan transaksi ke banyak Beneficiary Account yang berbeda 
3. Transaksi dilakukan secara berulang 
4. Terdapat transaksi yang dilakukan dengan nominal yang besar. 
5. Transaksi dilakukan melebihi Rp 10,000,000/transaksi 
6. Transaksi dilakukan antara waktu {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Apakah dari sisi sender terdapat indikasi fraud? 
3. Berapa limit harian/bulanan untuk melakukan transfer Disbursement 
4. Apakah profil sender sesuai dengan pola transaksinya? 
5. Apakah transaksi tersebut sudah sesuai dengan syarat dan ketentuan yang berlaku ? 
6. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case17_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini, kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada Sender {sender_name} ({sender_account}) pada Beneficiary {merchant_list_string}. 
 
Adapun Anomali transaksi yang kami temukan terkait transaksi tersebut : 
1. Total nilai transaksi Rp {formatted_amount} 
2. Transaksi didominasi dengan nominal yang besar 
3. Transaksi dilakukan secara berulang dalam waktu berdekatan 
4. Transaksi dilakukan oleh 1 Sender Account pada 1 Beneficiary dengan {unique_merchants} Account 
5. Transaksi dilakukan dalam periode waktu {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri? 
2. Apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Apabila transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya. 
4. Mohon diinformasikan ketentuan mengenai batas limit transaksi harian serta batas limit per transaksi yang berlaku untuk masing-masing account.""" + FOOTER_ID,

    "case18_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi anomali berpotensi fraud yang terjadi pada Sender {target_name} dengan Sender Account {sender_account} ({sender_name}). 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. Total nilai transaksi yang dilakukan adalah Rp {formatted_amount} 
2. Terdapat 1 Sender Account yang melakukan transaksi ke {unique_merchants} Beneficiary Account yang berbeda 
3. Transaksi dilakukan secara berulang dalam waktu berdekatan 
4. Terdapat transaksi yang dilakukan dengan nominal besar 
5. Transaksi dilakukan pada periode waktu antara {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Apakah dari sisi sender terdapat indikasi fraud? 
3. Barang / jasa apa yang ditawarkan sender pada transaksi terlampir? 
4. Berapa limit harian/bulanan untuk melakukan transfer Disbursement? 
5. Apakah profil sender sesuai dengan pola transaksinya? 
6. Apakah transaksi tersebut sudah sesuai dengan syarat dan ketentuan yang berlaku ? 
7. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case19_id": """Dear Tim {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada Benef di file terlampir. 
 
Indikasi Transaksi: 
1. Transaksi dilakukan dalam waktu yang berdekatan 
2. Periode waktu transaksi {min_date} - {max_date} dalam {total_trx} transaksi dengan total nilai Rp {formatted_amount} 
3. Sender/Pengirim dilakukan secara berulang kepada Beneficiary/Penerima yang sama 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut : 
1. Apakah dari sisi Benef terdapat indikasi fraud? 
2. Barang / jasa apa yang ditawarkan Benef pada transaksi terlampir? 
3. Apakah profil Benef sesuai dengan pola transaksinya? 
4. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.""" + FOOTER_ID,

    "case20_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada Beneficiary PAN ({mpan_display}). 
 
Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Terjadi transaksi berulang dalam interval waktu yang singkat 
2. Transaksi inquiry dengan Procode 266000 dilakukan sebanyak {total_trx} transaksi 
3. Transaksi terjadi pada periode {min_date} – {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah dari sisi beneficiary terdapat indikasi abuse? 
2. Apakah secara behaviour untuk transaksi transfer yang dilakukan dengan transaksi inquiry dengan jumlah yang cukup banyak sudah sesuai? 
3. Apakah transaksi tersebut sesuai dengan syarat dan ketentuan? 
4. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.""" + FOOTER_ID,

    "case21_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini, kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN ({cpan_list_string}) pada Beneficiary PAN ({mpan_display}). 
 
Adapun Anomali transaksi yang kami temukan terkait transaksi tersebut : 
1. Total nilai transaksi Rp {formatted_amount} 
2. Transaksi dilakukan dengan nominal besar kemudian semakin kecil 
3. Transaksi dilakukan secara berulang dalam waktu berdekatan 
4. Transaksi dilakukan oleh 1 CPAN yang sama pada 1 Benef PAN 
5. {indikasi_decline} 
6. Transaksi dilakukan dalam periode waktu {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri? 
2. Apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Apabila transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.""" + FOOTER_ID,

    "case22_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi anomali berpotensi fraud yang terjadi pada Transaksi Withdrawal PAN ({cpan_list_string}). 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. Transaksi dilakukan di 2 kota yang berbeda berdasarkan nama lokasi ATM 
2. Transaksi dilakukan dalam waktu dekat dan singkat 
3. Transaksi dilakukan antara waktu {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Apakah terdapat indikasi ATO pada kartu tersebut ? 
3. Apakah transaksi tersebut sudah sesuai dengan syarat dan ketentuan yang berlaku ? 
4. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case23_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi anomali berpotensi fraud yang terjadi pada Transaksi Transfer dengan Sender {target_name} ke Beneficiary {merchant_list_string}. 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. Total nilai transaksi yang dilakukan adalah Rp {formatted_amount} 
2. Terdapat Banyak Sender yang melakukan transaksi ke 1 Beneficiary Account yang sama. 
3. Terdapat sebanyak {unique_merchants} Beneficiary Account yang menerima banyak transaksi dari beberapa Sender. 
4. Transaksi dilakukan secara berulang dalam waktu berdekatan dan singkat. 
5. Transaksi dilakukan antara waktu {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Berapa limit harian/bulanan untuk melakukan transfer? 
3. Apakah transaksi tersebut sudah sesuai dengan syarat dan ketentuan yang berlaku ? 
4. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case24_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada Issuer {target_name}. 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. Total nilai transaksi keseluruhan Rp {formatted_amount} 
2. Transaksi yang dilakukan oleh 1 PAN dengan Response Code 55, kemudian transaksi selanjutnya mendapatkan Response Code 59 
3. Terdapat PAN yang transaksi setelah Response Code 59 mendapatkan Response Code 00 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Apakah ada abuse pada sisi Issuer? 
3. Bagaimana kebijakan transaksi dari sisi Issuer jika transaksi tersebut mendapatkan Response Code 55 atau Response Code 59? 
4. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,


    # -----------------------------------------------------------------
    # KELOMPOK CROSS BORDER (QRCB) - BILINGUAL (ID & EN)
    # -----------------------------------------------------------------
    
    "case4_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada MPAN ({mpan_display}) Acquirer {target_name} Merchant {m_name}. 
 
Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Transaksi merupakan QR cross-border 
2. Total nilai transaksi mencapai Rp {formatted_amount} 
3. Transaksi dilakukan dengan nominal besar 
4. {indikasi_decline} 
5. Transaksi berulang dilakukan dalam kurun waktu yang berdekatan dan singkat 
6. Transaksi dilakukan pada waktu yaitu {min_date} - {max_date} 
7. {indikasi_cpan_merchant} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah dari sisi merchant terdapat indikasi abuse? 
2. Barang / jasa apa yang ditawarkan merchant pada transaksi terlampir? 
3. Apakah profil merchant sesuai dengan pola transaksinya? 
4. Apakah sedang berlangsung event pada merchant tersebut? 
5. Jika transaksi di merchant tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.""" + FOOTER_ID,

    "case4_en": """Dear {target_name} Team, 
 
With reference to this email, we, as the switching provider, have an obligation as a Payment Infrastructure Provider to ensure consumer safety and protection. We kindly request your assistance in conducting due diligence on the potentially fraudulent transactions associated with MPAN ({mpan_display}) Acquirer {target_name} Merchant {m_name}. 
 
The indications we have identified in relation to these transactions are as follows: 
1. The transaction is a QR cross-border 
2. The total transaction amount reached IDR {formatted_amount} 
3. Transactions were conducted with large amounts 
4. {indikasi_decline} 
5. Repeated transactions were performed within a close and short period of time 
6. Transactions were conducted within the time of {min_date} - {max_date} 
7. {indikasi_cpan_merchant} 
 
Additionally, we kindly request your assistance in confirming the following points: 
1. Is there any indication of abuse from the merchant's side? 
2. What goods or services are offered by the merchant in the attached transactions? 
3. Does the merchant's profile match their transaction pattern? 
4. Is there an ongoing event at the merchant? 
5. If the transactions at the merchant are deemed genuine, kindly provide further explanation.""" + FOOTER_EN,

    "case6_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada Acquirer {target_name} Merchant {m_name}. 
 
Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Transaksi merupakan QR cross-border. 
2. Total nilai transaksi mencapai Rp {formatted_amount}. 
3. Volume transaksi tidak wajar, mencapai puluhan juta rupiah. 
4. Transaksi terjadi secara berurutan dalam interval waktu yang singkat, yaitu pada {min_date} – {max_date} (waktu lokal Indonesia). 
5. {indikasi_cpan_merchant} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah dari sisi merchant terdapat indikasi abuse? 
2. Barang / jasa apa yang ditawarkan merchant pada transaksi terlampir? 
3. Apakah profil merchant sesuai dengan pola transaksinya? 
4. Apakah merchant merupakan merchant online, jika iya apakah ada link web merchant/transaksi-nya? 
5. Jika transaksi di merchant tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya.""" + FOOTER_ID,

    "case6_en": """Dear Team {target_name}, 
 
With reference to this email, we, as the switching operator, have an obligation as a Payment Infrastructure Provider to ensure consumer protection and security. We kindly request your assistance in conducting due diligence on transactions with potential fraud indications involving the Acquirer {target_name} Merchant {m_name}. 
 
The indications we have identified regarding these transactions are as follows: 
1. The transactions were QR cross-border. 
2. A total transaction value of IDR {formatted_amount}. 
3. Unusually high transaction volume, reaching tens of millions of rupiah. 
4. Transactions occurred in rapid succession within a short time interval, specifically between {min_date} – {max_date} (local time indonesia) 
5. {indikasi_cpan_merchant} 
 
In addition, we kindly request your confirmation regarding the following points: 
1. Are there any indications of abuse from the merchant’s side? 
2. What goods/services were offered by the merchant in the attached transactions? 
3. Does the merchant’s profile align with the observed transaction patterns? 
4. Is the merchant an online merchant? If so, could you provide the merchant/transaction website link? 
5. If the transactions at this merchant are genuine, please provide your explanation.""" + FOOTER_EN,

    "case7_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN ({cpan_list_string}). 
 
Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Transaksi merupakan transaksi QR cross-border. 
2. Total nilai transaksi mencapai Rp {formatted_amount}. 
3. Terjadi transaksi berulang dalam interval waktu yang singkat. 
4. {indikasi_nominal} 
5. Transaksi terjadi pada periode waktu {min_date} - {max_date}. 
6. {indikasi_cpan_merchant} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut: 
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case7_en": """Dear {target_name} Team, 
 
With reference to this email, we, as the switching provider, have an obligation as a Payment Infrastructure Provider to ensure consumer safety and protection. We kindly request your assistance in conducting due diligence on the potentially fraudulent transactions associated with CPAN ({cpan_list_string}). 
 
The indications we have identified in relation to these transactions are as follows: 
1. The transactions are cross-border QR transactions 
2. Total transaction value is IDR {formatted_amount} 
3. Repeated transactions occurred within a short time interval 
4. {indikasi_nominal} 
5. The transactions were carried out during time periods {min_date} - {max_date} 
6. {indikasi_cpan_merchant} 
 
Additionally, we kindly request your assistance in confirming the following points: 
1. Were all the transactions listed in the attached file genuinely performed by the customer? 
2. If there is an ongoing promotion from the Issuer, were these transactions in compliance with the applicable terms and conditions? 
3. If the transactions are deemed genuine, kindly provide further explanation.""" + FOOTER_EN,

    "case12_id": """Dear Rekan {target_name}, 
 
Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada CPAN {cpan_list_string}. 
 
Adapun indikasi yang kami temukan terkait transaksi tersebut : 
1. Transaksi merupakan QR cross-border  
2. {indikasi_limit_cpan} 
3. Transaksi secara berulang dalam kurun waktu yang berdekatan dan singkat 
4. {indikasi_nominal} 
5. Transaksi dilakukan pada 1 Merchant yaitu {m_name} 
6. Transaksi terjadi pada periode {min_date} - {max_date} 
 
Serta, mohon bantuannya untuk melakukan konfirmasi terkait dengan indikasi pertanyaan berikut:   
1. Apakah semua transaksi pada file terlampir benar dilakukan oleh nasabah sendiri ? 
2. Jika saat ini sedang berlangsung kegiatan Promo dari sisi Issuer, apakah transaksi tersebut sudah sesuai dengan syarat & ketentuan yang berlaku? 
3. Jika transaksi tersebut merupakan transaksi genuine, mohon untuk memberikan penjelasannya?""" + FOOTER_ID,

    "case12_en": """Dear {target_name} Team, 
 
With reference to this email, we, as the switching provider, have an obligation as a Payment Infrastructure Provider to ensure consumer safety and protection. We kindly request your assistance in conducting due diligence on the potentially fraudulent transactions associated with CPAN {cpan_list_string}. 
 
The indications we have identified in relation to these transactions are as follows: 
1. The transaction is a QR cross-border 
2. {indikasi_limit_cpan} 
3. Repeated transactions were performed within a close and short period of time 
4. {indikasi_nominal} 
5. Transactions were performed at 1 Merchant, which is {m_name} 
6. Transactions occurred within the period of {min_date} - {max_date} 
 
Additionally, we kindly request your assistance in confirming the following points:   
1. Were all the transactions listed in the attached file genuinely performed by the customer? 
2. If there is an ongoing promotion from the Issuer, were these transactions in compliance with the applicable terms and conditions? 
3. If the transactions are deemed genuine, kindly provide further explanation.""" + FOOTER_EN,
}
