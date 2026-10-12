"""Pemuat data dan pengenal kartu.

Satu-satunya sumber data adalah berkas JSON di folder data/. Berkas di
data/csv/, anki/, worksheets/, dan webdata.js adalah hasil ekspor yang dibuat
ulang oleh skrip di tools/, bukan sumber yang disunting langsung.

Fakta bahasa yang bersifat aturan (tabel 44 konsonan dan kelasnya, pola vokal,
tabel nada) TIDAK disimpan di data/, melainkan di thaidrill/thai.py dan
thaidrill/tone.py. Berkas data/aksara.json hanya menunjuk kepada tabel itu
lewat huruf dan id polanya, supaya tidak ada dua sumber yang bisa berselisih.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache

from . import thai

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "data")

MODULE_FILES = {
    "aksara": "aksara.json",
    "nada": "nada.json",
    "vocab": "vocab.json",
    "grammar": "grammar.json",
    "frasa": "frasa.json",
}

MAX_STAGE = 6

POS_VALUES = {
    "sapaan", "ungkapan", "partikel", "ganti", "tunjuk", "tanya", "angka",
    "nomina", "verba", "sifat", "keterangan", "klasifikator", "depan", "sambung",
}

#: Awalan pengenal kartu untuk butir yang tidak memiliki id sendiri di dalam
#: datanya (konsonan, vokal, angka). Dipakai konsisten oleh quiz.py, aplikasi
#: web, dan semua ekspor.
ID_KONSONAN = "kon-"
ID_VOKAL = "vok-"
ID_ANGKA = "num-"


def _read_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=None)
def load(name: str) -> dict:
    """Muat satu modul data ('aksara', 'nada', 'vocab', 'grammar', 'frasa')."""
    if name not in MODULE_FILES:
        raise KeyError(f"modul tidak dikenal: {name}")
    return _read_json(os.path.join(DATA_DIR, MODULE_FILES[name]))


def load_all() -> dict[str, dict]:
    return {name: load(name) for name in MODULE_FILES}


def _upto(items: list[dict], stage: int | None) -> list[dict]:
    if stage is None:
        return list(items)
    return [i for i in items if i["stage"] <= stage]


# ------------------------------------------------------------ modul aksara ---

def consonants(stage: int | None = None) -> list[dict]:
    """Konsonan beserta keterangan lengkapnya.

    Huruf, tahap, dan catatan diambil dari data/aksara.json; nama, kelas, dan
    bunyinya digabungkan dari thai.CONSONANTS.
    """
    out = []
    for c in _upto(load("aksara")["consonants"], stage):
        info = thai.CONSONANTS[c["letter"]]
        out.append({**info, "stage": c["stage"], "note": c.get("note") or "",
                    "id": ID_KONSONAN + c["letter"]})
    return out


def vowels(stage: int | None = None) -> list[dict]:
    return [{**v, "id": ID_VOKAL + v["id"], "vowel_id": v["id"]}
            for v in _upto(load("aksara")["vowels"], stage)]


def marks(stage: int | None = None) -> list[dict]:
    return _upto(load("aksara")["marks"], stage)


def digits(stage: int | None = None) -> list[dict]:
    return [{**d, "id": ID_ANGKA + str(d["value"])}
            for d in _upto(load("aksara")["digits"], stage)]


def aksara_items(stage: int | None = None) -> list[dict]:
    return _upto(load("aksara")["items"], stage)


# -------------------------------------------------------------- modul nada ---

def tones(stage: int | None = None) -> list[dict]:
    return _upto(load("nada")["tones"], stage)


def tone_rules() -> list[dict]:
    """Sembilan baris aturan tanpa tanda nada, lalu baris bertanda nada."""
    d = load("nada")
    return list(d["rules_no_mark"]) + list(d["rules_mark"])


def tone_syllables(stage: int | None = None) -> list[dict]:
    return _upto(load("nada")["syllables"], stage)


def minimal_pairs(stage: int | None = None) -> list[dict]:
    return _upto(load("nada")["minimal_pairs"], stage)


def nada_items(stage: int | None = None) -> list[dict]:
    return _upto(load("nada")["items"], stage)


# ---------------------------------------------------------- modul kosakata ---

def vocab_entries(stage: int | None = None) -> list[dict]:
    return _upto(load("vocab")["entries"], stage)


# -------------------------------------------------------- modul tata bahasa ---

def grammar_topics(stage: int | None = None) -> list[dict]:
    return _upto(load("grammar")["topics"], stage)


def grammar_items(stage: int | None = None) -> list[dict]:
    out: list[dict] = []
    for topic in grammar_topics(stage):
        for item in topic["items"]:
            out.append({**item, "topic_id": topic["id"],
                        "topic_title": topic["title"], "stage": topic["stage"]})
    return out


# -------------------------------------------------------------- modul frasa ---

def phrases(stage: int | None = None) -> list[dict]:
    return _upto(load("frasa")["phrases"], stage)


# ---------------------------------------------------------------- gabungan ---

def all_card_ids() -> list[str]:
    """Semua id yang dipakai sebagai kartu Leitner, dari seluruh modul."""
    ids: list[str] = []
    ids += [c["id"] for c in consonants()]
    ids += [v["id"] for v in vowels()]
    ids += [m["id"] for m in marks()]
    ids += [d["id"] for d in digits()]
    ids += [i["id"] for i in aksara_items()]
    ids += [t["id"] for t in tones()]
    ids += [s["id"] for s in tone_syllables()]
    ids += [p["id"] for p in minimal_pairs()]
    ids += [i["id"] for i in nada_items()]
    ids += [e["id"] for e in vocab_entries()]
    ids += [i["id"] for i in grammar_items()]
    ids += [p["id"] for p in phrases()]
    return ids


def examples_with_syllables() -> list[tuple[str, dict]]:
    """Setiap butir data yang memuat ejaan Thai beserta pemecahan suku katanya.

    Dipakai pengujian otomatis untuk memeriksa bahwa nada pada lajur `phon`
    sama dengan nada yang dihitung thaidrill/tone.py. Nilai yang dikembalikan
    adalah pasangan (label, butir), dan setiap butir memuat kunci 'syl' dan
    'phon'.
    """
    out: list[tuple[str, dict]] = []

    def add(label: str, item: dict | None) -> None:
        if item and item.get("syl") and item.get("phon"):
            out.append((label, item))

    for v in load("aksara")["vowels"]:
        add(f"aksara.vowels[{v['id']}].example", v.get("example"))
    for m in load("aksara")["marks"]:
        add(f"aksara.marks[{m['id']}].example", m.get("example"))
    for d in load("aksara")["digits"]:
        add(f"aksara.digits[{d['value']}]", d)
    for t in load("nada")["tones"]:
        add(f"nada.tones[{t['id']}].example", t.get("example"))
    for r in tone_rules():
        add(f"nada.rules[{r['id']}].example", r.get("example"))
    for s in load("nada")["syllables"]:
        add(f"nada.syllables[{s['id']}]", s)
    for mp in load("nada")["minimal_pairs"]:
        for i, w in enumerate(mp["words"]):
            add(f"nada.minimal_pairs[{mp['id']}].words[{i}]", w)
    for e in load("vocab")["entries"]:
        add(f"vocab[{e['id']}]", e)
        add(f"vocab[{e['id']}].example", e.get("example"))
    for t in load("grammar")["topics"]:
        for i, ex in enumerate(t["examples"]):
            add(f"grammar[{t['id']}].examples[{i}]", ex)
    for p in load("frasa")["phrases"]:
        add(f"frasa[{p['id']}]", p)
    return out


__all__ = [
    "DATA_DIR", "ID_ANGKA", "ID_KONSONAN", "ID_VOKAL", "MAX_STAGE",
    "MODULE_FILES", "POS_VALUES", "ROOT", "aksara_items", "all_card_ids",
    "consonants", "digits", "examples_with_syllables", "grammar_items",
    "grammar_topics", "load", "load_all", "marks", "minimal_pairs",
    "nada_items", "phrases", "tone_rules", "tone_syllables", "tones",
    "vocab_entries", "vowels",
]
