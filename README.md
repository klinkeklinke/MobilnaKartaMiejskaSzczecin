# 🗺️ Szczecin Live Map

**Transport Publiczny Real-Time | Park & Ride | Points of Interest**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Interaktywna mapa pokazująca dane transportu publicznego Szczecina w czasie rzeczywistym, stan parkingów Park & Ride oraz punkty POI z możliwością zakupu biletów.

---

## 🌟 Features

### ✅ Transport Publiczny (LIVE)
- **Real-time tracking** autobusów i tramwajów
- **Wizualizacja opóźnień** (pulsujące czerwone ikony)
- **Dane z API ZDiTM** (aktualizacja co ~10 sekund)
- Tooltips z informacjami: linia, kierunek, prędkość, opóźnienie

### 🅿️ Parkingi Park & Ride
- **4 potwierdzone lokalizacje**: Głębokie, Hangarowa, Turkusowa, SKM Podjuchy
- **Symulowane dane obłożenia** (kod gotowy pod prawdziwe API)
- **Kolorowe markery** wg obłożenia: 🟢 dużo miejsc, 🟡 umiarkowane, 🔴 prawie pełne

### 📍 Points of Interest
- **8 lokalizacji**: baseny (Arkonka, Fabryka Wody), kultura (Filharmonia, Teatr), dziedzictwo
- **Klik → "Kup bilet"** - redirect do oficjalnych stron
- **Info o transporcie** - jak dojechać komunikacją miejską

---

## 🏆 Dlaczego Szczecin?

> **Szczecin #1 w Polsce** w realizacji koncepcji 15-Minute City!
>
> 40,6% mieszkańców ma dostęp do usług codziennych w zasięgu 15 minut
> (pieszo, rowerem, transportem publicznym)
>
> Źródło: [Friendly City Index 2025](https://som.szczecin.pl/2025/09/23/szczecin-liderem-w-polsce-w-dazeniu-do-miasta-15-minutowego/)

**Transport publiczny to kluczowy element tej wizji!**

---

## 🚀 Quick Start

### Wymagania
- Python 3.9 lub nowszy
- Połączenie internetowe (do API ZDiTM)

### Instalacja

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/[username]/MobilnaKartaMiejskaSzczecin.git
cd MobilnaKartaMiejskaSzczecin

# 2. Utwórz wirtualne środowisko (zalecane)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# lub
venv\Scripts\activate  # Windows

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Uruchom aplikację
streamlit run app.py
```

### Aplikacja otworzy się automatycznie w przeglądarce na `http://localhost:8501`

---

## 📁 Struktura projektu

```
MobilnaKartaMiejskaSzczecin/
├── app.py                      # 🎯 Główna aplikacja Streamlit
├── requirements.txt            # 📦 Zależności Python
├── README.md                   # 📖 Ten plik
│
├── docs/                       # 📚 Dokumentacja
│   ├── TECH_SPEC.md           # Specyfikacja techniczna
│   ├── IMPLEMENTATION.md      # Architektura i wybór technologii
│   ├── USER_GUIDE.md          # Instrukcja użytkownika
│   ├── GAPS_ANALYSIS.md       # Analiza Mapbox / Parking API
│   ├── RESEARCH_FINDINGS.md   # Research o 15-minute city
│   ├── PARKING_STATUS.md      # Status parkingów P+R
│   └── ZDITM_OUTREACH.md      # Strategia kontaktu z ZDiTM
│
├── data/                       # 📊 Dane statyczne
│   └── poi_locations.json     # 8 POI z pełnymi danymi
│
├── utils/                      # 🛠️ Moduły pomocnicze
│   ├── __init__.py
│   ├── zditm_api.py           # ✅ LIVE data z ZDiTM
│   ├── mock_parking.py        # ⚠️ Symulowane dane parkingów
│   └── map_builder.py         # 🗺️ Budowanie map Folium
│
├── app.md                      # Opis projektu (Figma prompt)
├── APIs.md                     # Dokumentacja API + rekomendacje map
└── sources.md                  # 29 źródeł (15-min city, turystyka...)
```

---

## 🎮 Jak używać?

### Sidebar - Kontrolki

1. **Warstwy mapy** - włącz/wyłącz:
   - 🚌 Transport publiczny
   - 🅿️ Parkingi P+R
   - 📍 Punkty POI

2. **Opcje transportu:**
   - ⚠️ Tylko opóźnione pojazdy (filtr)

3. **Odświeżanie:**
   - Slider: 10-60 sekund
   - 🔄 Auto-odświeżanie (on/off)

### Interakcja z mapą

- **Klik na pojazd** → tooltip z informacjami (linia, opóźnienie, prędkość)
- **Klik na parking** → popup z obłożeniem (wolne/zajęte)
- **Klik na POI** → popup z opisem + przycisk "Kup bilet"

---

## 📊 Tech Stack

| Komponent | Technologia | Dlaczego? |
|-----------|-------------|-----------|
| **Frontend** | Streamlit | Szybki prototyping, Python end-to-end |
| **Mapy** | Folium (Leaflet.js) | Darmowe, open source, GTFS-friendly |
| **Podkład** | OpenStreetMap | Darmowe tiles, doskonałe dla Polski |
| **API** | ZDiTM Szczecin | Oficjalne API transportu publicznego |
| **Język** | Python 3.9+ | Ecosystem data science, łatwa integracja |

**Dlaczego NIE Mapbox?** → Zobacz [docs/GAPS_ANALYSIS.md](docs/GAPS_ANALYSIS.md) (brak GTFS routing, koszt $50-100/mc)

---

## 📡 API ZDiTM

### Endpoints używane:

```
GET https://www.zditm.szczecin.pl/api/v1/vehicles
```

**Rate limit:** 100 requests/minute per IP
**Format:** JSON
**Aktualizacja:** ~10 sekund

**Dokumentacja:** https://www.zditm.szczecin.pl/en/zditm/for-developers

### Przykład odpowiedzi:

```json
{
  "data": [
    {
      "line_number": "75",
      "vehicle_type": "bus",
      "direction": "Osiedle Zawadzkiego",
      "latitude": 53.4571685791,
      "longitude": 14.4967002869,
      "velocity": 15,
      "punctuality": -2,  // 2 min opóźnienia!
      "updated_at": "2025-10-25T20:06:27Z"
    }
  ]
}
```

---

## ⚠️ Ważne informacje o danych

### ✅ Transport publiczny - LIVE
- Dane real-time z API ZDiTM
- Prawdziwe pozycje GPS pojazdów
- Rzeczywiste opóźnienia (`punctuality` field)

### ⚠️ Parkingi P+R - SYMULOWANE
- **ZDiTM nie udostępnia API** dla danych parkingowych
- Dane obłożenia są **symulowane** (realistyczna algorytmika)
- **Lokalizacje potwierdzone** z API ZDiTM (26 przystanków z `park_and_ride: true`)
- **Kod gotowy** do podmiany na prawdziwe API (gdy będzie dostępne)

**Dlaczego mock data?** → Zobacz [docs/PARKING_STATUS.md](docs/PARKING_STATUS.md)

### 📍 POI - STATYCZNE
- Dane zebrane ręcznie z oficjalnych źródeł
- Współrzędne zweryfikowane
- Aktualne linki do stron biletowych

---

## 🧪 Testing

### Ręczny test (quick check):

```bash
# Test ZDiTM API client
cd utils
python zditm_api.py

# Test mock parking data
python mock_parking.py

# Test map builder (requires data)
python map_builder.py
```

**Spodziewany output:**
```
🚌 ZDiTM API Client - Test
==================================================
📡 Fetching vehicle data...
✅ Received 150 vehicles

📊 Statistics:
  Total vehicles: 150
  Buses: 98
  Trams: 52
  On time: 135
  Delayed: 15
  Avg delay: 3.2 min
```

---

## 📚 Dokumentacja

### Dla deweloperów:
- **[TECH_SPEC.md](docs/TECH_SPEC.md)** - Szczegółowa specyfikacja techniczna
- **[IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** - Architektura, wybór tech stack
- **[GAPS_ANALYSIS.md](docs/GAPS_ANALYSIS.md)** - Dlaczego NIE Mapbox? Dlaczego brak parking API?

### Dla użytkowników:
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Instrukcja użytkownika, FAQ, troubleshooting

### Research i kontekst:
- **[RESEARCH_FINDINGS.md](docs/RESEARCH_FINDINGS.md)** - Szczecin 15-minute city, turystyka, smart mobility
- **[sources.md](sources.md)** - 29 źródeł akademickich i industry
- **[PARKING_STATUS.md](docs/PARKING_STATUS.md)** - Analiza P+R (4 operacyjne, Dąbie w budowie)

---

## 🔮 Roadmap

### v1.0 (Current) - Tech Demo ✅
- [x] Live tracking pojazdów ZDiTM
- [x] Mock parking data (4 lokalizacje)
- [x] 8 POI z biletami
- [x] Streamlit UI
- [x] Auto-refresh (basic)

### v2.0 (Planned) - Beta Production
- [ ] **Real parking API** (jeśli ZDiTM udostępni)
- [ ] **Smooth animations** (custom Streamlit component)
- [ ] **Routing A→B** (GTFS-based)
- [ ] **React migration** (multi-user support)
- [ ] **PWA** (Progressive Web App, offline mode)

### v3.0 (Future) - Full Platform
- [ ] SKM integration (Szczecin Metropolitan Railway)
- [ ] Bikeshare / e-scooter data
- [ ] Carbon footprint calculator
- [ ] Gamification (badges, achievements)
- [ ] Social features (share trips)

---

## 🤝 Kontakt z ZDiTM

Chcemy prawdziwe API dla parkingów P+R!

**Email template:** [docs/ZDITM_OUTREACH.md](docs/ZDITM_OUTREACH.md)

**Argumenty:**
- User experience (oszczędność czasu mieszkańców)
- Ekologia (mniej aut szukających parkingu)
- Smart City leadership (Szczecin pierwszy w PL z pełnym API)
- Analytics dla miasta (data-driven decisions)

---

## 🐛 Troubleshooting

### Aplikacja nie startuje

```bash
# Sprawdź wersję Python
python --version  # Powinna być 3.9+

# Reinstaluj zależności
pip install --upgrade -r requirements.txt
```

### Mapa się nie ładuje

- Sprawdź połączenie internetowe (potrzebne dla API ZDiTM i OSM tiles)
- Sprawdź czy `data/poi_locations.json` istnieje
- Otwórz DevTools (F12) i sprawdź console errors

### Brak danych o pojazdach

- API ZDiTM może być tymczasowo niedostępne
- Aplikacja użyje cached data (max 30s starych)
- Sprawdź status API: https://www.zditm.szczecin.pl/api/v1/vehicles

**Więcej:** [docs/USER_GUIDE.md](docs/USER_GUIDE.md) sekcja Troubleshooting

---

## 📄 License

MIT License - feel free to use, modify, distribute

---

## 🙏 Credits & Sources

### APIs
- **ZDiTM Szczecin** - Transport publiczny API (https://www.zditm.szczecin.pl)
- **OpenStreetMap** - Map tiles (© OSM contributors)

### Data Sources
- **Friendly City Index 2025** - 15-minute city ranking
- **GUS** - Turystyka w Szczecinie
- **Visit Szczecin** - Statystyki turystyczne

### Tech Stack
- **Streamlit** - Web framework (https://streamlit.io)
- **Folium** - Maps library (https://python-visualization.github.io/folium)
- **Leaflet.js** - Interactive maps (https://leafletjs.com)

**Total sources:** 29 (see [sources.md](sources.md))

---

## 📞 Contact & Support

- **GitHub Issues:** [Report bugs here]
- **Documentation:** [docs/](docs/)
- **Email:** [your-email@example.com]

---

Made with ❤️ for Szczecin - **#1 15-Minute City in Poland!**

**Last updated:** 2025-10-25