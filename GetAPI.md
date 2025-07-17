
<img width="591" height="719" alt="Screenshot 2025-07-18 005614" src="https://github.com/user-attachments/assets/5be4549b-df98-4b81-8294-7d85846f14ec" />
# Youtube Upload API (Disarankan untuk RDP Windows)

Prequisites :
1. Akun Gmail dummy/tidak terpakai/utama hanya untuk generate API
2. Akun Gmail berisi channel yang akan kita upload

Workflow :
1. Aktifkan YouTube API di Google Cloud Console dan tambahkan OAuth, Consent Screen & Scope
2. Download Client Secret dan Generate Token, client_secret & token bisa di upload ke RDP
3. Upload Thumbnail, Edit Metadata dan Upload Video

---

## Cara Mendapat Token
**1. Buat Google Cloud Console Project**

Login ke akun Google/Gmail dummy untuk generate API & masuk ke [Google Cloud Console](https://console.cloud.google.com/), kemudian create new project
<img width="1519" height="823" alt="Screenshot 2025-07-17 113909" src="https://github.com/user-attachments/assets/20c70c80-e4d0-4208-a774-ba401812ae11" />

---

**2. Search Youtube Data API V3**
Search Youtube Data API V3 di bagian atas kemudian Enable 
<img width="1033" height="236" alt="Screenshot 2025-07-17 114123" src="https://github.com/user-attachments/assets/1a776267-f862-43f1-8fea-d557dc1ae8eb" />
<img width="839" height="394" alt="Screenshot 2025-07-17 114216" src="https://github.com/user-attachments/assets/daba904a-a5f1-4c3f-bcbe-54f73eefb7b2" />

---

**3. Create Credential**
Create Credential kemudian isi informasi
- App Name : bisa di isi bebas
- User Support email : isi gmail kita
- Audience : EXTERNAL 
- Contact Information : isi gmail kita
- Kemudian Finish
<img width="920" height="477" alt="Screenshot 2025-07-17 114250" src="https://github.com/user-attachments/assets/350568a2-8636-4319-b96b-a4e351fb1cd7" />

---

**4. Membuat OAuth Client**
Pilih Create OAuth Client dan pilih Desktop App, nama bebas kemudian create
<img width="918" height="548" alt="Screenshot 2025-07-17 114503" src="https://github.com/user-attachments/assets/360b97bd-7f82-495b-8264-39c7d0ef45bc" />
<img width="602" height="413" alt="Screenshot 2025-07-17 114527" src="https://github.com/user-attachments/assets/6b263ec2-b2cc-4c5f-bda6-e017bb42c0d7" />

---

**5. Download Client Secret**
Jangan lupa Download JSON untuk mendapatkan info client_secret.json karena per Juni 2025, hanya bisa download sekali, jika lupa bisa diulang untuk create OAuth Client baru
<img width="503" height="642" alt="Screenshot 2025-07-17 114819" src="https://github.com/user-attachments/assets/69aceeff-8846-4334-ac64-d4c762ec0ccf" />

---

**6. Tambahkan User Audience**
Pindah ke tab Audience kemudian Add User, user ini adalah email kita yg berisi channel yang akan kita gunakan untuk proses upload, add emailnya kemudian Save
<img width="815" height="809" alt="Screenshot 2025-07-17 114844" src="https://github.com/user-attachments/assets/acb79165-542f-4ff7-9189-cdd89f5a2912" />
<img width="749" height="357" alt="Screenshot 2025-07-17 114856" src="https://github.com/user-attachments/assets/ccaa4283-150a-443f-903f-e2dab6f6f8ac" />

---

**7. Tambahkan Data Akses ke Youtube API**
Pindah ke tab Data Access kemudian Add or Remove Scopes. Pada bagian kanan filter (enter property) kita search "youtube" kemudian kita enter, kita centang semua scope kemudian Update.
Pastikan semua scope sudah tertambah di Data Access, kemudian Save.
<img width="838" height="434" alt="Screenshot 2025-07-17 114911" src="https://github.com/user-attachments/assets/5ef735f1-fd83-4b45-b939-b27102c25ce2" />
<img width="616" height="959" alt="Screenshot 2025-07-17 114954" src="https://github.com/user-attachments/assets/253fde77-ff3c-4ccb-a27b-809d547d4167" />

---

**8. Cara Generate Token (Sekali saja) & Refresh Token**
Pada input Client Secret paling atas, pilih client secret yang sudah kita download tadi, tidak perlu rename client_secret nya.

<img width="593" height="200" alt="Screenshot 2025-07-18 000754" src="https://github.com/user-attachments/assets/91b8ba06-e505-448a-8f22-dc024e1192a0" />

---
Kemudian Save Token To bisa kita pilih dimana akan kita letakkan file token kita, isi file name dengan token dan pastikan filetypenya .json.

<img width="248" height="84" alt="Screenshot 2025-07-18 000934" src="https://github.com/user-attachments/assets/5101bf65-18b4-47a5-aa53-99c8b3c88238" />

---
Selanjutnya generate dan browser akan terbuka, pilih email yang berisi channel yg akan kita upload.

<img width="1020" height="376" alt="Screenshot 2025-07-18 001347" src="https://github.com/user-attachments/assets/6047e4e9-5b53-4b2e-a747-5262b86e825c" />

---
Jika ada prompt Google Hasn't Verified This App, pilih continue.

<img width="1025" height="372" alt="Screenshot 2025-07-18 001406" src="https://github.com/user-attachments/assets/eb226329-e227-47cf-b72c-0a7e1b731d4b" />

---
Select all kemudian continue. Kita akan mendapat file token.json.

<img width="503" height="763" alt="Screenshot 2025-07-18 001503" src="https://github.com/user-attachments/assets/d88b0fee-7634-4659-8b81-1762738ee1c0" />

---
Disarankan untuk refresh token setiap hari, hanya perlu upload client_secret dan token yang sudah kita generate tadi.

<img width="596" height="210" alt="Screenshot 2025-07-18 001716" src="https://github.com/user-attachments/assets/c23447b7-8784-4739-bb9e-617b4c37da8a" />

---

>**Selanjutnya tinggal isi**
>- Video yang akan di upload
>- Thumbnail (Setau saya ada limit max 10 thumnbail perhari, CMIIW)
>- Category (Kategori Youtube, default 22: People and Blogs)
>- Untuk bisa langsung upload menggunakan judul, tag dan deskripsi, bisa centang Enable Custom Title & Tags
>- Isi judul, tag kemudian deskripsi kemudian Generate Metadata dan silahkan upload.











