"""Pengujian lembar kerja: kunci terpisah, bagian lengkap, isi dari data."""

import os
import re

import pytest
from conftest import ROOT, load_tool

from thaidrill import dataio, thai, tone

build_worksheets = load_tool("build_worksheets")

WS_DIR = os.path.join(ROOT, "worksheets")
ANS_DIR = os.path.join(WS_DIR, "answers")
NOMOR = list(range(1, 13))


def baca(path: str) -> str:
    return open(path, encoding="utf-8").read()


def lembar(no: int) -> str:
    return baca(os.path.join(WS_DIR, f"ws-{no:02d}.md"))


def kunci(no: int) -> str:
    return baca(os.path.join(ANS_DIR, f"ws-{no:02d}-kunci.md"))


def test_dua_belas_lembar_dan_dua_belas_kunci():
    # README.md di folder yang sama bukan lembar kerja, jadi tidak ikut dihitung.
    lembar_ada = [f for f in os.listdir(WS_DIR) if re.fullmatch(r"ws-\d\d\.md", f)]
    kunci_ada = [f for f in os.listdir(ANS_DIR) if re.fullmatch(r"ws-\d\d-kunci\.md", f)]
    assert sorted(lembar_ada) == [f"ws-{n:02d}.md" for n in NOMOR]
    assert sorted(kunci_ada) == [f"ws-{n:02d}-kunci.md" for n in NOMOR]


@pytest.mark.parametrize("no", NOMOR)
def test_lembar_mutakhir(no):
    stage = (no - 1) // 2 + 1
    part = (no - 1) % 2
    isi_lembar, isi_kunci = build_worksheets.build_sheet(no, stage, part)
    assert lembar(no) == isi_lembar, (
        f"ws-{no:02d}.md tertinggal. Jalankan: python tools/build_worksheets.py"
    )
    assert kunci(no) == isi_kunci, (
        f"kunci ws-{no:02d} tertinggal. Jalankan: python tools/build_worksheets.py"
    )


@pytest.mark.parametrize("no", NOMOR)
def test_bagian_wajib_ada(no):
    isi = lembar(no)
    for judul in ("## 1. Huruf", "## 2. Nada", "## 3. Arti kata",
                  "## 4. Tulis kata Thai"):
        assert judul in isi, f"ws-{no:02d}: {judul} hilang"


@pytest.mark.parametrize("no", NOMOR)
def test_lembar_menunjuk_berkas_kuncinya(no):
    assert f"worksheets/answers/ws-{no:02d}-kunci.md" in lembar(no)


@pytest.mark.parametrize("no", NOMOR)
def test_lembar_kerja_tidak_memuat_jawabannya(no):
    """Bagian 'tulis kata Thai' tidak boleh memuat tulisan Thainya.

    Yang diperiksa: baris tabel pada bagian 4 hanya berisi artinya, dan
    kolom jawabannya kosong.
    """
    isi = lembar(no)
    bagian = isi.split("## 4. Tulis kata Thai")[1].split("##")[0]
    for baris in bagian.splitlines():
        if not baris.startswith("|") or baris.startswith("|:"):
            continue
        if baris.startswith("| Arti"):
            continue
        sel = [s.strip() for s in baris.strip("|").split("|")]
        assert sel[1] == "" and sel[2] == "", f"ws-{no:02d}: jawaban terlihat"
        assert not thai.is_thai(sel[0]) or not sel[0]


@pytest.mark.parametrize("no", NOMOR)
def test_kunci_memuat_jawaban_yang_sebenarnya(no):
    isi = kunci(no)
    bagian = isi.split("## 4. Tulis kata Thai")[1].split("##")[0]
    baris_isi = [b for b in bagian.splitlines()
                 if b.startswith("|") and not b.startswith("|:")
                 and not b.startswith("| Arti")]
    assert baris_isi
    for b in baris_isi:
        sel = [s.strip() for s in b.strip("|").split("|")]
        assert thai.is_thai(sel[1]), f"ws-{no:02d}: kolom Thai kosong"
        assert sel[2]


@pytest.mark.parametrize("no", NOMOR)
def test_kunci_nada_sesuai_mesin(no):
    """Setiap nada pada kunci dihitung ulang dari ejaannya."""
    oleh_th = {s["th"]: s for s in dataio.tone_syllables()}
    bagian = kunci(no).split("## 2. Nada")[1].split("##")[0]
    diperiksa = 0
    for baris in bagian.splitlines():
        if not baris.startswith("|") or baris.startswith("|:") or baris.startswith("| Kata"):
            continue
        sel = [s.strip() for s in baris.strip("|").split("|")]
        s = oleh_th.get(sel[0])
        assert s, f"ws-{no:02d}: {sel[0]} bukan dari data"
        benar = " - ".join(x.tone for x in tone.parse_word(s["syl"]))
        assert sel[1] == benar, f"ws-{no:02d}: {sel[0]} ditulis {sel[1]}"
        diperiksa += 1
    assert diperiksa > 0


@pytest.mark.parametrize("no", NOMOR)
def test_butir_arti_kata_berasal_dari_data(no):
    oleh_th = {e["th"]: e for e in dataio.vocab_entries()}
    bagian = lembar(no).split("## 3. Arti kata")[1].split("##")[0]
    diperiksa = 0
    for baris in bagian.splitlines():
        if not baris.startswith("|") or baris.startswith("|:") or baris.startswith("| Kata"):
            continue
        sel = [s.strip() for s in baris.strip("|").split("|")]
        e = oleh_th.get(sel[0])
        assert e, f"ws-{no:02d}: {sel[0]} bukan dari data"
        assert sel[1] == e["phon"]
        diperiksa += 1
    assert diperiksa > 0


@pytest.mark.parametrize("no", NOMOR)
def test_kunci_huruf_sesuai_tabel_konsonan(no):
    bagian = kunci(no).split("## 1. Huruf")[1].split("##")[0]
    diperiksa = 0
    for baris in bagian.splitlines():
        if not baris.startswith("|") or baris.startswith("|:") or baris.startswith("| Huruf"):
            continue
        sel = [s.strip() for s in baris.strip("|").split("|")]
        info = thai.CONSONANTS[sel[0]]
        assert sel[1] == info["class"]
        assert sel[2] == info["initial"]
        diperiksa += 1
    assert diperiksa > 0


def test_setiap_tahap_punya_dua_lembar():
    for no in NOMOR:
        stage = (no - 1) // 2 + 1
        assert f"tahap {stage}" in lembar(no)


def test_kunci_tidak_disalin_ke_lembar_kerja():
    """Tidak ada berkas kunci yang isinya sama dengan lembar kerjanya."""
    for no in NOMOR:
        assert lembar(no) != kunci(no)
        assert "Kunci jawaban" in kunci(no)
        assert not re.search(r"^# Kunci", lembar(no), flags=re.M)
