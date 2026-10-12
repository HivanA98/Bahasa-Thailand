"""Aturan nada bahasa Thailand, dihitung dari ejaannya.

Nada sebuah suku kata Thai **tidak** ditentukan oleh tanda nada saja. Nada
adalah hasil empat hal:

1. kelas konsonan awal (tengah, tinggi, atau rendah);
2. jenis suku kata (hidup atau mati);
3. panjang vokal (hanya menentukan pada suku kata mati berkonsonan rendah);
4. tanda nada, bila ada.

Suku kata **mati** (คำตาย): vokal pendek tanpa konsonan akhir, atau berakhir
pada bunyi k, t, p. Suku kata **hidup** (คำเป็น): vokal panjang tanpa
konsonan akhir, atau berakhir pada bunyi ng, n, m, y, w.

Tabel nada tanpa tanda:

| kelas  | hidup  | mati (vokal pendek) | mati (vokal panjang) |
|:-------|:-------|:--------------------|:---------------------|
| tengah | sedang | rendah              | rendah               |
| tinggi | naik   | rendah              | rendah               |
| rendah | sedang | tinggi              | turun                |

Tabel nada dengan tanda:

| kelas  | mai ek | mai tho | mai tri | mai chattawa |
|:-------|:-------|:--------|:--------|:-------------|
| tengah | rendah | turun   | tinggi  | naik         |
| tinggi | rendah | turun   | -       | -            |
| rendah | turun  | tinggi  | -       | -            |

Mai tri dan mai chattawa hampir hanya dipakai pada konsonan kelas tengah.
Pada ejaan Thai baku keduanya tidak dipakai bersama konsonan kelas rendah.

Modul ini mengenal tiga pola ejaan yang tidak dapat dibaca huruf per huruf:
ห nam (หมา dibaca mǎa), อย pada empat kata (อยู่, อย่า, อย่าง, อยาก), dan
ทร yang dibaca s (ทราบ dibaca sâap).

Modul ini juga memuat pembaca suku kata: `parse_syllable` mencocokkan sebuah
suku kata tertulis dengan daftar pola vokal di `VOWEL_PATTERNS`. Ejaan Thai
kadang **bermakna ganda** bila dilihat dari polanya saja (ขวด bisa terbaca
sebagai gugus ขว + vokal o tersirat, atau sebagai ข + vokal ◌ว◌), sehingga
fungsi itu mengembalikan *semua* pembacaan yang mungkin. Pembaca Thai memilih
yang benar dari kosakata, bukan dari aturan; karena itu `tone_of_syllable`
menolak suku kata yang pembacaannya lebih dari satu dan berbeda nadanya.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .thai import (
    CLASS_OF,
    H_LEADABLE,
    HIGH,
    LOW,
    MAI_CHATTAWA,
    MAI_EK,
    MAI_THO,
    MAI_TRI,
    MID,
    O_LEAD,
    TONE_MARKS,
    TRUE_CLUSTERS,
    CONSONANTS,
)

PENDEK, PANJANG = "pendek", "panjang"
HIDUP, MATI = "hidup", "mati"

#: ทร di awal suku kata tidak dibaca thr, melainkan s: ทราบ (sâap, 'tahu'),
#: ทราย (saai, 'pasir'). Kelasnya tetap mengikuti ท, yaitu kelas rendah.
TR_DIGRAPH = "ทร"

# ------------------------------------------------------------ pola vokal ---

#: (id, tampilan, panjang, templat, akhiran tersirat)
#:
#: Templat memakai tiga tempat kosong: {C} konsonan awal, {T} tanda nada
#: (boleh kosong), {F} konsonan akhir. Urutan daftar ini adalah urutan
#: pencocokan, dari pola yang paling khas ke pola yang paling umum.
_VOWEL_ROWS = [
    # --- vokal khusus: pendek tetapi berakhiran nyaring, jadi suku hidup ---
    ("ia_s",   "เ◌ียะ", PENDEK,  "เ{C}ี{T}ยะ", None),
    ("uea_s",  "เ◌ือะ", PENDEK,  "เ{C}ื{T}อะ", None),
    ("ua_s",   "◌ัวะ",  PENDEK,  "{C}ั{T}วะ",  None),
    ("oe_s",   "เ◌อะ",  PENDEK,  "เ{C}{T}อะ",  None),
    ("aw_s",   "เ◌าะ",  PENDEK,  "เ{C}{T}าะ",  None),
    ("ia_l_f", "เ◌ีย◌", PANJANG, "เ{C}ี{T}ย{F}", None),
    ("ia_l",   "เ◌ีย",  PANJANG, "เ{C}ี{T}ย",  None),
    ("uea_l_f","เ◌ือ◌", PANJANG, "เ{C}ื{T}อ{F}", None),
    ("uea_l",  "เ◌ือ",  PANJANG, "เ{C}ื{T}อ",  None),
    ("oe_l",   "เ◌อ",   PANJANG, "เ{C}{T}อ",   None),
    ("oe_l_f", "เ◌ิ◌",  PANJANG, "เ{C}ิ{T}{F}", None),
    ("e_s_f",  "เ◌็◌",  PENDEK,  "เ{C}็{T}{F}", None),
    ("e_s",    "เ◌ะ",   PENDEK,  "เ{C}{T}ะ",   None),
    ("ao",     "เ◌า",   PENDEK,  "เ{C}{T}า",   "w"),
    ("e_l_f",  "เ◌◌",   PANJANG, "เ{C}{T}{F}", None),
    ("e_l",    "เ◌",    PANJANG, "เ{C}{T}",    None),
    ("ae_s_f", "แ◌็◌",  PENDEK,  "แ{C}็{T}{F}", None),
    ("ae_s",   "แ◌ะ",   PENDEK,  "แ{C}{T}ะ",   None),
    ("ae_l_f", "แ◌◌",   PANJANG, "แ{C}{T}{F}", None),
    ("ae_l",   "แ◌",    PANJANG, "แ{C}{T}",    None),
    ("o_s",    "โ◌ะ",   PENDEK,  "โ{C}{T}ะ",   None),
    ("o_l_f",  "โ◌◌",   PANJANG, "โ{C}{T}{F}", None),
    ("o_l",    "โ◌",    PANJANG, "โ{C}{T}",    None),
    ("ai_sai", "ไ◌",    PENDEK,  "ไ{C}{T}",    "y"),
    ("ai_mai", "ใ◌",    PENDEK,  "ใ{C}{T}",    "y"),
    # --- vokal yang ditulis sesudah atau di atas konsonan ---
    ("ue_l_f", "◌ื◌",   PANJANG, "{C}ื{T}{F}",  None),
    ("ue_l",   "◌ือ",   PANJANG, "{C}ื{T}อ",   None),
    ("ue_s_f", "◌ึ◌",   PENDEK,  "{C}ึ{T}{F}", None),
    ("ue_s",   "◌ึ",    PENDEK,  "{C}ึ{T}",    None),
    ("i_l_f",  "◌ี◌",   PANJANG, "{C}ี{T}{F}", None),
    ("i_l",    "◌ี",    PANJANG, "{C}ี{T}",    None),
    ("i_s_f",  "◌ิ◌",   PENDEK,  "{C}ิ{T}{F}", None),
    ("i_s",    "◌ิ",    PENDEK,  "{C}ิ{T}",    None),
    ("u_l_f",  "◌ู◌",   PANJANG, "{C}ู{T}{F}", None),
    ("u_l",    "◌ู",    PANJANG, "{C}ู{T}",    None),
    ("u_s_f",  "◌ุ◌",   PENDEK,  "{C}ุ{T}{F}", None),
    ("u_s",    "◌ุ",    PENDEK,  "{C}ุ{T}",    None),
    ("am",     "◌ำ",    PENDEK,  "{C}{T}ำ",    "m"),
    ("ua_l_f", "◌ว◌",   PANJANG, "{C}{T}ว{F}", None),
    ("ua_l",   "◌ัว",   PANJANG, "{C}ั{T}ว",   None),
    ("a_s_f",  "◌ั◌",   PENDEK,  "{C}ั{T}{F}", None),
    ("a_l_f",  "◌า◌",   PANJANG, "{C}{T}า{F}", None),
    ("a_l",    "◌า",    PANJANG, "{C}{T}า",    None),
    ("a_s",    "◌ะ",    PENDEK,  "{C}{T}ะ",    None),
    ("aw_l_f", "◌อ◌",   PANJANG, "{C}{T}อ{F}", None),
    ("aw_l",   "◌อ",    PANJANG, "{C}{T}อ",    None),
    # Vokal o pendek yang tidak ditulis sama sekali: dua konsonan berdempet
    # dibaca dengan vokal o di antaranya (คน kon, นก nók).
    ("o_s_f",  "◌◌",    PENDEK,  "{C}{T}{F}",  None),
    # Satu konsonan berdiri sendiri sebagai suku kata: vokal a pendek yang
    # tidak ditulis. Ini suku kata awal pada pola aksara nam (ขนม khà-nǒm,
    # ตลาด tà-làat, สบาย sà-baai).
    ("a_s_dalam", "◌",  PENDEK,  "{C}{T}",     None),
]

VOWEL_PATTERNS: dict[str, dict] = {
    row[0]: {
        "id": row[0],
        "display": row[1],
        "length": row[2],
        "template": row[3],
        "inherent_final": row[4],
        "has_final": "{F}" in row[3],
    }
    for row in _VOWEL_ROWS
}

# ----------------------------------------------------------------- regex ---

_CONS = "[ก-ฮ]"
_INIT_ALTS = (
    [f"ห[{''.join(H_LEADABLE)}]", O_LEAD, TR_DIGRAPH]
    + list(TRUE_CLUSTERS)
    + [_CONS]
)
_INIT = "(?:" + "|".join(_INIT_ALTS) + ")"
_TONE = f"[{''.join(TONE_MARKS)}]?"


def _compile(template: str) -> re.Pattern:
    pattern = (
        re.escape(template)
        .replace(re.escape("{C}"), f"(?P<init>{_INIT})")
        .replace(re.escape("{T}"), f"(?P<mark>{_TONE})")
        .replace(re.escape("{F}"), f"(?P<final>{_CONS})")
    )
    return re.compile("^" + pattern + "$")


_COMPILED = [(vid, _compile(v["template"])) for vid, v in VOWEL_PATTERNS.items()]


# ------------------------------------------------------------ suku kata ---


@dataclass(frozen=True)
class Syllable:
    """Hasil pembacaan satu suku kata tertulis."""

    text: str
    initial: str          # huruf (atau gugus) konsonan awal apa adanya
    consonant: str        # huruf yang menentukan kelas
    cls: str              # 'tengah' | 'tinggi' | 'rendah'
    vowel: str            # id pola vokal
    length: str           # 'pendek' | 'panjang'
    final: str | None     # huruf konsonan akhir, bila ditulis
    final_sound: str | None
    mark: str | None      # tanda nada
    kind: str             # 'hidup' | 'mati'
    tone: str

    @property
    def vowel_display(self) -> str:
        return VOWEL_PATTERNS[self.vowel]["display"]


def class_of_initial(initial: str) -> tuple[str, str]:
    """Kembalikan (huruf penentu kelas, kelas) untuk sebuah konsonan awal.

    * ห + konsonan kelas rendah: ห tidak dibunyikan, kelasnya menjadi tinggi.
    * อย: kelasnya tengah.
    * gugus sejati (กร, ปล, ...): kelas diambil dari huruf pertama.
    """
    if len(initial) == 2 and initial[0] == "ห" and initial[1] in H_LEADABLE:
        return initial[0], HIGH
    if initial == O_LEAD:
        return "อ", MID
    if initial == TR_DIGRAPH:
        return "ท", LOW
    return initial[0], CLASS_OF[initial[0]]


def tone_from_parts(cls: str, kind: str, length: str, mark: str | None) -> str:
    """Nada sebuah suku kata dari empat penentunya. Inilah inti aturannya."""
    if cls not in (MID, HIGH, LOW):
        raise ValueError(f"kelas konsonan tidak dikenal: {cls!r}")
    if mark is None:
        if kind == MATI:
            if cls == LOW:
                return "tinggi" if length == PENDEK else "turun"
            return "rendah"
        return "naik" if cls == HIGH else "sedang"
    if mark == MAI_EK:
        return "turun" if cls == LOW else "rendah"
    if mark == MAI_THO:
        return "tinggi" if cls == LOW else "turun"
    if mark == MAI_TRI:
        return "tinggi"
    if mark == MAI_CHATTAWA:
        return "naik"
    raise ValueError(f"tanda nada tidak dikenal: {mark!r}")


def syllable_kind(vowel_id: str, final: str | None) -> str:
    """Hidup atau mati, dari pola vokal dan konsonan akhirnya."""
    v = VOWEL_PATTERNS[vowel_id]
    if final:
        sound = CONSONANTS[final]["final"]
        if sound in ("k", "t", "p"):
            return MATI
        if sound is None:
            # Huruf seperti ห atau อ tidak pernah menjadi konsonan akhir.
            raise ValueError(f"{final} tidak dipakai sebagai konsonan akhir")
        return HIDUP
    if v["inherent_final"]:
        return HIDUP
    return HIDUP if v["length"] == PANJANG else MATI


def parse_syllable(text: str) -> list[Syllable]:
    """Semua pembacaan yang mungkin untuk satu suku kata tertulis.

    Daftar kosong berarti pola suku kata itu tidak dikenali modul ini.
    """
    out: list[Syllable] = []
    for vid, rx in _COMPILED:
        m = rx.match(text)
        if not m:
            continue
        initial = m.group("init")
        mark = m.group("mark") or None
        final = m.groupdict().get("final")
        if final and CONSONANTS[final]["final"] is None:
            continue
        cons, cls = class_of_initial(initial)
        try:
            kind = syllable_kind(vid, final)
        except ValueError:
            continue
        v = VOWEL_PATTERNS[vid]
        out.append(
            Syllable(
                text=text,
                initial=initial,
                consonant=cons,
                cls=cls,
                vowel=vid,
                length=v["length"],
                final=final,
                final_sound=CONSONANTS[final]["final"] if final else v["inherent_final"],
                mark=mark,
                kind=kind,
                tone=tone_from_parts(cls, kind, v["length"], mark),
            )
        )
    return out


def tones_of_syllable(text: str) -> set[str]:
    """Himpunan nada dari semua pembacaan yang mungkin."""
    return {s.tone for s in parse_syllable(text)}


def tone_of_syllable(text: str) -> str:
    """Nada satu suku kata tertulis.

    Melempar ValueError bila pola suku katanya tidak dikenali, atau bila
    pembacaannya lebih dari satu dengan nada yang berbeda.
    """
    readings = parse_syllable(text)
    if not readings:
        raise ValueError(f"pola suku kata tidak dikenali: {text!r}")
    tones = {s.tone for s in readings}
    if len(tones) > 1:
        rincian = ", ".join(f"{s.vowel}:{s.tone}" for s in readings)
        raise ValueError(f"pembacaan {text!r} lebih dari satu dan berbeda nada ({rincian})")
    return readings[0].tone


#: Konsonan nyaring kelas rendah yang bisa "dipimpin" oleh konsonan kelas
#: tinggi atau tengah pada pola aksara nam.
NAM_FOLLOWERS = H_LEADABLE


def parse_word(syllables: list[str]) -> list[Syllable]:
    """Baca sebuah kata yang sudah dipecah menjadi suku kata tertulis.

    Berbeda dari `parse_syllable`, fungsi ini menerapkan satu aturan yang
    hanya berlaku di dalam kata, yaitu **aksara nam** (อักษรนำ): bila suku
    kata pertama hanya berupa satu konsonan kelas tinggi atau tengah (vokal a
    pendek yang tidak ditulis), dan suku kata berikutnya dimulai dengan satu
    konsonan nyaring kelas rendah, maka nada suku kata kedua mengikuti kelas
    konsonan pemimpinnya.

        ขนม  = ข + นม  -> khà-nǒm   (นม ikut kelas tinggi ข, bukan rendah น)
        ตลาด = ต + ลาด -> tà-làat   (ลาด ikut kelas tengah ต)
        สนุก = ส + นุก -> sà-nùk

    Melempar ValueError bila ada suku kata yang tidak terbaca atau yang
    pembacaannya berbeda nada.
    """
    out: list[Syllable] = []
    for s in syllables:
        readings = parse_syllable(s)
        if not readings:
            raise ValueError(f"pola suku kata tidak dikenali: {s!r}")
        tones = {r.tone for r in readings}
        if len(tones) > 1:
            rincian = ", ".join(f"{r.vowel}:{r.tone}" for r in readings)
            raise ValueError(f"suku kata {s!r} berbeda nada antarpembacaan ({rincian})")
        out.append(readings[0])

    for i in range(len(out) - 1):
        leader, follower = out[i], out[i + 1]
        if leader.vowel != "a_s_dalam" or leader.cls == LOW:
            continue
        if len(follower.initial) != 1 or follower.initial not in NAM_FOLLOWERS:
            continue
        out[i + 1] = Syllable(
            **{
                **follower.__dict__,
                "cls": leader.cls,
                "tone": tone_from_parts(
                    leader.cls, follower.kind, follower.length, follower.mark
                ),
            }
        )
    return out


MARK_NAME = {
    MAI_EK: "mai ek",
    MAI_THO: "mai tho",
    MAI_TRI: "mai tri",
    MAI_CHATTAWA: "mai chattawa",
}


def explain(s: Syllable) -> str:
    """Satu kalimat bahasa Indonesia yang menerangkan asal nadanya."""
    if len(s.initial) == 2 and s.initial[0] == "ห":
        awal = (
            f"ห nam di depan {s.initial[1]} (ห tidak dibunyikan) sehingga kelasnya "
            f"menjadi {s.cls}"
        )
    elif s.initial == O_LEAD:
        awal = "อย berkelas tengah (hanya pada empat kata)"
    elif s.initial == TR_DIGRAPH:
        awal = "ทร dibaca s, kelasnya mengikuti ท yaitu kelas rendah"
    elif len(s.initial) == 2:
        awal = f"gugus {s.initial}, kelasnya mengikuti {s.consonant} yaitu kelas {s.cls}"
    else:
        awal = f"{s.consonant} kelas {s.cls}"

    bagian = [awal, f"vokal {s.vowel_display} {s.length}"]
    if s.final:
        bunyi = CONSONANTS[s.final]["final"]
        bagian.append(f"berakhiran {s.final} (bunyi -{bunyi}) sehingga suku kata {s.kind}")
    else:
        bagian.append(f"tanpa konsonan akhir sehingga suku kata {s.kind}")
    bagian.append(f"bertanda {MARK_NAME[s.mark]}" if s.mark else "tanpa tanda nada")
    return " + ".join(bagian) + f" → nada {s.tone}."


__all__ = [
    "HIDUP", "MATI", "PANJANG", "PENDEK", "Syllable", "VOWEL_PATTERNS",
    "class_of_initial", "explain", "parse_syllable", "syllable_kind",
    "TR_DIGRAPH", "tone_from_parts", "tone_of_syllable", "tones_of_syllable",
]
