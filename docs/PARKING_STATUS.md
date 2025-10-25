# Park & Ride Szczecin - Status Aktualny
## Analiza dostępności parkingów P+R w API i rzeczywistości

**Data analizy:** 2025-10-25
**Źródła:** ZDiTM API, oficjalna strona ZDiTM, wyszukiwanie online

---

## Executive Summary

### Kluczowe ustalenia

✅ **4 parkingi P+R działają** (potwierdzone w API i na stronie ZDiTM)
⏳ **P+R Dąbie w budowie** (completion: koniec 2024 / Q1 2025)
❌ **P+R Dąbie NIE MA w API** (parking_and_ride = false dla przystanków Dąbie)

### Rekomendacja
**NIE dodawać P+R Dąbie do mock data** - parking nie jest jeszcze operacyjny.
Użyć tylko 4 potwierdzonych parkingów.

---

## 1. Analiza API ZDiTM

### Zapytanie wykonane:
```bash
curl -s "https://www.zditm.szczecin.pl/api/v1/stops" | \
  jq '.data[] | select(.park_and_ride == true)'
```

### Wyniki: 4 lokalizacje Park & Ride

| Parking | Liczba przystanków | Koordinaty (śr.) | Status |
|---------|-------------------|------------------|--------|
| **Głębokie** | 7 przystanków | 53.471°N, 14.487°E | ✅ Operacyjny |
| **Hangarowa** | 4 przystanki | 53.388°N, 14.626°E | ✅ Operacyjny |
| **Turkusowa** | 10 przystanków | 53.380°N, 14.643°E | ✅ Operacyjny |
| **SKM Podjuchy** | 5 przystanków | 53.360°N, 14.587°E | ✅ Operacyjny |

**Total przystanków z park_and_ride = true:** 26

---

## 2. Szczegółowe dane z API

### P+R Głębokie (7 przystanków)

```json
{
  "name": "Głębokie",
  "location": "Skrzyżowanie ulic Miodowej i Kupczyka",
  "coordinates": {
    "latitude": 53.471,
    "longitude": 14.487
  },
  "stops": [
    {"number": "31740", "lat": 53.470838, "lon": 14.486788},
    {"number": "31741", "lat": 53.471148, "lon": 14.486624},
    {"number": "31742", "lat": 53.471175, "lon": 14.486799},
    {"number": "31743", "lat": 53.471199, "lon": 14.48696},
    {"number": "31751", "lat": 53.471023, "lon": 14.486825},
    {"number": "31752", "lat": 53.471052, "lon": 14.486976},
    {"number": "31753", "lat": 53.471083, "lon": 14.487121}
  ],
  "park_and_ride": true
}
```

---

### P+R Hangarowa (4 przystanki)

```json
{
  "name": "Hangarowa",
  "location": "Skrzyżowanie ulic Eskadrowej, Leszczynowej i Hangarowej",
  "coordinates": {
    "latitude": 53.388,
    "longitude": 14.625
  },
  "stops": [
    {"number": "80111", "lat": 53.388743, "lon": 14.624029},
    {"number": "80112", "lat": 53.387729, "lon": 14.626029},
    {"number": "80113", "lat": 53.387622, "lon": 14.626225},
    {"number": "80114", "lat": 53.38736, "lon": 14.626515}
  ],
  "park_and_ride": true
}
```

---

### P+R Turkusowa (10 przystanków!)

```json
{
  "name": "Turkusowa",
  "location": "Przy pętli tramwajowo-autobusowej Turkusowa",
  "coordinates": {
    "latitude": 53.380,
    "longitude": 14.643
  },
  "stops": [
    {"number": "86912", "lat": 53.379125, "lon": 14.643275},
    {"number": "86921", "lat": 53.379713, "lon": 14.643155},
    {"number": "86922", "lat": 53.379969, "lon": 14.642978},
    {"number": "86931", "lat": 53.380023, "lon": 14.643107},
    {"number": "86932", "lat": 53.380087, "lon": 14.643102},
    {"number": "86933", "lat": 53.380129, "lon": 14.64315},
    {"number": "86941", "lat": 53.380124, "lon": 14.643542},
    {"number": "86942", "lat": 53.380399, "lon": 14.643504},
    {"number": "86944", "lat": 53.380252, "lon": 14.644156},
    {"number": "86945", "lat": 53.379914, "lon": 14.64425}
  ],
  "park_and_ride": true,
  "note": "Największy P+R w Szczecinie (10 przystanków = duża pętla)"
}
```

---

### P+R SKM Podjuchy (5 przystanków)

```json
{
  "name": "SKM Podjuchy",
  "location": "Ulica Metalowa (przy stacji SKM)",
  "coordinates": {
    "latitude": 53.360,
    "longitude": 14.587
  },
  "stops": [
    {"number": "82711", "lat": 53.360557, "lon": 14.587725},
    {"number": "82712", "lat": 53.360051, "lon": 14.587263},
    {"number": "82721", "lat": 53.360667, "lon": 14.587199},
    {"number": "82722", "lat": 53.360636, "lon": 14.587275},
    {"number": "82723", "lat": 53.360598, "lon": 14.587368}
  ],
  "park_and_ride": true,
  "note": "Integracja z koleją metropolitalną (SKM)"
}
```

---

## 3. Potwierdzenie ze strony ZDiTM

### Oficjalna lista (zditm.szczecin.pl/en/passenger/park-ride)

✅ **P+R Głębokie**
- Lokalizacja: Skrzyżowanie ulic Miodowej i Kupczyka
- Status: **OPERACYJNY**
- Charakterystyka: Darmowy, publiczny, niestrzeżony, 24/7, max 24h parking

✅ **P+R Hangarowa**
- Lokalizacja: Skrzyżowanie ulic Eskadrowej, Leszczynowej i Hangarowej
- Status: **OPERACYJNY**
- Charakterystyka: Jak wyżej

✅ **P+R Turkusowa**
- Lokalizacja: Przy pętli tramwajowo-autobusowej Turkusowa
- Status: **OPERACYJNY**
- Charakterystyka: Jak wyżej

✅ **P+R Podjuchy**
- Lokalizacja: Ulica Metalowa
- Status: **OPERACYJNY**
- Charakterystyka: Jak wyżej

**Wspólne cechy wszystkich 4:**
- Free (darmowe)
- Public (publiczne)
- Unguarded (niestrzeżone)
- 24/7 open (otwarte całą dobę)
- Max 24h parking
- Do 3.5 tony (pojazdy osobowe + dostawcze)
- Miejsca dla osób niepełnosprawnych
- Parking dla rowerów
- Tablica informująca o wolnych miejscach (physical board)

---

## 4. P+R Dąbie - Status

### ❌ NIE ZNALEZIONY w API

**Test wykonany:**
```bash
curl -s "https://www.zditm.szczecin.pl/api/v1/stops" | \
  jq '.data[] | select(.name | contains("Dąbie")) | {name, park_and_ride}'
```

**Wynik:**
```json
// Przystanki "Dąbie" istnieją, ale:
{
  "name": "Dąbie",
  "park_and_ride": false  // ❌
}
```

---

### ⏳ Status budowy (z research)

#### Szczecin Metropolitan Railway Modernisation

**Projekt:** Modernizacja Szczecińskiej Kolei Metropolitalnej
**Scope:**
- 23.7 km sieci kolejowej
- Rekonstrakcja 17 stacji
- Budowa 10 nowych przystanków
- **Park & Ride facilities** (w tym Dąbie)

**Timeline:**
- Start projektu: **2019**
- Prace w Szczecin Dąbie: **po 2023**
- Planowane zakończenie budowy stacji Dąbie: **koniec 2024**
- Zakończenie wszystkich prac: **Q1 2025**
- Certyfikaty i pozwolenia: **koniec 2025**

**Źródło:** [Railway Pro - Szczecin rail modernisation](https://www.railwaypro.com/wp/szczecin-metropolitan-rail-modernisation-to-be-completed-in-2025/)

---

### 🔍 Dodatkowe wyszukiwanie

**Wyszukiwane hasła:**
- "Park and Ride Szczecin Dąbie"
- "P+R Dąbie otwarcie"
- "Szczecin Dąbie parking 2024"

**Wyniki:**
- Brak oficjalnych komunikatów o otwarciu P+R Dąbie
- Projekt SKM Dąbie w toku (railway station reconstruction)
- P+R Dąbie planowany **jako część projektu SKM**
- Brak potwierdzenia operacyjności

---

## 5. Porównanie: Planowane vs Działające

### Działające parkingi (4)

| Parking | API | Strona ZDiTM | Status |
|---------|-----|--------------|--------|
| **Głębokie** | ✅ park_and_ride: true | ✅ Listed | 🟢 **OPERACYJNY** |
| **Hangarowa** | ✅ park_and_ride: true | ✅ Listed | 🟢 **OPERACYJNY** |
| **Turkusowa** | ✅ park_and_ride: true | ✅ Listed | 🟢 **OPERACYJNY** |
| **SKM Podjuchy** | ✅ park_and_ride: true | ✅ Listed | 🟢 **OPERACYJNY** |

---

### Planowane / W budowie

| Parking | API | Strona ZDiTM | Planowane otwarcie | Status |
|---------|-----|--------------|-------------------|--------|
| **Dąbie** | ❌ park_and_ride: false | ❌ Not listed | Koniec 2024 / Q1 2025 | 🟡 **W BUDOWIE** |
| **Pomorzany** (?) | ❓ Nie znaleziono | ❌ Not listed | Nieznane | ❓ **BRAK DANYCH** |
| **Kijewo** (?) | ❓ Nie znaleziono | ❌ Not listed | Nieznane | ❓ **BRAK DANYCH** |

**Uwaga:** Pomorzany i Kijewo były wymienione w naszym mock data, ale **NIE MA ich w API ani na stronie ZDiTM!**

---

## 6. Implikacje dla projektu

### ❌ Co USUNĄĆ z mock data

```python
# TE PARKINGI NIE ISTNIEJĄ (lub nie są operacyjne):

REMOVE_FROM_MOCK = [
    "P&R Pomorzany",  # ❌ Brak w API i na stronie ZDiTM
    "P&R Kijewo",     # ❌ Brak w API i na stronie ZDiTM
    "P&R Dąbie"       # ⏳ W budowie, otwarcie Q1 2025
]
```

---

### ✅ Co ZACHOWAĆ w mock data (4 parkingi)

```python
# TYLKO TE 4 DZIAŁAJĄCE PARKINGI:

PARKING_LOTS_OPERATIONAL = [
    {
        "id": 1,
        "name": "P+R Głębokie",
        "location": "Skrzyżowanie ulic Miodowej i Kupczyka",
        "latitude": 53.471,
        "longitude": 14.487,
        "total_spaces": 150,  # Szacunek (brak oficjalnych danych)
        "status": "operational"
    },
    {
        "id": 2,
        "name": "P+R Hangarowa",
        "location": "Skrzyżowanie ulic Eskadrowej, Leszczynowej i Hangarowej",
        "latitude": 53.388,
        "longitude": 14.625,
        "total_spaces": 120,  # Szacunek
        "status": "operational"
    },
    {
        "id": 3,
        "name": "P+R Turkusowa",
        "location": "Przy pętli tramwajowo-autobusowej Turkusowa",
        "latitude": 53.380,
        "longitude": 14.643,
        "total_spaces": 200,  # Szacunek (największy - 10 przystanków!)
        "status": "operational"
    },
    {
        "id": 4,
        "name": "P+R SKM Podjuchy",
        "location": "Ulica Metalowa (przy stacji SKM)",
        "latitude": 53.360,
        "longitude": 14.587,
        "total_spaces": 100,  # Szacunek
        "status": "operational"
    }
]
```

---

### 🔮 Future additions (gdy będą operacyjne)

```python
# DO DODANIA GDY POJAWIĄ SIĘ W API:

PARKING_LOTS_PLANNED = [
    {
        "id": 5,
        "name": "P+R Dąbie",
        "location": "Przy stacji SKM Dąbie",
        "latitude": None,  # Do ustalenia gdy się otworzy
        "longitude": None,
        "total_spaces": None,
        "status": "planned",
        "expected_opening": "Q1 2025"
    }
]
```

---

## 7. Rekomendacje

### Dla wersji v1.0 (MVP)

✅ **UŻYWAJ TYLKO 4 PARKINGÓW:**
1. Głębokie
2. Hangarowa
3. Turkusowa
4. SKM Podjuchy

**Dlaczego?**
- ✅ Potwierdzone w API ZDiTM (park_and_ride: true)
- ✅ Potwierdzone na oficjalnej stronie ZDiTM
- ✅ Działające (open 24/7)
- ✅ Precyzyjne koordinaty z API

❌ **NIE UŻYWAJ:**
- Pomorzany (nie istnieje lub nieoperacyjny)
- Kijewo (nie istnieje lub nieoperacyjny)
- Dąbie (w budowie, Q1 2025)

---

### Monitoring nowych parkingów

#### Automatyczny check (opcjonalnie)

```python
import requests

def check_new_parkings():
    """
    Sprawdza czy pojawiły się nowe P+R w API
    """
    response = requests.get('https://www.zditm.szczecin.pl/api/v1/stops')
    data = response.json()

    parkings = {}
    for stop in data['data']:
        if stop.get('park_and_ride'):
            name = stop['name']
            if name not in parkings:
                parkings[name] = []
            parkings[name].append({
                'number': stop['number'],
                'lat': stop['latitude'],
                'lon': stop['longitude']
            })

    print(f"Znaleziono {len(parkings)} parkingów P+R:")
    for name, stops in parkings.items():
        print(f"  • {name}: {len(stops)} przystanków")

    return parkings

# Wywołuj co tydzień lub przed każdym release
# Jeśli pojawi się "Dąbie" → update mock data!
```

---

### Komunikacja w aplikacji

#### Disclaimer (v1.0)

```python
st.info("""
⚠️ **Parking data disclaimer:**

Dane o obłożeniu parkingów są SYMULOWANE (brak API real-time od ZDiTM).

Lokalizacje parkingów P+R są RZECZYWISTE i potwierdzone:
✅ P+R Głębokie
✅ P+R Hangarowa
✅ P+R Turkusowa
✅ P+R SKM Podjuchy

Źródło: ZDiTM API (https://www.zditm.szczecin.pl/api/v1/stops)
Ostatnia weryfikacja: 2025-10-25
""")
```

---

#### Future notice (gdy Dąbie się otworzy)

```python
st.success("""
🆕 **Nowy parking P+R!**

P+R Dąbie został otwarty w Q1 2025 i dodany do aplikacji.

Obecnie dostępne parkingi: 5
• Głębokie
• Hangarowa
• Turkusowa
• SKM Podjuchy
• **Dąbie** (NOWY!)
""")
```

---

## 8. Aktualizacja dokumentacji

### Pliki do zmiany

#### utils/mock_parking.py

```python
# PRZED (BŁĘDNE):
PARKING_LOTS = [
    {"name": "P&R Pomorzany", ...},  # ❌ Nie istnieje!
    {"name": "P&R Kijewo", ...},     # ❌ Nie istnieje!
    {"name": "P&R Turkusowa", ...},  # ✅ OK
    {"name": "P&R Dąbie", ...}       # ⏳ W budowie
]

# PO (POPRAWNE):
PARKING_LOTS = [
    {"name": "P+R Głębokie", ...},      # ✅ Potwierdzony
    {"name": "P+R Hangarowa", ...},     # ✅ Potwierdzony
    {"name": "P+R Turkusowa", ...},     # ✅ Potwierdzony
    {"name": "P+R SKM Podjuchy", ...}   # ✅ Potwierdzony
]
```

---

#### docs/TECH_SPEC.md

**Sekcja 2.2 - Park & Ride Mock Data:**

Aktualizacja tabeli lokalizacji:

```markdown
## PRZED:
| P&R | Lat | Lon | Status |
|-----|-----|-----|--------|
| Pomorzany | 53.4284 | 14.4833 | ❌ |
| Kijewo | 53.4012 | 14.5289 | ❌ |

## PO:
| P&R | Lat | Lon | Status | Przystanki w API |
|-----|-----|-----|--------|------------------|
| Głębokie | 53.471 | 14.487 | ✅ | 7 |
| Hangarowa | 53.388 | 14.625 | ✅ | 4 |
| Turkusowa | 53.380 | 14.643 | ✅ | 10 |
| SKM Podjuchy | 53.360 | 14.587 | ✅ | 5 |
| Dąbie | TBD | TBD | ⏳ Q1 2025 | 0 (planned) |
```

---

## 9. Summary & Action Items

### ✅ Confirmed Facts

1. **4 parkingi P+R działają** w Szczecinie (Głębokie, Hangarowa, Turkusowa, Podjuchy)
2. **26 przystanków total** ma flagę park_and_ride: true w API
3. **P+R Dąbie NIE DZIAŁA** - w budowie, otwarcie Q1 2025
4. **Pomorzany i Kijewo** - brak w API, prawdopodobnie nie istnieją jako P+R

### ❌ Co było błędne w pierwotnych założeniach

- ❌ Mock data zawierały nieistniejące parkingi (Pomorzany, Kijewo)
- ❌ Zakładaliśmy że Dąbie już działa (faktycznie: w budowie)

### ✅ Action Items

- [ ] **Update mock_parking.py** - tylko 4 parkingi
- [ ] **Update TECH_SPEC.md** - popraw tabelę parkingów
- [ ] **Add disclaimer w UI** - komunikat o symulowanych danych
- [ ] **Monitor API** - check co tydzień czy Dąbie się pojawił
- [ ] **Dokumentacja** - ten plik (PARKING_STATUS.md) jako reference

---

## 10. Załączniki

### A. Pełna lista przystanków z park_and_ride: true

**26 przystanków, 4 lokalizacje:**

```
Głębokie (7):
  31740, 31741, 31742, 31743, 31751, 31752, 31753

Hangarowa (4):
  80111, 80112, 80113, 80114

Turkusowa (10):
  86912, 86921, 86922, 86931, 86932, 86933,
  86941, 86942, 86944, 86945

SKM Podjuchy (5):
  82711, 82712, 82721, 82722, 82723
```

### B. Źródła

1. **ZDiTM API:** https://www.zditm.szczecin.pl/api/v1/stops
2. **ZDiTM Park & Ride:** https://www.zditm.szczecin.pl/en/passenger/park-ride
3. **Railway Pro:** https://www.railwaypro.com/wp/szczecin-metropolitan-rail-modernisation-to-be-completed-in-2025/
4. **Analiza wykonana:** 2025-10-25, curl + jq

---

**Document Status:** ✅ VERIFIED
**Last Check:** 2025-10-25
**Next Review:** Co tydzień (monitoring Dąbie)

**Wniosek:** Używaj TYLKO 4 potwierdzonych parkingów. Dąbie dodaj gdy pojawi się w API (Q1 2025).
