#!/usr/bin/env python3
"""Buat ekspor CSV dan berkas impor Anki dari data/*.json.

    python tools/build_exports.py

Hasilnya:

    data/csv/*.csv   tabel datar untuk dibaca manusia atau diolah ulang
    anki/*.csv       berkas impor Anki, lengkap dengan pengarah #separator

Semua berkas di kedua folder itu DIBUAT ULANG; jangan menyuntingnya langsung.
Nada pada kolom lafal berasal dari data yang sudah diperiksa mesin terhadap
thaidrill/tone.py, jadi ekspor tidak menghitung apa pun sendiri.
"""

from __future__ import annotations

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from thaidrill import dataio, tone  # noqa: E402
from thaidrill.questions import vocab_detail  # noqa: E402

ROOT = dataio.ROOT
CSV_DIR = os.path.join(ROOT, "data", "csv")
ANKI_DIR = os.path.join(ROOT, "anki")

#: Tiga baris pengarah untuk Anki 2.1.55 ke atas.
def anki_header(tags_column: int) -> list[str]:
    return ["#separator:Comma", "#html:false", f"#tags column:{tags_column}"]


def write_csv(path: str, header: list[str], rows: list[list], *,
              directives: list[str] | None = None) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        if directives:
            for line in directives:
                f.write(line + "\n")
        w = csv.writer(f, lineterminator="\n")
        if header:
            w.writerow(header)
        w.writerows(rows)


# ------------------------------------------------------------------ data ---

def dengar_rows() -> list[list]:
    out = []
    for c in dataio.listen_cards():
        w = c["word"]
        lain = " / ".join(x["th"] for x in c["words"] if x["th"] != w["th"])
        out.append([c["id"], c["type"], w["th"], w["phon"], w["gloss"], lain,
                    c["stage"], c["note"]])
    return out


def serumpun_rows() -> list[list]:
    return [
        [c["id"], c["th"], c["phon"], c["rom"], c["gloss"], c["id_word"],
         c["relation"], c["stage"], c.get("note") or ""]
        for c in dataio.cognates()
    ]


def bacaan_rows() -> list[list]:
    out = []
    for t in dataio.texts():
        for i, ln in enumerate(t["lines"], 1):
            out.append([t["id"], t["title"], i, ln["speaker"], ln["th"],
                        ln["phon"], ln["gloss"], t["stage"]])
    return out


def konsonan_rows() -> list[list]:
    return [
        [c["letter"], c["name_th"], c["name_rom"], c["name_id"], c["class"],
         c["initial"], c["final"] or "", "ya" if c["obsolete"] else "tidak",
         c["stage"], c["note"]]
        for c in dataio.consonants()
    ]


def vokal_rows() -> list[list]:
    out = []
    for v in dataio.vowels():
        ex = v.get("example") or {}
        out.append([
            v["display"], v["phon"], v["rom"],
            tone.VOWEL_PATTERNS[v["vowel_id"]]["length"],
            tone.VOWEL_PATTERNS[v["pair"]]["display"] if v["pair"] else "",
            ex.get("th", ""), ex.get("phon", ""), ex.get("gloss", ""),
            v["stage"], v.get("note") or "",
        ])
    return out


def nada_rows() -> list[list]:
    out = []
    for s in dataio.tone_syllables():
        syls = tone.parse_word(s["syl"])
        out.append([
            s["id"], s["th"], s["phon"], s["gloss"],
            " - ".join(x.tone for x in syls),
            " ".join(x.cls for x in syls),
            " ".join(x.kind for x in syls),
            s["stage"], s.get("note") or "",
        ])
    return out


def kosakata_rows() -> list[list]:
    return [
        [e["id"], e["th"], e["phon"], e["rom"], e["gloss"],
         "; ".join(e.get("alt") or []), e["pos"], e.get("cls") or "", e["cat"],
         e["stage"], e["example"]["th"], e["example"]["phon"],
         e["example"]["gloss"], e.get("note") or ""]
        for e in dataio.vocab_entries()
    ]


def tatabahasa_rows() -> list[list]:
    return [
        [i["id"], i["topic_id"], i["topic_title"], i["stage"], i["prompt"],
         i.get("prompt_th") or "", i["options_lang"], " | ".join(i["options"]),
         i["options"][i["answer"]], i.get("explain") or ""]
        for i in dataio.grammar_items()
    ]


def frasa_rows() -> list[list]:
    return [
        [p["id"], p["th"], p["phon"], p["rom"], p["gloss"], p.get("lit") or "",
         p["cat"], p["stage"], p.get("note") or ""]
        for p in dataio.phrases()
    ]


# -------------------------------------------------------------------- CSV ---

CSV_FILES = {
    "konsonan.csv": (
        ["huruf", "nama_th", "nama_rom", "arti_nama", "kelas", "bunyi_awal",
         "bunyi_akhir", "tidak_dipakai", "tahap", "catatan"],
        konsonan_rows,
    ),
    "vokal.csv": (
        ["pola", "lafal", "rtgs", "panjang", "pasangan", "contoh_th",
         "contoh_lafal", "contoh_arti", "tahap", "catatan"],
        vokal_rows,
    ),
    "nada_kata.csv": (
        ["id", "th", "lafal", "arti", "nada", "kelas_konsonan", "jenis_suku_kata",
         "tahap", "catatan"],
        nada_rows,
    ),
    "kosakata.csv": (
        ["id", "th", "lafal", "rtgs", "arti", "arti_lain", "kelas_kata",
         "klasifikator", "kategori", "tahap", "contoh_th", "contoh_lafal",
         "contoh_arti", "catatan"],
        kosakata_rows,
    ),
    "tatabahasa.csv": (
        ["id", "topik", "judul_topik", "tahap", "soal", "soal_th", "bahasa_pilihan",
         "pilihan", "jawaban", "penjelasan"],
        tatabahasa_rows,
    ),
    "frasa.csv": (
        ["id", "th", "lafal", "rtgs", "arti", "harfiah", "kategori", "tahap",
         "catatan"],
        frasa_rows,
    ),
    "dengar.csv": (
        ["id", "jenis", "th", "lafal", "arti", "pasangannya", "tahap", "catatan"],
        dengar_rows,
    ),
    "serumpun.csv": (
        ["id", "th", "lafal", "rtgs", "arti", "kata_indonesia", "hubungan",
         "tahap", "catatan"],
        serumpun_rows,
    ),
    "bacaan.csv": (
        ["teks", "judul", "baris", "pembicara", "th", "lafal", "arti", "tahap"],
        bacaan_rows,
    ),
}


# ------------------------------------------------------------------- Anki ---

def anki_aksara() -> list[list]:
    """Depan: huruf. Belakang: nama, kelas, bunyi."""
    rows = []
    for c in dataio.consonants():
        belakang = (
            f"{c['name_th']} ({c['name_rom']}, '{c['name_id']}') — kelas "
            f"{c['class']}, bunyi awal {c['initial']}, bunyi akhir "
            f"{c['final'] or 'tidak ada'}"
        )
        rows.append([c["letter"], belakang, c["class"], c["note"],
                     f"thai aksara konsonan tahap{c['stage']}"])
    for v in dataio.vowels():
        ex = v.get("example") or {}
        belakang = f"{v['phon']} ({tone.VOWEL_PATTERNS[v['vowel_id']]['length']})"
        contoh = f"{ex.get('th', '')} {ex.get('phon', '')} {ex.get('gloss', '')}".strip()
        rows.append([v["display"], belakang, contoh, v.get("note") or "",
                     f"thai aksara vokal tahap{v['stage']}"])
    return rows


def anki_nada() -> list[list]:
    rows = []
    for s in dataio.tone_syllables():
        syls = tone.parse_word(s["syl"])
        nada = " - ".join(x.tone for x in syls)
        alasan = " ".join(tone.explain(x) for x in syls)
        rows.append([s["th"], nada, s["phon"], s["gloss"], alasan,
                     f"thai nada tahap{s['stage']}"])
    return rows


def anki_kosakata() -> list[list]:
    rows = []
    for e in dataio.vocab_entries():
        rows.append([
            e["th"], e["gloss"], e["phon"], e["rom"], vocab_detail(e),
            f"{e['example']['th']} — {e['example']['phon']} — {e['example']['gloss']}",
            e.get("note") or "",
            f"thai kosakata {e['cat']} tahap{e['stage']}",
        ])
    return rows


def anki_tatabahasa() -> list[list]:
    rows = []
    for i in dataio.grammar_items():
        depan = i["prompt"]
        if i.get("prompt_th"):
            depan += "<br>" + i["prompt_th"]
        depan += "<br>" + " | ".join(
            f"{n}. {o}" for n, o in enumerate(i["options"], 1)
        )
        rows.append([depan, i["options"][i["answer"]], i.get("explain") or "",
                     f"thai tatabahasa {i['topic_id']} tahap{i['stage']}"])
    return rows


def anki_frasa() -> list[list]:
    return [
        [p["gloss"], p["th"], p["phon"], p.get("lit") or "", p.get("note") or "",
         f"thai frasa {p['cat']} tahap{p['stage']}"]
        for p in dataio.phrases()
    ]


def anki_serumpun() -> list[list]:
    rows = []
    for c in dataio.cognates():
        rows.append([
            c["th"], f"{c['gloss']} — seasal dengan '{c['id_word']}'",
            c["phon"], c["id_word"], c.get("note") or "",
            f"thai serumpun {c['relation']} tahap{c['stage']}",
        ])
    return rows


def anki_bacaan() -> list[list]:
    rows = []
    for t in dataio.texts():
        depan = "<br>".join(f"{ln['speaker']}: {ln['th']}" for ln in t["lines"])
        belakang = "<br>".join(
            f"{ln['speaker']}: {ln['phon']} — {ln['gloss']}" for ln in t["lines"]
        )
        rows.append([depan, belakang, t["title"], t.get("note") or "",
                     f"thai bacaan {t['cat']} tahap{t['stage']}"])
    return rows


ANKI_FILES = {
    "aksara.csv": (anki_aksara, 5),
    "nada.csv": (anki_nada, 6),
    "kosakata.csv": (anki_kosakata, 8),
    "tatabahasa.csv": (anki_tatabahasa, 4),
    "frasa.csv": (anki_frasa, 6),
    "serumpun.csv": (anki_serumpun, 6),
    "bacaan.csv": (anki_bacaan, 5),
}


# ------------------------------------------------------------------ main ---

def build() -> dict[str, int]:
    counts: dict[str, int] = {}
    for name, (header, fn) in CSV_FILES.items():
        rows = fn()
        write_csv(os.path.join(CSV_DIR, name), header, rows)
        counts["data/csv/" + name] = len(rows)
    for name, (fn, tags_col) in ANKI_FILES.items():
        rows = fn()
        write_csv(os.path.join(ANKI_DIR, name), [], rows,
                  directives=anki_header(tags_col))
        counts["anki/" + name] = len(rows)
    return counts


def main() -> int:
    for path, n in build().items():
        print(f"{path:28s} {n:4d} baris")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
