# Latihan Bahasa Thailand dari dasar

Bahan latihan bahasa Thailand untuk pelajar penutur bahasa Indonesia yang
**belum pernah belajar sama sekali**: belum mengenal hurufnya, belum tahu
nadanya, belum punya kosakata.

Materi ini berangkat dari huruf, bukan dari percakapan. Alasannya satu: tanpa
bisa membaca tulisan Thai, semua kosakata harus dihafal lewat tulisan Latin,
dan tulisan Latin tidak menuliskan nada. Nada mengubah arti kata, jadi jalan
itu buntu. Sasarannya tingkat A1 menuju A2.

| | |
|:--|:--|
| Konsonan | 44 huruf beserta kelasnya |
| Pola vokal | 31 pola, termasuk vokal yang tidak ditulis |
| Tanda dan angka | 7 tanda, 10 angka Thai |
| Nada | 5 nada, 17 baris aturan, 54 kata latihan, 6 pasangan nada |
| Latihan telinga | 12 pasangan bunyi, 24 kartu, 4 soal |
| Kosakata | 502 entri, 6 tahap, diurutkan menurut seberapa sering dipakai |
| Kata serumpun Sanskerta | 29 kata yang sama di Thai dan Indonesia |
| Tata bahasa | 12 topik, 60 soal |
| Frasa sehari-hari | 58 kalimat, 7 keadaan |
| Bacaan | 8 percakapan, 42 baris, 16 soal pemahaman |
| Total kartu | 882 |
| Lembar kerja tertulis | 12 lembar + 12 kunci jawaban |
| Pengujian otomatis | 6201 |

## Dua cara memakai

### 1. Aplikasi kartu di browser

Buka `index.html`. Tidak perlu memasang apa pun, dan tidak perlu peladen:
berkas datanya dimuat lewat tag `<script>`, bukan `fetch()`, sehingga halaman
ini jalan walau dibuka langsung dari berkas (`file://`).

Untuk menjalankannya lewat peladen lokal:

```bash
python -m http.server 8777
```

lalu buka <http://localhost:8777>.

Delapan modul dalam bentuk kartu bolak-balik dan pilihan ganda: aksara, nada,
telinga, kosakata (dua arah), kata serumpun, tata bahasa, frasa, dan bacaan.
Setiap kartu bertulisan Thai bisa dibunyikan dengan tombol **Dengarkan**.
Sakelar "Uji kelas konsonan" mengubah kartu huruf menjadi soal pilihan ganda,
sakelar "Lafal di depan" mematikan penyangga Latin bila Anda sudah siap
membaca langsung dari tulisan Thai, dan sakelar "Indonesia &rarr; Thai"
(menyala secara bawaan) menentukan arah latihan kosakata. Progres memakai lima
kotak Leitner yang sama dengan versi terminal dan tersimpan di `localStorage`
peramban Anda sendiri.

Pintasan papan ketik: `Spasi` balik kartu &middot; `&larr;` `&rarr;` navigasi
&middot; `1`&ndash;`5` pilih jawaban &middot; `A` dengarkan &middot; `H` sudah
hafal &middot; `B` belum hafal &middot; `S` acak &middot; `L` lafal
&middot; `/` cari.

### 2. Latihan di terminal

`python quiz.py` memberi hal yang tidak ada di versi web: jawaban yang
**ditulis sendiri** (bukan pilihan ganda), sesi berbatas waktu, interleaving
antarmodul, pembatasan materi baru per sesi, dan pengenalan materi menurut
urutan tahap. Rinciannya ada di bawah.

Progres kedua versi terpisah: aplikasi web memakai `localStorage`, versi
terminal memakai `progress.json`. Keduanya tidak saling tahu, jadi pilih salah
satu untuk materi yang sama.

## Mulai dari mana

Bila Anda benar-benar mulai dari nol, urutan ini yang dirancang:

1. **Modul Aksara, tahap 1.** Dua belas konsonan terpenting beserta kelasnya,
   dan enam pola vokal. Hafalkan kelasnya bersama hurufnya sejak awal —
   menambahkannya belakangan jauh lebih sulit.
2. **Modul Nada, tahap 1.** Lima nada dan sembilan baris aturan tanpa tanda
   nada. Di titik ini Anda sudah bisa menentukan nada kata yang hurufnya sudah
   dikenal.
3. **Modul Telinga, sejak hari pertama.** Latihan pendek yang sering lebih
   berguna daripada latihan panjang sesekali. Lima menit sehari sudah cukup.
4. **Modul Kosakata dan Frasa.** Baru di sini menghafal kata. Setiap kata
   sudah bisa Anda baca sendiri, bukan sekadar ditiru bunyinya.
5. **Modul Tata bahasa** menyusul, karena tata bahasanya dekat
   dengan bahasa Indonesia dan bukan penghalang utama.
6. **Modul Serumpun dan Bacaan** mempercepat kosakata dan memberi masukan
   yang bisa dipahami tanpa kamus.

`python quiz.py --stage 1` menjalankan semuanya pada tahap 1 saja, dengan
interleaving antarmodul.

## Pendekatan yang dipakai

Materi ini tidak disusun seperti kursus bahasa Thailand pada umumnya, sebab
kursus pada umumnya ditulis untuk penutur bahasa Inggris. Penutur bahasa
Indonesia berangkat dari titik yang berbeda, dan urutan materinya mengikuti
tiga keputusan berikut.

**Telinga lebih dahulu, baru mata, baru mulut.** Nada adalah bagian dari
identitas kata, sama seperti huruf. Kata yang masuk ke ingatan tanpa nadanya
masuk dalam keadaan rusak dan harus dihafal ulang kelak. Karena itu setiap
kartu bisa dibunyikan, dan ada satu modul khusus (Modul 6) yang melatih
telinga membedakan bunyi, bukan melatih mata membaca aturan.

**Yang sudah Anda miliki tidak perlu diajarkan panjang-panjang.** Banyak hal
yang menyulitkan penutur bahasa Inggris sudah Anda kuasai sejak kecil:

| Hal | Status bagi penutur bahasa Indonesia |
|:--|:--|
| Urutan kata, tanpa konjugasi, tanpa gender, tanpa kata sandang | Hampir sama dengan bahasa Indonesia |
| Bunyi `ng-` di awal kata (ngeri, ngilu) | Sudah dimiliki |
| `p t k` tanpa hembusan (ป ต ก) | Sudah dimiliki |
| Konsonan akhir yang tidak dilepas (sedap, sakit) | Sudah dimiliki; hanya perlu diperhatikan bahwa `-k` bahasa Indonesia sering menjadi hamzah, sedangkan Thai tetap [k] |
| Klasifikator (ekor, buah, batang) | Konsepnya sudah dikenal |
| Partikel akhir kalimat (ya, kok, dong) | Konsepnya sudah dikenal |
| Kosakata serapan Sanskerta | Ratusan kata sudah dikenal seumur hidup |

Itulah sebabnya modul tata bahasa di sini hanya 12 topik pendek, dan ada satu
modul khusus (Modul 7) untuk memanen kosakata serumpun.

**Waktu yang dihemat dipakai untuk tiga hal yang benar-benar baru.** Ketiganya
tidak ada dalam bahasa Indonesia, sehingga telinga Anda belum pernah
dilatih membedakannya:

1. **Nada** — bahasa Indonesia memakai tinggi-rendah suara untuk menandai
   jenis kalimat, bukan untuk membedakan kata. Akibatnya intonasi tanya Anda
   dapat merusak kata terakhir pada kalimat Thai.
2. **Panjang vokal** — เขา ('dia') dan ขาว ('putih') hanya berbeda lama
   vokalnya.
3. **Hembusan** — ไก่ ('ayam') dan ไข่ ('telur') hanya berbeda ada tidaknya
   embusan udara pada konsonan awalnya.

**Arah produksi didahulukan.** Untuk bisa berbicara, memanggil sendiri kata
Thainya jauh lebih berharga daripada sekadar mengenalinya saat dilihat. Karena
itu arah Indonesia &rarr; Thai dinyalakan secara bawaan di aplikasi web, dan
mode `kosakata-id` mendapat giliran lebih dahulu daripada `kosakata-th` ketika
sesi terpotong waktu.

**Yang tidak bisa dikerjakan aplikasi mana pun.** Tidak ada aplikasi yang bisa
mendengar dan mengoreksi nada ucapan Anda. Sesudah dua atau tiga bulan, carilah
penutur asli yang bersedia mengoreksi. Materi ini menyiapkan Anda supaya jam
bersama mereka tidak habis untuk hal yang bisa dipelajari sendiri.

## Suara

Setiap kartu yang memuat tulisan Thai punya tombol **Dengarkan** (pintasan
`A`). Pelafalannya memakai suara bawaan peramban dan perangkat Anda, jadi
tidak ada berkas audio yang perlu diunduh dan tidak ada yang dikirim ke mana
pun.

| Perangkat | Suara Thai |
|:--|:--|
| Android, iOS, iPadOS | Biasanya sudah tersedia |
| macOS | Tambahkan lewat System Settings &rarr; Accessibility &rarr; Spoken Content |
| Windows | Settings &rarr; Time &amp; language &rarr; Language &amp; region &rarr; tambahkan Thai beserta paket suaranya |

Bila perangkat Anda belum punya suara Thai, tombolnya mati dan aplikasi tetap
jalan: kartu Modul 6 berubah menjadi latihan mengucapkan, bukan mendengarkan.
Sakelar **Suara pelan** memperlambat pelafalan, berguna saat membandingkan
nada dan panjang vokal.

Suara mesin tidak sebaik penutur asli, terutama pada nada. Pakailah ia untuk
latihan harian, dan tetap dengarkan rekaman penutur asli untuk kata yang
Anda hafalkan.

## Mengapa kelas konsonan dihafal lebih dahulu

Bahasa Thailand punya 44 konsonan untuk 21 bunyi. Kelebihan hurufnya bukan
kekacauan sejarah, melainkan alat: setiap huruf berkelas **tengah**,
**tinggi**, atau **rendah**, dan kelas itulah yang menentukan nada kata
bersama jenis suku kata dan tanda nadanya.

ข dan ค sama-sama berbunyi *kh*. Bedanya:

| Tulisan | Kelas | Nada | Lafal |
|:--|:--|:--|:--|
| ขา | tinggi | naik | khǎa (kaki) |
| คา | rendah | sedang | khaa (tersangkut) |

Karena itu, menghafal huruf tanpa kelasnya berarti menghafal setengah. Modul
Aksara di sini selalu menyebutkan kelas pada sisi belakang kartu, dan punya
sakelar untuk menguji kelasnya saja.

## Aturan nada yang dipakai

Nada dihitung dari empat hal: kelas konsonan awal, jenis suku kata (hidup atau
mati), panjang vokal, dan tanda nada bila ada.

**Tanpa tanda nada**

| Kelas | Suku hidup | Suku mati, vokal pendek | Suku mati, vokal panjang |
|:--|:--|:--|:--|
| tengah | sedang | rendah | rendah |
| tinggi | naik | rendah | rendah |
| rendah | sedang | tinggi | turun |

**Dengan tanda nada**

| Kelas | mai ek ◌่ | mai tho ◌้ | mai tri ◌๊ | mai chattawa ◌๋ |
|:--|:--|:--|:--|:--|
| tengah | rendah | turun | tinggi | naik |
| tinggi | rendah | turun | — | — |
| rendah | turun | tinggi | — | — |

Tabel ini **tidak hanya ditulis di dokumentasi**. Ia dikerjakan ulang sebagai
kode di `thaidrill/tone.py`, dan pengujian otomatis memeriksa bahwa setiap
baris aturan di `data/nada.json` sama dengan hasil hitungan kode itu.

## Lafal yang diperiksa mesin

Setiap kata dan kalimat di seluruh data memuat tiga lajur:

| Lajur | Isi | Contoh |
|:--|:--|:--|
| `th` | tulisan Thai | ขนม |
| `syl` | pemecahan suku kata tertulis | `["ข", "นม"]` |
| `phon` | lafal bernada | khà-nǒm |

Pengujian otomatis mengambil `syl`, menghitung nada setiap suku kata dari
ejaannya memakai `thaidrill/tone.py`, lalu membandingkannya dengan nada pada
`phon`. **1334 kata dan kalimat** diperiksa dengan cara itu setiap kali
pengujian dijalankan.

Artinya: lafal yang tertulis di materi ini tidak mungkin bertentangan dengan
aturan nada yang diajarkannya. Bila suatu hari ada yang menyunting datanya dan
menulis lafal yang keliru nadanya, pengujian langsung gagal dan menyebutkan
kata mana yang salah.

Mesin itu juga memperhitungkan tiga pola ejaan yang tidak dapat dibaca huruf
per huruf:

- **ห nam** — ห di depan konsonan nyaring kelas rendah tidak dibunyikan dan
  menaikkan kelasnya: หมา dibaca mǎa, bukan hǎmaa.
- **อักษรนำ (aksara nam)** — konsonan kelas tinggi atau tengah yang berdiri
  sendiri sebagai suku kata menularkan kelasnya ke suku kata berikutnya:
  ขนม = khà-**nǒm**, bukan khà-nom.
- **ทร yang dibaca s** — ทราบ dibaca sâap, bukan thrâap.

Yang **tidak** diperiksa mesin: ketepatan arti bahasa Indonesia, kewajaran
kalimat contoh, dan alih huruf vokalnya (hanya nadanya yang diperiksa).
Daftar lengkapnya ada di [`data/NEEDS_REVIEW.md`](data/NEEDS_REVIEW.md).

## Dua lajur tulisan Latin

| Lajur | Untuk apa | Contoh |
|:--|:--|:--|
| `rom` (RTGS) | membaca papan nama jalan dan peta di Thailand | sawatdi |
| `phon` | melafalkan | sà-wàt-dii |

RTGS adalah alih huruf resmi pemerintah Thailand. Ia **tidak menuliskan nada**
dan tidak membedakan vokal panjang dari pendek, jadi ia berguna untuk mengenali
nama tempat, bukan untuk belajar mengucapkan.

Pada lajur `phon`: vokal panjang ditulis ganda (aa, ii, uu, ee, aae, oo, aaw,
uue, ooe), vokal pendek tunggal, dan nada ditulis sebagai tanda di atas vokal
pertama setiap suku kata — tanpa tanda (sedang), à (rendah), â (turun),
á (tinggi), ǎ (naik).

## Yang TIDAK ada di sini

- **Tidak ada dialek.** Hanya bahasa Thailand baku (Bangkok); ragam Isan,
  Utara, dan Selatan tidak dibahas.
- **Tidak ada pelajaran menyimak dan berbicara.** Proyek ini berupa teks,
  sedangkan nada pada akhirnya perlu didengar dari penutur asli. Lajur `phon` adalah
  penyangga, bukan pengganti telinga.
- **Tidak ada sistem penyebutan pukul.** Penyebutan pukul dalam bahasa
  Thailand memakai pola yang berbeda-beda menurut bagian hari dan memerlukan
  modulnya sendiri.
- **Tidak ada kata yang pembacaannya tidak bisa diperiksa mesin.** Beberapa
  kata sehari-hari (ผลไม้, โทรศัพท์) ejaannya menyimpang dari pola suku kata
  biasa. Kata-kata itu sengaja tidak dimasukkan, sebab lebih baik modulnya
  kurang lengkap daripada memuat lafal yang tidak terperiksa.
- **Tidak ada janji hasil.** Kecepatan belajar setiap orang berbeda.

## Persyaratan

Python 3.10 atau lebih baru. Tidak ada pustaka pihak ketiga yang perlu
dipasang untuk menjalankan latihannya; `pytest` hanya diperlukan untuk
menjalankan pengujian.

Terminal Anda perlu bisa menampilkan tulisan Thai. Di Windows, Windows
Terminal menampilkannya jauh lebih baik daripada `cmd.exe` lama.

## Mulai cepat

```bash
python quiz.py
```

Sesi bawaan: 20 menit, campuran semua mode, 8 kartu baru. Progres tersimpan di
`progress.json`.

```bash
python quiz.py --stats
```

## Bendera baris perintah

| Bendera | Arti |
|:--------|:-----|
| `--mode MODE` | Batasi mode. Boleh diulang atau dipisah koma. Bawaan: semua. |
| `--stage N` | Batasi materi sampai tahap N (1-6). |
| `--minutes M` | Lama sesi dalam menit (bawaan 20). Sesi berhenti saat waktunya habis. |
| `--limit N` | Batas jumlah soal dalam satu sesi. |
| `--new N` | Kartu baru per sesi (bawaan 8). `--new 0` berarti hanya mengulang. |
| `--no-phon` | Sembunyikan lafal bernada pada sisi depan kartu. |
| `--seed N` | Nilai awal pengacak, untuk mengulang susunan sesi yang sama. |
| `--progress BERKAS` | Lokasi berkas progres selain `progress.json`. |
| `--stats` | Tampilkan ringkasan kemajuan lalu keluar. |
| `--reset` | Hapus berkas progres (meminta konfirmasi). |
| `--no-color` | Matikan warna. |

Mode yang tersedia:

| Mode | Isi |
|:-----|:----|
| `aksara` | Huruf, kelas konsonan, pola vokal, tanda, dan angka. |
| `nada` | Lima nada, aturannya, dan soal "apa nada kata ini" yang dibuat otomatis. |
| `dengar` | Pasangan bunyi. Di terminal menjadi latihan mengucapkan, sebab terminal tidak membunyikan apa pun. |
| `kosakata-id` | Indonesia ke Thai. Pilihan ganda. Arah produksi, diberi giliran lebih dahulu. |
| `kosakata-th` | Thai ke Indonesia. Jawaban **ditulis** (bukan pilihan ganda). |
| `serumpun` | Kata serapan Sanskerta yang sama di Thai dan Indonesia. Jawaban ditulis. |
| `tatabahasa` | Soal tata bahasa. |
| `frasa` | Frasa sehari-hari; Anda menyusun kalimatnya lalu mencocokkan sendiri. |
| `bacaan` | Percakapan pendek beserta soal pemahaman. |

Di dalam sesi: ketik nomor untuk pilihan ganda, `l` untuk melewati, `k` untuk
keluar, `?` untuk melihat jawaban pada soal yang jawabannya ditulis (dihitung
salah).

## Isi materi

### Modul 1 — Aksara (`data/aksara.json`)

44 konsonan beserta nama Thainya (ก ไก่, "ko kai"), kelasnya, bunyi awal dan
bunyi akhirnya; 31 pola vokal termasuk dua pola yang **tidak ditulis sama
sekali** (vokal o pendek pada คน, dan vokal a pendek pada ขนม); 7 tanda
(empat tanda nada, ไม้ไต่คู้, ทัณฑฆาต, ไม้ยมก); 10 angka Thai; dan 12 soal.

Tabel 44 huruf tidak disimpan di `data/`, melainkan di `thaidrill/thai.py`,
dan `data/aksara.json` hanya menunjuk kepadanya lewat hurufnya. Dengan begitu
tidak ada dua sumber yang bisa berselisih tentang kelas sebuah huruf.

### Modul 2 — Nada (`data/nada.json`)

Lima nada beserta gambaran bunyinya, 17 baris aturan (9 tanpa tanda nada, 8
dengan tanda nada), 54 kata latihan, 6 kelompok pasangan nada, dan 12 soal.

Pasangan nada adalah latihan telinga yang tidak bisa digantikan oleh aturan:

| Kelompok | Kata |
|:--|:--|
| มา / ม้า / หมา | datang / kuda / anjing |
| ขาว / ข่าว / ข้าว | putih / berita / nasi |
| คา / ค่า / ค้า | tersangkut / nilai / berdagang |
| เสือ / เสื่อ / เสื้อ | harimau / tikar / baju |
| ปา / ป่า / ป้า / ป๊า / ป๋า | lima nada dengan satu huruf |
| ไกล / ใกล้ | jauh / dekat |

Pengujian otomatis memeriksa bahwa kata-kata dalam satu kelompok memang
berbeda nada satu sama lain.

### Modul 3 — Kosakata (`data/vocab.json`)

502 entri dalam 6 tahap dan 23 kelompok makna: sapaan, partikel, kata ganti,
kata tanya, angka, keluarga, orang, kata kerja, kata sifat, makanan, tempat,
waktu, arah, kendaraan, uang, klasifikator, tubuh dan kesehatan, alam dan
cuaca, perasaan, warna, hewan, benda sehari-hari, serta bangsa dan bahasa.

Setiap entri memuat tulisan Thai, pemecahan suku katanya, RTGS, lafal bernada,
arti, kelas kata, klasifikator (untuk kata benda), perkiraan seberapa sering
kata itu dipakai, satu kalimat contoh pendek, dan catatan pemakaian.

Setiap kata dan setiap kalimat contohnya diperiksa mesin: pemecahan suku
katanya harus sama dengan tulisannya, dan nadanya harus sama dengan hasil
hitungan dari ejaannya.

### Modul 4 — Tata bahasa (`data/grammar.json`)

| Topik | Isi |
|:------|:----|
| g01 | Susunan kalimat: pelaku - kata kerja - sasaran |
| g02 | Kata sifat sesudah kata benda, tanpa kata "adalah" |
| g03 | Tiga kata untuk "adalah": เป็น, คือ, อยู่ |
| g04 | Penafian: ไม่, ไม่ใช่, ยังไม่ |
| g05 | Membuat pertanyaan |
| g06 | Klasifikator dan cara menghitung |
| g07 | Kata tunjuk: นี่/นั่น dan นี้/นั้น |
| g08 | Waktu tanpa perubahan kata kerja: แล้ว, จะ, กำลัง, ยัง |
| g09 | Partikel sopan dan partikel rasa |
| g10 | Kata ganti dan sebutan |
| g11 | Tempat dan arah: ที่, ใน, บน, ไป, มา |
| g12 | Kata kerja berangkai dan tiga cara mengatakan "bisa" |

Setiap topik memiliki field `caveats` yang memuat pengecualian dan batas
berlakunya aturan. Hal-hal itu sengaja ditulis sebagai catatan, bukan sebagai
aturan mutlak.

### Modul 5 — Frasa sehari-hari (`data/frasa.json`)

58 kalimat utuh yang dipakai apa adanya, dikelompokkan menurut keadaan:
sapaan, perkenalan, warung dan restoran, belanja, arah dan jalan, darurat dan
sakit, serta waktu.

### Modul 6 — Latihan telinga (`data/dengar.json`)

Dua belas pasangan kata yang bedanya **hanya satu hal**: enam pasangan panjang
vokal (ปัก/ปาก, คัน/คาน, ทัน/ทาน, เขา/ขาว, ไต/ตาย, พัน/พาน) dan enam pasangan
hembusan (กา/คา, ตา/ทา, ปา/พา, ไก่/ไข่, ป่า/ผ่า, เป็น/เพ็ญ). Latihan nada
memakai enam kelompok pasangan nada di Modul 2.

Aplikasi web membunyikan salah satu kata lalu meminta Anda memilih kata mana
yang terdengar. Pengujian otomatis memeriksa bahwa semua kata dalam satu
pasangan **bernada sama** — kalau nadanya ikut berbeda, latihannya tidak lagi
melatih panjang vokal atau hembusan saja.

### Modul 7 — Kata serumpun (`data/serumpun.json`)

29 kata serapan Sanskerta-Pali yang hidup di kedua bahasa: มนุษย์ (manusia),
นรก (neraka), ราชา (raja), สัตว์ (satwa), ครุฑ (garuda), อักษร (aksara), dan
seterusnya; ditambah enam nama hari yang sama dengan penanggalan Jawa-Bali
(วันอังคาร = Anggara, วันพุธ = Buda) dan tiga angka Sanskerta yang menjadi nama
tanda nada (เอก, โท, ตรี = eka, dwi, tri).

Modul ini juga memberi peringatan untuk kata yang maknanya sudah bergeser:
สุข bukan 'suka' melainkan 'bahagia', ภูมิ bukan 'bumi' sebagai planet, dan
ชาติ bukan 'sejati'.

### Modul 8 — Bacaan (`data/bacaan.json`)

Delapan percakapan pendek (42 baris) beserta 16 soal pemahaman. Seluruh katanya
sudah ada di modul kosakata dan frasa, sehingga bisa dibaca tanpa kamus —
dan ada pengujian otomatis yang memeriksa hal itu.

## Cara kerja penjadwalan

Lima kotak Leitner. Jawaban benar menaikkan kartu satu kotak, jawaban salah
mengembalikannya ke kotak 1.

| Kotak | Jeda sebelum diulang |
|------:|---------------------:|
| 1 | hari itu juga |
| 2 | 1 hari |
| 3 | 3 hari |
| 4 | 7 hari |
| 5 | 16 hari |

Angka-angka itu adalah pilihan praktis yang lazim dipakai pada kartu Leitner,
**bukan hasil pengukuran**. Ubah `INTERVALS` di `thaidrill/leitner.py` bila
jadwal lain lebih cocok (dan `BOX_DAYS` di `app.js`; pengujian memeriksa
bahwa keduanya sama).

Empat hal lain yang diterapkan penjadwal:

- **Ulangan didahulukan.** Selama masih ada kartu jatuh tempo, materi baru
  dibatasi paling banyak 45% dari satu sesi.
- **Interleaving.** Soal dari modul berbeda disilang bergantian, dan materi
  lama disisipkan di antara materi baru kira-kira 2 lama : 1 baru. Mencampur
  materi umumnya menghasilkan ingatan yang lebih tahan lama daripada
  mengerjakan satu blok materi sejenis, meski terasa lebih sulit saat
  dikerjakan.
- **Materi baru masuk menurut urutan tahap**, bukan acak dari seluruh materi.
- **Lintasan kedua.** Pada hari-hari awal, ketika belum ada kartu jatuh tempo,
  kartu baru diulang sekali lagi di akhir sesi. Pengulangan itu tidak
  menaikkan kotak Leitner dua kali.

Jatah kartu baru dibagi per kelompok materi dengan bobot: aksara 3, nada 2,
telinga 2, kosakata 3, kata serumpun 1, tata bahasa 1, frasa 1, bacaan 1.
Aksara dan nada diberi bobot besar karena keduanya menjadi syarat bagi segala
hal lain; latihan telinga diberi bobot 2 karena nada, panjang vokal, dan
hembusan tidak ada dalam bahasa Indonesia sehingga perlu diulang jauh lebih
sering daripada hal yang sudah dimiliki penuturnya.

Di dalam satu tahap, kata yang **lebih sering dipakai** diperkenalkan lebih
dahulu. Lajur `freq` pada `data/vocab.json` membaginya menjadi tiga: 73 kata
inti, 260 kata yang sering, dan 169 kata yang lebih jarang. Pembagian itu
perkiraan penyusun, bukan hasil hitungan korpus — lihat `data/NEEDS_REVIEW.md`.

## Jadwal 10 minggu

Dengan pengaturan bawaan (20 menit per sesi, 8 kartu baru, 5 sesi per minggu):

| Minggu | Konsonan | Vokal | Kata latihan nada | Kosakata | Tata bahasa | Frasa | Kartu dikenal |
|-------:|---------:|------:|------------------:|---------:|------------:|------:|--------------:|
| 1 | 5 | 2 | 5 | 10 | 5 | 5 | 60 |
| 2 | 10 | 6 | 8 | 20 | 10 | 10 | 120 |
| 3 | 15 | 9 | 12 | 30 | 15 | 15 | 178 |
| 4 | 20 | 14 | 20 | 40 | 20 | 20 | 228 |
| 6 | 28 | 20 | 28 | 60 | 30 | 30 | 321 |
| 8 | 36 | 27 | 44 | 80 | 40 | 40 | 401 |
| 10 | 43 | 29 | 54 | 100 | 50 | 50 | 475 |

Dengan delapan modul, materi baru tersebar lebih lebar daripada sebelumnya:
pada minggu ke-10 hampir seluruh huruf dan pola vokal sudah diperkenalkan,
dan 475 dari 882 kartu sudah pernah dilihat. Kosakata baru mencapai sekitar
100 dari 502 kata, sebab penjadwal membagi jatah kartu baru ke delapan modul
sekaligus.

Dengan kosakata sebanyak ini, jalur bawaan tidak lagi cukup bila sasaran Anda
adalah menguasai kosakatanya. Dua pilihan yang masuk akal:

```bash
python quiz.py --mode kosakata-id,kosakata-th --new 15
```

untuk sesi khusus kosakata, atau menaikkan `--new` pada sesi campuran setelah
huruf dan nadanya mantap. Seluruh 502 kata memerlukan kira-kira 35 sesi
khusus kosakata dengan 15 kata baru per sesi.

### Dari mana angka-angka itu

Angka di tabel berasal dari **simulasi penjadwal**, bukan dari pengamatan
pembelajar nyata: 50 sesi berurutan, 5 sesi per minggu, dengan asumsi
ketepatan jawaban 85%. Pada simulasi itu, tunggakan soal jatuh tempo memuncak
di sekitar 357 soal. Dengan ketepatan 95%, puncaknya lebih rendah.

Tunggakan sebesar itu **lebih banyak daripada yang bisa dikerjakan dalam sesi
20 menit**. Itu bukan kesalahan hitung, melainkan akibat laju 8 kartu baru per
sesi pada materi sebanyak ini. Kecepatan setiap orang berbeda, dan tidak ada
yang menjamin angka ini berlaku untuk Anda.

### Bila tunggakan menumpuk

Bila `--stats` menunjukkan kartu jatuh tempo jauh lebih banyak daripada yang
bisa Anda kerjakan:

```bash
python quiz.py --new 0            # satu sesi khusus mengulang, tanpa materi baru
python quiz.py --new 4            # perlambat laju materi baru
python quiz.py --minutes 30       # sesi lebih panjang
```

Memperlambat materi baru lebih baik daripada menumpuk kartu yang tidak pernah
diulang.

## Lembar kerja

12 lembar kerja Markdown di `worksheets/`, dua lembar per tahap, dengan kunci
jawaban **terpisah** di `worksheets/answers/`. Setiap lembar memuat enam
bagian: kelas huruf, penentuan nada beserta alasannya, arti kata, menulis kata
Thai, tata bahasa, dan frasa.

Lembar kerja dibuat dari data oleh skrip, bukan ditulis tangan, sehingga
kuncinya selalu sejalan dengan datanya. Jangan menyuntingnya langsung.

```bash
python tools/build_worksheets.py
```

Menulis aksara Thai dengan tangan membantu membedakan huruf yang bentuknya
mirip (ก/ถ/ภ, ด/ค/ต, บ/ป/ษ); lihat [`worksheets/README.md`](worksheets/README.md).

## Anki

Ekspor CSV untuk Anki ada di `anki/`, beserta pemetaan kolom ke field di
[`anki/README.md`](anki/README.md).

```bash
python tools/build_exports.py
```

Catatan: bila Anda memakai Anki, pakailah penjadwalan Anki dan jangan
menjalankan `quiz.py` untuk materi yang sama. `progress.json` dan koleksi Anki
tidak saling tahu, sehingga satu kartu akan dijadwalkan oleh dua sistem
sekaligus.

## Pengujian

```bash
python -m pytest
```

6201 pengujian. Yang diperiksa:

| Berkas | Isi |
|:-------|:----|
| `test_thai.py` | Tabel 44 konsonan: jumlah tiap kelas, bunyi akhir yang sah, huruf yang tidak pernah menjadi konsonan akhir, dua huruf usang, bentuk NFC, dan pembacaan lajur `phon`. |
| `test_tone.py` | Tabel nada lengkap, panjang vokal hanya menentukan pada satu keadaan, 48 kata patokan, ห nam, อย, ทร yang dibaca s, gugus konsonan, aksara nam, dan jenis suku kata. |
| `test_data.py` | **Inti proyek:** 1334 kata dan kalimat diperiksa — gabungan suku katanya sama dengan tulisannya, dan nadanya sama dengan hitungan mesin. Juga: baris aturan sesuai mesin, pasangan nada benar-benar berbeda nada, id pola vokal dikenali mesin. |
| `test_schema.py` | Id unik di seluruh modul, format id, tahap 1-6 terisi pada tiap modul, kelas kata sah, field wajib terisi, pengecualian pemeriksaan wajib beralasan. |
| `test_keys.py` | Setiap soal punya tepat satu jawaban benar, tidak ada pilihan kembar, kunci soal buatan diambil dari mesin, pengecoh kosakata tidak pernah ikut benar, jawaban bertaip menerima arti lain. |
| `test_leitner.py` | Kenaikan dan penurunan kotak, jeda sesuai tabel, jatuh tempo, simpan dan muat ulang, berkas rusak tidak merusak pemuatan, penulisan atomik. |
| `test_session.py` | Batas kartu baru, ulangan tidak tergeser habis, kartu belum jatuh tempo tidak muncul, interleaving mencampur mode, satu kata dilatih dua arah, sesi dapat diulang dengan seed sama. |
| `test_exports.py` | Semua ekspor mutakhir (CSV, Anki, `webdata.js`), kunci soal di `webdata.js` sama dengan di `data/`, jeda Leitner di `app.js` sama dengan di Python, dan aplikasi web tidak memakai `fetch()` sehingga tetap jalan di `file://`. |
| `test_modul_baru.py` | Pasangan latihan telinga bernada sama, pasangan hembusan memang berbeda hembusan saja, pasangan panjang memakai vokal pendek dan panjang, kata serumpun tidak mengulang modul kosakata, kata yang maknanya bergeser wajib diberi peringatan, dan seluruh kata pada bacaan sudah pernah diajarkan. |
| `test_worksheets.py` | Kunci berada di berkas terpisah, semua bagian ada, lembar kerja tidak memuat jawabannya, kunci nada dihitung ulang dari ejaan, setiap butir berasal dari data. |

### Apa yang TIDAK bisa diuji mesin

Pengujian di atas memeriksa **bentuk** dan **keterikatan pada aturan nada**,
bukan kebenaran isi bahasanya. Yang tidak diperiksa mesin:

- Apakah arti bahasa Indonesianya tepat dan wajar.
- Apakah kalimat contohnya terdengar wajar bagi penutur asli.
- Apakah klasifikator yang dicantumkan memang yang lazim dipakai.
- Apakah catatan budaya dan pemakaiannya benar.
- Apakah alih huruf vokal dan konsonannya tepat — hanya nadanya yang
  diperiksa.

**Periksalah isinya dengan kamus atau pengajar** sebelum menghafalkannya.
Daftar lengkapnya ada di [`data/NEEDS_REVIEW.md`](data/NEEDS_REVIEW.md).

## Menyunting data

`data/*.json` adalah **satu-satunya sumber data**, kecuali tabel aksara dan
aturan nada yang berada di `thaidrill/thai.py` dan `thaidrill/tone.py`. Berkas
di `data/csv/`, `anki/`, `worksheets/`, dan `webdata.js` adalah turunan yang
dibuat ulang oleh skrip.

```bash
# 1. sunting data/vocab.json (atau modul lain)
python -m pytest                      # 2. pastikan data masih sah
python tools/build_exports.py         # 3. buat ulang CSV dan Anki
python tools/build_worksheets.py      # 4. buat ulang lembar kerja
python tools/build_web.py             # 5. buat ulang data aplikasi web
python -m pytest                      # 6. pastikan semua hasil mutakhir
```

Pengujian `test_exports.py` akan gagal bila data sudah berubah tetapi
ekspornya belum dibuat ulang.

### Menambah kata baru

Setiap entri baru wajib memuat `syl`, yaitu kata itu yang dipecah menjadi suku
kata **tertulis**. Pengujian akan menghitung nadanya dari ejaan dan
membandingkannya dengan `phon`. Bila pemecahannya keliru atau lafalnya salah
nada, pengujian gagal dan menyebutkan kata mana yang bermasalah:

```
vocab[v123]: มาก ditulis máak (nada ['tinggi']) tetapi ejaannya
memberi nada ['turun']
```

Bila sebuah kata memang tidak bisa diperiksa mesin (misalnya memuat huruf yang
dimatikan `◌์`), matikan pemeriksaannya dengan `"check_syl": false` dan
**wajib** sertakan `"check_why"` yang menjelaskan sebabnya — ada pengujian
yang memeriksa hal itu.

## Struktur folder

```
index.html            aplikasi kartu di browser
style.css             tiga tema: siam, ratri, baitoei
app.js                kartu, saringan, suara, Leitner di localStorage
webdata.js            data aplikasi web (dibuat ulang)
.nojekyll             agar GitHub Pages tidak memproses berkas lewat Jekyll
data/                 sumber data JSON + NEEDS_REVIEW.md
  aksara.json         Modul 1: huruf, vokal, tanda, angka
  nada.json           Modul 2: lima nada dan aturannya
  vocab.json          Modul 3: kosakata
  grammar.json        Modul 4: tata bahasa
  frasa.json          Modul 5: frasa sehari-hari
  dengar.json         Modul 6: pasangan bunyi untuk latihan telinga
  serumpun.json       Modul 7: kata serapan Sanskerta
  bacaan.json         Modul 8: percakapan pendek
  csv/                ekspor CSV (dibuat ulang)
thaidrill/            paket inti
  thai.py             tabel 44 konsonan, kelas, tanda, utilitas lafal
  tone.py             aturan nada, pembaca suku kata, ห nam, aksara nam
  leitner.py          lima kotak + jadwal + berkas progres
  dataio.py           pemuat data dan pengenal kartu
  questions.py        pembuat soal per mode
  session.py          penyusun sesi (jatuh tempo, materi baru, interleaving)
quiz.py               antarmuka baris perintah
tools/                build_exports.py, build_worksheets.py, build_web.py
anki/                 ekspor Anki (dibuat ulang) + pemetaan field
worksheets/           lembar kerja (dibuat ulang)
  answers/            kunci jawaban
tests/                pengujian otomatis
progress.json         progres Anda (dibuat saat latihan pertama)
```

## Catatan keterbatasan

- Materi ini disusun oleh model bahasa dan diperiksa secara otomatis hanya
  pada hal-hal yang bisa diperiksa mesin. Isi bahasanya belum ditinjau penutur
  asli atau pengajar.
- Tingkat A1-A2 berarti kalimat pendek dan kosakata sehari-hari. Membaca surat
  kabar Thailand dengan lancar memerlukan kosakata yang jauh lebih banyak
  daripada yang ada di sini.
- Suara pada aplikasi ini berasal dari pelafal mesin bawaan perangkat Anda.
  Ia cukup untuk latihan membedakan panjang vokal dan hembusan, tetapi nadanya
  tidak selalu setepat penutur asli. Tetap dengarkan rekaman penutur asli untuk
  kata yang Anda hafalkan.
- Tidak ada koreksi ucapan. Aplikasi bisa membunyikan kata dan menguji telinga
  Anda, tetapi tidak bisa mendengar Anda. Untuk itu diperlukan penutur asli.
- Kosakata 502 kata cukup untuk percakapan sehari-hari pada tingkat A1 menuju
  A2, tetapi belum cukup untuk membaca surat kabar. Daftar frekuensi dari
  korpus Thai akan membuat urutan pengenalannya lebih tepat daripada
  perkiraan yang dipakai sekarang.
- Beberapa kata sehari-hari sengaja tidak dimasukkan karena pembacaannya
  tidak bisa diperiksa mesin, misalnya ผลไม้ ('buah') dan ตำรวจ ('polisi')
  yang satu hurufnya dibaca dua kali. Lihat `data/NEEDS_REVIEW.md`.
