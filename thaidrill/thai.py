"""Tabel aksara Thai, kelas konsonan, dan utilitas teks.

Modul ini memuat satu-satunya salinan tabel 44 konsonan beserta kelasnya
(kelas tengah, tinggi, rendah). Kelas konsonan menentukan nada, jadi tabel ini
dipakai oleh tone.py, oleh pembuat soal, dan oleh pengujian otomatis.

Skema alih huruf yang dipakai proyek ini:

* `rom`  — alih huruf RTGS (Royal Thai General System), yaitu tulisan Latin
  yang Anda lihat di papan nama jalan dan peta di Thailand. RTGS **tidak**
  menuliskan nada dan tidak membedakan vokal panjang/pendek.
* `phon` — lafal untuk pembelajar: suku kata dipisah tanda hubung, nada
  ditulis sebagai tanda di atas vokal pertama suku kata itu.

      tanpa tanda   nada sedang   (สามัญ)   kha
      a + grave     nada rendah   (เอก)     khà
      a + sirkum    nada turun    (โท)      khâ
      a + akut      nada tinggi   (ตรี)     khá
      a + karon     nada naik     (จัตวา)   khǎ

Dua lajur itu sengaja dipisah: `rom` berguna untuk membaca papan nama,
`phon` berguna untuk melafalkan. Keduanya bukan pengganti tulisan Thai.
"""

from __future__ import annotations

import unicodedata

# --------------------------------------------------------------- karakter ---

#: Rentang Unicode blok Thai.
THAI_RANGE = (0x0E00, 0x0E7F)

#: Tanda nada: mai ek, mai tho, mai tri, mai chattawa.
TONE_MARKS = ("่", "้", "๊", "๋")
MAI_EK, MAI_THO, MAI_TRI, MAI_CHATTAWA = TONE_MARKS

#: Tanda lain yang menempel di atas atau di bawah konsonan.
THANTHAKHAT = "์"   # penanda huruf mati (karan)
MAITAIKHU = "็"     # pemendek vokal e / ae
NIKHAHIT = "ํ"
PHINTHU = "ฺ"

#: Tanda vokal yang ditulis di atas atau di bawah konsonan.
UPPER_VOWELS = "ัิีึืํ"
LOWER_VOWELS = "ฺุู"
#: Vokal yang ditulis sebelum konsonan.
LEADING_VOWELS = "เแโใไ"
#: Vokal yang ditulis sesudah konsonan.
TRAILING_VOWELS = "ะาำๅ"

MARKS = set(TONE_MARKS) | set(UPPER_VOWELS) | set(LOWER_VOWELS) | {THANTHAKHAT, MAITAIKHU}

PUNCT = ".,!?;:๏๚๛ "

#: Angka Thai 0-9.
DIGITS = "๐๑๒๓๔๕๖๗๘๙"

# ---------------------------------------------------------------- konsonan ---

MID, HIGH, LOW = "tengah", "tinggi", "rendah"

#: (huruf, nama Thai, nama Latin, arti nama dalam bahasa Indonesia, kelas,
#:  bunyi awal, bunyi akhir, sudah tidak dipakai)
_CONSONANT_ROWS = [
    ("ก", "ก ไก่", "ko kai", "ayam", MID, "k", "k", False),
    ("ข", "ข ไข่", "kho khai", "telur", HIGH, "kh", "k", False),
    ("ฃ", "ฃ ขวด", "kho khuat", "botol", HIGH, "kh", "k", True),
    ("ค", "ค ควาย", "kho khwai", "kerbau", LOW, "kh", "k", False),
    ("ฅ", "ฅ คน", "kho khon", "orang", LOW, "kh", "k", True),
    ("ฆ", "ฆ ระฆัง", "kho ra-khang", "lonceng besar", LOW, "kh", "k", False),
    ("ง", "ง งู", "ngo ngu", "ular", LOW, "ng", "ng", False),
    ("จ", "จ จาน", "cho chan", "piring", MID, "ch", "t", False),
    ("ฉ", "ฉ ฉิ่ง", "cho ching", "kerincing logam", HIGH, "ch", None, False),
    ("ช", "ช ช้าง", "cho chang", "gajah", LOW, "ch", "t", False),
    ("ซ", "ซ โซ่", "so so", "rantai", LOW, "s", "t", False),
    ("ฌ", "ฌ เฌอ", "cho choe", "pohon", LOW, "ch", None, False),
    ("ญ", "ญ หญิง", "yo ying", "perempuan", LOW, "y", "n", False),
    ("ฎ", "ฎ ชฎา", "do cha-da", "mahkota penari", MID, "d", "t", False),
    ("ฏ", "ฏ ปฏัก", "to pa-tak", "tombak penggiring", MID, "t", "t", False),
    ("ฐ", "ฐ ฐาน", "tho than", "alas, dasar", HIGH, "th", "t", False),
    ("ฑ", "ฑ มณโฑ", "tho montho", "Montho (nama tokoh)", LOW, "th", "t", False),
    ("ฒ", "ฒ ผู้เฒ่า", "tho phu-thao", "orang tua", LOW, "th", "t", False),
    ("ณ", "ณ เณร", "no nen", "biksu muda", LOW, "n", "n", False),
    ("ด", "ด เด็ก", "do dek", "anak", MID, "d", "t", False),
    ("ต", "ต เต่า", "to tao", "kura-kura", MID, "t", "t", False),
    ("ถ", "ถ ถุง", "tho thung", "kantong", HIGH, "th", "t", False),
    ("ท", "ท ทหาร", "tho thahan", "tentara", LOW, "th", "t", False),
    ("ธ", "ธ ธง", "tho thong", "bendera", LOW, "th", "t", False),
    ("น", "น หนู", "no nu", "tikus", LOW, "n", "n", False),
    ("บ", "บ ใบไม้", "bo baimai", "daun", MID, "b", "p", False),
    ("ป", "ป ปลา", "po pla", "ikan", MID, "p", "p", False),
    ("ผ", "ผ ผึ้ง", "pho phueng", "lebah", HIGH, "ph", None, False),
    ("ฝ", "ฝ ฝา", "fo fa", "tutup", HIGH, "f", None, False),
    ("พ", "พ พาน", "pho phan", "baki bertangkai", LOW, "ph", "p", False),
    ("ฟ", "ฟ ฟัน", "fo fan", "gigi", LOW, "f", "p", False),
    ("ภ", "ภ สำเภา", "pho sam-phao", "perahu jung", LOW, "ph", "p", False),
    ("ม", "ม ม้า", "mo ma", "kuda", LOW, "m", "m", False),
    ("ย", "ย ยักษ์", "yo yak", "raksasa", LOW, "y", "y", False),
    ("ร", "ร เรือ", "ro ruea", "perahu", LOW, "r", "n", False),
    ("ล", "ล ลิง", "lo ling", "kera", LOW, "l", "n", False),
    ("ว", "ว แหวน", "wo waen", "cincin", LOW, "w", "w", False),
    ("ศ", "ศ ศาลา", "so sala", "balai", HIGH, "s", "t", False),
    ("ษ", "ษ ฤษี", "so rue-si", "pertapa", HIGH, "s", "t", False),
    ("ส", "ส เสือ", "so suea", "harimau", HIGH, "s", "t", False),
    ("ห", "ห หีบ", "ho hip", "peti", HIGH, "h", None, False),
    ("ฬ", "ฬ จุฬา", "lo chu-la", "layang-layang chula", LOW, "l", "n", False),
    ("อ", "อ อ่าง", "o ang", "baskom", MID, "-", None, False),
    ("ฮ", "ฮ นกฮูก", "ho nok-huk", "burung hantu", LOW, "h", None, False),
]

CONSONANTS: dict[str, dict] = {
    row[0]: {
        "letter": row[0],
        "name_th": row[1],
        "name_rom": row[2],
        "name_id": row[3],
        "class": row[4],
        "initial": row[5],
        "final": row[6],
        "obsolete": row[7],
    }
    for row in _CONSONANT_ROWS
}

CLASS_OF = {k: v["class"] for k, v in CONSONANTS.items()}
MID_CONSONANTS = tuple(k for k, v in CONSONANTS.items() if v["class"] == MID)
HIGH_CONSONANTS = tuple(k for k, v in CONSONANTS.items() if v["class"] == HIGH)
LOW_CONSONANTS = tuple(k for k, v in CONSONANTS.items() if v["class"] == LOW)

#: Konsonan akhir dikelompokkan menurut bunyinya. Bunyi ng, n, m, y, w nyaring
#: (sonoran) sehingga suku katanya hidup; bunyi k, t, p menutup suku kata
#: sehingga suku katanya mati.
SONORANT_FINALS = tuple(
    k for k, v in CONSONANTS.items() if v["final"] in ("ng", "n", "m", "y", "w")
)
STOP_FINALS = tuple(k for k, v in CONSONANTS.items() if v["final"] in ("k", "t", "p"))

#: Gugus konsonan sejati: kedua huruf dibunyikan, kelas diambil dari huruf
#: pertama.
TRUE_CLUSTERS = (
    "กร", "กล", "กว", "ขร", "ขล", "ขว", "คร", "คล", "คว",
    "ตร", "ปร", "ปล", "พร", "พล", "ผล",
)

#: ห di depan konsonan kelas rendah tidak dibunyikan; fungsinya menaikkan
#: kelas konsonan berikutnya menjadi kelas tinggi, supaya kata itu bisa
#: bernada naik atau bernada rendah.
H_LEADABLE = ("ง", "ญ", "ณ", "น", "ม", "ย", "ร", "ล", "ว")

#: อย ada pada empat kata saja (อย่า อยู่ อย่าง อยาก) dan berkelas tengah.
O_LEAD = "อย"

# -------------------------------------------------------------------- nada ---

#: Kunci nada dipakai di seluruh proyek.
TONES = ("sedang", "rendah", "turun", "tinggi", "naik")

TONE_TH = {
    "sedang": "เสียงสามัญ",
    "rendah": "เสียงเอก",
    "turun": "เสียงโท",
    "tinggi": "เสียงตรี",
    "naik": "เสียงจัตวา",
}

#: Tanda diakritik pada lajur `phon` untuk setiap nada.
TONE_DIACRITIC = {
    "sedang": "",
    "rendah": "̀",
    "turun": "̂",
    "tinggi": "́",
    "naik": "̌",
}
DIACRITIC_TONE = {v: k for k, v in TONE_DIACRITIC.items() if v}

# -------------------------------------------------------------- utilitas ---


def is_thai(text: str) -> bool:
    """True bila seluruh karakter berada di blok Thai (tanda baca diabaikan)."""
    return all(
        THAI_RANGE[0] <= ord(ch) <= THAI_RANGE[1]
        for ch in text
        if ch not in PUNCT
    )


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def strip_tone_marks(text: str) -> str:
    """Buang tanda nada; sisanya dibiarkan utuh."""
    return "".join(ch for ch in text if ch not in TONE_MARKS)


def tone_mark_of(syllable: str) -> str | None:
    """Tanda nada pada satu suku kata, atau None bila tidak ada."""
    for ch in syllable:
        if ch in TONE_MARKS:
            return ch
    return None


def syllables_of(phon: str) -> list[str]:
    """Pecah lajur `phon` menjadi suku kata.

    Di dalam satu kata, suku kata dipisah tanda hubung; antarkata dipisah
    spasi. Keduanya sama-sama batas suku kata, sehingga kalimat contoh dapat
    diperiksa dengan cara yang sama seperti kata tunggal.
    """
    return [s for s in phon.replace("-", " ").split() if s]


def tone_of_phon_syllable(syllable: str) -> str:
    """Nada satu suku kata `phon`, dibaca dari diakritiknya."""
    decomposed = unicodedata.normalize("NFD", syllable)
    found = [DIACRITIC_TONE[ch] for ch in decomposed if ch in DIACRITIC_TONE]
    if len(found) > 1:
        raise ValueError(f"lebih dari satu tanda nada pada suku kata: {syllable!r}")
    return found[0] if found else "sedang"


def tones_of_phon(phon: str) -> list[str]:
    """Daftar nada per suku kata dari lajur `phon`."""
    return [tone_of_phon_syllable(s) for s in syllables_of(phon)]


def consonant_rows(include_obsolete: bool = True) -> list[dict]:
    return [
        dict(v) for v in CONSONANTS.values()
        if include_obsolete or not v["obsolete"]
    ]


__all__ = [
    "CLASS_OF", "CONSONANTS", "DIACRITIC_TONE", "DIGITS", "HIGH", "HIGH_CONSONANTS",
    "H_LEADABLE", "LEADING_VOWELS", "LOW", "LOWER_VOWELS", "LOW_CONSONANTS",
    "MAITAIKHU", "MAI_CHATTAWA", "MAI_EK", "MAI_THO", "MAI_TRI", "MARKS", "MID",
    "MID_CONSONANTS", "O_LEAD", "PUNCT", "SONORANT_FINALS", "STOP_FINALS",
    "THAI_RANGE", "THANTHAKHAT", "TONES", "TONE_DIACRITIC", "TONE_MARKS", "TONE_TH",
    "TRAILING_VOWELS", "TRUE_CLUSTERS", "UPPER_VOWELS", "consonant_rows", "is_thai",
    "nfc", "strip_tone_marks", "syllables_of", "tone_mark_of", "tone_of_phon_syllable",
    "tones_of_phon",
]
