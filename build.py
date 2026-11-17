#!/usr/bin/env python3
"""Stasio Zako svetainės demo maketas: surenka puslapius iš _parts/ + _body/ + _templates/ + _data/.

Naudojimas:
    python3 build.py            surenka visus puslapius (rašo tik pasikeitusius failus)
    python3 build.py --check    tik patikra, nieko nerašo

Reikia tik python3 (standartinė biblioteka).

ŠALTINIAI
    _parts/head.html, header.html, footer.html, scripts.html   bendros dalys
    _body/<vardas>.html      puslapio turinys; PIRMA eilutė yra meta komentaras su JSON:
                             <!--meta {"title": "...", "description": "...", "nav": "kuryba",
                                       "css": ["p-kuryba.css"], "js": ["p-kuryba.js"], "body_class": "page-kuryba",
                                       "header": "transparent", "og_image": "assets/img/works/x-1600.jpg"} -->
    _templates/darbas.html   vieno darbo puslapio šablonas -> kuryba/<slug>.html (kiekvienam _data/works.json įrašui)
    _templates/*.html        pasikartojančių elementų šablonai (žr. BLOKAI)
    _data/works.json         darbų katalogas (generuoja _tools/prepare_images.py; ranka neredaguoti)
    _data/site.json          autoriaus duomenys, parodos, biografijos faktai, kontaktai

ŽYMĖS (galioja _parts, _body ir _templates failuose)
    {{root}}                  kelias iki projekto šaknies ("" šaknies puslapiams, "../" kuryba/ puslapiams)
    {{title}} {{description}} {{body_class}} {{header_mode}} {{og_image}} {{page}} {{year}}
    {{css_links}} {{js_links}}   puslapio papildomi CSS / JS (tik head.html / scripts.html)
    {{nav:raktas}}            " is-active", jei puslapio meta "nav" == raktas, kitaip ""
    {{site.kelias.iki.reiksmes}}   reikšmė iš _data/site.json (taškais atskirtas kelias; sąrašo elementas - skaičiumi)
    {{count:all}} {{count:peizazas}} ...   darbų skaičius (visų arba kategorijos)
    {{block:vardas}} / {{block:vardas:arg}}   sugeneruotas elementų sąrašas (žr. BLOKAI)

BLOKAI ({{block:...}}) - kiekvienam elementui pritaikomas šablonas iš _templates/
    works_grid            visi darbai                        -> card.html          (kintamasis w)
    featured_stack        darbai su featured > 0, pagal eilę  -> stack-item.html    (w)
    home_grid:N           pirmi N darbų, kurie nėra featured  -> card.html          (w)
    filters               kategorijos su darbų skaičiumi      -> filter.html        (c)
    category_tiles        kategorijos su viršelio darbu       -> category-tile.html (c)
    poems                 darbai su eilėmis (poem_pick > 0)   -> poem.html          (w)
    exhibitions           site.json "exhibitions"             -> list-row.html      (e)
    timeline              site.json "timeline"                -> timeline-row.html  (e)
    related               (tik darbas.html) 3 tos pačios kategorijos darbai -> card.html (w)
    list:kelias:sablonas  bet kuris site.json sąrašas pagal kelią -> _templates/<sablonas>.html (e)

ELEMENTO ŽYMĖS šablonuose
    {{w.laukas}} {{c.laukas}} {{e.laukas}}   reikšmė (HTML ekranuojama; laukai, kurių vardas baigiasi _html, įterpiami kaip yra)
    {{i}} eilės numeris nuo 1, {{i0}} nuo 0, {{i2}} dviženklis ("01")
    <!--if w.laukas--> ... <!--/if-->           rodoma, jei laukas netuščias
    <!--unless w.laukas--> ... <!--/unless-->   rodoma, jei laukas tuščias
    darbas.html šablone tie patys {{w.*}} ir sąlygos galioja visam puslapiui; papildomai
    {{prev.url}} {{prev.title_display}} {{next.url}} {{next.title_display}}.

DARBO (w) LAUKAI: žr. work_view() žemiau ir _brief/COMPONENTS.md.
"""
import datetime
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PARTS = ROOT / "_parts"
BODY = ROOT / "_body"
TPL = ROOT / "_templates"
DATA = ROOT / "_data"
WORK_DIR = "kuryba"  # vieno darbo puslapių aplankas

CATEGORIES = [
    ("peizazas", "Peizažai", "Peizažas"),
    ("jura", "Jūra ir laivai", "Jūra ir laivai"),
    ("miestas", "Miestai", "Miestas"),
    ("geles", "Gėlės ir natiurmortai", "Gėlės ir natiurmortai"),
    ("portretas", "Portretai ir figūros", "Portretai ir figūros"),
    ("kita", "Kita", "Kita"),
]
CAT_PLURAL = {k: p for k, p, s in CATEGORIES}
CAT_SINGLE = {k: s for k, p, s in CATEGORIES}

META_RE = re.compile(r"^\s*<!--meta\s+(\{.*?\})\s*-->\s*\n?", re.S)
TOKEN_RE = re.compile(r"\{\{\s*([a-z_0-9]+(?:[.:][^{}\s]+)?)\s*\}\}")
IF_RE = re.compile(r"<!--(if|unless)\s+([a-z]+)\.([a-z_0-9]+)\s*-->((?:(?!<!--(?:if|unless)\s).)*?)<!--/\1-->", re.S)


def read(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_json(name, default):
    p = DATA / name
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def esc(v):
    return html.escape("" if v is None else str(v), quote=True)


def poem_to_html(text):
    """Eilėraštis -> <p> posmai su <br>. Tuščia eilutė skiria posmus."""
    text = (text or "").replace("\r", "").strip("\n")
    if not text.strip():
        return ""
    stanzas = [s for s in re.split(r"\n\s*\n", text) if s.strip()]
    out = []
    for s in stanzas:
        lines = [esc(line.strip()) for line in s.split("\n") if line.strip()]
        out.append("<p>" + "<br>\n".join(lines) + "</p>")
    return "\n".join(out)


def work_view(w, root):
    """Darbo įrašas -> šablonams patogus žodynas. Keliai jau su {{root}} reikšme."""
    v = dict(w)
    slug = w["slug"]
    base = f"{root}assets/img/works/{slug}"
    titled = bool(w.get("titled")) and bool(w.get("title"))
    v["title_display"] = w["title"] if titled else "Be pavadinimo"
    v["untitled"] = "" if titled else "1"
    v["url"] = f"{root}{WORK_DIR}/{slug}.html"
    v["img480"], v["img960"], v["img1600"] = base + "-480.jpg", base + "-960.jpg", base + "-1600.jpg"
    sw = w.get("src_w") or {"480": 480, "960": 960, "1600": 1600}  # tikrieji failų pločiai (maži šaltiniai nedidinami)
    seen, parts = set(), []
    for name in ("480", "960", "1600"):
        width = int(sw.get(name, name))
        if width not in seen:
            seen.add(width)
            parts.append(f"{base}-{name}.jpg {width}w")
    v["srcset"] = ", ".join(parts)
    v["max_w"] = max(seen)  # didžiausias turimas plotis px: neplėsti vaizdo plačiau
    v["small"] = "1" if max(w["w"], w["h"]) < 1000 else ""
    v["ratio"] = f'{w["w"]} / {w["h"]}'
    v["orientation"] = "wide" if w["w"] > w["h"] * 1.15 else ("tall" if w["h"] > w["w"] * 1.15 else "square")
    v["category_label"] = CAT_SINGLE.get(w["category"], "")
    v["category_plural"] = CAT_PLURAL.get(w["category"], "")
    tech = w.get("technique", "") if w.get("technique_stated") else ""
    v["technique_display"] = tech
    v["meta_line"] = ", ".join([x for x in (tech, w.get("size", "")) if x])
    v["year"] = str(w.get("year") or "")
    v["poem_html"] = poem_to_html(w.get("poem", ""))
    v["has_poem"] = "1" if v["poem_html"] else ""
    pt = (w.get("poem_title") or "").strip()
    v["poem_title_display"] = (pt[:1] + pt[1:].lower()) if pt.isupper() else pt  # „SAPNAS“ -> „Sapnas“
    first = (w.get("poem") or "").strip().split("\n")[0].strip()
    v["poem_heading"] = v["poem_title_display"] or (first.rstrip(".,") + "..." if first else "")
    v["sale_label"] = {"parduodamas": "Parduodamas", "parduota": "Privati kolekcija"}.get(w.get("sale", ""), "")
    v["inquiry_url"] = f"{root}kontaktai.html?darbas={slug}"
    alt_bits = [v["title_display"]]
    if w.get("desc"):
        alt_bits.append(w["desc"].rstrip("."))
    v["alt"] = ". ".join(alt_bits) + "."
    v["focus"] = w.get("focus") or "50% 50%"
    v["accent"] = (w.get("palette") or ["#141414"])[0]
    return v


class Site:
    def __init__(self):
        self.works = load_json("works.json", [])
        self.site = load_json("site.json", {})
        self.by_slug = {w["slug"]: w for w in self.works}
        self.year = datetime.date.today().year
        self.warnings = []

    # ---------- data helpers
    def categories(self, root):
        out = []
        for key, plural, single in CATEGORIES:
            items = [w for w in self.works if w["category"] == key]
            if not items or key == "kita":  # „Kita“ matoma tik prie „Visi“
                continue
            cover = max(items, key=lambda w: (w.get("cover", 0), w.get("strength", 0), w.get("quality", 0)))
            c = {"key": key, "label": plural, "single": single, "count": len(items), "count_label": darbai(len(items))}
            cv = work_view(cover, root)
            c.update({"cover_img480": cv["img480"], "cover_img960": cv["img960"], "cover_srcset": cv["srcset"],
                      "cover_alt": cv["alt"], "cover_title": cv["title_display"], "cover_ratio": cv["ratio"],
                      "cover_focus": cv["focus"], "url": f"{root}kuryba.html?tema={key}"})
            out.append(c)
        return out

    def get_path(self, path):
        cur = self.site
        for part in path.split("."):
            if isinstance(cur, list):
                try:
                    cur = cur[int(part)]
                except (ValueError, IndexError):
                    return None
            elif isinstance(cur, dict):
                cur = cur.get(part)
            else:
                return None
            if cur is None:
                return None
        return cur

    # ---------- templating
    def item(self, tpl_name, var, obj, i, root, extra=None):
        tpl = read(TPL / tpl_name)
        if not tpl:
            self.warnings.append(f"nėra šablono _templates/{tpl_name}")
            return ""
        scope = {var: obj}
        if extra:
            scope.update(extra)
        return self.fill(tpl, scope, i, root)

    def fill(self, text, scope, i, root):
        def cond(m):
            kind, var, field, inner = m.group(1), m.group(2), m.group(3), m.group(4)
            obj = scope.get(var) or {}
            val = obj.get(field)
            truthy = bool(val) and val not in ("0", 0)
            return inner if (truthy if kind == "if" else not truthy) else ""

        prev = None
        while prev != text:  # iš vidaus į išorę, kol nelieka sąlygų
            prev = text
            text = IF_RE.sub(cond, text)

        def tok(m):
            key = m.group(1)
            if key == "i":
                return str(i + 1)
            if key == "i0":
                return str(i)
            if key == "i2":
                return f"{i + 1:02d}"
            if "." in key:
                var, field = key.split(".", 1)
                if var in scope:
                    val = (scope[var] or {}).get(field, "")
                    return str(val) if field.endswith("_html") else esc(val)
            return m.group(0)

        return TOKEN_RE.sub(tok, text)

    def block(self, name, arg, root, current=None):
        if name == "works_grid":
            return "\n".join(self.item("card.html", "w", work_view(w, root), i, root) for i, w in enumerate(self.works))
        if name == "featured_stack":
            feat = sorted([w for w in self.works if w.get("featured")], key=lambda w: w["featured"])
            return "\n".join(self.item("stack-item.html", "w", work_view(w, root), i, root) for i, w in enumerate(feat))
        if name == "home_grid":
            n = int(arg or 6)
            rest = [w for w in self.works if not w.get("featured")][:n]
            return "\n".join(self.item("card.html", "w", work_view(w, root), i, root) for i, w in enumerate(rest))
        if name == "filters":
            return "\n".join(self.item("filter.html", "c", c, i, root) for i, c in enumerate(self.categories(root)))
        if name == "category_tiles":
            return "\n".join(self.item("category-tile.html", "c", c, i, root) for i, c in enumerate(self.categories(root)))
        if name == "poems":
            ps = sorted([w for w in self.works if w.get("poem_pick")], key=lambda w: w["poem_pick"])
            return "\n".join(self.item("poem.html", "w", work_view(w, root), i, root) for i, w in enumerate(ps))
        if name in ("exhibitions", "timeline"):
            tpl = "list-row.html" if name == "exhibitions" else "timeline-row.html"
            rows = self.site.get(name, [])
            return "\n".join(self.item(tpl, "e", e, i, root) for i, e in enumerate(rows))
        if name == "list":
            path, _, tpl = (arg or "").partition(":")
            rows = self.get_path(path) or []
            return "\n".join(self.item(f"{tpl}.html", "e", e, i, root) for i, e in enumerate(rows))
        if name == "related":
            if not current:
                return ""
            same = [w for w in self.works if w["category"] == current["category"] and w["slug"] != current["slug"]]
            pos = self.works.index(current)
            same.sort(key=lambda w: (self.works.index(w) - pos) % len(self.works))  # artimiausi toliau sąraše
            return "\n".join(self.item("card.html", "w", work_view(w, root), i, root) for i, w in enumerate(same[:3]))
        self.warnings.append(f"nežinomas blokas {name}")
        return ""

    def render(self, text, ctx, nav, root, current=None):
        def tok(m):
            key = m.group(1)
            if key.startswith("block:"):
                parts = key.split(":", 2)
                return self.block(parts[1], parts[2] if len(parts) > 2 else "", root, current)
            if key.startswith("nav:"):
                return " is-active" if key[4:] == nav else ""
            if key.startswith("count:"):
                k = key[6:]
                return str(len(self.works) if k == "all" else sum(1 for w in self.works if w["category"] == k))
            if key == "works_label":
                return darbai(len(self.works))
            if key.startswith("site."):
                val = self.get_path(key[5:])
                if val is None:
                    return m.group(0)
                return str(val) if key.endswith("_html") else esc(val)
            return str(ctx[key]) if key in ctx else m.group(0)

        return TOKEN_RE.sub(tok, text)

    # ---------- pages
    def assemble(self, body, meta, root, page_name, current=None, scope=None):
        css_links = "\n".join(f'<link rel="stylesheet" href="{root}assets/css/{c}">' for c in meta.get("css", []))
        js_links = "\n".join(f'<script src="{root}assets/js/{j}" defer></script>' for j in meta.get("js", []))
        ctx = {
            "root": root, "year": self.year, "page": page_name,
            "title": esc(meta.get("title", "Stasys Zakas")),
            "description": esc(meta.get("description", "")),
            "body_class": meta.get("body_class", ""),
            "header_mode": meta.get("header", "transparent"),
            "og_image": root + meta.get("og_image", "assets/img/og.jpg"),
            "css_links": css_links, "js_links": js_links,
        }
        nav = meta.get("nav", "")
        page = "".join([
            read(PARTS / "head.html"), read(PARTS / "header.html"),
            '<main id="turinys">\n', body, "\n</main>\n",
            read(PARTS / "footer.html"), read(PARTS / "scripts.html"),
        ])
        if scope:
            page = self.fill(page, scope, 0, root)
        # du kartai: blokų šablonuose gali būti {{root}} ir kitų bendrų žymių
        return self.render(self.render(page, ctx, nav, root, current), ctx, nav, root, current)

    def build(self, write=True):
        results = []
        for src in sorted(BODY.glob("*.html")):
            raw = read(src)
            m = META_RE.match(raw)
            meta = json.loads(m.group(1)) if m else {}
            body = raw[m.end():] if m else raw
            results.append((ROOT / src.name, self.assemble(body, meta, "", src.stem)))
        tpl_raw = read(TPL / "darbas.html")
        if tpl_raw and self.works:
            m = META_RE.match(tpl_raw)
            meta_tpl = m.group(1) if m else "{}"
            body_tpl = tpl_raw[m.end():] if m else tpl_raw
            root = "../"
            n = len(self.works)
            for i, w in enumerate(self.works):
                v = work_view(w, root)
                scope = {"w": v, "prev": work_view(self.works[(i - 1) % n], root), "next": work_view(self.works[(i + 1) % n], root)}
                # fill() ekranuoja HTML, o assemble() ekranuos dar kartą, todėl čia grąžiname paprastą tekstą
                meta = json.loads(html.unescape(self.fill(meta_tpl, {k: {kk: json_safe(vv) for kk, vv in d.items()} for k, d in scope.items()}, i, root)))
                results.append((ROOT / WORK_DIR / f'{w["slug"]}.html', self.assemble(body_tpl, meta, root, "darbas", current=w, scope=scope)))
        elif tpl_raw and not self.works:
            self.warnings.append("_data/works.json tuščias: darbų puslapiai negeneruojami")
        built = changed = 0
        for out, text in results:  # pirma viską įrašome, tik tada tikriname nuorodas tarp puslapių
            built += 1
            if write:
                out.parent.mkdir(exist_ok=True)
                if not out.exists() or out.read_text(encoding="utf-8") != text:
                    out.write_text(text, encoding="utf-8")
                    changed += 1
        if write and (ROOT / WORK_DIR).exists():  # pasenę darbų puslapiai
            keep = {f'{w["slug"]}.html' for w in self.works}
            for old in (ROOT / WORK_DIR).glob("*.html"):
                if old.name not in keep:
                    old.unlink()
        for out, text in results:
            for p in check(out, text):
                self.warnings.append(f"{out.relative_to(ROOT)}: {p}")
        return built, changed


def darbai(n):
    """Lietuviška daugiskaita: 1 darbas, 2 darbai, 10 darbų, 21 darbas."""
    if n % 10 == 0 or 10 < n % 100 < 20:
        return f"{n} darbų"
    return f"{n} darbas" if n % 10 == 1 else f"{n} darbai"


def json_safe(v):
    """Reikšmė, kurią galima įterpti į meta JSON eilutę tarp kabučių (HTML ekranavimą atlieka fill)."""
    return "" if v is None else str(v).replace("\\", "\\\\").replace('"', "'").replace("\n", " ")


def check(out, text):
    problems = []
    for tok in sorted(set(re.findall(r"\{\{[^}]*\}\}", text)))[:6]:
        problems.append(f"nepakeista žymė {tok}")
    for href in sorted(set(re.findall(r'(?:href|src|poster)="([^"#?]+)', text))):
        if re.match(r"^(https?:|mailto:|tel:|data:|javascript:|sms:)", href) or not href:
            continue
        if not (out.parent / href).resolve().exists():
            problems.append(f"nėra failo: {href}")
    for srcset in re.findall(r'srcset="([^"]+)"', text):
        for part in srcset.split(","):
            url = part.strip().split(" ")[0]
            if url and not re.match(r"^(https?:|data:)", url) and not (out.parent / url).resolve().exists():
                problems.append(f"nėra failo (srcset): {url}")
    ids = re.findall(r'\sid="([^"]+)"', text)
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"pasikartojantis id=\"{dup}\"")
    if len(re.findall(r"<img\b(?![^>]*\balt=)[^>]*>", text)):
        problems.append("yra <img> be alt")
    h1 = len(re.findall(r"<h1\b", text))
    if h1 != 1:
        problems.append(f"h1 skaičius: {h1} (turi būti 1)")
    visible = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.S)
    visible = re.sub(r"<!--.*?-->", "", visible, flags=re.S)
    if "—" in visible:
        problems.append("tekste yra ilgasis brūkšnys (—): naudokite kablelį, tašką arba trumpą brūkšnį")
    return problems


def main():
    write = "--check" not in sys.argv
    site = Site()
    built, changed = site.build(write=write)
    seen = set()
    for w in site.warnings:
        if w not in seen:
            seen.add(w)
            print("  ⚠ " + w)
    print(f"Puslapių: {built} (pakeista {changed}), darbų kataloge: {len(site.works)}, įspėjimų: {len(seen)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
