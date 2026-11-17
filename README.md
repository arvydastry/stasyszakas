# Stasys Zakas: demo maketas (pagal Salient „Portfolio Layered“)

Statinis HTML demo kliento pristatymui: dailininko ir poeto Stasio Zako (Panevėžys) kūrybos svetainė.
Tai ne galutinė svetainė. Jei patiks, ji būtų kuriama WordPress + Salient 18.2.1, todėl kiekvienas blokas turi natyvų Salient atitikmenį.

## Kaip peržiūrėti

```bash
python3 -m http.server 8472
```

Atidaryti http://localhost:8472/ (tas pats nustatyta `.claude/launch.json`). 
Po pakeitimų `_body/`, `_parts/`, `_templates/` ar `_data/` perrinkti: `python3 build.py` (turi rodyti 0 įspėjimų).

## Puslapiai

| Puslapis | Kas jame |
|---|---|
| `index.html` Pradžia | Hero su paveikslu „Ryto gaivumas“, 5 sluoksniuotos darbų kortelės, autoriaus žodis (posmas iš „Rašau...“), temos, trumpai apie autorių, parodų sąrašas, kvietimas |
| `kuryba.html` Kūryba | 194 darbų galerija natūraliomis proporcijomis, filtrai pagal temą su skaičiais, „Rodyti daugiau“ |
| `kuryba/<slug>.html` Darbas | 194 puslapiai iš vieno šablono: pavadinimas, technika, dydis, visas paveikslas su padidinimu, aprašas, eilės (jei yra), „Teirautis dėl šio paveikslo“, kiti darbai |
| `eiles.html` Eilės | 8 autoriaus eilėraščiai greta paveikslų, su kuriais jie paskelbti |
| `apie.html` Apie | Autoriaus sakinys, portretas, biografija, faktai, nuotraukos, parodos, posmas apie spalvas |
| `kontaktai.html` Kontaktai | Forma (nieko nesiunčia), Facebook nuoroda; `?darbas=<slug>` parodo dominantį paveikslą |

## Salient atitikmenys

| Blokas | Salient elementas |
|---|---|
| Antraštė (permatoma, meniu centre, piliulė, slepiasi slenkant) | Header: Centered Menu, Transparent, Hide Until Needed, CTA button |
| Hero | Row: full height, bg image zoom-out + parallax, advanced gradient; Split Line Heading; Responsive Text; CTA next-section |
| Sluoksniuotos kortelės | Post Loop Builder: Portfolio, Stack, Blurred Scale, 80vh, content overlaid, mouse indicator |
| Etiketė + stambus tekstas | Inner Row 1/3 + 2/3: Text (h6) + Responsive Text |
| Temų plytelės | Category Grid arba Fancy Box su fono vaizdu |
| Parodų ir faktų sąrašai | Horizontal List Item, border animation |
| Galerija, filtrai, „Rodyti daugiau“ | Post Loop Builder: Grid (masonry), category filters, Load More, content under image |
| Darbo puslapis | Portfolio projektas (page builder): Split Line Heading, Project Categories, Image With Animation + lightbox |
| Eilės greta paveikslo | Sticky Media Sections |
| Kiti darbai | Global Section su Post Loop Builder (3 stulpeliai) |
| Forma | Contact Form 7 arba Fluent Forms |
| Poraštė su milžinišku © | Global Section: Split Line Heading |

Šriftai kaip demo: Gloock ir DM Sans (talpinami lokaliai, OFL). Akcentas pakeistas iš laimo į geltoną `#F4C430`, paimtą iš autoriaus paletės.

## Failai

- `build.py` surenka puslapius iš `_parts/` + `_body/` + `_templates/` + `_data/` (žymių aprašas failo pradžioje).
- `_data/works.json` darbų katalogas (generuoja `_tools/prepare_images.py` pagal `_data/curation.json`); `_data/site.json` tekstai, parodos, kontaktai.
- `assets/img/works/` kiekvienas darbas trimis dydžiais; `_originals/works/` pilnos raiškos apkarpyti paveikslai būsimai svetainei.
- `_brief/MEDIA.md` visų darbų šaltiniai (Facebook nuorodos) ir autoriaus įrašai; `_brief/BRIEF.md` dizaino užduotis.

## Iš kur turinys

Paveikslai, pavadinimai, technikos, dydžiai ir eilės paimti iš viešos autoriaus Facebook paskyros (facebook.com/stasys599). Nuotraukos apkarpytos iki paveikslo krašto.
Pavadinimas rodomas tik tada, kai jį užrašė pats autorius (122 iš 194); kiti darbai rodomi kaip „Be pavadinimo“. Eilės cituojamos taip, kaip parašytos.

## Ką reikia patvirtinti su autoriumi

1. Ar galima naudoti visus paveikslus ir eiles; kuriuos darbus išimti ar pridėti. „Ruskij mir“ ir aktas į demo neįtraukti.
2. Darbų be pavadinimų pavadinimai, technikos, dydžiai ir sukūrimo metai (dabar rodomi tik Facebook paskelbimo metai).
3. Kurie darbai tikrai parduodami: žymos „Parduodamas“ ir „Privati kolekcija“ paimtos iš senų įrašų.
4. Biografija: parašyta tik iš viešų faktų. Reikia gimimo metų, kūrybos pradžios, ar minėti darbą muitinėje ir mokslus Panevėžio politechnikume.
5. Parodų sąrašas: Raseinių bibliotekos paroda (atidaryta lapkričio 14 d., plakatas paskelbtas 2025 m.), Šilaičių menų festivalis (metai ir dalyvavimas), skaitymai „Vilties paukštė“ Berčiūnuose (metai). Papildyti kitomis parodomis.
6. Kontaktai: telefonas ir el. paštas (dabar tik Facebook nuoroda).
7. Nuotraukų leidimai: portretas (Almutės Juzėnienės), parodos nuotraukos (Prano Laurinavičiaus, jose matomi kiti žmonės).
8. Pavadinime „Triumfo Akra. Paryžius“ pataisyta į „Triumfo arka“. Eilėse niekas netaisyta (pvz. „pasaris“, „arodo“).
9. Geresnės raiškos nuotraukos: 29 darbų šaltiniai mažesni nei 1000 px; pradžios puslapiui praverstų profesionalus portretas.

## Ko demo neapima

Formos siuntimo, anglų kalbos versijos, pirkimo krepšelio, WordPress diegimo. Tikrinta tik Chrome (1440 ir 390 px pločiai).
