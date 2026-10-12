#!/usr/bin/env python3
"""Buat webdata.js untuk aplikasi kartu di browser.

    python tools/build_web.py

Data tetap bersumber dari data/*.json. Berkas hasilnya dimuat lewat tag
<script>, bukan fetch(), supaya aplikasi jalan baik di GitHub Pages maupun
saat index.html dibuka langsung dari berkas (file://) tanpa masalah CORS.

Teks Thai ditulis sebagai escape \\uXXXX (ASCII murni) supaya tidak bergantung
pada charset yang dikirim peladen.

Semua kunci soal nada dan kelas konsonan dihitung di sini memakai
thaidrill/tone.py dan thaidrill/thai.py, sehingga aturan nada tidak perlu
ditulis ulang dalam JavaScript dan tetap satu sumber dengan quiz.py. Pengecoh
diacak dengan seed tetap supaya hasil bangunannya sama setiap kali dijalankan
dan bisa diperiksa pengujian otomatis.
"""

from __future__ import annotations

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from thaidrill import dataio, thai, tone  # noqa: E402
from thaidrill.questions import (  # noqa: E402
    BEDA_LABEL,
    RELASI_LABEL,
    consonant_class_question,
    syllable_tone_question,
    tone_rule_question,
    vocab_detail,
)

ROOT = dataio.ROOT
OUT = os.path.join(ROOT, "webdata.js")

#: Seed tetap: bangunan harus bisa diulang persis.
SEED = 20240101

CAT_LABEL = {
    # modul aksara
    "konsonan": "Konsonan",
    "vokal": "Vokal",
    "tanda": "Tanda",
    "angka": "Angka",
    "soal-aksara": "Soal aksara",
    # modul nada
    "nada": "Lima nada",
    "aturan": "Aturan nada",
    "suku": "Nada kata",
    "pasangan": "Pasangan nada",
    "soal-nada": "Soal nada",
    # modul kosakata
    "sapaan": "Sapaan",
    "partikel": "Partikel",
    "ganti": "Kata ganti",
    "tunjuk": "Kata tunjuk",
    "tanya": "Kata tanya",
    "angka-kata": "Angka",
    "keluarga": "Keluarga",
    "orang": "Orang",
    "kerja": "Kata kerja",
    "sifat": "Kata sifat",
    "makanan": "Makanan",
    "tempat": "Tempat",
    "waktu": "Waktu",
    "arah": "Arah",
    "jalan": "Kendaraan",
    "uang": "Uang & belanja",
    "klasifikator": "Klasifikator",
    "keterangan": "Kata penanda",
    "tubuh": "Tubuh & sakit",
    "alam": "Alam & cuaca",
    "rasa": "Perasaan",
    "bangsa": "Bangsa & bahasa",
    "benda": "Benda",
    # modul latihan telinga
    "telinga-panjang": "Panjang vokal",
    "telinga-hembusan": "Hembusan",
    "soal-telinga": "Soal telinga",
    # modul kata serumpun
    "serumpun-sama": "Arti sejalan",
    "serumpun-bergeser": "Arti bergeser",
    "serumpun-sebagian": "Jarang di Indonesia",
    # modul bacaan
    "percakapan": "Percakapan",
    "soal-bacaan": "Soal pemahaman",
    # modul frasa
    "kenalan": "Perkenalan",
    "restoran": "Warung & restoran",
    "belanja": "Belanja",
    "darurat": "Darurat & sakit",
}

CLASS_COUNT = {thai.MID: 9, thai.HIGH: 11, thai.LOW: 24}


def label(cat: str) -> str:
    return CAT_LABEL.get(cat, cat)


def _ex(item: dict | None) -> dict:
    if not item:
        return {"th": "", "phon": "", "gloss": ""}
    return {"th": item["th"], "phon": item["phon"], "gloss": item["gloss"]}


# ------------------------------------------------------------ modul aksara ---

def build_aksara(rng: random.Random) -> list[dict]:
    out: list[dict] = []
    for c in dataio.consonants():
        q = consonant_class_question(c, rng)
        out.append({
            "id": c["id"], "kind": "flip", "cat": "konsonan",
            "catLabel": label("konsonan"), "stage": c["stage"],
            "th": c["letter"],
            "audio": c["name_th"],
            "title": f"{c['name_th']} — {c['name_rom']}",
            "meaning": f"kelas {c['class']} ({CLASS_COUNT[c['class']]} huruf)",
            "rows": [
                ["Nama", f"{c['name_th']} ({c['name_rom']}) — '{c['name_id']}'"],
                ["Kelas", c["class"]],
                ["Bunyi awal", c["initial"]],
                ["Bunyi akhir", c["final"] or "tidak dipakai sebagai akhir"],
            ],
            "note": c["note"],
            "quiz": {"prompt": q.question, "options": q.options, "answer": q.answer},
        })
    for v in dataio.vowels():
        ex = _ex(v.get("example"))
        out.append({
            "id": v["id"], "kind": "flip", "cat": "vokal",
            "catLabel": label("vokal"), "stage": v["stage"],
            "th": v["display"],
            "audio": ex["th"],
            "title": f"{v['phon']} ({tone.VOWEL_PATTERNS[v['vowel_id']]['length']})",
            "meaning": f"bunyi {v['phon']}",
            "rows": [
                ["Panjang", tone.VOWEL_PATTERNS[v["vowel_id"]]["length"]],
                ["RTGS", v["rom"]],
                ["Pasangan", v["pair"] and tone.VOWEL_PATTERNS[v["pair"]]["display"] or "-"],
            ],
            "exTh": ex["th"], "exPhon": ex["phon"], "exGloss": ex["gloss"],
            "note": v.get("note") or "",
        })
    for m in dataio.marks():
        ex = _ex(m.get("example"))
        out.append({
            "id": m["id"], "kind": "flip", "cat": "tanda",
            "catLabel": label("tanda"), "stage": m["stage"],
            "th": m["mark"],
            "audio": ex["th"],
            "title": f"{m['name_th']} — {m['name_rom']}",
            "meaning": m["name_rom"],
            "rows": [["Nama Thai", m["name_th"]], ["Nama Latin", m["name_rom"]]],
            "exTh": ex["th"], "exPhon": ex["phon"], "exGloss": ex["gloss"],
            "note": m.get("note") or "",
        })
    for d in dataio.digits():
        out.append({
            "id": d["id"], "kind": "flip", "cat": "angka",
            "catLabel": label("angka"), "stage": d["stage"],
            "th": d["digit"],
            "audio": d["th"],
            "title": str(d["value"]),
            "meaning": f"{d['value']}",
            "rows": [["Angka", str(d["value"])], ["Kata", f"{d['th']} ({d['phon']})"]],
            "note": "",
        })
    for i in dataio.aksara_items():
        out.append({
            "id": i["id"], "kind": "mcq", "cat": "soal-aksara",
            "catLabel": label("soal-aksara"), "stage": i["stage"],
            "prompt": i["prompt"], "promptTh": i.get("prompt_th") or "",
            "optionsLang": i["options_lang"], "options": i["options"],
            "answer": i["answer"], "explain": i.get("explain") or "",
        })
    return out


# -------------------------------------------------------------- modul nada ---

def build_nada(rng: random.Random) -> list[dict]:
    out: list[dict] = []
    for t in dataio.tones():
        ex = _ex(t["example"])
        out.append({
            "id": t["id"], "kind": "flip", "cat": "nada",
            "catLabel": label("nada"), "stage": t["stage"],
            "th": ex["th"],
            "audio": ex["th"],
            "title": f"nada {t['key']}",
            "meaning": f"nada {t['key']} — {t['name_th']} ({t['name_rom']})",
            "rows": [["Bunyinya", t["contour"]], ["Lafal contoh", ex["phon"]],
                     ["Arti contoh", ex["gloss"]]],
            "note": t["tip"],
            "hint": "Nada apa ini, dan bagaimana bunyinya?",
        })
    for r in dataio.tone_rules():
        q = tone_rule_question(r, rng)
        out.append({
            "id": r["id"], "kind": "mcq", "cat": "aturan",
            "catLabel": label("aturan"), "stage": q.stage,
            "prompt": q.question, "promptTh": "",
            "optionsLang": "id", "options": q.options, "answer": q.answer,
            "explain": q.explain,
        })
    for s in dataio.tone_syllables():
        q = syllable_tone_question(s, rng)
        out.append({
            "id": s["id"], "kind": "mcq", "cat": "suku",
            "catLabel": label("suku"), "stage": s["stage"],
            "prompt": q.question, "promptTh": s["th"], "audio": s["th"],
            "promptLabel": f"arti: {s['gloss']}",
            "optionsLang": "id", "options": q.options, "answer": q.answer,
            "explain": q.explain,
            "reveal": f"{s['th']} = {s['phon']} ({s['gloss']})",
        })
    for mp in dataio.minimal_pairs():
        out.append({
            "id": mp["id"], "kind": "flip", "cat": "pasangan",
            "catLabel": label("pasangan"), "stage": mp["stage"],
            "th": " / ".join(w["th"] for w in mp["words"]),
            "audio": " ".join(w["th"] for w in mp["words"]),
            "title": mp["title"],
            "meaning": "Kata-kata ini hanya berbeda nada",
            "rows": [[w["th"], f"{w['phon']} — {w['gloss']}"] for w in mp["words"]],
            "note": mp.get("note") or "",
            "hint": "Baca semuanya dengan nada yang berbeda, lalu cocokkan artinya",
        })
    for i in dataio.nada_items():
        out.append({
            "id": i["id"], "kind": "mcq", "cat": "soal-nada",
            "catLabel": label("soal-nada"), "stage": i["stage"],
            "prompt": i["prompt"], "promptTh": i.get("prompt_th") or "",
            "optionsLang": i["options_lang"], "options": i["options"],
            "answer": i["answer"], "explain": i.get("explain") or "",
        })
    return out


# ---------------------------------------------------------- modul kosakata ---

def build_kosakata() -> list[dict]:
    out = []
    for e in dataio.vocab_entries():
        cat = "angka-kata" if e["cat"] == "angka" else e["cat"]
        out.append({
            "id": e["id"], "kind": "flip", "cat": cat, "catLabel": label(cat),
            "stage": e["stage"],
            "th": e["th"], "audio": e["th"], "phon": e["phon"],
            "rom": e["rom"], "freq": e.get("freq", 2),
            "gloss": e["gloss"], "alt": e.get("alt") or [],
            "detail": vocab_detail(e),
            "cls": e.get("cls") or "",
            "exTh": e["example"]["th"], "exPhon": e["example"]["phon"],
            "exGloss": e["example"]["gloss"],
            "note": e.get("note") or "",
        })
    return out


# ------------------------------------------------------- modul tata bahasa ---

def build_tatabahasa() -> list[dict]:
    out = []
    for item in dataio.grammar_items():
        out.append({
            "id": item["id"], "kind": "mcq", "cat": item["topic_id"],
            "catLabel": item["topic_title"], "stage": item["stage"],
            "prompt": item["prompt"], "promptTh": item.get("prompt_th") or "",
            "optionsLang": item["options_lang"], "options": item["options"],
            "answer": item["answer"], "explain": item.get("explain") or "",
        })
    return out


def build_topik() -> list[dict]:
    return [
        {
            "id": t["id"], "title": t["title"], "stage": t["stage"],
            "explanation": t["explanation"], "caveats": t["caveats"],
            "examples": [
                {"th": e["th"], "phon": e["phon"], "gloss": e["gloss"]}
                for e in t["examples"]
            ],
        }
        for t in dataio.grammar_topics()
    ]


# -------------------------------------------------------------- modul frasa ---

def build_frasa() -> list[dict]:
    out = []
    for p in dataio.phrases():
        out.append({
            "id": p["id"], "kind": "flip", "cat": p["cat"], "catLabel": label(p["cat"]),
            "stage": p["stage"],
            "th": p["th"], "audio": p["th"], "phon": p["phon"], "rom": p["rom"],
            "gloss": p["gloss"], "lit": p.get("lit") or "",
            "note": p.get("note") or "",
        })
    return out


# ---------------------------------------------------- modul latihan telinga ---

def build_dengar() -> list[dict]:
    """Kartu mendengarkan: bunyikan satu kata, lalu pilih kata mana itu.

    Kunci jawabannya adalah kata yang dibunyikan, sehingga tidak ada daftar
    jawaban terpisah yang bisa menyimpang darinya. Urutan pilihan dibuat tetap
    mengikuti urutan di data, supaya yang terlatih adalah membedakan bunyi,
    bukan menghafal letak jawaban.
    """
    out: list[dict] = []
    for c in dataio.listen_cards():
        w = c["word"]
        rincian = " · ".join(
            f"{x['th']} = {x['phon']} ({x['gloss']})" for x in c["words"]
        )
        cat = "telinga-" + c["type"]
        out.append({
            "id": c["id"], "kind": "mcq", "cat": cat, "catLabel": label(cat),
            "stage": c["stage"],
            "prompt": "Dengarkan, lalu pilih kata yang Anda dengar.",
            "promptTh": "",
            "promptLabel": f"bedanya hanya {BEDA_LABEL[c['type']]}",
            "audio": w["th"], "audioOnly": True,
            "optionsLang": "th",
            "options": [x["th"] for x in c["words"]],
            "answer": c["index"],
            "reveal": f"{w['th']} = {w['phon']} ({w['gloss']})",
            "explain": (c["note"] + "  " if c["note"] else "") + rincian,
        })
    for i in dataio.listen_items():
        out.append({
            "id": i["id"], "kind": "mcq", "cat": "soal-telinga",
            "catLabel": label("soal-telinga"), "stage": i["stage"],
            "prompt": i["prompt"], "promptTh": i.get("prompt_th") or "",
            "optionsLang": i["options_lang"], "options": i["options"],
            "answer": i["answer"], "explain": i.get("explain") or "",
        })
    return out


# ----------------------------------------------------- modul kata serumpun ---

def build_serumpun() -> list[dict]:
    out = []
    for c in dataio.cognates():
        cat = "serumpun-" + c["relation"]
        out.append({
            "id": c["id"], "kind": "flip", "cat": cat, "catLabel": label(cat),
            "stage": c["stage"],
            "th": c["th"], "audio": c["th"], "phon": c["phon"], "rom": c["rom"],
            "gloss": c["gloss"], "idWord": c["id_word"],
            "relation": RELASI_LABEL[c["relation"]],
            "note": c.get("note") or "",
        })
    return out


# ------------------------------------------------------------- modul bacaan ---

def build_bacaan() -> list[dict]:
    out = []
    for t in dataio.texts():
        out.append({
            "id": t["id"], "kind": "flip", "cat": "percakapan",
            "catLabel": label("percakapan"), "stage": t["stage"],
            "title": t["title"],
            "audio": " ".join(ln["th"] for ln in t["lines"]),
            "lines": [
                {"speaker": ln["speaker"], "th": ln["th"], "phon": ln["phon"],
                 "gloss": ln["gloss"]}
                for ln in t["lines"]
            ],
            "note": t.get("note") or "",
        })
    for i in dataio.text_items():
        out.append({
            "id": i["id"], "kind": "mcq", "cat": "soal-bacaan",
            "catLabel": label("soal-bacaan"), "stage": i["stage"],
            "prompt": i["prompt"], "promptTh": i.get("prompt_th") or "",
            "promptLabel": i["text_title"],
            "optionsLang": i["options_lang"], "options": i["options"],
            "answer": i["answer"], "explain": i.get("explain") or "",
        })
    return out


# ------------------------------------------------------------- keterangan ---

def build_info() -> dict:
    d = dataio.load("nada")
    return {
        "nada": {
            "tones": [
                {"key": t["key"], "nameTh": t["name_th"], "contour": t["contour"]}
                for t in d["tones"]
            ],
            "noMark": [
                {"cls": r["cls"], "kind": r["kind"], "length": r["length"],
                 "tone": r["tone"], "ex": r["example"]["th"],
                 "phon": r["example"]["phon"]}
                for r in d["rules_no_mark"]
            ],
            "mark": [
                {"mark": r["mark"], "markRom": r["mark_rom"], "cls": r["cls"],
                 "tone": r["tone"], "ex": r["example"]["th"],
                 "phon": r["example"]["phon"]}
                for r in d["rules_mark"]
            ],
            "notes": d["rules_note"],
        },
        "serumpun": dataio.cognate_notes(),
        "aksara": {
            "classes": [
                {"name": cls, "count": CLASS_COUNT[cls],
                 "letters": " ".join(
                     c["letter"] for c in dataio.consonants() if c["class"] == cls
                 )}
                for cls in (thai.MID, thai.HIGH, thai.LOW)
            ],
        },
    }


# ------------------------------------------------------------------ tulis ---

def build() -> dict:
    rng = random.Random(SEED)
    return {
        "aksara": build_aksara(rng),
        "nada": build_nada(rng),
        "dengar": build_dengar(),
        "kosakata": build_kosakata(),
        "serumpun": build_serumpun(),
        "tatabahasa": build_tatabahasa(),
        "frasa": build_frasa(),
        "bacaan": build_bacaan(),
        "topik": build_topik(),
        "info": build_info(),
    }


def render(data: dict) -> str:
    body = json.dumps(data, ensure_ascii=True, indent=1, sort_keys=False)
    return (
        "/* Berkas ini DIBUAT OTOMATIS oleh tools/build_web.py.\n"
        "   Jangan disunting langsung; sunting data/*.json lalu jalankan ulang:\n"
        "       python tools/build_web.py\n"
        "   Teks Thai ditulis sebagai escape \\uXXXX supaya tidak bergantung\n"
        "   pada charset yang dikirim peladen. */\n"
        "\"use strict\";\n"
        "const THAI_DATA = " + body + ";\n"
    )


def main() -> int:
    text = render(build())
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    data = build()
    modul = ("aksara", "nada", "dengar", "kosakata", "serumpun", "tatabahasa",
             "frasa", "bacaan")
    print(f"webdata.js dibuat: {sum(len(data[k]) for k in modul)} kartu")
    for k in modul:
        print(f"  {k:12s} {len(data[k]):4d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
