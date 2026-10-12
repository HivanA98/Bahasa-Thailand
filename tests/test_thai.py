"""Pengujian tabel aksara dan utilitas teks Thai."""

import unicodedata

import pytest

from thaidrill import thai


def test_jumlah_konsonan_44():
    assert len(thai.CONSONANTS) == 44


def test_jumlah_tiap_kelas():
    # Pembagian baku: 9 kelas tengah, 11 kelas tinggi, 24 kelas rendah.
    assert len(thai.MID_CONSONANTS) == 9
    assert len(thai.HIGH_CONSONANTS) == 11
    assert len(thai.LOW_CONSONANTS) == 24
    assert (
        len(thai.MID_CONSONANTS) + len(thai.HIGH_CONSONANTS) + len(thai.LOW_CONSONANTS)
        == 44
    )


def test_kelas_tengah_tepat_sembilan_huruf_itu():
    assert set(thai.MID_CONSONANTS) == set("กจฎฏดตบปอ")


def test_setiap_huruf_punya_keterangan_lengkap():
    for letter, info in thai.CONSONANTS.items():
        assert info["letter"] == letter
        assert info["name_th"].startswith(letter)
        assert info["name_rom"] and info["name_id"]
        assert info["class"] in (thai.MID, thai.HIGH, thai.LOW)
        assert info["initial"]
        assert isinstance(info["obsolete"], bool)


def test_bunyi_akhir_hanya_delapan_kemungkinan():
    sah = {"k", "ng", "t", "n", "p", "m", "y", "w", None}
    for info in thai.CONSONANTS.values():
        assert info["final"] in sah


def test_huruf_yang_tidak_pernah_jadi_konsonan_akhir():
    tanpa_akhir = {k for k, v in thai.CONSONANTS.items() if v["final"] is None}
    assert tanpa_akhir == set("ฉฌผฝหอฮ")


def test_dua_huruf_usang():
    usang = {k for k, v in thai.CONSONANTS.items() if v["obsolete"]}
    assert usang == set("ฃฅ")


def test_huruf_berada_dalam_blok_thai():
    for letter in thai.CONSONANTS:
        assert thai.THAI_RANGE[0] <= ord(letter) <= thai.THAI_RANGE[1]


def test_nama_huruf_dalam_bentuk_nfc():
    for info in thai.CONSONANTS.values():
        assert unicodedata.normalize("NFC", info["name_th"]) == info["name_th"]


def test_konsonan_nyaring_yang_bisa_dipimpin_ho_nam():
    # Hanya konsonan kelas rendah nyaring yang bisa dipimpin ห.
    for letter in thai.H_LEADABLE:
        assert thai.CLASS_OF[letter] == thai.LOW
        assert thai.CONSONANTS[letter]["final"] in ("ng", "n", "m", "y", "w")


def test_gugus_sejati_selalu_dua_huruf_konsonan():
    for gugus in thai.TRUE_CLUSTERS:
        assert len(gugus) == 2
        assert all(ch in thai.CONSONANTS for ch in gugus)


def test_is_thai():
    assert thai.is_thai("สวัสดี")
    assert thai.is_thai("ผม กิน ข้าว")
    assert not thai.is_thai("sawatdi")
    assert not thai.is_thai("สวัสดีA")


def test_strip_tone_marks():
    assert thai.strip_tone_marks("ม้า") == "มา"
    assert thai.strip_tone_marks("ไม่") == "ไม"
    assert thai.strip_tone_marks("มา") == "มา"


def test_tone_mark_of():
    assert thai.tone_mark_of("ม้า") == thai.MAI_THO
    assert thai.tone_mark_of("ไม่") == thai.MAI_EK
    assert thai.tone_mark_of("มา") is None


@pytest.mark.parametrize(
    "suku,nada",
    [
        ("maa", "sedang"),
        ("pàa", "rendah"),
        ("pâa", "turun"),
        ("máa", "tinggi"),
        ("mǎa", "naik"),
    ],
)
def test_nada_dari_lajur_phon(suku, nada):
    assert thai.tone_of_phon_syllable(suku) == nada


def test_pecah_suku_kata_phon_pada_tanda_hubung_dan_spasi():
    assert thai.syllables_of("sà-wàt-dii khráp") == ["sà", "wàt", "dii", "khráp"]
    assert thai.tones_of_phon("sà-wàt-dii khráp") == [
        "rendah", "rendah", "sedang", "tinggi"
    ]


def test_dua_tanda_nada_pada_satu_suku_kata_ditolak():
    with pytest.raises(ValueError):
        thai.tone_of_phon_syllable("mâáa")


def test_lima_nada_dan_namanya():
    assert len(thai.TONES) == 5
    assert set(thai.TONE_TH) == set(thai.TONES)
    assert set(thai.TONE_DIACRITIC) == set(thai.TONES)
    # Nada sedang tidak bertanda; empat lainnya bertanda dan semuanya berbeda.
    assert thai.TONE_DIACRITIC["sedang"] == ""
    bertanda = [v for v in thai.TONE_DIACRITIC.values() if v]
    assert len(set(bertanda)) == 4


def test_empat_tanda_nada():
    assert len(thai.TONE_MARKS) == 4
    assert len(set(thai.TONE_MARKS)) == 4
