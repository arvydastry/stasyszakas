#!/usr/bin/env python3
"""Iš apkarpytų paveikslų ir katalogo įrašų paruošia svetainės vaizdus ir _data/works.json.

Naudojimas:
    python3 -P _tools/prepare_images.py <catalog_dir> [--no-images] [--report]

    <catalog_dir>   aplankas su katalogo JSON failais (L1.json, M1.json ...), kuriuos sukūrė karpymo agentai;
                    įrašuose "cropFile" rodo į pilnos raiškos apkarpytą paveikslą.
    --no-images     perrašo tik _data/works.json ir _brief/MEDIA.md (vaizdų nekeičia)
    --report        tik išspausdina santrauką, nieko nerašo

Kuravimas: _data/curation.json (redaguojamas ranka):
    exclude    [idx, ...]              nerodomi darbai
    featured   [idx, ...]              pradžios puslapio sluoksniuotos kortelės (eilės tvarka)
    hero       idx                     pradžios hero paveikslas (tik informacijai; slug rašomas į site.json)
    poems      [idx, ...]              eilių puslapio tvarka
    covers     {"peizazas": idx, ...}  kategorijų plytelių viršeliai
    first      [idx, ...]              darbai, kurie galerijoje eina pirmi (tokia tvarka)
    overrides  {"<idx>": {laukai}}     pataisymai: title, titled, technique, technique_stated, size, desc,
                                       category, sale, focus, slug, poem, poem_title

Rezultatas:
    assets/img/works/<slug>-480.jpg, -960.jpg, -1600.jpg   (tik mažinama, niekada nedidinama)
    _originals/works/<slug>.jpg                             pilna apkarpyto paveikslo kopija
    _data/works.json                                        katalogas maketui (žr. build.py work_view)
    _brief/MEDIA.md                                         šaltinių ir pataisymų lentelė
Reikia Pillow (pip install pillow). Paleisti su -P.
"""
import datetime
import glob
import json
import pathlib
import re
import shutil
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_IMG = ROOT / "assets" / "img" / "works"
OUT_ORIG = ROOT / "_originals" / "works"
DATA = ROOT / "_data"

LT_MAP = str.maketrans("ąčęėįšųūžĄČĘĖĮŠŲŪŽ", "aceeisuuzACEEISUUZ")
CAT_ORDER = ["peizazas", "jura", "miestas", "geles", "portretas", "kita"]


def slugify(text):
    t = text.translate(LT_MAP)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t[:60].strip("-") or "darbas"


def clean_title(t):
    t = (t or "").strip()
    t = re.sub(r"\s+", " ", t)
    t = t.strip(' "„“”')
    t = re.sub(r"\s*\.$", "", t) if not t.endswith("...") else t
    return t


def norm_size(s):
    s = (s or "").strip()
    s = re.sub(r"\s*[xX×]\s*", " × ", s)
    return s


def load_records(cat_dir):
    recs = []
    for f in sorted(glob.glob(str(pathlib.Path(cat_dir) / "[A-Z][0-9]*.json"))):
        d = json.loads(pathlib.Path(f).read_text(encoding="utf-8"))
        d = d if isinstance(d, list) else d.get("records", [])
        for r in d:
            r["_batch"] = pathlib.Path(f).stem
        recs += d
    return recs


def order_works(works, first):
    """Stipriausi pirmi, bet kaimynai skirtingų kategorijų ir, jei pavyksta, skirtingo šviesumo."""
    head = [w for i in first for w in works if w["id"] == i]
    rest = [w for w in works if w["id"] not in set(first)]
    rest.sort(key=lambda w: (-w["strength"], -w["quality"], -(1 if w["titled"] else 0), w["id"]))
    out = list(head)
    pool = rest
    while pool:
        last = out[-2:] if out else []
        best, best_score = None, None
        for k, w in enumerate(pool[:14]):  # žiūrime tik į artimiausius pagal reitingą
            score = -k * 1.0
            if any(w["category"] == p["category"] for p in last[-1:]):
                score -= 6
            if len(last) == 2 and all(w["category"] == p["category"] for p in last):
                score -= 8
            if last and abs(w["lum"] - last[-1]["lum"]) < 18:
                score -= 1.5
            if best_score is None or score > best_score:
                best, best_score = k, score
        out.append(pool.pop(best))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        raise SystemExit(__doc__)
    cur_path = DATA / "curation.json"
    cur = json.loads(cur_path.read_text(encoding="utf-8")) if cur_path.exists() else {}
    exclude = set(cur.get("exclude", []))
    overrides = {int(k): v for k, v in cur.get("overrides", {}).items()}
    featured = cur.get("featured", [])
    poems = cur.get("poems", [])
    covers = {v: k for k, v in cur.get("covers", {}).items()}

    recs = load_records(args[0])
    keepers = [r for r in recs if r.get("isArtwork") and not r.get("duplicateOf") and r.get("cropFile")]
    dup_of = {}
    for r in recs:
        if r.get("duplicateOf"):
            dup_of.setdefault(r["duplicateOf"], []).append(r)

    works, used_slugs, media_rows, skipped = [], set(), [], []
    for r in sorted(keepers, key=lambda r: r["idx"]):
        idx = r["idx"]
        if idx in exclude:
            skipped.append((idx, "exclude"))
            continue
        src = pathlib.Path(r["cropFile"])
        if not src.exists():
            skipped.append((idx, "nėra failo"))
            continue
        o = overrides.get(idx, {})
        titled = o.get("titled", r.get("titleSource") == "author")
        title_raw = r.get("title", "")
        title = clean_title(o.get("title", title_raw if titled else ""))
        working = clean_title(r.get("title", "")) if r.get("titleSource") != "author" else ""
        tech_stated = o.get("technique_stated", r.get("techniqueSource") == "author")
        technique = o.get("technique", r.get("technique", ""))
        desc = o.get("desc", r.get("descriptionLt", "")).strip()
        slug = o.get("slug") or slugify(title if titled and title else (working or desc or "darbas"))
        base, n = slug, 2
        while slug in used_slugs:
            slug = f"{base}-{n}"
            n += 1
        used_slugs.add(slug)
        posted = r.get("postedDate", "")
        w = {
            "id": idx, "slug": slug,
            "title": title, "titled": bool(titled and title), "working_title": working,
            "desc": desc,
            "category": o.get("category", r.get("category", "kita")),
            "technique": technique, "technique_stated": bool(tech_stated and technique),
            "size": norm_size(o.get("size", r.get("size", ""))),
            "posted": posted, "year": int(posted[:4]) if posted[:4].isdigit() else None,
            "signature": r.get("signature", ""),
            "poem": o.get("poem", r.get("poem", "")), "poem_title": o.get("poem_title", r.get("poemTitle", "")),
            "sale": o.get("sale", r.get("saleNote", "")),
            "palette": r.get("palette", [])[:6], "lum": int(r.get("luminance") or 0),
            "quality": int(r.get("quality") or 0), "strength": int(r.get("strength") or 0), "hero_fit": int(r.get("heroFit") or 0),
            "featured": featured.index(idx) + 1 if idx in featured else 0,
            "poem_pick": poems.index(idx) + 1 if idx in poems else 0,
            "cover": 9 if idx in covers else 0,
            "focus": o.get("focus", ""),
            "framed": bool(r.get("framedInPhoto")),
            "fb": r.get("fbUrl", ""),
            "_src": str(src), "_caption": r.get("authorCaption", ""), "_raw_title": title_raw,
            "_dups": [d["idx"] for d in dup_of.get(idx, [])],
            "_dup_captions": [d.get("authorCaption", "") for d in dup_of.get(idx, []) if d.get("authorCaption")],
            "_issues": r.get("issues", []),
        }
        works.append(w)

    works = order_works(works, cur.get("first", []))

    if "--report" in flags:
        import collections
        print("darbų:", len(works), "praleista:", skipped)
        print("kategorijos:", dict(collections.Counter(w["category"] for w in works)))
        print("su autoriaus pavadinimu:", sum(1 for w in works if w["titled"]), "su eilėmis:", sum(1 for w in works if w["poem"]))
        return

    if "--no-images" not in flags:
        from PIL import Image, ImageOps
        OUT_IMG.mkdir(parents=True, exist_ok=True)
        OUT_ORIG.mkdir(parents=True, exist_ok=True)
        keep_files = set()
        for w in works:
            im = ImageOps.exif_transpose(Image.open(w["_src"])).convert("RGB")
            W, H = im.size
            w["w"], w["h"] = W, H
            variants = {}
            for name, kind, limit, q in (("1600", "long", 1600, 84), ("960", "width", 960, 82), ("480", "width", 480, 80)):
                s = min(1.0, limit / (max(W, H) if kind == "long" else W))
                size = (max(1, round(W * s)), max(1, round(H * s)))
                out = OUT_IMG / f'{w["slug"]}-{name}.jpg'
                (im if s == 1.0 else im.resize(size, Image.LANCZOS)).save(out, "JPEG", quality=q, optimize=True, progressive=True)
                variants[name] = size[0]
                keep_files.add(out.name)
            w["src_w"] = variants
            shutil.copyfile(w["_src"], OUT_ORIG / f'{w["slug"]}.jpg')
        for old in OUT_IMG.glob("*.jpg"):
            if old.name not in keep_files:
                old.unlink()
        keep_orig = {f'{w["slug"]}.jpg' for w in works}
        for old in OUT_ORIG.glob("*.jpg"):
            if old.name not in keep_orig:
                old.unlink()
    else:
        prev = {w["slug"]: w for w in json.loads((DATA / "works.json").read_text(encoding="utf-8"))} if (DATA / "works.json").exists() else {}
        for w in works:
            p = prev.get(w["slug"])
            if not p:
                raise SystemExit(f'--no-images: naujas darbas {w["slug"]} dar neturi vaizdų; paleiskite be --no-images')
            w["w"], w["h"], w["src_w"] = p["w"], p["h"], p["src_w"]

    public = [{k: v for k, v in w.items() if not k.startswith("_")} for w in works]
    DATA.mkdir(exist_ok=True)
    (DATA / "works.json").write_text(json.dumps(public, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    # MEDIA.md: šaltiniai ir pataisymai
    lines = [
        "# Darbų šaltiniai ir katalogo pastabos", "",
        f"Sugeneruota {datetime.date.today().isoformat()} įrankiu `_tools/prepare_images.py`. Visi paveikslai paimti iš viešos autoriaus Facebook paskyros",
        "(https://www.facebook.com/stasys599), apkarpyti iki paveikslo krašto (be rėmų, paspartu ir datos žymų).", "",
        "- **Pavadinimas**: rodomas tik autoriaus užrašytas. „Be pavadinimo“ reiškia, kad prie nuotraukos pavadinimo nebuvo; skliaustuose darbinis aprašas (svetainėje nerodomas kaip pavadinimas).",
        "- **Technika, dydis**: tik jei nurodė autorius; „(spėjama)“ žymi agento spėjimą, svetainėje jis nerodomas.",
        "- **Paskelbta**: Facebook įrašo data, nebūtinai sukūrimo metai.", "",
        "| Nr. | Pavadinimas svetainėje | Autoriaus įrašas prie nuotraukos | Technika | Dydis | Paskelbta | Kokybė | Šaltinis |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for w in sorted(works, key=lambda w: w["id"]):
        shown = w["title"] if w["titled"] else f'Be pavadinimo ({w["working_title"] or "be aprašo"})'
        cap = " / ".join([c for c in [w["_caption"]] + w["_dup_captions"] if c]).replace("\n", " / ").replace("|", "/")
        cap = (cap[:150] + "…") if len(cap) > 150 else cap
        tech = w["technique"] + ("" if w["technique_stated"] else " (spėjama)") if w["technique"] else ""
        px = f'{w.get("w", "?")}×{w.get("h", "?")} px, {w["quality"]}/5'
        lines.append(f'| {w["id"]} | {shown} | {cap} | {tech} | {w["size"]} | {w["posted"]} | {px} | [FB]({w["fb"]}) |')
    (ROOT / "_brief").mkdir(exist_ok=True)
    (ROOT / "_brief" / "MEDIA.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"darbų: {len(works)}; praleista: {skipped}; works.json ir MEDIA.md įrašyti" + ("" if "--no-images" in flags else f"; vaizdų: {len(works) * 3}"))


if __name__ == "__main__":
    main()
