"""Pengujian kunci jawaban: satu jawaban benar, tanpa pilihan ganda identik.

Soal yang dibuat otomatis (kelas konsonan dan nada kata) diperiksa terhadap
thaidrill/thai.py dan thaidrill/tone.py, bukan terhadap daftar jawaban yang
ditulis tangan, sehingga kuncinya tidak bisa menyimpang dari aturannya.
"""

import random

import pytest

from thaidrill import dataio, questions, thai, tone

RNG_SEED = 99

SOAL_TULISAN_TANGAN = (
    dataio.aksara_items() + dataio.nada_items() + dataio.grammar_items()
)


@pytest.mark.parametrize("item", SOAL_TULISAN_TANGAN, ids=lambda i: i["id"])
def test_soal_tulisan_tangan_punya_jawaban_yang_sah(item):
    assert 0 <= item["answer"] < len(item["options"]), item["id"]


@pytest.mark.parametrize("item", SOAL_TULISAN_TANGAN, ids=lambda i: i["id"])
def test_pilihan_jawaban_tidak_ada_yang_kembar(item):
    assert len(set(item["options"])) == len(item["options"]), item["id"]


@pytest.mark.parametrize("item", SOAL_TULISAN_TANGAN, ids=lambda i: i["id"])
def test_jumlah_pilihan_antara_dua_dan_lima(item):
    assert 2 <= len(item["options"]) <= 5, item["id"]


@pytest.mark.parametrize("item", SOAL_TULISAN_TANGAN, ids=lambda i: i["id"])
def test_bahasa_pilihan_sah_dan_sesuai_isinya(item):
    assert item["options_lang"] in ("id", "th"), item["id"]
    if item["options_lang"] == "th":
        for o in item["options"]:
            assert thai.is_thai(o), f"{item['id']}: pilihan {o!r} bukan tulisan Thai"


@pytest.mark.parametrize("item", SOAL_TULISAN_TANGAN, ids=lambda i: i["id"])
def test_setiap_soal_punya_penjelasan(item):
    assert item.get("explain"), item["id"]


def test_setiap_soal_tata_bahasa_menunjuk_topiknya():
    for i in dataio.grammar_items():
        assert i["id"].startswith(i["topic_id"])


# --------------------------------------------------- soal buatan otomatis ---

def test_kunci_soal_kelas_konsonan_diambil_dari_tabel():
    rng = random.Random(RNG_SEED)
    for c in dataio.consonants():
        q = questions.consonant_class_question(c, rng)
        assert q.options[q.answer] == thai.CLASS_OF[c["letter"]]
        assert set(q.options) == {thai.MID, thai.HIGH, thai.LOW}


def test_kunci_soal_nada_kata_dihitung_dari_ejaannya():
    rng = random.Random(RNG_SEED)
    for s in dataio.tone_syllables():
        q = questions.syllable_tone_question(s, rng)
        dihitung = " - ".join(x.tone for x in tone.parse_word(s["syl"]))
        assert q.options[q.answer] == dihitung, s["id"]
        # Lafal pada data juga harus sejalan dengan kunci itu.
        assert " - ".join(thai.tones_of_phon(s["phon"])) == dihitung, s["id"]


def test_pengecoh_soal_nada_tidak_ikut_benar():
    rng = random.Random(RNG_SEED)
    for s in dataio.tone_syllables():
        q = questions.syllable_tone_question(s, rng)
        benar = q.options[q.answer]
        assert q.options.count(benar) == 1, s["id"]


def test_kunci_soal_aturan_nada_dihitung_mesin():
    rng = random.Random(RNG_SEED)
    for r in dataio.tone_rules():
        q = questions.tone_rule_question(r, rng)
        assert q.options[q.answer] == r["tone"], r["id"]
        assert len(set(q.options)) == len(q.options)


def test_soal_angka_punya_satu_jawaban_benar():
    rng = random.Random(RNG_SEED)
    for d in dataio.digits():
        q = questions.digit_question(d, rng)
        assert q.options[q.answer] == str(d["value"])
        assert len(set(q.options)) == len(q.options)


# ------------------------------------------- kosakata: Indonesia ke Thai ---

def test_pengecoh_kosakata_tidak_pernah_ikut_benar():
    """Pengecoh tidak boleh menerima arti yang ditanyakan sebagai jawabannya.

    Tanpa saringan ini, soal 'kata Thai untuk sakit' bisa memuat เจ็บ dan ป่วย
    sekaligus, sehingga ada dua jawaban benar.
    """
    rng = random.Random(RNG_SEED)
    pool = dataio.vocab_entries()
    oleh_th = {e["th"]: e for e in pool}
    for e in pool:
        q = questions.vocab_id_to_th(e, pool, rng)
        kunci = questions.normalize(e["gloss"])
        for i, opt in enumerate(q.options):
            if i == q.answer:
                continue
            lain = oleh_th.get(opt)
            if lain is None:
                continue
            assert kunci not in questions.accepted_set(lain), (
                f"{e['id']}: pengecoh {opt} juga berarti '{e['gloss']}'"
            )


def test_jawaban_kosakata_adalah_kata_itu_sendiri():
    rng = random.Random(RNG_SEED)
    pool = dataio.vocab_entries()
    for e in pool:
        q = questions.vocab_id_to_th(e, pool, rng)
        assert q.options[q.answer] == e["th"]


def test_semua_pilihan_kosakata_tertulis_dalam_aksara_thai():
    rng = random.Random(RNG_SEED)
    pool = dataio.vocab_entries()
    for e in pool[:40]:
        q = questions.vocab_id_to_th(e, pool, rng)
        for o in q.options:
            assert thai.is_thai(o)


# -------------------------------------------------- jawaban yang ditulis ---

def test_jawaban_bertaip_menerima_arti_utama_dan_arti_lain():
    for e in dataio.vocab_entries():
        q = questions.vocab_th_to_id(e)
        assert q.is_correct_text(e["gloss"]), e["id"]
        for a in e["alt"]:
            assert q.is_correct_text(a), f"{e['id']}: {a}"


def test_jawaban_bertaip_menerima_satu_bagian_arti_bertanda_koma():
    q = questions.vocab_th_to_id(
        {"id": "x", "th": "ถูก", "phon": "thùuk", "rom": "thuk",
         "gloss": "murah; benar", "alt": [], "pos": "sifat", "cls": None,
         "stage": 1, "cat": "sifat",
         "example": {"th": "ถูก", "phon": "thùuk", "gloss": "murah"}}
    )
    assert q.is_correct_text("murah")
    assert q.is_correct_text("benar")
    assert q.is_correct_text("MURAH ")
    assert not q.is_correct_text("mahal")


def test_normalisasi_jawaban_mengabaikan_huruf_besar_dan_tanda_baca():
    assert questions.normalize("Tidak apa-apa!") == questions.normalize("tidak apa apa")


def test_pengembangan_arti_memecah_pada_tanda_koma_dan_titik_koma():
    hasil = questions.expand_accepted("besar, luas; agung", ["raya"])
    for kata in ("besar", "luas", "agung", "raya"):
        assert kata in hasil


# --------------------------------------------------------- semua mode ---

@pytest.mark.parametrize("mode", questions.MODES)
def test_setiap_mode_menghasilkan_soal_yang_sah(mode):
    rng = random.Random(RNG_SEED)
    pool = questions.build_pool(mode, None, rng)
    assert pool, mode
    for q in pool:
        assert q.card_id
        assert q.question
        assert q.kind in ("mcq", "typed", "selfcheck")
        if q.kind == "mcq":
            assert q.options and q.answer is not None
            assert 0 <= q.answer < len(q.options)
            assert len(set(q.options)) == len(q.options)
        if q.kind == "typed":
            assert q.accepted
        if q.kind == "selfcheck":
            assert q.reveal


@pytest.mark.parametrize("mode", questions.MODES)
def test_batas_tahap_tidak_memuat_materi_lebih_tinggi(mode):
    rng = random.Random(RNG_SEED)
    for stage in range(1, dataio.MAX_STAGE + 1):
        for q in questions.build_pool(mode, stage, rng):
            if q.stage is not None:
                assert q.stage <= stage, f"{mode}: {q.card_id} tahap {q.stage}"


def test_mode_yang_tidak_dikenal_ditolak():
    with pytest.raises(ValueError):
        questions.build_pool("tidak-ada", None, random.Random(1))
