"""Pembuat soal untuk setiap mode latihan.

Sebagian besar soal di modul aksara dan nada DIBUAT OTOMATIS, dan kunci
jawabannya diambil langsung dari thaidrill/thai.py dan thaidrill/tone.py,
bukan dari daftar jawaban yang ditulis tangan. Dengan begitu kunci soal
"apa kelas huruf ini" dan "apa nada kata ini" tidak mungkin menyimpang dari
aturan yang diajarkan modulnya. Pengecoh dipilih dengan generator acak
ber-seed agar susunan soal dapat diulang dan diuji.
"""

from __future__ import annotations

import random
import re
import unicodedata
from dataclasses import dataclass, field

from . import dataio, thai, tone

#: Urutan di sini menentukan giliran soal saat sesi disilang (interleaving).
#: "kosakata-id" sengaja berada SEBELUM "kosakata-th": untuk bisa berbicara,
#: latihan arah produksi (Anda yang memanggil kata Thainya) lebih berharga
#: daripada arah pengenalan, dan arah yang lebih berharga diberi giliran lebih
#: dahulu ketika sesi terpotong waktu.
MODES = (
    "aksara", "nada", "dengar", "kosakata-id", "kosakata-th",
    "serumpun", "tatabahasa", "frasa", "bacaan",
)

MODE_LABELS = {
    "aksara": "Aksara: huruf, vokal, tanda",
    "nada": "Nada dan aturannya",
    "dengar": "Latihan telinga",
    "kosakata-id": "Kosakata: Indonesia ke Thai",
    "kosakata-th": "Kosakata: Thai ke Indonesia",
    "serumpun": "Kata serumpun Sanskerta",
    "tatabahasa": "Tata bahasa",
    "frasa": "Frasa sehari-hari",
    "bacaan": "Bacaan dan percakapan",
}

_ACCEPTED_CACHE: dict[tuple, frozenset[str]] = {}


@dataclass
class Question:
    card_id: str
    mode: str
    kind: str  # "mcq" | "typed" | "selfcheck"
    question: str
    stimulus_th: str | None = None
    stimulus_label: str | None = None
    phon: str | None = None
    options: list[str] | None = None
    options_lang: str | None = None
    answer: int | None = None
    accepted: list[str] = field(default_factory=list)
    reveal: str = ""
    reveal_th: str | None = None
    explain: str | None = None
    #: True bila soal ini pengulangan materi baru di lintasan kedua sesi yang
    #: sama. quiz.py tidak menaikkan kotak Leitner dua kali.
    repeat: bool = False
    #: Tahap materi (1-6). Dipakai session.py untuk memperkenalkan kartu baru
    #: menurut urutan tahap, bukan acak dari seluruh materi.
    stage: int | None = None
    #: Perkiraan seberapa sering kata itu dipakai (1 = paling sering). Di dalam
    #: satu tahap, kata yang lebih sering diperkenalkan lebih dahulu.
    freq: int | None = None

    def is_correct_text(self, text: str) -> bool:
        return normalize(text) in {normalize(a) for a in self.accepted}


# ------------------------------------------------------- jawaban bertaip ---

_PUNCT_RE = re.compile(r"[^\w\s]", flags=re.UNICODE)
_SPACE_RE = re.compile(r"\s+")


def normalize(text: str) -> str:
    """Bakukan jawaban bertaip: huruf kecil, tanpa tanda baca, spasi tunggal."""
    text = unicodedata.normalize("NFKC", text).strip().lower()
    text = _PUNCT_RE.sub(" ", text)
    return _SPACE_RE.sub(" ", text).strip()


def expand_accepted(gloss: str, alt: list[str] | None = None) -> list[str]:
    """Kembangkan arti menjadi daftar jawaban yang diterima.

    "murah; benar" menghasilkan kalimat utuhnya, "murah", dan "benar", supaya
    pengguna tidak dihukum karena menulis salah satu arti saja.
    """
    out: list[str] = []

    def add(s: str) -> None:
        s = s.strip()
        if s and s not in out:
            out.append(s)

    add(gloss)
    for piece in re.split(r"[,;/]", gloss):
        add(piece)
        add(re.sub(r"\([^)]*\)", "", piece))
    for a in alt or []:
        add(a)
        add(re.sub(r"\([^)]*\)", "", a))
    return [o for o in out if o]


def accepted_set(entry: dict) -> frozenset[str]:
    """Himpunan jawaban yang diterima untuk satu entri, sudah dibakukan."""
    key = (entry["gloss"], tuple(entry.get("alt") or ()))
    cached = _ACCEPTED_CACHE.get(key)
    if cached is None:
        cached = frozenset(
            normalize(a) for a in expand_accepted(entry["gloss"], entry.get("alt"))
        )
        _ACCEPTED_CACHE[key] = cached
    return cached


# ------------------------------------------------------------- pengecoh ---

def _shuffle_options(
    rng: random.Random, correct: str, distractors: list[str]
) -> tuple[list[str], int]:
    opts = [correct] + [d for d in distractors if d != correct]
    rng.shuffle(opts)
    return opts, opts.index(correct)


def _pick_distractors(
    rng: random.Random, pool: list[dict], target: dict, key: str, n: int = 3
) -> list[str]:
    """Pilih n pengecoh, mengutamakan kata yang sekelas atau sekategori."""
    want = target[key]
    buckets = [
        [e for e in pool if e[key] != want and e.get("pos") == target.get("pos")],
        [e for e in pool if e[key] != want and e.get("cat") == target.get("cat")],
        [e for e in pool if e[key] != want],
    ]
    chosen: list[str] = []
    for bucket in buckets:
        bucket = list(bucket)
        rng.shuffle(bucket)
        for e in bucket:
            if e[key] not in chosen and len(chosen) < n:
                chosen.append(e[key])
        if len(chosen) >= n:
            break
    return chosen[:n]


# ------------------------------------------------------------ modul aksara ---

def consonant_class_question(c: dict, rng: random.Random) -> Question:
    """Soal buatan: 'Apa kelas konsonan ini?' Kunci diambil dari thai.py."""
    others = [k for k in (thai.MID, thai.HIGH, thai.LOW) if k != c["class"]]
    options, answer = _shuffle_options(rng, c["class"], others)
    jumlah = {thai.MID: 9, thai.HIGH: 11, thai.LOW: 24}
    return Question(
        card_id=c["id"],
        mode="aksara",
        kind="mcq",
        stage=c["stage"],
        question=f"Apa kelas konsonan {c['letter']} ({c['name_rom']})?",
        stimulus_th=c["letter"],
        options=options,
        options_lang="id",
        answer=answer,
        reveal=f"{c['letter']} = kelas {c['class']}",
        explain=(
            f"{c['name_th']} ({c['name_rom']}, '{c['name_id']}'), kelas "
            f"{c['class']} ({jumlah[c['class']]} huruf), bunyi awal "
            f"{c['initial']}, bunyi akhir "
            f"{c['final'] if c['final'] else 'tidak dipakai sebagai akhir'}."
        ),
    )


def consonant_name_question(c: dict) -> Question:
    """Kartu bolak-balik: huruf di depan, nama dan bunyinya di belakang."""
    akhir = c["final"] if c["final"] else "tidak dipakai sebagai konsonan akhir"
    return Question(
        card_id=c["id"],
        mode="aksara",
        kind="selfcheck",
        stage=c["stage"],
        question="Apa nama huruf ini, kelasnya, dan bunyinya?",
        stimulus_th=c["letter"],
        reveal=(
            f"{c['name_th']} — {c['name_rom']} ('{c['name_id']}') · kelas "
            f"{c['class']} · bunyi awal {c['initial']} · bunyi akhir {akhir}"
        ),
        explain=c["note"] or None,
    )


def vowel_question(v: dict) -> Question:
    ex = v.get("example")
    contoh = (
        f"{ex['th']} = {ex['phon']} ({ex['gloss']})" if ex
        else "tidak ada contoh kata yang dipakai di sini"
    )
    return Question(
        card_id=v["id"],
        mode="aksara",
        kind="selfcheck",
        stage=v["stage"],
        question="Apa bunyi pola vokal ini, dan panjang atau pendek?",
        stimulus_th=v["display"],
        reveal=(
            f"{v['display']} = {v['phon']} "
            f"({tone.VOWEL_PATTERNS[v['vowel_id']]['length']}) · contoh: {contoh}"
        ),
        phon=ex["phon"] if ex else None,
        explain=v.get("note") or None,
    )


def mark_question(m: dict) -> Question:
    ex = m.get("example")
    return Question(
        card_id=m["id"],
        mode="aksara",
        kind="selfcheck",
        stage=m["stage"],
        question="Apa nama tanda ini dan apa gunanya?",
        stimulus_th=m["mark"],
        reveal=(
            f"{m['name_th']} ({m['name_rom']})"
            + (f" · contoh: {ex['th']} = {ex['phon']} ({ex['gloss']})" if ex else "")
        ),
        explain=m.get("note") or None,
    )


def digit_question(d: dict, rng: random.Random) -> Question:
    others = [str(x) for x in range(10) if x != d["value"]]
    rng.shuffle(others)
    options, answer = _shuffle_options(rng, str(d["value"]), others[:3])
    return Question(
        card_id=d["id"],
        mode="aksara",
        kind="mcq",
        stage=d["stage"],
        question="Berapa nilai angka Thai ini?",
        stimulus_th=d["digit"],
        options=options,
        options_lang="id",
        answer=answer,
        reveal=f"{d['digit']} = {d['value']} ({d['th']}, {d['phon']})",
        explain=(
            "Angka Thai masih dipakai pada papan nama, harga tiket wisatawan, "
            "dan dokumen resmi, meski angka Latin lebih umum."
        ),
    )


def aksara_item_question(item: dict) -> Question:
    return Question(
        card_id=item["id"],
        mode="aksara",
        kind="mcq",
        stage=item["stage"],
        question=item["prompt"],
        stimulus_th=item.get("prompt_th"),
        options=list(item["options"]),
        options_lang=item["options_lang"],
        answer=item["answer"],
        reveal=item["options"][item["answer"]],
        explain=item.get("explain"),
    )


# -------------------------------------------------------------- modul nada ---

def tone_card_question(t: dict) -> Question:
    ex = t["example"]
    return Question(
        card_id=t["id"],
        mode="nada",
        kind="selfcheck",
        stage=t["stage"],
        question=f"Bagaimana bunyi nada {t['key']}?",
        stimulus_th=ex["th"],
        phon=ex["phon"],
        reveal=(
            f"nada {t['key']} ({t['name_th']}, {t['name_rom']}) — {t['contour']} "
            f"Contoh: {ex['th']} = {ex['phon']} ({ex['gloss']})"
        ),
        explain=t["tip"],
    )


def syllable_tone_question(s: dict, rng: random.Random) -> Question:
    """Soal buatan: 'Apa nada kata ini?'

    Kunci jawaban dihitung thaidrill/tone.py dari ejaannya, bukan dibaca dari
    data, sehingga kunci tidak bisa menyimpang dari aturan nada.
    """
    syls = tone.parse_word(s["syl"])
    nada = [x.tone for x in syls]
    jawaban = " - ".join(nada)
    semua = list(thai.TONES)
    if len(nada) == 1:
        pengecoh = [n for n in semua if n != jawaban]
        rng.shuffle(pengecoh)
        options, answer = _shuffle_options(rng, jawaban, pengecoh[:3])
    else:
        pengecoh = []
        while len(pengecoh) < 3:
            calon = " - ".join(rng.choice(semua) for _ in nada)
            if calon != jawaban and calon not in pengecoh:
                pengecoh.append(calon)
        options, answer = _shuffle_options(rng, jawaban, pengecoh)
    return Question(
        card_id=s["id"],
        mode="nada",
        kind="mcq",
        stage=s["stage"],
        question="Apa nada kata ini?",
        stimulus_th=s["th"],
        stimulus_label=f"arti: {s['gloss']}",
        options=options,
        options_lang="id",
        answer=answer,
        reveal=f"{s['th']} = {s['phon']} ({s['gloss']})",
        explain=" ".join(tone.explain(x) for x in syls)
        + (f" {s['note']}" if s.get("note") else ""),
    )


def tone_rule_question(r: dict, rng: random.Random) -> Question:
    """Soal buatan dari satu baris tabel nada. Kunci dihitung tone.py."""
    if "mark" in r:
        nada = tone.tone_from_parts(r["cls"], tone.HIDUP, tone.PANJANG, r["mark"])
        soal = (
            f"Konsonan kelas {r['cls']} dengan tanda nada {r['mark']} "
            f"({r['mark_rom']}) menghasilkan nada apa?"
        )
    else:
        nada = tone.tone_from_parts(r["cls"], r["kind"], r["length"], None)
        soal = (
            f"Konsonan kelas {r['cls']}, suku kata {r['kind']}, vokal "
            f"{r['length']}, tanpa tanda nada. Nadanya apa?"
        )
    pengecoh = [n for n in thai.TONES if n != nada]
    rng.shuffle(pengecoh)
    options, answer = _shuffle_options(rng, nada, pengecoh[:3])
    ex = r["example"]
    return Question(
        card_id=r["id"],
        mode="nada",
        kind="mcq",
        stage=1 if "mark" not in r else 2,
        question=soal,
        options=options,
        options_lang="id",
        answer=answer,
        reveal=f"nada {nada}",
        reveal_th=ex["th"],
        explain=f"Contoh: {ex['th']} = {ex['phon']} ({ex['gloss']}).",
    )


def minimal_pair_question(mp: dict) -> Question:
    rincian = " · ".join(
        f"{w['th']} = {w['phon']} ({w['gloss']})" for w in mp["words"]
    )
    return Question(
        card_id=mp["id"],
        mode="nada",
        kind="selfcheck",
        stage=mp["stage"],
        question=(
            "Baca ketiga kata ini dengan nada yang berbeda, lalu cocokkan "
            "artinya." if len(mp["words"]) == 3 else
            "Baca kata-kata ini dengan nada yang berbeda, lalu cocokkan artinya."
        ),
        stimulus_th=" / ".join(w["th"] for w in mp["words"]),
        reveal=rincian,
        explain=mp.get("note"),
    )


def nada_item_question(item: dict) -> Question:
    return Question(
        card_id=item["id"],
        mode="nada",
        kind="mcq",
        stage=item["stage"],
        question=item["prompt"],
        stimulus_th=item.get("prompt_th"),
        options=list(item["options"]),
        options_lang=item["options_lang"],
        answer=item["answer"],
        reveal=item["options"][item["answer"]],
        explain=item.get("explain"),
    )


# ---------------------------------------------------------- modul kosakata ---

def vocab_detail(e: dict) -> str:
    bits = [e["pos"]]
    if e.get("cls"):
        bits.append(f"klasifikator: {e['cls']}")
    bits.append(f"RTGS: {e['rom']}")
    return " · ".join(bits)


def vocab_th_to_id(e: dict) -> Question:
    return Question(
        card_id=e["id"],
        mode="kosakata-th",
        kind="typed",
        stage=e["stage"],
        freq=e.get("freq"),
        question="Apa arti kata ini?",
        stimulus_th=e["th"],
        phon=e["phon"],
        accepted=expand_accepted(e["gloss"], e.get("alt")),
        reveal=f"{e['phon']} = {e['gloss']}  ({vocab_detail(e)})",
        reveal_th=e["example"]["th"],
        explain=f"{e['example']['th']} = {e['example']['phon']} — {e['example']['gloss']}",
    )


def vocab_id_to_th(e: dict, pool: list[dict], rng: random.Random) -> Question:
    # Pengecoh tidak boleh menerima teks pertanyaan sebagai jawabannya sendiri.
    # Tanpa saringan ini, soal "kata Thai untuk 'sakit'" bisa memuat เจ็บ dan
    # ป่วย sekaligus, sehingga ada dua jawaban benar.
    prompt_key = normalize(e["gloss"])
    safe = [
        o for o in pool
        if o["id"] != e["id"] and prompt_key not in accepted_set(o)
    ]
    distractors = _pick_distractors(rng, safe, e, "th", 3)
    options, answer = _shuffle_options(rng, e["th"], distractors)
    return Question(
        card_id=e["id"],
        mode="kosakata-id",
        kind="mcq",
        stage=e["stage"],
        freq=e.get("freq"),
        question=f"Mana kata Thai untuk '{e['gloss']}'?",
        options=options,
        options_lang="th",
        answer=answer,
        reveal=f"{e['th']} = {e['phon']} — {e['gloss']}",
        reveal_th=e["th"],
        explain=f"{e['example']['th']} = {e['example']['phon']} — {e['example']['gloss']}",
    )


# ------------------------------------------------------- modul tata bahasa ---

def grammar_question(item: dict) -> Question:
    return Question(
        card_id=item["id"],
        mode="tatabahasa",
        kind="mcq",
        stage=item["stage"],
        question=item["prompt"],
        stimulus_th=item.get("prompt_th"),
        options=list(item["options"]),
        options_lang=item["options_lang"],
        answer=item["answer"],
        reveal=item["options"][item["answer"]],
        explain=item.get("explain"),
        stimulus_label=item["topic_title"],
    )


# -------------------------------------------------------------- modul frasa ---

def phrase_question(p: dict) -> Question:
    return Question(
        card_id=p["id"],
        mode="frasa",
        kind="selfcheck",
        stage=p["stage"],
        question="Bagaimana mengatakan ini dalam bahasa Thailand?",
        stimulus_label=p["gloss"],
        reveal=f"{p['th']} = {p['phon']}"
        + (f"  (harfiah: {p['lit']})" if p.get("lit") else ""),
        reveal_th=p["th"],
        phon=p["phon"],
        explain=p.get("note"),
    )


# ------------------------------------------------------ modul latihan telinga ---

BEDA_LABEL = {
    "panjang": "panjang vokal",
    "hembusan": "hembusan konsonan awal",
    "nada": "nada",
}


def listen_question(card: dict) -> Question:
    """Kartu latihan telinga.

    Di terminal tidak ada bunyi, sehingga kartu ini menjadi latihan
    MENGUCAPKAN: bacalah kata sasaran dan pasangannya berturut-turut dengan
    perbedaan yang tepat, lalu nilai sendiri. Aplikasi web memakai kartu yang
    sama sebagai latihan MENDENGARKAN.
    """
    w = card["word"]
    pasangan = " / ".join(x["th"] for x in card["words"])
    rincian = " · ".join(f"{x['th']} = {x['phon']} ({x['gloss']})" for x in card["words"])
    return Question(
        card_id=card["id"],
        mode="dengar",
        kind="selfcheck",
        stage=card["stage"],
        question=(
            f"Ucapkan kata ini dan pasangannya berturut-turut. Yang membedakan "
            f"keduanya hanya {BEDA_LABEL[card['type']]}."
        ),
        stimulus_th=pasangan,
        stimulus_label=f"kata sasaran: {w['th']}",
        phon=None,
        reveal=rincian,
        reveal_th=w["th"],
        explain=card["note"] or None,
    )


def listen_item_question(item: dict) -> Question:
    return Question(
        card_id=item["id"],
        mode="dengar",
        kind="mcq",
        stage=item["stage"],
        question=item["prompt"],
        stimulus_th=item.get("prompt_th"),
        options=list(item["options"]),
        options_lang=item["options_lang"],
        answer=item["answer"],
        reveal=item["options"][item["answer"]],
        explain=item.get("explain"),
    )


# ------------------------------------------------------ modul kata serumpun ---

RELASI_LABEL = {
    "sama": "artinya sejalan",
    "bergeser": "seasal tetapi artinya sudah bergeser",
    "sebagian": "kata Indonesianya jarang dipakai sehari-hari",
}


def cognate_question(c: dict) -> Question:
    return Question(
        card_id=c["id"],
        mode="serumpun",
        kind="typed",
        stage=c["stage"],
        question="Apa arti kata ini, dan kata Bahasa Indonesia apa yang seasal dengannya?",
        stimulus_th=c["th"],
        phon=c["phon"],
        accepted=expand_accepted(c["gloss"]) + [c["id_word"]],
        reveal=f"{c['phon']} = {c['gloss']}  (seasal dengan '{c['id_word']}', "
               f"{RELASI_LABEL[c['relation']]})",
        explain=c.get("note"),
    )


# ------------------------------------------------------------ modul bacaan ---

#: Pemisah baris beserta lekukannya, dipakai saat menampilkan percakapan
#: utuh pada satu kartu di terminal.
NEWLINE_INDENT = chr(10) + '   '

def text_question(t: dict) -> Question:
    teks = "  ".join(ln["th"] for ln in t["lines"])
    isi = NEWLINE_INDENT.join(
        f"{ln['speaker']}: {ln['th']}  [{ln['phon']}]  {ln['gloss']}"
        for ln in t["lines"]
    )
    return Question(
        card_id=t["id"],
        mode="bacaan",
        kind="selfcheck",
        stage=t["stage"],
        question=(
            f"Bacalah percakapan '{t['title']}' dengan suara, tentukan nadanya, "
            "lalu cocokkan dengan terjemahannya."
        ),
        stimulus_th=teks,
        reveal=NEWLINE_INDENT + isi,
        explain=t.get("note"),
    )


def text_item_question(item: dict) -> Question:
    return Question(
        card_id=item["id"],
        mode="bacaan",
        kind="mcq",
        stage=item["stage"],
        question=item["prompt"],
        stimulus_th=item.get("prompt_th"),
        stimulus_label=item["text_title"],
        options=list(item["options"]),
        options_lang=item["options_lang"],
        answer=item["answer"],
        reveal=item["options"][item["answer"]],
        explain=item.get("explain"),
    )


# -------------------------------------------------------------- kumpulan ---

def build_pool(mode: str, stage: int | None, rng: random.Random) -> list[Question]:
    """Bangun seluruh soal yang tersedia untuk satu mode."""
    if mode == "aksara":
        qs: list[Question] = []
        for c in dataio.consonants(stage):
            qs.append(consonant_name_question(c))
            qs.append(consonant_class_question(c, rng))
        qs += [vowel_question(v) for v in dataio.vowels(stage)]
        qs += [mark_question(m) for m in dataio.marks(stage)]
        qs += [digit_question(d, rng) for d in dataio.digits(stage)]
        qs += [aksara_item_question(i) for i in dataio.aksara_items(stage)]
        return qs
    if mode == "nada":
        qs = [tone_card_question(t) for t in dataio.tones(stage)]
        # Baris aturan tidak punya tahap sendiri di dalam datanya: aturan tanpa
        # tanda nada masuk tahap 1, aturan bertanda nada tahap 2.
        aturan = [tone_rule_question(r, rng) for r in dataio.tone_rules()]
        qs += [q for q in aturan if stage is None or q.stage <= stage]
        qs += [syllable_tone_question(s, rng) for s in dataio.tone_syllables(stage)]
        qs += [minimal_pair_question(mp) for mp in dataio.minimal_pairs(stage)]
        qs += [nada_item_question(i) for i in dataio.nada_items(stage)]
        return qs
    if mode == "kosakata-th":
        return [vocab_th_to_id(e) for e in dataio.vocab_entries(stage)]
    if mode == "kosakata-id":
        pool = dataio.vocab_entries(stage)
        return [vocab_id_to_th(e, pool, rng) for e in pool]
    if mode == "tatabahasa":
        return [grammar_question(i) for i in dataio.grammar_items(stage)]
    if mode == "frasa":
        return [phrase_question(p) for p in dataio.phrases(stage)]
    if mode == "dengar":
        qs = [listen_question(c) for c in dataio.listen_cards(stage)]
        qs += [listen_item_question(i) for i in dataio.listen_items(stage)]
        return qs
    if mode == "serumpun":
        return [cognate_question(c) for c in dataio.cognates(stage)]
    if mode == "bacaan":
        qs = [text_question(t) for t in dataio.texts(stage)]
        qs += [text_item_question(i) for i in dataio.text_items(stage)]
        return qs
    raise ValueError(f"mode tidak dikenal: {mode}")


__all__ = [
    "MODES", "MODE_LABELS", "Question", "accepted_set", "aksara_item_question",
    "build_pool", "consonant_class_question", "consonant_name_question",
    "digit_question", "expand_accepted", "grammar_question", "mark_question",
    "minimal_pair_question", "nada_item_question", "normalize",
    "phrase_question", "syllable_tone_question", "tone_card_question",
    "tone_rule_question", "vocab_detail", "vocab_id_to_th", "vocab_th_to_id",
    "vowel_question", "BEDA_LABEL", "RELASI_LABEL", "cognate_question",
    "listen_item_question", "listen_question", "text_item_question",
    "text_question",
]
