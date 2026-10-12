"""Pengujian bahwa semua hasil ekspor mutakhir terhadap data.

Berkas di data/csv/, anki/, worksheets/, dan webdata.js adalah turunan. Bila
data/*.json berubah tetapi ekspornya belum dibuat ulang, pengujian di sini
gagal, dan itu memang tujuannya.
"""

import csv
import io
import json
import os
import re

import pytest
from conftest import ROOT, load_tool

from thaidrill import dataio

build_exports = load_tool("build_exports")
build_web = load_tool("build_web")
build_worksheets = load_tool("build_worksheets")


# ------------------------------------------------------------- webdata.js ---

def _webdata() -> dict:
    teks = open(os.path.join(ROOT, "webdata.js"), encoding="utf-8").read()
    body = teks[teks.index("const THAI_DATA = ") + len("const THAI_DATA = "):]
    return json.loads(body.rstrip().rstrip(";"))


def test_webdata_mutakhir():
    diharapkan = build_web.render(build_web.build())
    sekarang = open(os.path.join(ROOT, "webdata.js"), encoding="utf-8").read()
    assert sekarang == diharapkan, (
        "webdata.js tertinggal dari data/. Jalankan: python tools/build_web.py"
    )


def test_webdata_hanya_ascii():
    """Teks Thai ditulis sebagai escape, supaya tidak bergantung charset peladen."""
    isi = open(os.path.join(ROOT, "webdata.js"), encoding="utf-8").read()
    assert isi.isascii()


def test_webdata_memuat_semua_modul():
    d = _webdata()
    for kunci in ("aksara", "nada", "kosakata", "tatabahasa", "frasa", "topik", "info"):
        assert kunci in d and d[kunci], kunci


def test_jumlah_kartu_web_sama_dengan_data():
    d = _webdata()
    assert len(d["kosakata"]) == len(dataio.vocab_entries())
    assert len(d["frasa"]) == len(dataio.phrases())
    assert len(d["tatabahasa"]) == len(dataio.grammar_items())
    assert len(d["topik"]) == len(dataio.grammar_topics())


def test_id_kartu_web_unik_per_modul():
    d = _webdata()
    for modul in ("aksara", "nada", "kosakata", "tatabahasa", "frasa"):
        ids = [x["id"] for x in d[modul]]
        assert len(ids) == len(set(ids)), modul


def test_kunci_soal_web_sama_dengan_data():
    """Kunci soal tata bahasa di webdata.js harus sama dengan di data/."""
    d = _webdata()
    oleh_id = {i["id"]: i for i in dataio.grammar_items()}
    for kartu in d["tatabahasa"]:
        asli = oleh_id[kartu["id"]]
        assert kartu["options"] == asli["options"]
        assert kartu["answer"] == asli["answer"]


def test_kunci_soal_nada_web_sesuai_mesin():
    from thaidrill import tone
    d = _webdata()
    oleh_id = {s["id"]: s for s in dataio.tone_syllables()}
    for kartu in d["nada"]:
        if kartu["cat"] != "suku":
            continue
        s = oleh_id[kartu["id"]]
        benar = " - ".join(x.tone for x in tone.parse_word(s["syl"]))
        assert kartu["options"][kartu["answer"]] == benar, kartu["id"]


def test_setiap_kartu_web_punya_tahap_dan_kategori():
    d = _webdata()
    for modul in ("aksara", "nada", "kosakata", "tatabahasa", "frasa"):
        for kartu in d[modul]:
            assert 1 <= kartu["stage"] <= dataio.MAX_STAGE, kartu["id"]
            assert kartu["cat"] and kartu["catLabel"], kartu["id"]
            assert kartu["kind"] in ("flip", "mcq"), kartu["id"]


def test_kartu_mcq_web_lengkap():
    d = _webdata()
    for modul in ("aksara", "nada", "tatabahasa"):
        for kartu in d[modul]:
            if kartu["kind"] != "mcq":
                continue
            assert kartu["options"], kartu["id"]
            assert 0 <= kartu["answer"] < len(kartu["options"]), kartu["id"]
            assert kartu["optionsLang"] in ("id", "th"), kartu["id"]


def test_kartu_konsonan_membawa_soal_kelasnya():
    d = _webdata()
    konsonan = [k for k in d["aksara"] if k["cat"] == "konsonan"]
    assert len(konsonan) == 44
    for k in konsonan:
        assert k["quiz"]["options"][k["quiz"]["answer"]] in (
            "tengah", "tinggi", "rendah"
        )


def test_bangunan_web_dapat_diulang_persis():
    """Pengecoh diacak dengan seed tetap, jadi dua bangunan harus sama."""
    assert build_web.render(build_web.build()) == build_web.render(build_web.build())


# --------------------------------------------------------------- aplikasi ---

def _tanpa_komentar(kode: str) -> str:
    kode = re.sub(r"/\*.*?\*/", "", kode, flags=re.S)
    return re.sub(r"^\s*//.*$", "", kode, flags=re.M)


def test_aplikasi_web_tidak_memakai_fetch():
    """Data dimuat lewat tag <script> supaya index.html jalan dari file://."""
    app = _tanpa_komentar(open(os.path.join(ROOT, "app.js"), encoding="utf-8").read())
    assert "fetch(" not in app
    assert "XMLHttpRequest" not in app
    assert "import(" not in app


def test_index_memuat_webdata_sebelum_app():
    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    assert html.index("webdata.js") < html.index("app.js")


def test_jeda_leitner_di_app_sama_dengan_di_python():
    from thaidrill.leitner import INTERVALS
    app = open(os.path.join(ROOT, "app.js"), encoding="utf-8").read()
    m = re.search(r"BOX_DAYS = \{([^}]*)\}", app)
    assert m
    angka = [int(x) for x in re.findall(r":\s*(\d+)", m.group(1))]
    assert angka == [INTERVALS[b] for b in sorted(INTERVALS)]


def test_sakelar_di_html_dipakai_app():
    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    app = open(os.path.join(ROOT, "app.js"), encoding="utf-8").read()
    for sakelar in re.findall(r'id="(tg-[a-z]+)"', html):
        assert f'#{sakelar}' in app, f"{sakelar} ada di HTML tetapi tidak dipakai app.js"


# -------------------------------------------------------------------- CSV ---

@pytest.mark.parametrize("nama", sorted(build_exports.CSV_FILES))
def test_csv_mutakhir(nama):
    header, fn = build_exports.CSV_FILES[nama]
    path = os.path.join(ROOT, "data", "csv", nama)
    assert os.path.exists(path), f"{nama} belum dibuat"
    with open(path, encoding="utf-8", newline="") as f:
        baris = list(csv.reader(f))
    assert baris[0] == header, nama
    diharapkan = [[str(x) for x in r] for r in fn()]
    assert baris[1:] == diharapkan, (
        f"{nama} tertinggal dari data/. Jalankan: python tools/build_exports.py"
    )


@pytest.mark.parametrize("nama", sorted(build_exports.ANKI_FILES))
def test_anki_mutakhir(nama):
    fn, tags_col = build_exports.ANKI_FILES[nama]
    path = os.path.join(ROOT, "anki", nama)
    assert os.path.exists(path), f"{nama} belum dibuat"
    isi = open(path, encoding="utf-8", newline="").read()
    pengarah, _, sisa = isi.partition("#tags column:")
    assert isi.startswith("#separator:Comma\n#html:false\n#tags column:")
    assert sisa.startswith(str(tags_col))
    baris = list(csv.reader(io.StringIO(isi.split("\n", 3)[3])))
    diharapkan = [[str(x) for x in r] for r in fn()]
    assert baris == diharapkan, (
        f"anki/{nama} tertinggal dari data/. Jalankan: python tools/build_exports.py"
    )


@pytest.mark.parametrize("nama", sorted(build_exports.ANKI_FILES))
def test_kolom_tag_anki_menunjuk_kolom_terakhir(nama):
    fn, tags_col = build_exports.ANKI_FILES[nama]
    rows = fn()
    assert rows
    for r in rows:
        assert len(r) == tags_col, nama
        assert r[-1].startswith("thai "), nama


def test_csv_dan_anki_memuat_semua_entri_kosakata():
    assert len(build_exports.kosakata_rows()) == len(dataio.vocab_entries())
    assert len(build_exports.anki_kosakata()) == len(dataio.vocab_entries())
