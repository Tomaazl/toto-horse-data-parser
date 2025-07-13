# Ravitietojen Jäsennin

Python-skripti ravitietojen jäsentämiseen "ohjelmatiedot" PDF-tiedostoista ja muuntamiseen Excel-muotoon. Jäsennin poimii hevostiedot, ennätykset ja juoksuhistorian suomalaisista raviohjelmista.

## Ominaisuudet

- Poimii hevosten nimet, iät ja ennätykset PDF-tiedostoista
- Jäsentää sekä auto- (a) että tasuri- (t) ennätysajat
- Poimii täydellisen juoksuhistorian päivämäärineen ja aikoineen
- Käsittelee päivämäärien jäsentämisen
- Tulostaa tiedot Excel-muotoon
- Käsittelee useita hevosia ja lähtöjä yhdestä PDF-tiedostosta

## Vaatimukset

Asenna tarvittavat riippuvuudet:

```bash
pip install pandas PyPDF2 openpyxl
```

## Käyttö

### Peruskäyttö
main.py tiedoston funktiokutsuun syötetään parametriksi haluttu tiedosto (muista .pdf-pääte)

```python
from horse_parser import parse_lahdot

# Jäsennä PDF-tiedosto
hevosdata = parse_lahdot("ohjelmatiedot.R_13.07.2025.pdf")

# Tallenna Excel-tiedostoon
hevosdata.to_excel("Hevosdata_Riihimaki.xlsx", index=False)
```

### Komentorivi-käyttö

Suorita skripti suoraan:

```bash
python horse_parser.py
```

Tämä käsittelee oletustiedoston `ohjelmatiedot.R_13.07.2025.pdf` ja luo tiedoston `Hevosdata_Riihimaki.xlsx`.

## Syöttötiedoston muoto

Jäsennin odottaa PDF-tiedostoja, jotka sisältävät suomalaisten raviohjelmien tietoja seuraavalla rakenteella:

- Hevosten nimet ja perustiedot
- Ennätykset merkittyinä aikamalleina (esim. "1,5" tarkoittaa 1,5 sekuntia)
- Juoksuhistoria päivämäärineen PP.KK-muodossa
- Lähtöjen otsikot ja ohjelman tiedot

## Tulosteen muoto

Jäsennin tuottaa Excel-tiedoston seuraavilla sarakkeilla:

| Sarake | Kuvaus |
|--------|--------|
| **Lähtö** | Lähtö-/kilpailutiedot |
| **Hevonen** | Hevosen nimi |
| **Ikä** | Hevosen ikä |
| **Ennätys (a)** | Autolähdön ennätysaika |
| **Ennätys (t)** | Tasurilähdön ennätysaika |
| **Ennätys pvm (a)** | Autolähdön ennätyksen päivämäärä |
| **Ennätys pvm (t)** | Tasurilähdön ennätyksen päivämäärä |
| **Juoksu pvm** | Juoksun päivämäärä |
| **Juoksu aika** | Juoksun aika |

## Tietorakenne

Tuloste sisältää yhden rivin per hevosen juoksu, jossa hevosen perustiedot toistuvat jokaisella juoksurivillä. Jos hevosella ei ole merkittyjä juoksuja, yksi rivi perustietoineen sisällytetään silti.

## Tärkeimmät funktiot

### `parse_lahdot(pdf_path)`
Pääjäsennysfunktio, joka käsittelee koko PDF-tiedoston.

**Parametrit:**
- `pdf_path` (str): Jäsennettävän PDF-tiedoston polku

**Palauttaa:**
- `pandas.DataFrame`: Jäsennetyt ravitiedot

### `extract_all_runs(lines, start_idx, run_pattern)`
Poimii kaikki tietyn hevosen juoksut tekstriveistä.

### `parse_age(age_text)`
Muuntaa ikätekstin numeeriseen muotoon.

### `parse_date(date_str)`
Jäsentää PP.KK-muotoiset päivämäärät älykkäällä vuoden tunnistuksella.

### `find_date_for_time(lines, start_idx, time_str, date_pattern, max_search=15)`
Apufunktio tietyn aikaennätyksen päivämäärän löytämiseksi.

## Päivämäärien käsittely

Jäsennin käyttää älykästä päivämäärien jäsentämistä:
- Päivämäärät odotetaan PP.KK-muodossa
- Jos jäsennetty päivämäärä olisi tulevaisuudessa, käytetään edellistä vuotta
- Tämä käsittelee vuodenvaihteen siirtymät oikein

## Virheenkäsittely

Jäsennin sisältää vankan virheenkäsittelyn:
- Puuttuvat tai virheelliset tiedot
- Virheelliset päivämäärämuodot
- PDF-jäsennysvirheet
- Puuttuvat hevostiedot

## Mukauttaminen

Jäsentimen mukauttaminen eri PDF-muodoille:

1. **Regex-mallit**: Päivitä regex-mallit `parse_lahdot()`-funktiossa vastaamaan PDF-muotoasi
2. **Sarakkeiden nimet**: Muokkaa sarakkeiden nimiä tietosanakirjassa
3. **Hakuparametrit**: Säädä `max_search`-parametreja hallitaksesi, kuinka kauas jäsennin etsii liittyvää tietoa

## Esimerkki

```python
import pandas as pd
from horse_parser import parse_lahdot

# Jäsennä PDF
data = parse_lahdot("oma_raviohjelma.pdf")

# Näytä perustilastot
print(f"Hevosia yhteensä: {data['Hevonen'].nunique()}")
print(f"Juoksuja yhteensä: {len(data)}")

# Tallenna Excel-tiedostoon
data.to_excel("ravitiedot.xlsx", index=False)
```

## Vianmääritys

**Yleiset ongelmat:**

1. **Ei tietoja poimittu**: Tarkista, että PDF-muoto vastaa odotettua rakennetta
2. **Päivämäärien jäsentämisvirheet**: Varmista, että päivämäärät ovat PP.KK-muodossa
3. **Puuttuvat ennätykset**: Varmista, että PDF sisältää odotetut aikammallit
4. **Koodausongelmat**: Varmista, että PDF käyttää standardia tekstikoodausta

**Vianmääritysvinkkejä:**

- Lisää print-lauseita nähdäksesi poimitut rivit
- Testaa regex-malleja esimerkkitekstillä
- Tarkista PDF-tekstin poimimisen laatu

## Lisenssi

Tämä projekti on avoimen lähdekoodin. Voit vapaasti muokata ja jakaa tarpeidesi mukaan.

## Osallistuminen

Osallistuminen on tervetullutta! Ole hyvä ja:
1. Haaroita repositorio
2. Luo ominaisuushaara
3. Tee muutoksesi
4. Lähetä pull request

## Tuki

Ongelmissa tai kysymyksissä, tarkista koodin kommentit tai luo issue repositorioon.