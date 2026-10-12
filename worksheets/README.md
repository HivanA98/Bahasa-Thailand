# worksheets/ — lembar kerja tertulis

Dua belas lembar kerja, dua lembar untuk setiap tahap, beserta kunci
jawabannya yang **disimpan terpisah** di `worksheets/answers/` supaya lembar
kerjanya bisa dicetak tanpa ikut memperlihatkan jawabannya.

Semua berkas di sini **dibuat ulang** dari `data/*.json`. Jangan menyuntingnya
langsung; sunting datanya lalu jalankan:

```bash
python tools/build_worksheets.py
```

## Isi setiap lembar

| Bagian | Yang dikerjakan |
|:--|:--|
| 1. Huruf | Tulis kelas konsonan dan bunyi awalnya |
| 2. Nada | Tentukan nada setiap kata beserta alasannya |
| 3. Arti kata | Tulis arti bahasa Indonesianya |
| 4. Tulis kata Thai | Tulis tulisan Thai dan lafalnya dari arti yang diberikan |
| 5. Tata bahasa | Pilihan ganda |
| 6. Frasa | Tulis kalimat Thainya |

Bagian 2 adalah bagian yang paling penting dikerjakan dengan tangan: menulis
alasan nada ("kelas tinggi + suku kata mati + tanpa tanda → rendah") memaksa
Anda menjalankan aturannya, bukan sekadar menghafal bunyinya.

## Mengapa ditulis tangan

Menulis aksara Thai dengan tangan membantu membedakan huruf yang bentuknya
mirip, dan itu tidak terlatih lewat kartu di layar:

| Pasangan | Bedanya |
|:--|:--|
| ก / ถ / ภ | arah dan jumlah lengkungannya |
| ด / ค / ต | ada tidaknya gigi di ujung |
| ข / ช | arah lengkungan atasnya |
| บ / ป / ษ | tinggi batang dan ada tidaknya ekor |
| ฎ / ฏ | bentuk kaki di bawahnya |
| พ / ผ / ฟ / ฝ | ada tidaknya lingkaran kedua dan ekor |

Mulailah menulis dari **lingkaran kecilnya** (หัว, "kepala"), lalu teruskan
tanpa mengangkat pena. Huruf yang tidak punya lingkaran (ก, ธ, ฐ) ditulis dari
ujung kirinya.

## Hubungan dengan tahap

| Lembar | Tahap |
|:--|:--|
| ws-01, ws-02 | 1 |
| ws-03, ws-04 | 2 |
| ws-05, ws-06 | 3 |
| ws-07, ws-08 | 4 |
| ws-09, ws-10 | 5 |
| ws-11, ws-12 | 6 |

Kedua lembar pada satu tahap memuat butir yang berbeda, diambil selang-seling
dari materi tahap itu, sehingga tidak ada butir yang muncul dua kali.
