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
| Kosakata | 186 entri, 6 tahap |
| Tata bahasa | 12 topik, 60 soal |
| Frasa sehari-hari | 58 kalimat, 7 keadaan |
| Total kartu | 485 |
| Lembar kerja tertulis | 12 lembar + 12 kunci jawaban |
| Pengujian otomatis | 3193 |

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

Lima modul dalam bentuk kartu bolak-balik dan pilihan ganda: aksara, nada,
kosakata (dua arah), tata bahasa, dan frasa. Sakelar "Uji kelas konsonan"
mengubah kartu huruf menjadi soal pilihan ganda, dan sakelar "Lafal di depan"
mematikan penyangga Latin bila Anda sudah siap membaca langsung dari tulisan
Thai. Progres memakai lima kotak Leitner yang sama dengan versi terminal dan
tersimpan di `localStorage` peramban Anda sendiri.

Pintasan papan ketik: `Spasi` balik kartu &middot; `&larr;` `&rarr;` navigasi
&middot; `1`&ndash;`5` pilih jawaban &middot; `H` sudah hafal &middot; `B`
belum hafal &middot; `S` acak &middot; `L` lafal &middot; `/` cari.

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
3. **Modul Kosakata dan Frasa.** Baru di sini menghafal kata. Setiap kata
   sudah bisa Anda baca sendiri, bukan sekadar ditiru bunyinya.
4. **Modul Tata bahasa** menyusul, karena tata bahasanya dekat
   dengan bahasa Indonesia dan bukan penghalang utama.

`python quiz.py --stage 1` menjalankan semuanya pada tahap 1 saja, dengan
interleaving antarmodul.

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
`phon`. **607 kata dan kalimat** diperiksa dengan cara itu setiap kali
pengujian dijalankan.

Artinya: lafal yang tertulis di materi ini tidak mungkin bertentangan dengan
aturan nada yang diajarkannya. Bila suatu hari ada yang menyunting datanya dan
menulis lafal yang keliru nadanya, pengujian langsung gagal dan menyebutkan
kata mana yang salah.

Mesin itu juga memperhitungkan dua hal yang sering membuat pembelajar
tersandung:

- **ห nam** — ห di depan konsonan nyaring kelas rendah tidak dibunyikan dan
  menaikkan kelasnya: หมา dibaca mǎa, bukan hǎmaa.
- **อักษรนำ (aksara nam)** — konsonan kelas tinggi atau tengah yang berdiri
  sendiri sebagai suku kata menularkan kelasnya ke suku kata berikutnya:
  ขนม = khà-**nǒm**, bukan khà-nom.

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
| `kosakata-th` | Thai ke Indonesia. Jawaban **ditulis** (bukan pilihan ganda). |
| `kosakata-id` | Indonesia ke Thai. Pilihan ganda. |
| `tatabahasa` | Soal tata bahasa. |
| `frasa` | Frasa sehari-hari; Anda menyusun kalimatnya lalu mencocokkan sendiri. |

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

186 entri dalam 6 tahap: sapaan, partikel sopan, kata ganti, kata tanya,
angka, keluarga, orang, kata kerja, kata sifat, makanan, tempat, waktu, arah,
kendaraan, uang, klasifikator, tubuh, cuaca, dan perasaan.

Setiap entri memuat tulisan Thai, pemecahan suku katanya, RTGS, lafal bernada,
arti, kelas kata, klasifikator (untuk kata benda), satu kalimat contoh pendek,
dan catatan pemakaian.

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
kosakata 3, tata bahasa 1, frasa 1. Aksara dan nada diberi bobot besar karena
keduanya menjadi syarat bagi segala hal lain.

## Jadwal 10 minggu

Dengan pengaturan bawaan (20 menit per sesi, 8 kartu baru, 5 sesi per minggu):

| Minggu | Konsonan | Vokal | Kata latihan nada | Kosakata | Tata bahasa | Frasa | Kartu dikenal |
|-------:|---------:|------:|------------------:|---------:|------------:|------:|--------------:|
| 1 | 8 | 3 | 2 | 15 | 5 | 5 | 50 |
| 2 | 16 | 9 | 6 | 30 | 10 | 10 | 100 |
| 3 | 21 | 16 | 12 | 45 | 15 | 15 | 150 |
| 4 | 30 | 20 | 18 | 60 | 20 | 20 | 200 |
| 5 | 33 | 26 | 23 | 75 | 25 | 25 | 250 |
| 6 | 38 | 27 | 29 | 90 | 30 | 30 | 300 |
| 7 | 44 | 31 | 36 | 105 | 35 | 35 | 349 |
| 10 | 44 | 31 | 54 | 150 | 50 | 50 | 448 |

**Seluruh 44 konsonan dan 31 pola vokal sudah diperkenalkan pada akhir minggu
ke-7.** Kosakata mencapai sekitar 150 dari 186 kata pada minggu ke-10.

### Dari mana angka-angka itu

Angka di tabel berasal dari **simulasi penjadwal**, bukan dari pengamatan
pembelajar nyata: 50 sesi berurutan, 5 sesi per minggu, dengan asumsi
ketepatan jawaban 85%. Pada simulasi itu, tunggakan soal jatuh tempo memuncak
di sekitar 360 soal. Dengan ketepatan 95%, puncaknya sekitar 280.

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

3193 pengujian. Yang diperiksa:

| Berkas | Isi |
|:-------|:----|
| `test_thai.py` | Tabel 44 konsonan: jumlah tiap kelas, bunyi akhir yang sah, huruf yang tidak pernah menjadi konsonan akhir, dua huruf usang, bentuk NFC, dan pembacaan lajur `phon`. |
| `test_tone.py` | Tabel nada lengkap, panjang vokal hanya menentukan pada satu keadaan, 48 kata patokan, ห nam, อย, gugus konsonan, aksara nam, dan jenis suku kata. |
| `test_data.py` | **Inti proyek:** 607 kata dan kalimat diperiksa — gabungan suku katanya sama dengan tulisannya, dan nadanya sama dengan hitungan mesin. Juga: baris aturan sesuai mesin, pasangan nada benar-benar berbeda nada, id pola vokal dikenali mesin. |
| `test_schema.py` | Id unik di seluruh modul, format id, tahap 1-6 terisi pada tiap modul, kelas kata sah, field wajib terisi, pengecualian pemeriksaan wajib beralasan. |
| `test_keys.py` | Setiap soal punya tepat satu jawaban benar, tidak ada pilihan kembar, kunci soal buatan diambil dari mesin, pengecoh kosakata tidak pernah ikut benar, jawaban bertaip menerima arti lain. |
| `test_leitner.py` | Kenaikan dan penurunan kotak, jeda sesuai tabel, jatuh tempo, simpan dan muat ulang, berkas rusak tidak merusak pemuatan, penulisan atomik. |
| `test_session.py` | Batas kartu baru, ulangan tidak tergeser habis, kartu belum jatuh tempo tidak muncul, interleaving mencampur mode, satu kata dilatih dua arah, sesi dapat diulang dengan seed sama. |
| `test_exports.py` | Semua ekspor mutakhir (CSV, Anki, `webdata.js`), kunci soal di `webdata.js` sama dengan di `data/`, jeda Leitner di `app.js` sama dengan di Python, dan aplikasi web tidak memakai `fetch()` sehingga tetap jalan di `file://`. |
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
app.js                kartu, saringan, Leitner di localStorage
webdata.js            data aplikasi web (dibuat ulang)
.nojekyll             agar GitHub Pages tidak memproses berkas lewat Jekyll
data/                 sumber data JSON + NEEDS_REVIEW.md
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
- Nada perlu didengar. Lajur `phon` memberi tahu nada apa yang seharusnya
  diucapkan, tetapi tidak bisa mengajari telinga Anda membedakannya. Carilah
  rekaman penutur asli untuk setiap kata yang Anda hafalkan, terutama untuk
  enam kelompok pasangan nada di Modul 2.
- Tidak ada latihan menyimak dan berbicara di proyek ini.
