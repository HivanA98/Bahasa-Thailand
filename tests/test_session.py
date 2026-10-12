"""Pengujian penyusun sesi: batas materi baru, ulangan, dan interleaving."""

import datetime as dt

from thaidrill import dataio
from thaidrill.leitner import Progress
from thaidrill.session import (
    GROUP_WEIGHTS,
    MODE_GROUPS,
    NEW_SHARE,
    plan_session,
    upcoming_counts,
)

HARI_INI = dt.date(2026, 1, 1)


def test_sesi_pertama_memperkenalkan_kartu_baru():
    plan = plan_session(Progress(), seed=1, on=HARI_INI)
    assert plan.questions
    assert plan.n_new > 0


def test_batas_kartu_baru_dipatuhi():
    for n in (0, 3, 8, 15):
        plan = plan_session(Progress(), new_per_session=n, seed=1, on=HARI_INI)
        if n == 0:
            assert plan.n_new == 0
            assert not plan.questions, "tanpa kartu baru dan tanpa ulangan, sesi kosong"
        else:
            # Jatah dibulatkan ke atas per kelompok materi, jadi jumlahnya bisa
            # sedikit melebihi n, tetapi tidak boleh berlipat.
            assert 0 < plan.n_new <= n + len(GROUP_WEIGHTS)


def test_kartu_baru_masuk_menurut_urutan_tahap():
    plan = plan_session(Progress(), new_per_session=6, seed=3, on=HARI_INI)
    tahap = [q.stage for q in plan.questions if q.stage is not None]
    assert tahap and max(tahap) <= 2, "sesi pertama seharusnya materi tahap awal"


def test_kartu_yang_belum_jatuh_tempo_tidak_muncul():
    p = Progress()
    ids = dataio.all_card_ids()
    for cid in ids:
        p.record_answer(cid, True, HARI_INI)      # semua naik ke kotak 2
    plan = plan_session(p, new_per_session=0, seed=1, on=HARI_INI)
    assert plan.questions == []
    besok = HARI_INI + dt.timedelta(days=1)
    plan = plan_session(p, new_per_session=0, seed=1, on=besok)
    assert plan.questions, "kotak 2 jatuh tempo sehari kemudian"


def test_ulangan_tidak_tergeser_habis_oleh_materi_baru():
    p = Progress()
    # 60 kartu lama yang semuanya jatuh tempo hari ini.
    for cid in dataio.all_card_ids()[:60]:
        p.record_answer(cid, False, HARI_INI)
    plan = plan_session(p, new_per_session=40, limit=30, seed=2, on=HARI_INI)
    baru = sum(1 for q in plan.questions if p.is_new(q.card_id))
    assert baru <= int(30 * NEW_SHARE) + 1
    assert len(plan.questions) - baru > 0


def test_interleaving_mencampur_mode():
    plan = plan_session(Progress(), new_per_session=12, seed=5, on=HARI_INI)
    modes = [q.mode for q in plan.questions]
    assert len(set(modes)) >= 3, "sesi campuran seharusnya memuat beberapa mode"
    # Tidak boleh ada blok panjang dari satu mode yang sama.
    terpanjang = 1
    berjalan = 1
    for a, b in zip(modes, modes[1:]):
        berjalan = berjalan + 1 if a == b else 1
        terpanjang = max(terpanjang, berjalan)
    assert terpanjang <= 6


def test_satu_kata_baru_dilatih_dua_arah():
    plan = plan_session(
        Progress(), modes=["kosakata-th", "kosakata-id"], new_per_session=4,
        seed=4, on=HARI_INI,
    )
    per_kartu = {}
    for q in plan.questions:
        per_kartu.setdefault(q.card_id, set()).add(q.mode)
    assert any(len(v) == 2 for v in per_kartu.values())


def test_sesi_dapat_diulang_dengan_seed_sama():
    a = plan_session(Progress(), seed=11, on=HARI_INI)
    b = plan_session(Progress(), seed=11, on=HARI_INI)
    assert [q.card_id for q in a.questions] == [q.card_id for q in b.questions]
    assert [q.question for q in a.questions] == [q.question for q in b.questions]


def test_seed_berbeda_menghasilkan_susunan_berbeda():
    a = plan_session(Progress(), seed=11, on=HARI_INI)
    b = plan_session(Progress(), seed=12, on=HARI_INI)
    assert [q.card_id for q in a.questions] != [q.card_id for q in b.questions]


def test_batas_jumlah_soal_dipatuhi():
    plan = plan_session(Progress(), limit=12, new_per_session=20, seed=1, on=HARI_INI)
    assert len(plan.questions) <= 12


def test_lintasan_kedua_tidak_menambah_kartu_baru():
    plan = plan_session(Progress(), new_per_session=4, limit=40, seed=6, on=HARI_INI)
    ulangan = [q for q in plan.questions if q.repeat]
    if ulangan:
        kartu_baru = {q.card_id for q in plan.questions if not q.repeat}
        for q in ulangan:
            assert q.card_id in kartu_baru


def test_batas_tahap_pada_sesi():
    plan = plan_session(Progress(), stage=1, new_per_session=10, seed=7, on=HARI_INI)
    for q in plan.questions:
        if q.stage is not None:
            assert q.stage <= 1


def test_setiap_mode_punya_kelompok_dan_bobot():
    from thaidrill.questions import MODES
    for m in MODES:
        assert m in MODE_GROUPS
        assert MODE_GROUPS[m] in GROUP_WEIGHTS


def test_ringkasan_jumlah_kartu():
    p = Progress()
    ids = dataio.all_card_ids()[:10]
    p.record_answer(ids[0], True, HARI_INI)
    hitung = upcoming_counts(p, ids, HARI_INI)
    assert hitung["baru"] == 9
    assert hitung["jatuh_tempo"] == 0
    assert hitung["belum_jatuh_tempo"] == 1
    assert sum(hitung.values()) == len(ids)


def test_mode_tunggal_menghasilkan_soal_mode_itu_saja():
    plan = plan_session(Progress(), modes=["nada"], new_per_session=5, seed=8,
                        on=HARI_INI)
    assert plan.questions
    assert {q.mode for q in plan.questions} == {"nada"}
