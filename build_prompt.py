#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_prompt.py — Ghép prompt sinh ảnh cho 1 lá bài Tarot theo chuẩn "Sensual Tarot 78".

Nguồn dữ liệu (xem WORKFLOW.md):
  1. tarot prompt/cards.json         -> TITLE, EMBLEM, SCENE, count-lock, fallback spec
  2. tarot prompt/01-CARD-TABLE.md   -> CHARACTER_SPECIFICATION (bang chuan 72 nhan vat)
  3. tarot prompt/template.md        -> Master prompt template (5 placeholder)

Cách dùng:
  python3 build_prompt.py 03-empress                 # in prompt ra stdout
  python3 build_prompt.py 03-empress -o empress.txt  # ghi ra file
  python3 build_prompt.py --list                     # liệt kê 78 slug
  python3 build_prompt.py --all -d prompts/          # sinh 78 file prompt
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPT_DIR = ROOT / "tarot prompt"
CARDS_JSON = PROMPT_DIR / "cards.json"
CARD_TABLE = PROMPT_DIR / "01-CARD-TABLE.md"
TEMPLATE_MD = PROMPT_DIR / "template.md"

# count = null trong cards.json  ->  "no suit objects" COUNT LOCK (theo meta.note)
NO_SUIT_LOCK = (
    "COUNT LOCK (HARD): this card shows NO suit objects anywhere — "
    "no wands, no chalices, no swords and no coins; do not invent any."
)


def load_cards() -> dict:
    data = json.loads(CARDS_JSON.read_text(encoding="utf-8"))
    return {c["slug"]: c for c in data["cards"]}


def load_specs() -> dict:
    """Parse bảng markdown trong 01-CARD-TABLE.md -> {slug: {...}}.

    Dòng dữ liệu có dạng:
      | **[A]** **THE FOOL** `00-fool` | 19 | <mắt> | <tóc> | <dáng> | <da> | <nét riêng> | <không khí> |
    """
    specs = {}
    slug_re = re.compile(r"`([^`]+)`")
    for line in CARD_TABLE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 8:
            continue
        m = slug_re.search(cells[0])
        if not m:
            continue  # dòng header / phân bố A–D
        slug = m.group(1)
        specs[slug] = {
            "age": cells[1],
            "eyes": cells[2],
            "hair": cells[3],
            "build": cells[4],
            "skin": cells[5],
            "signature": cells[6],
            "aura": cells[7],
        }
    return specs


def md_clean(text: str) -> str:
    """Gỡ markdown nhẹ (bold **) khỏi chuỗi lấy từ bảng."""
    return text.replace("**", "").strip()


def count_lock(card: dict) -> str:
    c = card.get("count")
    if not c:
        return NO_SUIT_LOCK
    layout = c["layout"].strip()
    if "exactly" in layout.lower():
        return f"COUNT LOCK (HARD): {layout}"
    return f"COUNT LOCK (HARD): exactly {c['n']} {c['obj']}. {layout}"


def character_spec(card: dict, spec: dict | None) -> str:
    # 6 lá vật thể thuần (femme=false): không nhân vật
    if not card.get("femme", True):
        return "There is no character on this card — a pure object scene."
    parts = []
    if spec:
        age = md_clean(spec["age"])
        parts.append(
            f"The woman is {age} years old, {md_clean(spec['build'])}, "
            f"with {md_clean(spec['hair'])}."
        )
        parts.append(
            f"Her eyes: {md_clean(spec['eyes'])}. "
            f"Skin tone: {md_clean(spec['skin'])} (a light tone only — never dark, never deep)."
        )
        parts.append(
            f"Her one signature detail: {md_clean(spec['signature'])}. "
            f"Mood and aura: {md_clean(spec['aura'])}."
        )
    else:  # fallback: chỉ dùng cards.json
        bits = [card.get("age"), card.get("build")]
        if card.get("hair"):
            bits.append(f"hair: {card['hair']}")
        parts.append("The character: " + ", ".join(b for b in bits if b) + ".")
    if card.get("allure"):
        parts.append(card["allure"].strip())
    return " ".join(parts)


def build_prompt(slug: str, cards: dict, specs: dict) -> str:
    if slug not in cards:
        raise KeyError(f"Không tìm thấy slug '{slug}' trong cards.json")
    card = cards[slug]
    prompt = TEMPLATE_MD.read_text(encoding="utf-8")
    prompt = prompt.replace("{TITLE}", card["title"])
    prompt = prompt.replace("{EMBLEM}", card["emblem"])
    prompt = prompt.replace("{SCENE}", card["scene"].strip())
    prompt = prompt.replace(
        "{CHARACTER_SPECIFICATION}", character_spec(card, specs.get(slug))
    )
    prompt = prompt.replace("{COUNT_LOCK}", count_lock(card))
    return prompt


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", nargs="?", help="slug lá bài, vd: 03-empress, wands-ace")
    ap.add_argument("-o", "--out", help="ghi prompt ra file thay vì stdout")
    ap.add_argument("--list", action="store_true", help="liệt kê 78 slug và thoát")
    ap.add_argument("--all", action="store_true", help="sinh prompt cho cả 78 lá")
    ap.add_argument("-d", "--outdir", default="prompts",
                    help="thư mục output khi dùng --all (mặc định: prompts/)")
    args = ap.parse_args()

    cards = load_cards()
    specs = load_specs()

    if args.list:
        for slug in cards:
            tag = "nhân vật" if cards[slug].get("femme") else "vật thể "
            lock = "no-suit" if not cards[slug].get("count") else f"n={cards[slug]['count']['n']}"
            print(f"{slug:<22} [{tag}] [{lock}]  {cards[slug]['title']}")
        return 0

    if args.all:
        outdir = Path(args.outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        for slug in cards:
            (outdir / f"{slug}.txt").write_text(
                build_prompt(slug, cards, specs) + "\n", encoding="utf-8")
        print(f"Đã sinh {len(cards)} prompt vào {outdir}/")
        return 0

    if not args.slug:
        ap.error("cần truyền slug (hoặc --list / --all)")

    prompt = build_prompt(args.slug, cards, specs)
    if args.out:
        Path(args.out).write_text(prompt + "\n", encoding="utf-8")
        print(f"Đã ghi {args.out}")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
