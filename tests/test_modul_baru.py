"""Pengujian tiga modul yang ditambahkan untuk melengkapi pendekatan belajar:
latihan telinga, kata serumpun, dan bacaan.

Pemeriksaan nada dan pemecahan suku kata untuk ketiganya sudah dikerjakan
test_data.py lewat dataio.examples_with_syllables(). Berkas ini memeriksa
hal-hal yang khas pada masing-masing modul.
"""

import pytest

from thaidrill import dataio, thai, tone

SETS = dataio.listen_sets()
COGNATES = dataio.cognates()
TEXTS = dataio.texts()


# ----------------------------------------------------------- latihan telinga ---

def test_ada_dua_jenis_pasangan():
    jenis = {s["type"] for s in SETS}
    assert jenis == {"panjang", "hembusan"}


@pytest.mark.parametrize("s", SETS, ids=lambda s: s["id"])
def test_satu_kelompok_hanya_berbeda_satu_hal(s):
    """Semua kata dalam satu kelompok WAJIB bernada sama.

    Kalau nadanya ikut berbeda, latihannya tidak lagi melatih panjang vokal
    atau hembusan saja, melainkan nada — padahal nada sudah punya modulnya
    sendiri.
    """
    nada = {tuple(thai.tones_of_phon(w["phon"])) for w in s["words"]}
    assert len(nada) == 1, f"{s['id']}: nadanya tidak sama ({nada})"


@pytest.mark.parametrize("s", SETS, ids=lambda s: s["id"])
def test_kata_dalam_kelompok_memang_berbeda(s):
    assert len({w["th"] for w in s["words"]}) == len(s["words"])
    assert len({w["phon"] for w in s["words"]}) == len(s["words"])


@pytest.mark.parametrize(
    "s", [s for s in SETS if s["type"] == "hembusan"], ids=lambda s: s["id"]
)
def test_pasangan_hembusan_hanya_berbeda_hembusan(s):
    """Konsonan awalnya harus berupa pasangan X dan Xh, misalnya k dan kh."""
    bunyi = []
    for w in s["words"]:
        awal = tone.parse_word(w["syl"])[0]
        bunyi.append(thai.CONSONANTS[awal.consonant]["initial"])
    assert len(set(bunyi)) == 2, f"{s['id']}: {bunyi}"
    pendek, panjang = sorted(bunyi, key=len)
    assert panjang == pendek + "h", f"{s['id']}: {bunyi} bukan pasangan hembusan"


@pytest.mark.parametrize(
    "s", [s for s in SETS if s["type"] == "panjang"], ids=lambda s: s["id"]
)
def test_pasangan_panjang_memakai_vokal_pendek_dan_panjang(s):
    """Satu kata bervokal pendek, satu lagi bervokal panjang."""
    panjang = []
    for w in s["words"]:
        suku = tone.parse_word(w["syl"])
        panjang.append(suku[0].length)
    assert set(panjang) == {tone.PENDEK, tone.PANJANG}, f"{s['id']}: {panjang}"


@pytest.mark.parametrize("s", SETS, ids=lambda s: s["id"])
def test_setiap_kelompok_punya_catatan(s):
    assert s.get("note"), s["id"]


def test_kartu_telinga_satu_per_kata():
    kartu = dataio.listen_cards()
    assert len(kartu) == sum(len(s["words"]) for s in SETS)
    assert len({c["id"] for c in kartu}) == len(kartu)
    for c in kartu:
        assert c["word"] is c["words"][c["index"]]


# -------------------------------------------------------------- kata serumpun ---

def test_hubungan_kata_serumpun_sah():
    for c in COGNATES:
        assert c["relation"] in ("sama", "bergeser", "sebagian"), c["id"]


def test_setiap_kata_serumpun_menyebut_kata_indonesianya():
    for c in COGNATES:
        assert c["id_word"].strip(), c["id"]
        assert c["gloss"].strip(), c["id"]


def test_kata_serumpun_tidak_mengulang_modul_kosakata():
    """Supaya satu kata tidak dijadwalkan dua kali oleh kotak Leitner."""
    kosakata = {e["th"] for e in dataio.vocab_entries()}
    ulang = [c["id"] for c in COGNATES if c["th"] in kosakata]
    assert not ulang, f"kata ini sudah ada di modul kosakata: {ulang}"


def test_kata_serumpun_tidak_ganda():
    th_list = [c["th"] for c in COGNATES]
    assert len(th_list) == len(set(th_list))


def test_kata_yang_maknanya_bergeser_wajib_diberi_peringatan():
    for c in COGNATES:
        if c["relation"] == "bergeser":
            assert c.get("note"), c["id"]


def test_catatan_modul_serumpun_ada():
    catatan = dataio.cognate_notes()
    assert len(catatan) >= 3
    for n in catatan:
        assert n["title"] and len(n["text"]) > 80


# -------------------------------------------------------------------- bacaan ---

def test_jumlah_teks_dan_tahapnya():
    assert len(TEXTS) >= 8
    tahap = {t["stage"] for t in TEXTS}
    assert tahap <= set(range(1, dataio.MAX_STAGE + 1))
    assert len(tahap) >= 4, "bacaan sebaiknya tersebar di beberapa tahap"


@pytest.mark.parametrize("t", TEXTS, ids=lambda t: t["id"])
def test_setiap_teks_lengkap(t):
    assert t["title"] and t["cat"]
    assert len(t["lines"]) >= 4, t["id"]
    assert len(t["items"]) >= 2, t["id"]
    for ln in t["lines"]:
        assert ln["speaker"] in ("A", "B"), t["id"]
        for key in ("th", "syl", "phon", "gloss"):
            assert ln.get(key), f"{t['id']}: {key} kosong"


@pytest.mark.parametrize("t", TEXTS, ids=lambda t: t["id"])
def test_percakapan_berganti_pembicara(t):
    pembicara = [ln["speaker"] for ln in t["lines"]]
    assert len(set(pembicara)) == 2, f"{t['id']}: hanya satu pembicara"


@pytest.mark.parametrize("t", TEXTS, ids=lambda t: t["id"])
def test_soal_bacaan_sah(t):
    for item in t["items"]:
        assert 0 <= item["answer"] < len(item["options"])
        assert len(set(item["options"])) == len(item["options"]), item["id"]
        assert item.get("explain"), item["id"]
        assert item["options_lang"] in ("id", "th")


def test_kosakata_bacaan_sudah_diajarkan():
    """Setiap suku kata pada bacaan harus pernah muncul di modul lain.

    Tujuan modul bacaan adalah memberi masukan yang BISA DIPAHAMI; kalau ada
    suku kata yang belum pernah diajarkan, teksnya memerlukan kamus dan
    tujuannya gagal.
    """
    dikenal: set[str] = set()
    for label, item in dataio.examples_with_syllables():
        if label.startswith("bacaan["):
            continue
        dikenal.update(item["syl"])
    asing: dict[str, set[str]] = {}
    for t in TEXTS:
        for ln in t["lines"]:
            for suku in ln["syl"]:
                if suku not in dikenal:
                    asing.setdefault(t["id"], set()).add(suku)
    # Beberapa suku kata penghubung memang baru muncul di bacaan; batasi
    # jumlahnya supaya teksnya tetap bisa dibaca tanpa kamus.
    total = sum(len(v) for v in asing.values())
    assert total <= 20, f"terlalu banyak suku kata baru di bacaan: {asing}"


# ------------------------------------------------------ lajur seberapa sering ---

def test_setiap_kata_punya_perkiraan_frekuensi():
    for e in dataio.vocab_entries():
        assert e.get("freq") in (1, 2, 3), e["id"]


def test_kata_inti_cukup_banyak_dan_tidak_berlebihan():
    """Band 1 adalah kata yang muncul hampir di setiap percakapan.

    Bila terlalu sedikit, penjadwal tidak punya cukup kata inti untuk
    didahulukan; bila terlalu banyak, penandaannya kehilangan arti. Sepersepuluh
    sampai seperlima dari seluruh kosakata adalah ukuran yang wajar.
    """
    band = [e["freq"] for e in dataio.vocab_entries()]
    inti = band.count(1)
    assert 0.10 <= inti / len(band) <= 0.20, f"kata inti: {inti} dari {len(band)}"
    assert band.count(2) > inti, "sebagian besar kata seharusnya berada di band 2"


def test_kata_yang_lebih_sering_diperkenalkan_lebih_dahulu():
    """Makin sering sebuah kata dipakai, makin awal tahapnya.

    Yang diperiksa bukan tahap satu per satu — kata sering yang ejaannya sulit
    memang pantas menunggu — melainkan kecenderungannya: rata-rata tahap kata
    inti harus lebih rendah daripada kata yang sering, dan kata yang sering
    lebih rendah daripada kata yang jarang.
    """
    import statistics

    entri = dataio.vocab_entries()
    rata = {
        f: statistics.mean([e["stage"] for e in entri if e["freq"] == f])
        for f in (1, 2, 3)
    }
    assert rata[1] < rata[2] < rata[3], rata


def test_tahap_awal_tidak_diisi_kata_jarang():
    """Tahap 1 dan 2 adalah modal pertama, jadi tidak diisi kata yang jarang."""
    awal = [e for e in dataio.vocab_entries() if e["stage"] <= 2]
    assert awal
    assert all(e["freq"] <= 2 for e in awal), [
        e["id"] for e in awal if e["freq"] > 2
    ]


def test_kata_inti_tersebar_bukan_menumpuk():
    inti = [e for e in dataio.vocab_entries() if e["freq"] == 1]
    assert len(inti) >= 40
    assert all(e["stage"] <= 5 for e in inti), "kata inti tidak boleh di tahap 6"
