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


# ================= KAMUS TEMPLATE (DIRAMPINGKAN) =================
TEMPLATES = {
    # -----------------------------------------------------------------
    # KELOMPOK DOMESTIK (HANYA BAHASA INDONESIA)
    # -----------------------------------------------------------------
    
    "case1_id": """Dear Rekan {target_name}, 

Berkaitan dengan email ini kami pihak (switching) memiliki kewajiban sebagai Penyelenggara Infrastruktur Pembayaran untuk memastikan keamanan perlindungan konsumen. Mohon bantuannya untuk dapat melakukan pengecekan (due diligence) terhadap transaksi berpotensi fraud yang terjadi pada MPAN ({mpan_display}) Acquirer {target_name} Merchant {m_name} 

Indikasi yang kami temukan terkait transaksi tersebut adalah sebagai berikut: 
1. Total nilai transaksi Rp {formatted_amount} 
2. Transaksi didominasi dengan nominal yang besar 
3. Transaksi dilakukan secara berulang dan dalam waktu yang singkat 
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
}
