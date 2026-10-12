"""Pengujian bentuk data: id, tahap, kelas kata, dan kelengkapan field."""

import re
from collections import Counter

import pytest

from thaidrill import dataio


def test_semua_id_kartu_unik_di_seluruh_modul():
    ids = dataio.all_card_ids()
    ganda = [i for i, n in Counter(ids).items() if n > 1]
    assert not ganda, f"id kartu ganda: {ganda}"


def test_jumlah_kartu_masuk_akal():
    assert len(dataio.all_card_ids()) > 400


@pytest.mark.parametrize(
    "items,pola",
    [
        (dataio.vocab_entries(), r"^v\d{3}$"),
        (dataio.phrases(), r"^f\d{2}$"),
        (dataio.tone_syllables(), r"^s\d{2}$"),
        (dataio.minimal_pairs(), r"^mp\d{2}$"),
        (dataio.tones(), r"^t\d$"),
        (dataio.marks(), r"^m\d{2}$"),
        (dataio.aksara_items(), r"^a-q\d{2}$"),
        (dataio.nada_items(), r"^n-q\d{2}$"),
        (dataio.grammar_topics(), r"^g\d{2}$"),
        (dataio.grammar_items(), r"^g\d{2}-\d$"),
    ],
)
def test_format_id(items, pola):
    for i in items:
        assert re.match(pola, i["id"]), i["id"]


def test_tahap_selalu_antara_1_dan_6():
    for item in (
        dataio.consonants() + dataio.vowels() + dataio.marks() + dataio.digits()
        + dataio.aksara_items() + dataio.tones() + dataio.tone_syllables()
        + dataio.minimal_pairs() + dataio.nada_items() + dataio.vocab_entries()
        + dataio.grammar_items() + dataio.phrases()
    ):
        assert 1 <= item["stage"] <= dataio.MAX_STAGE, item.get("id")


def test_setiap_tahap_terisi_pada_tiap_modul():
    for nama, items in (
        ("aksara", dataio.consonants() + dataio.vowels()),
        ("kosakata", dataio.vocab_entries()),
        ("tatabahasa", dataio.grammar_items()),
        ("frasa", dataio.phrases()),
    ):
        tahap = {i["stage"] for i in items}
        assert tahap == set(range(1, dataio.MAX_STAGE + 1)), f"{nama}: {sorted(tahap)}"


def test_kelas_kata_kosakata_sah():
    for e in dataio.vocab_entries():
        assert e["pos"] in dataio.POS_VALUES, f"{e['id']}: {e['pos']}"


def test_field_wajib_kosakata_terisi():
    for e in dataio.vocab_entries():
        for key in ("th", "syl", "rom", "phon", "gloss", "pos", "cat"):
            assert e.get(key), f"{e['id']}: {key} kosong"
        assert isinstance(e["alt"], list)
        assert isinstance(e["syl"], list) and e["syl"]
        assert "cls" in e, e["id"]


def test_contoh_kosakata_lengkap():
    for e in dataio.vocab_entries():
        ex = e["example"]
        for key in ("th", "syl", "phon", "gloss"):
            assert ex.get(key), f"{e['id']}.example: {key} kosong"


def test_arti_tidak_sama_dengan_tulisan_thainya():
    for e in dataio.vocab_entries():
        assert e["gloss"] != e["th"]
        assert e["gloss"] != e["phon"]


def test_arti_lain_tidak_mengulang_arti_utama():
    for e in dataio.vocab_entries():
        assert e["gloss"] not in e["alt"], e["id"]


def test_klasifikator_yang_dipakai_tertulis_dalam_aksara_thai():
    from thaidrill import thai
    for e in dataio.vocab_entries():
        if e.get("cls"):
            assert thai.is_thai(e["cls"]), f"{e['id']}: {e['cls']}"


def test_frasa_lengkap():
    for p in dataio.phrases():
        for key in ("th", "syl", "rom", "phon", "gloss", "cat"):
            assert p.get(key), f"{p['id']}: {key} kosong"
        assert "lit" in p, p["id"]


def test_dua_belas_topik_tata_bahasa():
    topik = dataio.grammar_topics()
    assert len(topik) == 12
    assert [t["id"] for t in topik] == [f"g{i:02d}" for i in range(1, 13)]


def test_setiap_topik_punya_penjelasan_catatan_contoh_dan_soal():
    for t in dataio.grammar_topics():
        assert len(t["explanation"]) > 200, t["id"]
        assert len(t["caveats"]) >= 2, t["id"]
        assert len(t["examples"]) >= 2, t["id"]
        assert len(t["items"]) == 5, t["id"]


def test_lima_nada_dan_sembilan_aturan():
    assert len(dataio.tones()) == 5
    assert len(dataio.load("nada")["rules_no_mark"]) == 9
    assert len(dataio.load("nada")["rules_mark"]) == 8


def test_tanda_pada_modul_aksara_tertulis_dalam_aksara_thai():
    from thaidrill import thai
    for m in dataio.marks():
        assert thai.is_thai(m["mark"]), m["id"]
        assert m["name_th"] and m["name_rom"]


def test_sepuluh_angka_thai_berurutan():
    angka = dataio.digits()
    assert [d["value"] for d in angka] == list(range(10))
    from thaidrill import thai
    assert "".join(d["digit"] for d in angka) == thai.DIGITS


def test_tidak_ada_field_null_yang_seharusnya_terisi():
    for e in dataio.vocab_entries():
        for key, nilai in e.items():
            if key in ("cls", "note", "check_why"):
                continue
            assert nilai is not None, f"{e['id']}: {key} bernilai null"


def test_setiap_pengecualian_pemeriksaan_punya_alasan():
    """Entri yang mematikan pemeriksaan mesin wajib menjelaskan sebabnya."""
    for label, item in dataio.examples_with_syllables():
        if not item.get("check_syl", True) or not item.get("check_tone", True):
            assert item.get("check_why"), label
