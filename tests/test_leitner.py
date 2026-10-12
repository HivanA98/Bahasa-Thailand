"""Pengujian kotak Leitner, jadwal jatuh tempo, dan berkas progres."""

import datetime as dt
import json
import os

from thaidrill.leitner import (
    INTERVALS,
    MAX_BOX,
    MIN_BOX,
    CardState,
    Progress,
)

HARI_INI = dt.date(2026, 1, 1)


def test_kartu_baru_mulai_di_kotak_satu_dan_jatuh_tempo():
    st = CardState()
    assert st.box == MIN_BOX
    assert st.is_due()


def test_jawaban_benar_menaikkan_satu_kotak():
    st = CardState(due="2026-01-01")
    st.answer(True, HARI_INI)
    assert st.box == 2
    assert st.correct == 1 and st.seen == 1


def test_jawaban_salah_mengembalikan_ke_kotak_satu():
    st = CardState(box=4, due="2026-01-01")
    st.answer(False, HARI_INI)
    assert st.box == MIN_BOX
    assert st.wrong == 1


def test_kotak_tidak_melewati_batas_atas():
    st = CardState(box=MAX_BOX)
    st.answer(True, HARI_INI)
    assert st.box == MAX_BOX


def test_jeda_setiap_kotak_sesuai_tabel():
    for box in range(MIN_BOX, MAX_BOX + 1):
        st = CardState(box=box - 1 if box > MIN_BOX else MIN_BOX)
        st.box = box - 1 if box > MIN_BOX else MIN_BOX
        st.answer(True, HARI_INI)
        if box > MIN_BOX:
            diharapkan = HARI_INI + dt.timedelta(days=INTERVALS[box])
            assert st.due == diharapkan.isoformat(), box


def test_tabel_jeda_sama_dengan_yang_didokumentasikan():
    assert INTERVALS == {1: 0, 2: 1, 3: 3, 4: 7, 5: 16}


def test_kartu_belum_jatuh_tempo_tidak_dianggap_jatuh_tempo():
    st = CardState(box=3, due="2026-01-05")
    assert not st.is_due(HARI_INI)
    assert st.is_due(dt.date(2026, 1, 5))


def test_simpan_dan_muat_ulang(tmp_path):
    path = str(tmp_path / "progress.json")
    p = Progress()
    p.record_answer("v001", True, HARI_INI)
    p.record_answer("v002", False, HARI_INI)
    p.log_session({"tanggal": "2026-01-01", "soal": 2})
    p.save(path)

    q = Progress.load(path)
    assert q.state("v001").box == 2
    assert q.state("v002").box == 1
    assert q.sessions[-1]["soal"] == 2


def test_muat_berkas_yang_belum_ada_menghasilkan_progres_kosong(tmp_path):
    p = Progress.load(str(tmp_path / "belum-ada.json"))
    assert p.cards == {}


def test_berkas_rusak_tidak_menggagalkan_pemuatan(tmp_path):
    path = tmp_path / "rusak.json"
    path.write_text("{ ini bukan json", encoding="utf-8")
    p = Progress.load(str(path))
    assert p.cards == {}


def test_berkas_berisi_senarai_tidak_menggagalkan_pemuatan(tmp_path):
    path = tmp_path / "salah-bentuk.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")
    assert Progress.load(str(path)).cards == {}


def test_kartu_dengan_kotak_di_luar_batas_diperbaiki(tmp_path):
    path = tmp_path / "aneh.json"
    path.write_text(json.dumps({
        "version": 1, "cards": {"v001": {"box": 99, "due": "2026-01-01"}}
    }), encoding="utf-8")
    p = Progress.load(str(path))
    assert p.state("v001").box == MAX_BOX


def test_penulisan_atomik_tidak_meninggalkan_berkas_sementara(tmp_path):
    path = str(tmp_path / "progress.json")
    p = Progress()
    p.record_answer("v001", True, HARI_INI)
    p.save(path)
    sisa = [f for f in os.listdir(tmp_path) if f.endswith(".tmp")]
    assert not sisa


def test_berkas_progres_ditulis_sebagai_json_utf8(tmp_path):
    path = str(tmp_path / "progress.json")
    p = Progress()
    p.record_answer("kon-ก", True, HARI_INI)
    p.save(path)
    isi = json.loads(open(path, encoding="utf-8").read())
    assert "kon-ก" in isi["cards"]


def test_hitung_kotak():
    p = Progress()
    p.record_answer("a", True, HARI_INI)
    p.record_answer("b", True, HARI_INI)
    p.record_answer("c", False, HARI_INI)
    counts = p.box_counts(["a", "b", "c"])
    assert counts[1] == 1 and counts[2] == 2


def test_daftar_kartu_baru_dan_jatuh_tempo():
    p = Progress()
    p.record_answer("a", True, HARI_INI)   # naik ke kotak 2, jatuh tempo besok
    assert p.new_ids(["a", "b"]) == ["b"]
    assert p.due_ids(["a"], HARI_INI) == []
    assert p.due_ids(["a"], HARI_INI + dt.timedelta(days=1)) == ["a"]


def test_sesi_yang_disimpan_dibatasi_200_terakhir(tmp_path):
    path = str(tmp_path / "progress.json")
    p = Progress()
    for i in range(250):
        p.log_session({"tanggal": "2026-01-01", "soal": i})
    p.save(path)
    q = Progress.load(path)
    assert len(q.sessions) == 200
    assert q.sessions[-1]["soal"] == 249
