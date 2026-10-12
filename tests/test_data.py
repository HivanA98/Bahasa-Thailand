"""Pengujian kesesuaian data dengan mesin aturan nada.

Inilah pengujian terpenting di proyek ini. Untuk SETIAP kata dan kalimat
contoh di seluruh data, dua hal diperiksa:

1. gabungan pemecahan suku kata ('syl') sama persis dengan tulisan Thainya;
2. nada setiap suku kata yang dihitung thaidrill/tone.py dari ejaannya sama
   dengan nada yang ditulis pada lajur lafal ('phon').

Dengan begitu, lafal yang dicantumkan tidak bisa menyimpang dari aturan nada
yang diajarkan Modul 2. Yang TIDAK diperiksa: apakah vokal dan konsonannya
dialihhurufkan dengan benar, dan apakah arti bahasa Indonesianya tepat. Lihat
data/NEEDS_REVIEW.md.
"""

import pytest

from thaidrill import dataio, thai, tone

CONTOH = dataio.examples_with_syllables()
IDS = [label for label, _ in CONTOH]


def test_ada_banyak_contoh_yang_diperiksa():
    assert len(CONTOH) > 400


@pytest.mark.parametrize("label,item", CONTOH, ids=IDS)
def test_gabungan_suku_kata_sama_dengan_tulisannya(label, item):
    if not item.get("check_syl", True):
        assert item.get("check_why"), f"{label}: pengecualian wajib punya alasan"
        return
    # Tulisan Thai tidak memakai spasi antarkata, tetapi spasi dipakai untuk
    # memisahkan klausa. Spasi itu tidak termasuk suku kata, jadi diabaikan.
    assert "".join(item["syl"]) == item["th"].replace(" ", ""), label


@pytest.mark.parametrize("label,item", CONTOH, ids=IDS)
def test_nada_sesuai_hitungan_mesin(label, item):
    if not item.get("check_tone", True):
        assert item.get("check_why"), f"{label}: pengecualian wajib punya alasan"
        return
    dihitung = [s.tone for s in tone.parse_word(item["syl"])]
    ditulis = thai.tones_of_phon(item["phon"])
    assert dihitung == ditulis, (
        f"{label}: {item['th']} ditulis {item['phon']} (nada {ditulis}) "
        f"tetapi ejaannya memberi nada {dihitung}"
    )


@pytest.mark.parametrize("label,item", CONTOH, ids=IDS)
def test_tulisan_thai_hanya_memakai_karakter_thai(label, item):
    assert thai.is_thai(item["th"]), label


@pytest.mark.parametrize("label,item", CONTOH, ids=IDS)
def test_setiap_suku_kata_terbaca(label, item):
    for s in item["syl"]:
        assert tone.parse_syllable(s), f"{label}: suku kata {s!r} tidak terbaca"


# ------------------------------------------- baris aturan nada di data/ ---

def test_baris_aturan_tanpa_tanda_sesuai_mesin():
    baris = dataio.load("nada")["rules_no_mark"]
    assert len(baris) == 9, "sembilan gabungan kelas x jenis suku kata x panjang"
    for r in baris:
        assert tone.tone_from_parts(r["cls"], r["kind"], r["length"], None) == r["tone"]


def test_baris_aturan_bertanda_sesuai_mesin():
    for r in dataio.load("nada")["rules_mark"]:
        hasil = tone.tone_from_parts(r["cls"], tone.HIDUP, tone.PANJANG, r["mark"])
        assert hasil == r["tone"], r["id"]


def test_contoh_pada_baris_aturan_memang_bernada_itu():
    for r in dataio.tone_rules():
        ex = r["example"]
        nada = [s.tone for s in tone.parse_word(ex["syl"])]
        assert nada == [r["tone"]], f"{r['id']}: {ex['th']}"


def test_setiap_nada_punya_kartu_dan_contohnya_bernada_itu():
    kunci = []
    for t in dataio.tones():
        ex = t["example"]
        assert thai.tones_of_phon(ex["phon"]) == [t["key"]], t["id"]
        kunci.append(t["key"])
    assert set(kunci) == set(thai.TONES)


def test_pasangan_nada_benar_benar_berbeda_nada():
    for mp in dataio.minimal_pairs():
        nada = [tuple(thai.tones_of_phon(w["phon"])) for w in mp["words"]]
        assert len(set(nada)) == len(nada), f"{mp['id']}: ada dua kata bernada sama"


def test_pasangan_nada_rangka_hurufnya_sama():
    """Kata dalam satu pasangan hanya boleh berbeda tanda nada, bukan huruf.

    Kecuali bila perbedaannya memang dicatat pada keterangannya, seperti ห nam
    pada หมา dan pilihan ไ/ใ pada ไกล/ใกล้.
    """
    for mp in dataio.minimal_pairs():
        rangka = {thai.strip_tone_marks(w["th"]) for w in mp["words"]}
        if len(rangka) > 1:
            assert mp.get("note"), (
                f"{mp['id']}: ejaannya berbeda lebih dari tanda nada, "
                "tetapi tidak ada catatan yang menjelaskannya"
            )


# ------------------------------------------------- pola vokal di data/ ---

def test_id_pola_vokal_dikenali_mesin():
    for v in dataio.vowels():
        assert v["vowel_id"] in tone.VOWEL_PATTERNS, v["vowel_id"]


def test_tampilan_pola_vokal_sama_dengan_yang_di_mesin():
    for v in dataio.vowels():
        assert v["display"] == tone.VOWEL_PATTERNS[v["vowel_id"]]["display"]


def test_pasangan_pendek_panjang_saling_menunjuk():
    oleh_id = {v["vowel_id"]: v for v in dataio.vowels()}
    for v in dataio.vowels():
        pair = v["pair"]
        if not pair:
            continue
        assert pair in tone.VOWEL_PATTERNS
        if pair in oleh_id:
            assert oleh_id[pair]["pair"] == v["vowel_id"], v["vowel_id"]
            panjang = {
                tone.VOWEL_PATTERNS[v["vowel_id"]]["length"],
                tone.VOWEL_PATTERNS[pair]["length"],
            }
            assert panjang == {tone.PENDEK, tone.PANJANG}


def test_pola_vokal_tanpa_contoh_wajib_punya_catatan():
    for v in dataio.vowels():
        if v.get("example") is None:
            assert v.get("note"), v["vowel_id"]


# ------------------------------------------------ konsonan di data/ ---

def test_data_aksara_memuat_tepat_44_konsonan_sekali_masing_masing():
    huruf = [c["letter"] for c in dataio.load("aksara")["consonants"]]
    assert len(huruf) == 44
    assert len(set(huruf)) == 44
    assert set(huruf) == set(thai.CONSONANTS)


def test_catatan_konsonan_tidak_kosong():
    for c in dataio.consonants():
        assert c["note"].strip(), c["letter"]


def test_huruf_usang_disebut_tidak_dipakai_pada_catatannya():
    for c in dataio.consonants():
        if c["obsolete"]:
            assert "TIDAK DIPAKAI" in c["note"], c["letter"]
