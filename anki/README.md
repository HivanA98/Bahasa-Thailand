# anki/ — ekspor untuk Anki

Berkas di folder ini **dibuat ulang** oleh `tools/build_exports.py` dari
`data/*.json`. Jangan menyuntingnya langsung; sunting datanya lalu jalankan:

```bash
python tools/build_exports.py
```

## Berkas

| Berkas | Jumlah kartu | Isi |
|:-------|-------------:|:----|
| `aksara.csv` | 75 | 44 konsonan dan 31 pola vokal |
| `nada.csv` | 54 | kata latihan nada beserta alasan nadanya |
| `kosakata.csv` | 186 | kosakata inti |
| `tatabahasa.csv` | 60 | soal tata bahasa |
| `frasa.csv` | 58 | frasa sehari-hari |

## Cara impor

1. Anki: **File → Import**, pilih berkasnya.
2. Pilih jenis catatan (note type) yang jumlah fieldnya cukup. Untuk
   `kosakata.csv` diperlukan **8 field**; untuk berkas lain lihat tabel di bawah.
3. Petakan setiap kolom ke field sesuai tabel. Kolom terakhir adalah **Tags**.
4. Pastikan "Allow HTML in fields" **dimatikan**, kecuali untuk
   `tatabahasa.csv` yang memakai `<br>` pada sisi depan.

Tiga baris pertama setiap berkas adalah pengarah untuk Anki 2.1.55 ke atas:

```
#separator:Comma
#html:false
#tags column:N
```

Anki versi tersebut dan yang lebih baru membaca pengarah itu, lalu langsung
memakai pemisah serta kolom tag yang benar. Bila Anki Anda lebih tua dan
menolak berkasnya, **hapus tiga baris itu** lalu atur pemisah dan kolom tag
secara manual di jendela impor.

## Pemetaan kolom

### `aksara.csv` — 5 kolom

| Kolom | Isi |
|------:|:----|
| 1 | huruf atau pola vokal (sisi depan) |
| 2 | nama, kelas, dan bunyinya (sisi belakang) |
| 3 | kelas konsonan, atau contoh kata untuk baris vokal |
| 4 | catatan |
| 5 | Tags |

### `nada.csv` — 6 kolom

| Kolom | Isi |
|------:|:----|
| 1 | kata (sisi depan) |
| 2 | nada (sisi belakang) |
| 3 | lafal bernada |
| 4 | arti |
| 5 | alasan nadanya, dihitung dari ejaan |
| 6 | Tags |

### `kosakata.csv` — 8 kolom

| Kolom | Isi |
|------:|:----|
| 1 | tulisan Thai |
| 2 | arti |
| 3 | lafal bernada |
| 4 | alih huruf RTGS |
| 5 | kelas kata, klasifikator, RTGS |
| 6 | kalimat contoh |
| 7 | catatan |
| 8 | Tags |

### `tatabahasa.csv` — 4 kolom

| Kolom | Isi |
|------:|:----|
| 1 | soal beserta pilihan jawabannya (memakai `<br>`) |
| 2 | jawaban |
| 3 | penjelasan |
| 4 | Tags |

### `frasa.csv` — 6 kolom

| Kolom | Isi |
|------:|:----|
| 1 | arti bahasa Indonesia (sisi depan) |
| 2 | kalimat Thai |
| 3 | lafal bernada |
| 4 | arti harfiah |
| 5 | catatan |
| 6 | Tags |

## Tag yang dipakai

Setiap kartu memuat tag `thai`, nama modulnya, kategorinya, dan tahapnya,
misalnya `thai kosakata makanan tahap3`. Dengan begitu Anda bisa membatasi
belajar per tahap di Anki, sama seperti `--stage` pada `quiz.py`.

## Peringatan

Bila Anda memakai Anki, pakailah penjadwalan Anki dan **jangan** menjalankan
`quiz.py` untuk materi yang sama. `progress.json` dan koleksi Anki tidak
saling tahu, sehingga satu kartu akan dijadwalkan oleh dua sistem sekaligus.
