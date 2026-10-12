#!/usr/bin/env python3
"""Buat lembar kerja tertulis beserta kunci jawabannya.

    python tools/build_worksheets.py

Hasilnya 12 lembar di worksheets/ (dua lembar per tahap) dan 12 kunci jawaban
di worksheets/answers/. Keduanya DIBUAT dari data/*.json, bukan ditulis
tangan, sehingga kunci jawaban selalu sejalan dengan datanya. Jangan
menyunting hasilnya langsung.

Kunci jawaban sengaja disimpan di berkas terpisah supaya Anda bisa mencetak
lembar kerjanya tanpa ikut melihat jawabannya.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from thaidrill import dataio, tone  # noqa: E402

ROOT = dataio.ROOT
WS_DIR = os.path.join(ROOT, "worksheets")
ANS_DIR = os.path.join(WS_DIR, "answers")

PER_SECTION = 6


def _half(items: list, part: int) -> list:
    """Bagi dua daftar secara selang-seling supaya kedua lembar seimbang."""
    return [x for i, x in enumerate(items) if i % 2 == part]


def _stage_only(items: list[dict], stage: int) -> list[dict]:
    return [i for i in items if i["stage"] == stage]


def build_sheet(no: int, stage: int, part: int) -> tuple[str, str]:
    """Kembalikan (isi lembar kerja, isi kunci jawaban) untuk satu lembar."""
    konsonan = _half(_stage_only(dataio.consonants(), stage), part)[:PER_SECTION]
    suku = _half(_stage_only(dataio.tone_syllables(), stage), part)[:PER_SECTION]
    kata = _half(_stage_only(dataio.vocab_entries(), stage), part)
    kata_arti = kata[:PER_SECTION]
    kata_tulis = kata[PER_SECTION:PER_SECTION * 2] or kata[:PER_SECTION]
    tbhs = _half(_stage_only(dataio.grammar_items(), stage), part)[:4]
    frasa = _half(_stage_only(dataio.phrases(), stage), part)[:4]

    judul = f"Lembar kerja {no:02d} — tahap {stage} ({'A' if part == 0 else 'B'})"
    L = [f"# {judul}", ""]
    K = [f"# Kunci jawaban {judul}", ""]
    L.append("Kerjakan tanpa melihat kunci jawaban di `worksheets/answers/`.")
    L.append("")

    # --- 1. huruf ---------------------------------------------------------
    L += ["## 1. Huruf: kelas dan bunyi", "",
          "Tulis kelas konsonan (tengah/tinggi/rendah) dan bunyi awalnya.", "",
          "| Huruf | Kelas | Bunyi awal |", "|:--|:--|:--|"]
    K += ["## 1. Huruf: kelas dan bunyi", "",
          "| Huruf | Kelas | Bunyi awal | Nama |", "|:--|:--|:--|:--|"]
    for c in konsonan:
        L.append(f"| {c['letter']} | | |")
        K.append(f"| {c['letter']} | {c['class']} | {c['initial']} | "
                 f"{c['name_th']} ({c['name_rom']}) |")
    L.append("")
    K.append("")

    # --- 2. nada ----------------------------------------------------------
    L += ["## 2. Nada", "",
          "Tentukan nada setiap kata, lalu tulis alasannya secara singkat "
          "(kelas konsonan, jenis suku kata, tanda nada).", "",
          "| Kata | Nada | Alasan |", "|:--|:--|:--|"]
    K += ["## 2. Nada", "", "| Kata | Nada | Alasan |", "|:--|:--|:--|"]
    for s in suku:
        L.append(f"| {s['th']} | | |")
        syls = tone.parse_word(s["syl"])
        nada = " - ".join(x.tone for x in syls)
        alasan = " ".join(tone.explain(x) for x in syls)
        K.append(f"| {s['th']} | {nada} | {alasan} |")
    L.append("")
    K.append("")

    # --- 3. arti kata -----------------------------------------------------
    L += ["## 3. Arti kata", "", "Tulis artinya dalam bahasa Indonesia.", "",
          "| Kata | Lafal | Arti |", "|:--|:--|:--|"]
    K += ["## 3. Arti kata", "", "| Kata | Lafal | Arti |", "|:--|:--|:--|"]
    for e in kata_arti:
        L.append(f"| {e['th']} | {e['phon']} | |")
        K.append(f"| {e['th']} | {e['phon']} | {e['gloss']} |")
    L.append("")
    K.append("")

    # --- 4. tulis kata Thai ----------------------------------------------
    L += ["## 4. Tulis kata Thai", "",
          "Tulis kata Thainya beserta lafal bernadanya.", "",
          "| Arti | Tulisan Thai | Lafal |", "|:--|:--|:--|"]
    K += ["## 4. Tulis kata Thai", "", "| Arti | Tulisan Thai | Lafal |",
          "|:--|:--|:--|"]
    for e in kata_tulis:
        L.append(f"| {e['gloss']} | | |")
        K.append(f"| {e['gloss']} | {e['th']} | {e['phon']} |")
    L.append("")
    K.append("")

    # --- 5. tata bahasa ---------------------------------------------------
    if tbhs:
        L += ["## 5. Tata bahasa", ""]
        K += ["## 5. Tata bahasa", ""]
        for n, i in enumerate(tbhs, 1):
            L.append(f"{n}. {i['prompt']}"
                     + (f" — {i['prompt_th']}" if i.get("prompt_th") else ""))
            for huruf, opt in zip("abcd", i["options"]):
                L.append(f"   {huruf}. {opt}")
            L.append("")
            K.append(f"{n}. {i['options'][i['answer']]}"
                     + (f" — {i['explain']}" if i.get("explain") else ""))
        K.append("")

    # --- 6. frasa ---------------------------------------------------------
    if frasa:
        L += ["## 6. Frasa", "",
              "Tulis kalimat Thainya. Lafal boleh ditulis bila membantu.", "",
              "| Arti | Kalimat Thai |", "|:--|:--|"]
        K += ["## 6. Frasa", "", "| Arti | Kalimat Thai | Lafal |", "|:--|:--|:--|"]
        for p in frasa:
            L.append(f"| {p['gloss']} | |")
            K.append(f"| {p['gloss']} | {p['th']} | {p['phon']} |")
        L.append("")
        K.append("")

    L.append(f"Kunci jawaban: `worksheets/answers/ws-{no:02d}-kunci.md`")
    L.append("")
    K.append("Dibuat oleh `tools/build_worksheets.py` dari `data/*.json`. "
             "Jangan disunting langsung.")
    K.append("")
    return "\n".join(L), "\n".join(K)


def build() -> list[str]:
    os.makedirs(ANS_DIR, exist_ok=True)
    written: list[str] = []
    no = 0
    for stage in range(1, dataio.MAX_STAGE + 1):
        for part in (0, 1):
            no += 1
            lembar, kunci = build_sheet(no, stage, part)
            p1 = os.path.join(WS_DIR, f"ws-{no:02d}.md")
            p2 = os.path.join(ANS_DIR, f"ws-{no:02d}-kunci.md")
            with open(p1, "w", encoding="utf-8", newline="\n") as f:
                f.write(lembar)
            with open(p2, "w", encoding="utf-8", newline="\n") as f:
                f.write(kunci)
            written += [p1, p2]
    return written


def main() -> int:
    files = build()
    print(f"{len(files)} berkas dibuat di worksheets/ dan worksheets/answers/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
