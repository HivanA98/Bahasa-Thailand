"""Pengujian mesin aturan nada.

Yang diperiksa di sini adalah ATURANNYA, bukan datanya: tabel nada, pembacaan
suku kata, pola aksara nam, dan sederet kata yang nadanya dipatok dalam
pengujian. Kesesuaian data dengan mesin diuji di test_data.py.
"""

import pytest

from thaidrill import thai, tone


# ------------------------------------------------------------ tabel nada ---

@pytest.mark.parametrize(
    "cls,kind,length,nada",
    [
        (thai.MID, tone.HIDUP, tone.PANJANG, "sedang"),
        (thai.MID, tone.MATI, tone.PENDEK, "rendah"),
        (thai.MID, tone.MATI, tone.PANJANG, "rendah"),
        (thai.HIGH, tone.HIDUP, tone.PANJANG, "naik"),
        (thai.HIGH, tone.MATI, tone.PENDEK, "rendah"),
        (thai.HIGH, tone.MATI, tone.PANJANG, "rendah"),
        (thai.LOW, tone.HIDUP, tone.PANJANG, "sedang"),
        (thai.LOW, tone.MATI, tone.PENDEK, "tinggi"),
        (thai.LOW, tone.MATI, tone.PANJANG, "turun"),
    ],
)
def test_tabel_tanpa_tanda_nada(cls, kind, length, nada):
    assert tone.tone_from_parts(cls, kind, length, None) == nada


@pytest.mark.parametrize(
    "cls,mark,nada",
    [
        (thai.MID, thai.MAI_EK, "rendah"),
        (thai.HIGH, thai.MAI_EK, "rendah"),
        (thai.LOW, thai.MAI_EK, "turun"),
        (thai.MID, thai.MAI_THO, "turun"),
        (thai.HIGH, thai.MAI_THO, "turun"),
        (thai.LOW, thai.MAI_THO, "tinggi"),
        (thai.MID, thai.MAI_TRI, "tinggi"),
        (thai.MID, thai.MAI_CHATTAWA, "naik"),
    ],
)
def test_tabel_dengan_tanda_nada(cls, mark, nada):
    assert tone.tone_from_parts(cls, tone.HIDUP, tone.PANJANG, mark) == nada


def test_panjang_vokal_hanya_menentukan_pada_satu_keadaan():
    """Panjang vokal hanya mengubah nada pada suku kata mati kelas rendah."""
    beda = 0
    for cls in (thai.MID, thai.HIGH, thai.LOW):
        for kind in (tone.HIDUP, tone.MATI):
            a = tone.tone_from_parts(cls, kind, tone.PENDEK, None)
            b = tone.tone_from_parts(cls, kind, tone.PANJANG, None)
            if a != b:
                beda += 1
                assert (cls, kind) == (thai.LOW, tone.MATI)
    assert beda == 1


def test_kelas_tidak_dikenal_ditolak():
    with pytest.raises(ValueError):
        tone.tone_from_parts("sedang", tone.HIDUP, tone.PANJANG, None)


# --------------------------------------------------------- pembaca suku ---

PATOKAN = [
    # kata, nada yang diharapkan
    ("มา", "sedang"), ("ม้า", "tinggi"), ("หมา", "naik"),
    ("ขา", "naik"), ("ข่า", "rendah"), ("ข้า", "turun"),
    ("กา", "sedang"), ("นก", "tinggi"), ("คน", "sedang"),
    ("ไม่", "turun"), ("ไหม", "naik"), ("ครับ", "tinggi"),
    ("ค่ะ", "turun"), ("นะ", "tinggi"), ("ดี", "sedang"),
    ("สี", "naik"), ("สี่", "rendah"), ("ที่", "turun"),
    ("เสือ", "naik"), ("เรียน", "sedang"), ("เดือน", "sedang"),
    ("เดิน", "sedang"), ("เล็ก", "tinggi"), ("แข็ง", "naik"),
    ("ของ", "naik"), ("ขอบ", "rendah"), ("จาก", "rendah"),
    ("ปลา", "sedang"), ("เขา", "naik"), ("น้ำ", "tinggi"),
    ("ทำ", "sedang"), ("ใจ", "sedang"), ("อยู่", "rendah"),
    ("กิน", "sedang"), ("ผม", "naik"), ("ฉัน", "naik"),
    ("หก", "rendah"), ("เก้า", "turun"), ("สิบ", "rendah"),
    ("ห้า", "turun"), ("คืน", "sedang"), ("ดื่ม", "rendah"),
    ("กล้วย", "turun"), ("สวย", "naik"), ("โต๊ะ", "tinggi"),
    ("เดี๋ยว", "naik"), ("มาก", "turun"), ("ลูก", "turun"),
]


@pytest.mark.parametrize("kata,nada", PATOKAN)
def test_nada_kata_patokan(kata, nada):
    assert tone.tone_of_syllable(kata) == nada


def test_pola_tak_dikenal_melempar_galat():
    with pytest.raises(ValueError):
        tone.tone_of_syllable("xyz")


def test_konsonan_yang_tidak_bisa_jadi_akhir_tidak_dibaca_sebagai_akhir():
    # คห bukan suku kata: ห tidak pernah menjadi konsonan akhir.
    for s in tone.parse_syllable("คห"):
        assert s.final != "ห"


# ----------------------------------------------------------- ho nam & อย ---

def test_ho_nam_menaikkan_kelas():
    (s,) = tone.parse_syllable("หมา")
    assert s.cls == thai.HIGH
    assert s.consonant == "ห"
    assert s.tone == "naik"


def test_tanpa_ho_nam_kelasnya_rendah():
    (s,) = tone.parse_syllable("มา")
    assert s.cls == thai.LOW
    assert s.tone == "sedang"


def test_tr_dibaca_s_dan_berkelas_rendah():
    """ทร di awal suku kata dibaca s, bukan thr; kelasnya mengikuti ท."""
    (s,) = tone.parse_syllable("ทราบ")
    assert s.initial == tone.TR_DIGRAPH
    assert s.consonant == "ท"
    assert s.cls == thai.LOW
    assert s.tone == "turun"
    assert "dibaca s" in tone.explain(s)


def test_tr_tidak_mengubah_kata_lain_yang_berawalan_tho():
    # ท tanpa ร tetap dibaca th seperti biasa.
    (s,) = tone.parse_syllable("ทาน")
    assert s.initial == "ท"
    assert s.tone == "sedang"


def test_o_lead_berkelas_tengah():
    (s,) = tone.parse_syllable("อยู่")
    assert s.cls == thai.MID
    assert s.tone == "rendah"


def test_gugus_mengambil_kelas_huruf_pertama():
    (s,) = tone.parse_syllable("ปลา")
    assert s.initial == "ปล"
    assert s.consonant == "ป"
    assert s.cls == thai.MID


# -------------------------------------------------------------- aksara nam ---

AKSARA_NAM = [
    (["ข", "นม"], ["rendah", "naik"]),
    (["ต", "ลาด"], ["rendah", "rendah"]),
    (["ส", "นุก"], ["rendah", "rendah"]),
]


@pytest.mark.parametrize("syl,nada", AKSARA_NAM)
def test_aksara_nam_menularkan_kelas(syl, nada):
    assert [s.tone for s in tone.parse_word(syl)] == nada


def test_aksara_nam_tidak_berlaku_untuk_konsonan_tengah_sendiri():
    # บ sudah berkelas tengah, jadi ส tidak mengubah apa pun pada สบาย.
    hasil = tone.parse_word(["ส", "บาย"])
    assert hasil[1].cls == thai.MID
    assert hasil[1].tone == "sedang"


def test_suku_kata_sendiri_tidak_terkena_aturan_aksara_nam():
    # Dibaca satu per satu, นม bernada sedang; aturan baru berlaku di dalam kata.
    assert tone.tone_of_syllable("นม") == "sedang"
    assert tone.parse_word(["ข", "นม"])[1].tone == "naik"


# ------------------------------------------------------------ jenis suku ---

@pytest.mark.parametrize(
    "kata,jenis",
    [("มา", tone.HIDUP), ("จะ", tone.MATI), ("จาก", tone.MATI),
     ("คน", tone.HIDUP), ("น้ำ", tone.HIDUP), ("ไป", tone.HIDUP),
     ("เขา", tone.HIDUP), ("นก", tone.MATI)],
)
def test_jenis_suku_kata(kata, jenis):
    (s,) = [x for x in tone.parse_syllable(kata)][:1]
    assert s.kind == jenis


def test_vokal_pendek_berakhiran_nyaring_tetap_hidup():
    # ไ◌, ใ◌, เ◌า, dan ◌ำ pendek tetapi berakhir bunyi nyaring.
    for kata in ("ไป", "ใจ", "เขา", "ทำ"):
        for s in tone.parse_syllable(kata):
            assert s.kind == tone.HIDUP


# ---------------------------------------------------------------- pola ---

def test_setiap_pola_vokal_punya_templat_yang_bisa_dicocokkan():
    for vid, v in tone.VOWEL_PATTERNS.items():
        assert "{C}" in v["template"]
        assert "{T}" in v["template"]
        assert v["length"] in (tone.PENDEK, tone.PANJANG)
        assert v["has_final"] == ("{F}" in v["template"])


def test_id_pola_vokal_unik_dan_tampilannya_unik():
    tampilan = [v["display"] for v in tone.VOWEL_PATTERNS.values()]
    assert len(tampilan) == len(set(tampilan))


# -------------------------------------------------------------- explain ---

def test_explain_menyebut_kelas_jenis_dan_hasil():
    (s,) = tone.parse_syllable("นก")
    teks = tone.explain(s)
    assert "kelas rendah" in teks
    assert tone.MATI in teks
    assert "nada tinggi" in teks


def test_explain_menyebut_ho_nam():
    (s,) = tone.parse_syllable("หมา")
    assert "ห nam" in tone.explain(s)
