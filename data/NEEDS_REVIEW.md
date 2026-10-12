# Yang masih perlu ditinjau manusia

Berkas ini mendaftar hal-hal yang **tidak bisa diperiksa mesin**, atau yang
sudah diperiksa tetapi dengan batas tertentu. Mesin di proyek ini memeriksa
bentuk dan keterikatan pada aturan nada; ia tidak tahu apakah sebuah kata
wajar dipakai, apakah artinya tepat, dan apakah catatan budayanya benar.

Materi ini disusun oleh model bahasa dan **belum ditinjau penutur asli atau
pengajar**. Periksalah dengan kamus atau pengajar sebelum menghafalkannya.

## Yang sudah diperiksa mesin

| Hal | Diperiksa di |
|:--|:--|
| Setiap kata dan kalimat contoh: gabungan suku katanya sama dengan tulisannya | `tests/test_data.py` |
| Nada pada lajur `phon` sama dengan nada yang dihitung dari ejaannya | `tests/test_data.py` |
| Sembilan baris aturan nada tanpa tanda dan delapan baris bertanda sesuai mesin | `tests/test_data.py` |
| Kelas konsonan pada soal buatan diambil dari tabel 44 huruf | `tests/test_keys.py` |
| Pasangan nada memang berbeda nada satu sama lain | `tests/test_data.py` |
| Setiap soal pilihan ganda punya tepat satu jawaban benar | `tests/test_keys.py` |
| Semua ekspor (CSV, Anki, lembar kerja, `webdata.js`) mutakhir | `tests/test_exports.py` |
| Pasangan latihan telinga bernada SAMA, sehingga yang dilatih memang panjang vokal atau hembusannya saja | `tests/test_modul_baru.py` |
| Pasangan hembusan memang berupa pasangan X dan Xh menurut tabel konsonan | `tests/test_modul_baru.py` |
| Kata serumpun tidak mengulang kata yang sudah ada di modul kosakata | `tests/test_modul_baru.py` |
| Seluruh kata pada modul bacaan sudah pernah diajarkan di modul lain | `tests/test_modul_baru.py` |

702 kata dan kalimat contoh diperiksa dengan cara itu.

## Yang TIDAK diperiksa mesin

1. **Ketepatan arti bahasa Indonesia.** Mesin tidak tahu apakah `อร่อย`
   sebaiknya diterjemahkan "enak" atau "lezat", dan tidak tahu bila sebuah
   arti salah sama sekali.
2. **Kewajaran kalimat contoh.** Kalimat contoh dibuat pendek dan memakai
   kosakata yang sudah ada di modul ini. Pendek tidak selalu berarti wajar
   bagi penutur asli.
3. **Alih huruf vokal dan konsonan pada lajur `phon`.** Yang diperiksa mesin
   hanya NADA-nya. Bila `เสือ` ditulis `sǔea` atau `sǔa`, keduanya akan lolos
   pengujian selama nadanya naik.
4. **Klasifikator.** Pilihan klasifikator pada setiap kata benda belum
   diperiksa terhadap kamus.
5. **Catatan budaya dan pemakaian.** Semua kalimat pada field `note` —
   termasuk hal seperti kapan memakai `พี่` dan `น้อง`, atau kebiasaan
   menawar — perlu ditinjau manusia.
6. **Penjelasan tata bahasa.** Dua belas topik di `grammar.json` sengaja
   disederhanakan untuk tingkat A1-A2. Field `caveats` memuat batasnya, tetapi
   penyederhanaan yang menyesatkan tetap mungkin lolos.
7. **Lajur `freq` pada kosakata.** Pembagian 48 kata inti, 113 kata sering,
   dan 25 kata lebih jarang adalah **perkiraan penyusun**, bukan hasil
   hitungan korpus. Ia menentukan kata mana yang diperkenalkan lebih dahulu,
   jadi kekeliruan di sini memperlambat belajar tetapi tidak membuat materinya
   salah. Daftar frekuensi dari korpus Thai akan jauh lebih baik.
8. **Hubungan asal kata pada modul serumpun.** Kesamaan bentuk dan makna
   antara มนุษย์ dan 'manusia' kasatmata, tetapi berkas ini tidak merujuk kamus
   etimologi. Beberapa hubungan yang ditandai `sebagian` (วาจา/'wacana',
   วิชา/'widya') perlu diperiksa ahli. Pakailah kemiripan itu untuk MENGINGAT
   kata, bukan untuk menyimpulkan sejarah bahasanya.
9. **Suara.** Pelafalan di aplikasi web memakai pelafal mesin bawaan perangkat,
   bukan rekaman penutur asli. Mutunya berbeda-beda antar perangkat, dan
   nadanya tidak selalu setepat penutur asli. Proyek ini tidak memuat berkas
   audio sendiri.

## Butir tertentu yang diberi tanda

Tiga puluh butir berikut mematikan sebagian pemeriksaan mesin, dan
masing-masing wajib menyertakan alasannya di field `check_why` (diuji di
`tests/test_schema.py`). Sisanya, 672 butir, diperiksa penuh.

Hampir semuanya satu sebab yang sama: **huruf yang ditulis tetapi tidak
dibunyikan.** Ejaan Thai mempertahankan bentuk asal kata serapan, sedangkan
yang dibaca lebih pendek daripada yang ditulis.

| Butir | Yang dimatikan | Sebab |
|:--|:--|:--|
| 18 entri yang memuat `ไทย` (kosakata, frasa, bacaan) | pemeriksaan suku kata | `ย` pada `ไทย` tidak dibunyikan, jadi suku kata yang dibaca hanya `ไท` |
| 9 kata serumpun: `มนุษย์`, `สัตว์`, `ทุกข์`, `ภูมิ`, `ชาติ`, `อาทิตย์`, `จันทร์`, `ศุกร์`, `เสาร์` | pemeriksaan suku kata | huruf terakhirnya dimatikan oleh `◌์`, atau tanda vokalnya tidak dibunyikan |
| `aksara.marks[m06]` (`ยักษ์`) | pemeriksaan suku kata | `ษ` dimatikan oleh `◌์` |
| `aksara.digits[0]` (`ศูนย์`) | pemeriksaan suku kata | `ย` dimatikan oleh `◌์` |
| `aksara.marks[m07]` (`เด็กๆ`) | pemeriksaan suku kata dan nada | `ๆ` menyuruh kata dibaca dua kali |

Perhatikan bahwa **nadanya tetap diperiksa** pada 29 dari 30 butir itu; yang
dimatikan hanya perbandingan jumlah suku kata. Hanya `เด็กๆ` yang nadanya
tidak diperiksa.

## Hal yang sengaja dihindari

- **Kata yang ejaannya tidak terbaca pembaca suku kata.** Beberapa kata
  sehari-hari (misalnya `ผลไม้`, `โทรศัพท์`) punya pembacaan yang tidak
  mengikuti pola suku kata biasa. Kata-kata itu **tidak dimasukkan** ke modul
  ini, bukan dimasukkan dengan pemeriksaan dimatikan. Lebih baik modulnya
  kurang lengkap daripada memuat lafal yang tidak bisa diperiksa.
- **Penyebutan pukul.** Sistem jam bahasa Thailand berbeda-beda menurut bagian
  hari dan memerlukan modul tersendiri. Yang ada di sini hanya `กี่โมง`
  ("jam berapa") sebagai frasa.
- **Nada percakapan yang menyimpang dari ejaan.** Beberapa kata diucapkan
  dengan nada lain dalam percakapan sehari-hari (`ไหม`, `ฉัน`, `เขา`).
  Datanya memakai nada menurut ATURAN EJAAN, dan perbedaannya dicatat pada
  field `note`. Itu pilihan sadar: aturan ejaan bisa diperiksa mesin,
  kebiasaan lisan tidak.
