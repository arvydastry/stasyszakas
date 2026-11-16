# Stasys Zakas: demo maketo brief'as (visiems agentams)

Klientas: dailininkas ir poetas **Stasys Zakas** (Panevėžys). Savo Facebook paskyroje jis prisistato: „Rašau poeziją ir tapau, nes tai man patinka“. Tapo aliejumi, akrilu, akvarele, pastele: peizažai, jūra ir laivai, miestai, gėlės, portretai. Prie paveikslų dažnai pats prirašo pavadinimą, techniką, dydį arba visą eilėraštį. Šaltiniai: `DOSJE.md` (faktai), `_data/works.json` (darbų katalogas), `_data/site.json` (tekstai ir sąrašai).

**Užduotis (Arvydas, 2026-11-16):** demo dizainas pagal Salient temą, vieną iš portfolio variantų, dailininko darbams rodyti. Svetainė turi būti meniška ir gerai parodyti autoriaus kūrybą bei istoriją.

**Kas tai:** statinis HTML DEMO kliento pristatymui, NE galutinė svetainė. Jei patiks, svetainė bus kuriama **WordPress + Salient 18.2.1** (Salient Core 3.1.5, WPBakery 8.7.3, Salient Portfolio). Todėl:

- kiekvienas blokas turi turėti **natyvų Salient elementą** (žr. 5 sk. lentelę); ko Salient nedaro pats, to demo nerodo;
- jokio React, shadcn, CDN ar išorinių bibliotekų: HTML + CSS + vanilla JS, veikia iš `file://` ir per `python3 -m http.server`;
- bendras `CLAUDE.md` siūlo shadcn registrus. Šiame projekte jie sąmoningai NENAUDOJAMI dėl tikslinės platformos.

---

## 1. Bazinis demo: Salient „Portfolio Layered“

Iš šešių Salient portfolio demo (Layered, Quantum, Minimal, Freelance, Fullscreen Slider, Photography) pasirinktas **Portfolio Layered**: juodas „galerijos“ fonas, ant kurio ryškios Zako spalvos šviečia; literatūriškas serifinis šriftas tinka poetui; sluoksniuotos darbų kortelės su dideliu pavadinimu ir „apdovanojimų“ sąrašas tiesiogiai virsta paveikslais ir parodomis. Tiksli analizė, išmatavimai ir ekrano nuotraukos: `_brief/salient-layered/` (skaityti prieš rašant CSS).

**Demo parašas, kurį privaloma išlaikyti:**

1. Juodas fonas `#000`, baltas tekstas, vienintelė akcento spalva tik mygtukui ir smulkiems akcentams.
2. Antraštės **Gloock** (serif, 400), tekstas **DM Sans**. Didžiosios antraštės `6vw` (iki 108 px), eilutės aukštis 1.
3. Hero: viso ekrano aukščio eilutė, fono vaizdas su „zoom-out“ ir parallax, apačioje juodas gradientas (`linear-gradient(0deg,#000 0%,transparent 43%)`), turinys prispaustas prie apačios: kairėje vardas dviem eilutėmis, dešinėje trumpas prisistatymas (iki 375 px pločio), kampe rodyklė žemyn.
4. **Sluoksniuotos darbų kortelės** (Post Loop Builder, „Stack“ + „Blurred Scale“): viena kortelė per eilutę, aukštis `80vh`, kampai 25 px, tarpas 40 px, lipni pozicija `top: 40px`; užslenkant kitai kortelei ankstesnė sumažėja iki 0,8 ir susilieja (`blur(5px)`). Kortelėje: vaizdas per visą plotą, tamsinimas `#141414` 30 %, centre milžiniškas pavadinimas Gloock `12vw` (iki 220 px), viršuje kairėje kategorijos „piliulė“ (14 px, didžiosios, tarpai 0,1em), dešinėje data. Pelės žymeklį seka matinė piliulė „Žiūrėti“.
5. Sąrašas „Professional Achievements“: didelė antraštė dviem eilutėmis + **Horizontal List Item** eilutės keturiais stulpeliais (h3 | p | h4 | p dešinėje), tarp jų 1 px balta linija, kuri įslenkant „nusipiešia“ (1,1 s, `cubic-bezier(.65,0,.25,1)`).
6. Projekto puslapis: didelė antraštė, po ja meta stulpeliai su mažomis didžiosiomis etiketėmis (h6) ir kategorijos piliule dešinėje; vaizdas per visą plotį; dviejų stulpelių blokai „etiketė kairėje (1/3), stambus tekstas dešinėje (2/3, 1,5em)“; galerija „vienas platus + du po pusę“ (kampai 5 px, tarpas 10 px); citata; „Explore More Work“ trijų kortelių tinklelis (turinys po vaizdu, hover: vaizdo priartinimas + animuotas pabraukimas).
7. Poraštė: per visą plotį ištemptas milžiniškas užrašas „© [linija] 2026“ (Gloock, apie 21vw).
8. Antraštė (header): permatoma, 80 px, logotipas tekstu kairėje (Gloock 20 px), meniu centre (DM Sans 16 px, 500), dešinėje akcento spalvos piliulė (45 px aukščio, hover `scale`). Slenkant žemyn slepiasi, aukštyn pasirodo („hide until needed“). Mobiliame: kairėje „mėsainis“, logotipas, dešinėje ta pati piliulė.
9. Judesys: antraštės išnyra raidėmis iš apačios („Split Line Heading: line-reveal-by-space + letter-reveal-bottom“, su stagger), stulpeliai „fade-in“ su 300 / 500 ms vėlavimu, tinklelio kortelės „fade in from bottom“, perėjimai tarp puslapių „View Transitions“. Stulpelių animacijos easing `easeOutCubic`, trukmė 1300 ms.

**Ką keičiame (ir kodėl):**

| Demo | Mūsų | Kodėl |
|---|---|---|
| Akcentas `#c4ff23` (laimo) | `--accent: #F4C430` (šilta saulės geltona iš paveikslo „Ryto gaivumas“) | Akcentas turi kilti iš autoriaus paletės; viena spalva visoje svetainėje |
| Hero fone nespalvotas portretas | Hero fone paveikslas | Nėra pakankamos raiškos portreto; pirmas įspūdis turi būti tapyba. Portretas rodomas „Apie“ blokuose |
| 5 projektai, vienas puslapis | Katalogas (apie 190 darbų), 5 puslapiai + puslapis kiekvienam darbui | Dailininko svetainei reikia galerijos, istorijos, eilių, kontaktų |
| „© — 2026“ su ilguoju brūkšniu | Linija nupiešta CSS, ne simboliu | Tekste ilgųjų brūkšnių nenaudojame |

---

## 2. Failų struktūra ir sutartis

```
build.py                    surinkimas (skaityti jo antraštę: žymės, blokai, sąlygos). NEKEISTI be orkestruotojo
_parts/head.html            <!doctype>, <head>, @font-face per style.css, meta, <body ...> atidarymas
_parts/mockbar.html         tamsi „Demo maketas“ juosta viršuje (į WordPress neperkeliama)
_parts/header.html          antraštė + mobilus meniu
_parts/footer.html          poraštė (nuorodų eilutė + milžiniškas ©)
_parts/scripts.html         lightbox ir kiti bendri konteineriai, main.js, {{js_links}}, </body></html>
_body/<puslapis>.html       puslapio turinys; 1 eilutė yra meta komentaras su JSON
_templates/darbas.html      vieno darbo puslapio šablonas -> kuryba/<slug>.html
_templates/*.html           elementų šablonai: card, stack-item, filter, category-tile, poem, list-row, timeline-row ...
_data/works.json            darbų katalogas (generuojamas; ranka neredaguoti)
_data/site.json             autoriaus tekstai, parodos, faktai, kontaktai (savininkas: orkestruotojas)
assets/css/style.css        BENDRA dizaino sistema (savininkas: pamatų agentas)
assets/css/p-<raktas>.css   puslapio stiliai (savininkas: to puslapio agentas)
assets/js/main.js           BENDRAS JS (savininkas: pamatų agentas)
assets/js/p-<raktas>.js     puslapio JS, jei reikia
assets/fonts/               gloock.woff2 (400), dmsans.woff2 (kintamas 100-1000), dmsans-italic.woff2; OFL licencijos
assets/img/works/           <slug>-480.jpg, -960.jpg, -1600.jpg (generuoja _tools/prepare_images.py)
assets/img/artist/, parodos/   autoriaus ir parodų nuotraukos
_originals/                 pilnos raiškos apkarpyti paveikslai būsimai svetainei (maketas jų nenaudoja)
_tools/shot.mjs             ekrano nuotraukos per Chrome CDP: node _tools/shot.mjs <url> <out.png> [plotis] [aukštis] [--full] [--reduce] [--js="..."]
_brief/                     BRIEF.md, COMPONENTS.md, DOSJE.md, MEDIA.md, salient-layered/ (bazinio demo analizė)
```

Puslapiai ir meta `nav` raktai:

| Failas | Meniu | nav | Šablonas Salient'e |
|---|---|---|---|
| `index.html` | Pradžia | `home` | Portfolio Layered Landing |
| `kuryba.html` | Kūryba | `kuryba` | puslapis su Post Loop Builder (Grid, filtrai) |
| `kuryba/<slug>.html` | (iš galerijos) | `kuryba` | Portfolio projektas (page builder) |
| `eiles.html` | Eilės | `eiles` | puslapis su Sticky Media Sections |
| `apie.html` | Apie | `apie` | puslapis pagal projekto puslapio išdėstymą |
| `kontaktai.html` | mygtukas „Susisiekti“ | `kontaktai` | puslapis su forma |

Taisyklės:

- Nuorodos į puslapius ir failus VISADA su `{{root}}` (`{{root}}kuryba.html`, `{{root}}assets/img/...`), nes darbų puslapiai yra aplanke `kuryba/`.
- Meta pavyzdys: `<!--meta {"title": "Kūryba | Stasys Zakas", "description": "...", "nav": "kuryba", "css": ["p-kuryba.css"], "js": ["p-kuryba.js"], "body_class": "page-kuryba", "header": "transparent", "og_image": "assets/img/works/ryto-gaivumas-1600.jpg"} -->`
- Surinkimas: `python3 build.py`. Turi būti **0 įspėjimų** (tikrina nepakeistas žymes, neegzistuojančius failus, pasikartojančius id, `<img>` be alt, h1 skaičių, ilguosius brūkšnius).
- Sugeneruotų `*.html` šaknyje ir `kuryba/` ranka neredaguoti.
- **Nuosavybė lygiagrečiam darbui:** puslapių agentai NEREDAGUOJA `style.css`, `main.js`, `_parts/*`, `build.py`, `_data/*` ir kitų agentų failų. Trūkstamą bendrą dalyką aprašo savo ataskaitoje; savo stilius rašo į `p-<raktas>.css`.
- Kiekvienas blokas, kuris Salient'e būtų atskiras elementas ar eilutė, turi atributą `data-salient="Elemento pavadinimas: svarbiausios parinktys"` (anglų k., kaip Salient administravime). Pvz. `data-salient="Split Line Heading: line-reveal-by-space, letter-reveal-bottom, 6vw"`. Maketo juostos mygtukas „Salient žymės“ jas parodo.

---

## 3. Dizaino sistema

### Spalvos (`:root`)

```
--bg:        #000000   puslapio fonas (kaip demo)
--surface:   #141414   kortelių pagrindas, tamsinimo spalva
--surface-2: #1c1c1c   formos laukai, hover paviršiai
--line:      rgba(255,255,255,.22)   plonos linijos; sąrašo eilutėms pilnai balta kaip demo
--text:      #ffffff
--muted:     rgba(255,255,255,.64)   pagalbinis tekstas (kontrastas ant #000 ne mažesnis kaip 7:1)
--accent:    #F4C430   VIENINTELIS akcentas: CTA piliulė (juodas tekstas), aktyvus filtras, focus žiedas, teksto žymėjimas
--accent-ink:#000000
```

Daugiau spalvų nėra. Spalvą puslapiui duoda paveikslai. Jokių gradientų tekste, švytėjimų, tekstūrų. Viena tema (tamsi) visuose puslapiuose ir sekcijose.

### Tipografija

- `@font-face` iš `assets/fonts/` su `font-display: swap`; DM Sans kintamas (`font-weight: 100 1000`). Be Google Fonts nuorodų.
- Tekstas: DM Sans 17 px / 31 px, `letter-spacing: -0.02em`, 400. Stambus tekstas (dviejų stulpelių blokuose): `1.5em`, eilutė 1,6.
- h1 (tema): Gloock 65 / 67 px. h2: Gloock 35 / 45 px. h3: DM Sans 25 / 35, 600, `-0.01em`. h4: DM Sans 18 px, 600. h6 ir etiketės: DM Sans 14 px, didžiosios, `letter-spacing: .1em`.
- Didžiosios antraštės (`.split-heading`): `font-size: clamp(44px, 6vw, 108px)`, eilutė 1 (ilgesnėms 1,1-1,2), planšetėje `10vw`, telefone `12vw` (jei žodis netelpa, mažinti iki `10.5vw`).
- Kortelių pavadinimai stack'e: `12vw` (iki 220 px), centre, `max-width: 90%`. Ilgesniems pavadinimams (daugiau kaip 9 ženklai) dydis mažėja: klasės `.is-long` (8.5vw) ir `.is-xlong` (6.2vw), kad tilptų į 2 eilutes.
- Eilėraščiai: Gloock (kaip h2 stilius), `clamp(22px, 2.3vw, 38px)`, eilutė 1,35; posmai `<p>`, eilutės `<br>`.
- Lietuviškos kabutės „…“. Tekste NĖRA ilgųjų brūkšnių; intervalams trumpas brūkšnys be tarpų („2024–2026“).
- Kursyvo Gloock neturi: akcentui naudoti DM Sans arba nieko. Nemaišyti kitų šriftų.

### Erdvė ir formos

- Eilutės per visą plotį, šoniniai tarpai 40 px (planšetėje ir telefone 6 %, ne mažiau 20 px). Didžiausias turinio plotis 1800 px.
- Vertikalūs tarpai procentais nuo pločio kaip demo: sekcijos `padding: 10% 0 6%` arba `6% 0`; telefone ne mažiau 64 px.
- Kampai (viena sistema): stack kortelės 25 px; visi kiti vaizdai ir kortelės 5 px; piliulės ir mygtukai 200 px; formos laukai 5 px.
- Šešėlių nėra (juodame fone jų nereikia).

### Judesys (tik tai, ką Salient daro pats)

| Efektas | Salient | Įgyvendinimas makete |
|---|---|---|
| Antraštė išnyra raidėmis iš apačios | Split Line Heading: line-reveal-by-space + letter-reveal-bottom, stagger | `[data-split]`: JS suskaido į žodžius ir raides, `overflow: hidden` kaukė, `translateY(110%) -> 0`, 30-40 ms stagger, 1,1 s |
| Stulpelio atsiradimas | Column animation: fade-in / fade-in-from-bottom, delay | `[data-reveal="fade"|"up"]` + `data-delay` |
| Hero fonas | Row: bg image animation zoom-out, parallax medium_fast | `scale(1.12 -> 1)` per 2,2 s ir `translateY` pagal slinkimą |
| Sluoksniuotos kortelės | Post Loop Builder: Stack, Blurred Scale | `position: sticky` + JS skaičiuoja uždengimo progresą -> `scale(1 -> .8)`, `blur(0 -> 5px)` |
| Sąrašo linija | Horizontal List Item: border animation | `::after` linija `scaleX(0 -> 1)` iš kairės |
| Kortelės hover | Post Grid: animated_underline_zoom | vaizdas `scale(1.05)`, pavadinimo pabraukimas išauga iš kairės |
| Žymeklio piliulė „Žiūrėti“ | Post Grid: mouse indicator, tooltip text, blurred bg | tik `(hover: hover) and (pointer: fine)`, seka pelę virš stack kortelių |
| Lipnus vaizdas prie eilių | Sticky Media Sections | kairėje slenka eilėraščiai, dešinėje lipnus paveikslas keičiasi su `opacity` |
| Antraštės slėpimas | Header: hide until needed | slenkant žemyn `translateY(-100%)`, aukštyn grįžta |
| Puslapių perėjimai | Page transitions: View Transitions | `@view-transition { navigation: auto; }` (kur nepalaikoma, tiesiog nieko) |

Taisyklės: animuoti tik `transform`, `opacity`, `filter`, `clip-path`. `prefers-reduced-motion: reduce`: be parallax, be stack mastelio ir suliejimo, be raidžių animacijos, viskas iškart matoma. Be JS turinys taip pat matomas: pradinės „paslėptos“ būsenos galioja tik kai `<html class="js">`. Slinkimo logikai naudoti `IntersectionObserver` ir vieną pasyvų `scroll` klausytoją su `requestAnimationFrame`.

---

## 4. Turinio taisyklės

1. **Jokių išgalvotų faktų.** Biografija, parodos, datos, technikos, dydžiai tik iš `DOSJE.md`, `_data/site.json` ir `_data/works.json`. Jei fakto nėra, bloko dalis praleidžiama. Neaiškūs dalykai keliauja į README sąrašą „Ką patvirtinti su autoriumi“.
2. **Pavadinimai tik autoriaus.** Darbas be autoriaus pavadinimo rodomas kaip „Be pavadinimo“; aprašomasis sakinys (`desc`) naudojamas `alt` tekstui ir darbo puslapio aprašui. Technika rodoma tik jei ją nurodė autorius (`technique_display`). Metai: rodoma etiketė „Paskelbta“ ir paskelbimo metai (tai ne būtinai sukūrimo metai).
3. **Eilės necituojamos iš atminties ir netaisomos**: tekstas imamas iš `works.json` lauko `poem` (autoriaus rašyba ir skyryba).
4. Tonas: ramus, žmogiškas, be reklaminių žodžių („unikalus“, „nepakartojamas“, „išskirtinis“). Trumpi sakiniai. Kreipinys į lankytoją „jūs“.
5. Vienas veiksmas, vienas pavadinimas: kontakto veiksmas visur vadinamas **„Susisiekti“** (antraštėje, sekcijose, poraštėje), galerijos veiksmas **„Visa kūryba“**, darbo puslapyje **„Teirautis dėl šio paveikslo“**.
6. Mažų didžiųjų etikečių (h6) ne daugiau kaip viena trims sekcijoms. Jokių sekcijų numerių, „scroll“ užrašų, dekoratyvių taškų, versijų žymų. Hero rodyklė žemyn lieka (tai demo elementas, veikia kaip nuoroda į kitą sekciją).
7. Ant paveikslų nededame užrašų, išskyrus stack korteles (demo parašas). Galerijoje ir darbo puslapyje paveikslas rodomas VISAS, neapkarpytas (`object-fit: contain` arba natūrali proporcija).
8. Nuotraukų autoriai nurodomi po nuotrauka mažu tekstu, kai žinomi: portretas „Nuotr. Almutės Juzėnienės“, paroda Raseiniuose „Nuotr. Prano Laurinavičiaus“.
9. Prieinamumas: vienas `<h1>` puslapyje, prasmingi `alt`, matomas fokusas (2 px `--accent` kontūras), `aria-expanded` meniu ir filtrams, `aria-live` galerijos skaitikliui, „Pereiti prie turinio“ nuoroda, kontrastas ne mažesnis kaip 4,5:1. Formos: etiketė virš lauko, klaida po lauku.
10. `<meta name="robots" content="noindex, nofollow">` visuose puslapiuose (demo).

---

## 5. Komponentai ir Salient atitikmenys

Pamatų agentas juos sukuria `style.css` + `main.js` ir aprašo `_brief/COMPONENTS.md` su HTML pavyzdžiais. Puslapių agentai juos NAUDOJA.

| Komponentas (klasė) | Paskirtis | Salient elementas ir parinktys |
|---|---|---|
| `.row`, `.row--full`, `.row__inner`, `.cols`, `.col-1-3`, `.col-2-3`, `.col-1-2` ... | eilutės ir stulpeliai | Row (full width background / full width content), Inner Row, Column |
| `.split-heading[data-split]` | didžiosios antraštės | Split Line Heading |
| `.rtext`, `.rtext--lg` | prisitaikantis tekstas (1.3vw arba 1.5em) | Responsive Text |
| `.label` (h6) | mažos didžiosios etiketės | Text Block su h6 |
| `.btn-pill` (akcentas), `.btn-pill--ghost`, `.link-underline`, `.cta-arrow` | veiksmai | Header CTA button; Nectar Button; Call To Action (link); CTA next-section minimal-arrow |
| `.pill` | kategorijos / būsenos žyma su plonu rėmeliu | Project Categories: outline; Post Grid category style: see-through button |
| `.hero` | pradžios hero | Row full height, bg image zoom-out + parallax, advanced gradient |
| `.stack`, `.stack__item` | sluoksniuotos darbų kortelės | Post Loop Builder: Portfolio, Stack, Blurred Scale, 80vh, spacing 40px, content overlaid, all middle, overlay #141414 |
| `.view-indicator` | „Žiūrėti“ piliulė prie pelės | Post Loop Builder: mouse indicator, tooltip text, blurred bg |
| `.hlist`, `.hlist__row` | parodų ir faktų sąrašai (2-4 stulpeliai) | Horizontal List Item ×N, border animation |
| `.twocol` (etiketė 1/3 + turinys 2/3) | teksto blokai | Inner Row 1/3 + 2/3: Text Block h6 + Responsive Text |
| `.gallery-3` (1 platus + 2 po pusę) | nuotraukų blokas | Image With Animation ×3, radius 5px, column margin 10px |
| `.grid-works`, `.card` | galerijos tinklelis ir kortelė | Post Loop Builder: Grid, masonry, 3 / 2 / 2 stulpeliai, spacing 5-10px, content under image, hover animated underline + zoom, radius 5px |
| `.filters` | kategorijų filtrai su skaičiais | Post Loop Builder: category filters (sortable) |
| `.btn-more` | „Rodyti daugiau“ | Post Loop Builder: Load More |
| `.tiles` | temų plytelės | Category Grid arba Fancy Box su fono vaizdu |
| `.sticky-media` | eilės + lipnus paveikslas | Sticky Media Sections |
| `.poem` | eilėraščio tipografija | Responsive Text su h2 stiliumi |
| `.artwork-figure` + `[data-lightbox]` | visas paveikslas + padidinimas | Image With Animation, „link to larger image“ (lightbox) |
| `.form`, `.field` | kontaktų forma (nieko nesiunčia, rodo sėkmės būseną) | Contact Form 7 arba Fluent Forms |
| `.site-footer`, `.footer-giant` | poraštė | Global Section „Portfolio Layered Footer“: Split Line Heading, fit to width |
| `.site-header`, `.offcanvas` | antraštė, mobilus meniu | Header: centered menu, transparent, permanent transparent, hide until needed; off-canvas menu |
| `.mockbar`, `[data-salient]` žymės, `[data-demo]` toast | tik demo | į WordPress neperkeliama |

---

## 6. Puslapiai (sekcija po sekcijos)

### 6.1 Pradžia `index.html`

1. **Hero.** Fonas: paveikslas (`site.hero.work` slug'as, `object-position` iš `focus`). H1 „Stasys Zakas“ (dvi eilutės). Dešinėje: `site.hero.intro` (iki 20 žodžių). Po juo maža nuoroda „Paveiksle: „…“ į to darbo puslapį (14 px, `--muted`). Kampe rodyklė į kitą sekciją.
2. **Sluoksniuotos kortelės** `{{block:featured_stack}}` (5 darbai su trumpais autoriaus pavadinimais). Po jomis viena eilutė: sakinys su tikru darbų skaičiumi (`{{count:all}}`) ir nuoroda „Visa kūryba“.
3. **Autoriaus žodis.** `.twocol`: etiketė „Autoriaus žodis“, dešinėje pirmas eilėraščio „Rašau...“ posmas stambiu Gloock, po juo parašas ir nuoroda „Skaityti eiles“.
4. **Temos.** `.tiles`: penkios kategorijos su viršelio paveikslu, pavadinimu ir darbų skaičiumi (`{{block:category_tiles}}`), asimetrinis tinklelis (2 didelės + 3 mažesnės), nuoroda į `kuryba.html?tema=<raktas>`.
5. **Apie autorių (trumpai).** Portretas (4:5, 5 px kampai, su nuotraukos autoriumi) + 2-3 sakiniai iš `site.about.short` + nuoroda „Apie autorių“.
6. **Parodos ir renginiai.** Didelė antraštė dviem eilutėmis + `{{block:exhibitions}}` (`.hlist` 4 stulpeliai: pavadinimas | vieta | tipas | metai).
7. **Kvietimas.** Antraštė (h2 dydžio, 3.5vw iki 60 px) „Domina paveikslas? Parašykite.“ + trumpas sakinys + piliulė „Susisiekti“.
8. Poraštė.

Skirtingos išdėstymo šeimos: hero, kortelių rietuvė, etiketė + stambus tekstas, plytelių tinklelis, vaizdas + tekstas, sąrašas, kvietimas. Nekartoti tos pačios šeimos du kartus.

### 6.2 Kūryba `kuryba.html`

1. Antraštė: H1 „Kūryba“ (split heading), po ja viena eilutė su tikrais skaičiais.
2. `.filters`: „Visi“ + `{{block:filters}}`; aktyvus filtras akcento spalva; URL `?tema=jura` parenka filtrą; skaitiklis „Rodoma N iš M“ su `aria-live`.
3. `.grid-works` su `{{block:works_grid}}`: masonry pagal natūralias proporcijas (3 stulpeliai nuo 1000 px, 2 stulpeliai žemiau), kortelėje vaizdas, pavadinimas, meta eilutė (technika, dydis arba kategorija), „Parduodamas“ žyma, jei yra. Pirmi 24, toliau „Rodyti daugiau“.
4. Kvietimas + poraštė.

### 6.3 Darbas `kuryba/<slug>.html` (šablonas `_templates/darbas.html`)

1. H1 = `{{w.title_display}}`; meta stulpeliai (rodyti tik esamus): „Technika“, „Dydis“, „Paskelbta“; dešinėje kategorijos piliulė ir, jei yra, būsena („Parduodamas“ / „Privati kolekcija“).
2. Paveikslas: visas, centre, juodame fone, `max-height: 88vh`, paspaudus atsidaro padidinimas.
3. `.twocol` „Apie darbą“: `{{w.desc}}` + nuoroda „Teirautis dėl šio paveikslo“ (`{{w.inquiry_url}}`).
4. Jei yra eilės: `.twocol` „Eilės“ su `{{w.poem_html}}` ir parašu „Stasys Zakas“.
5. „Kiti darbai“: `{{block:related}}` (3 kortelės) + nuoroda „Visa kūryba“.
6. Poraštė.

### 6.4 Eilės `eiles.html`

1. H1 „Eilės“ + vienas sakinys (eilėraščius autorius skelbia kartu su paveikslais).
2. `.sticky-media` su `{{block:poems}}`: kiekvienas eilėraštis (pavadinimas, jei yra, posmai) ir šalia paveikslas, su kuriuo jis paskelbtas (nuoroda į darbo puslapį). Telefone paveikslas virš eilėraščio.
3. Kvietimas + poraštė.

### 6.5 Apie `apie.html`

Išdėstymas pagal Layered projekto puslapį:

1. H1: autoriaus sakinys „Rašau poeziją ir tapau, nes tai man patinka.“ (split heading); meta stulpeliai iš `site.about.meta`; piliulė „Apie autorių“.
2. Platus vaizdas arba portretas + `.twocol` „Biografija“ (`site.about.bio_html`).
3. `.hlist` faktai (`site.about.facts`: technikos, temos, darbų skaičius kataloge).
4. `.gallery-3`: parodos ir dirbtuvės nuotraukos su parašais ir nuotraukų autoriais.
5. „Parodos ir renginiai“: pilnas `{{block:exhibitions}}`.
6. `.twocol` „Autoriaus žodis“: posmas apie spalvas iš eilėraščio (`site.about.statement_html`).
7. Kvietimas + poraštė.

### 6.6 Kontaktai `kontaktai.html`

1. H1 „Susisiekime“ + sakinys: paveikslus galima įsigyti, galima kviesti surengti parodą.
2. Dvi dalys: kairėje kontaktai iš `site.contacts` (tik tie, kurie yra) ir pastaba, dešinėje forma: Vardas, El. paštas, Tema (pasirinkimas), Žinutė, sutikimas. Jei URL yra `?darbas=<slug>`, virš formos rodoma to darbo miniatiūra su pavadinimu, o tema parenkama „Noriu įsigyti paveikslą“. Forma nieko nesiunčia: rodo sėkmės būseną.
3. Poraštė.

---

## 7. Kokybės kartelė

- 1440×900, 1024×768, 820×1180, 390×844: jokio horizontalaus slinkimo, konsolės klaidų, sugadintų vaizdų; antraštė vienoje eilutėje; hero telpa į pirmą ekraną (vardas, tekstas ir rodyklė matomi).
- `python3 build.py` be įspėjimų. `node --check` visiems JS.
- Sumažinto judesio režimas (`shot.mjs --reduce`): viskas matoma, niekas nejuda.
- Paveikslai aštrūs: `srcset` + `sizes`, `loading="lazy"` (išskyrus hero ir pirmą kortelę), nurodyta proporcija (`aspect-ratio`), kad puslapis nešokinėtų.
- Kiekvienas puslapis atrodo kaip tos pačios svetainės dalis: tie patys tarpai, kampai, etikečių stilius, vienas akcentas.
- Prieš baigiant perskaityti VISUS matomus tekstus: lietuvių kalbos klaidos, netaisyklingi linksniai ir „dirbtiniai“ sakiniai yra defektas.
