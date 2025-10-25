# Analiza Braków i Ograniczeń
## Mapbox vs Park & Ride API - Szczegółowe Wyjaśnienie

**Data:** 2025-10-25
**Autor:** Tech Analysis Team

---

## Spis treści

1. [Mapbox - Ograniczenia transportu publicznego](#1-mapbox---ograniczenia-transportu-publicznego)
2. [Park & Ride API - Brak danych real-time](#2-park--ride-api---brak-danych-real-time)
3. [Porównanie alternatyw](#3-porównanie-alternatyw)
4. [Rekomendacje dla projektu](#4-rekomendacje-dla-projektu)
5. [Potencjalne rozwiązania przyszłościowe](#5-potencjalne-rozwiązania-przyszłościowe)

---

## 1. Mapbox - Ograniczenia transportu publicznego

### 1.1 Problem główny: Brak wsparcia GTFS routing

#### Co oferuje Mapbox Directions API?

Mapbox Directions API wspiera **tylko 4 tryby transportu:**

| Tryb | Status | Możliwości |
|------|--------|------------|
| 🚗 **Driving** | ✅ Dostępne | • Standard driving<br>• Driving with traffic<br>• Electric vehicles (z ładowaniem) |
| 🚶 **Walking** | ✅ Dostępne | • Pedestrian routing<br>• Sidewalk preference |
| 🚴 **Cycling** | ✅ Dostępne | • Bike lanes preference<br>• Elevation awareness |
| 🚌 **Public Transit** | ❌ **BRAK** | • **Nie wspiera GTFS**<br>• **Nie wspiera rozkładów jazdy**<br>• **Nie wspiera przesiadek** |

**Źródło:** [Mapbox Directions API Documentation](https://docs.mapbox.com/api/navigation/directions/)

---

### 1.2 Co to oznacza w praktyce?

#### Scenariusz: Użytkownik chce dojechać z hotelu do Arkonki

**Z Mapbox:**
```javascript
// Mapbox może zwrócić TYLKO:
{
  "routes": [
    {
      "mode": "driving",        // Samochód
      "duration": 900,          // 15 minut
      "distance": 8500          // 8.5 km
    },
    {
      "mode": "walking",        // Pieszo
      "duration": 6300,         // 105 minut (!)
      "distance": 8500
    }
  ]
}

// ❌ NIE MOŻE zwrócić:
// - Tramwaj linia 1 → przesiadka → Autobus 80
// - Czasy odjazdu (10:15, 10:30, 10:45...)
// - Cena biletu
// - Opóźnienia real-time
```

**Dla porównania - idealny routing (GTFS):**
```json
{
  "routes": [
    {
      "mode": "transit",
      "duration": 1800,           // 30 minut
      "legs": [
        {
          "mode": "walk",
          "from": "Hotel",
          "to": "Przystanek Plac Rodła",
          "duration": 300           // 5 min
        },
        {
          "mode": "tram",
          "line": "1",
          "from": "Plac Rodła",
          "to": "Las Arkoński",
          "departure": "10:15",
          "arrival": "10:38",
          "duration": 1380,
          "delay": -2               // 2 min wcześniej (!)
        },
        {
          "mode": "walk",
          "from": "Las Arkoński",
          "to": "Arkonka",
          "duration": 120           // 2 min
        }
      ],
      "price": {
        "amount": 4.40,
        "currency": "PLN",
        "ticket_type": "single"
      }
    }
  ]
}
```

---

### 1.3 Dlaczego Mapbox nie wspiera GTFS?

#### Biznesowe powody

1. **Fokus na automotive**
   - Główni klienci Mapbox: Uber, Lyft, Tesla
   - Prywatny transport > transport publiczny

2. **Złożoność GTFS**
   - Każde miasto ma inny format danych
   - Rozkłady jazdy zmieniają się często (weekendy, święta, remonty)
   - Potrzeba real-time updates (GTFS-RT)
   - Koszt utrzymania infrastruktury

3. **Konkurencja z Google Maps**
   - Google ma monopol na transit routing (Google Maps, Google Directions API)
   - Trudno konkurować bez ogromnych inwestycji

#### Techniczne wyzwania

```
Transport publiczny wymaga:
┌─────────────────────────────────────────────────┐
│ GTFS Static (rozkłady)                          │
│ + GTFS-RT (opóźnienia, odwołania)               │
│ + Multi-modal routing (pieszo + tram + bus)     │
│ + Transfer logic (przesiadki, czasy oczekiwania)│
│ + Fare calculation (strefy, zniżki, karnety)    │
│ + Accessibility (niskopodłogowe, windy)         │
│ + Service alerts (remonty, objazdy)             │
└─────────────────────────────────────────────────┘
              vs.
┌─────────────────────────────────────────────────┐
│ Driving routing:                                │
│ OSM roads + traffic data = DONE ✅              │
└─────────────────────────────────────────────────┘
```

---

### 1.4 Mapbox Transit v2 Tileset - co to jest?

Mapbox **oferuje wizualizację** tras transit, ale **NIE routing:**

```javascript
// ✅ CO MOŻNA zrobić z Transit v2 Tileset:
map.addSource('transit-lines', {
  type: 'vector',
  url: 'mapbox://mapbox.transit-v2'
});

// Rezultat: Linie tramwajowe/autobusowe NARYSOWANE na mapie
// (statyczne, wizualne, bez rozkładu jazdy)

// ❌ CZEGO NIE MOŻNA:
// - Obliczyć trasy "jak dojechać tramwajem z A do B"
// - Pokazać godzin odjazdów
// - Uwzględnić opóźnień
```

**To jak różnica między:**
- **Mapą papierową** (widzisz gdzie biegną linie) ← Mapbox Transit Tileset
- **Plannerem podróży** (mówi Ci którym tramwajem jechać i o której) ← GTFS Routing (brak w Mapbox!)

---

### 1.5 Workaround - jak rozwiązać problem Mapbox?

#### Opcja A: Mapbox (mapa) + Transitland API (routing)

```javascript
// 1. Użyj Mapbox do wyświetlenia mapy
const map = new mapboxgl.Map({...});

// 2. Użyj Transitland do obliczenia trasy
const route = await fetch('https://transit.land/api/v2/routing', {
  params: {
    from: '53.428,14.552',
    to: '53.453,14.483',
    mode: 'transit'
  }
});

// 3. Narysuj trasę na Mapbox
route.legs.forEach(leg => {
  map.addLayer({
    id: 'route-' + leg.id,
    type: 'line',
    source: leg.geometry
  });
});
```

**Koszty:**
- Mapbox: ~$50-100/miesiąc (przy średnim ruchu)
- Transitland: **DARMOWE** (open data) ✅

**Wady:**
- Więcej kodu (2 API zamiast 1)
- Możliwe rozbieżności w danych
- Brak single vendor support

---

#### Opcja B: Leaflet.js + OpenStreetMap (POLECANE!)

```javascript
// WSZYSTKO DARMOWE:
// 1. Leaflet.js (darmowy) - mapa
// 2. OpenStreetMap (darmowy) - tiles
// 3. ZDiTM API (darmowy) - dane transportu Szczecina
// 4. GTFS (darmowy) - rozkłady jazdy

const map = L.map('map').setView([53.4285, 14.5528], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Własny routing engine z GTFS:
const route = calculateTransitRoute(fromCoords, toCoords, gtfsData);
```

**Dlaczego lepsze od Mapbox dla naszego projektu?**

| Kryterium | Mapbox | Leaflet.js + OSM |
|-----------|--------|------------------|
| **Koszt** | $50-100/mc | **$0** ✅ |
| **GTFS support** | ❌ Brak | ✅ Pełne (własna implementacja) |
| **ZDiTM integration** | ⚠️ Dodatkowy kod | ✅ Natywnie |
| **Customization** | ⚠️ Ograniczone | ✅ Pełna kontrola |
| **Offline mode** | ❌ | ✅ Możliwe (cache tiles) |
| **Vendor lock-in** | ⚠️ Tak | ✅ Nie |

---

### 1.6 Podsumowanie: Dlaczego NIE Mapbox?

```
┌─────────────────────────────────────────────────────────┐
│  MAPBOX - Analiza dla projektu Szczecin                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ✅ ZALETY:                                             │
│  • Piękny design (3D buildings, smooth animations)      │
│  • Premium feeling                                       │
│  • Świetny dla driving/walking/cycling                  │
│                                                          │
│  ❌ DEALBREAKERS dla naszego projektu:                  │
│  • Brak GTFS routing (KRYTYCZNE!)                       │
│  • Koszt $50-100/mc (mamy darmowe alternatywy)          │
│  • Wymaga dodatkowej usługi dla transit                 │
│  • Overkill dla 2D map (nie używamy 3D)                 │
│                                                          │
│  🎯 DECYZJA: NIE WYBIERAMY MAPBOX                       │
│                                                          │
│  Zamiast tego: Leaflet.js + OSM + ZDiTM API             │
│  • Darmowe                                               │
│  • Pełna kontrola nad GTFS                              │
│  • Dedykowane dla transportu publicznego                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Park & Ride API - Brak danych real-time

### 2.1 Co znaleźliśmy w API ZDiTM?

#### Endpoint `/api/v1/stops` zawiera pole `park_and_ride`

```bash
curl https://www.zditm.szczecin.pl/api/v1/stops | jq '.data[0]'
```

**Odpowiedź:**
```json
{
  "id": 1,
  "latitude": 53.4284,
  "longitude": 14.4833,
  "name": "Pomorzany",
  "number": "1001",
  "park_and_ride": true,        // ✅ Informacja: "Jest P&R przy tym przystanku"
  "railway_station_name": null,
  "request_stop": false,
  "updated_at": "2025-10-25T20:00:00Z"
}
```

#### Co to pole oznacza?

**`park_and_ride: true`** = "W pobliżu tego przystanku jest parking Park & Ride"

**To wszystko.** ❌

---

### 2.2 Czego BRAKUJE?

#### Potrzebne dane dla użytkownika:

```json
// ❌ BRAK W API:
{
  "parking_id": 1,
  "name": "P&R Pomorzany",
  "location": {
    "latitude": 53.4284,
    "longitude": 14.4833
  },

  // 🔴 KRYTYCZNE BRAKI:
  "capacity": {
    "total_spaces": 150,              // ❌ Brak
    "occupied_spaces": 87,            // ❌ Brak
    "available_spaces": 63,           // ❌ Brak
    "occupancy_percent": 58           // ❌ Brak
  },

  "real_time": {
    "last_updated": "2025-10-25T20:30:15Z",  // ❌ Brak
    "trend": "filling_up",                    // ❌ Brak
    "predicted_full_time": "21:45"            // ❌ Brak (advanced)
  },

  "pricing": {
    "price_per_hour": 0,              // ❌ Brak (darmowy, ale nie w API)
    "max_stay_hours": 24              // ❌ Brak
  },

  "features": {
    "security": "cctv",               // ❌ Brak
    "lighting": true,                 // ❌ Brak
    "accessible_spaces": 5            // ❌ Brak
  }
}
```

---

### 2.3 Fizyczna infrastruktura istnieje!

#### Według strony ZDiTM:

> "a board informing drivers about the number of free parking spaces"

**Czyli:**
- ✅ Sensory liczące miejsca **ISTNIEJĄ** na parkingach
- ✅ Tablice elektroniczne **DZIAŁAJĄ** (pokazują dane na miejscu)
- ❌ **Brak API** udostępniającego te dane programistom

```
┌────────────────────────────────────────────────┐
│   P&R Pomorzany - Tablica na miejscu          │
│                                                │
│        Wolnych miejsc: 63 / 150               │
│                                                │
└────────────────────────────────────────────────┘
                    │
                    │ ❌ Te dane NIE są w API!
                    ▼
           🚫 Brak endpointu
```

---

### 2.4 Dlaczego to problem?

#### Scenariusz użycia: Ania jedzie do pracy

**Bez API parking:**
1. Ania wychodzi z domu o 7:45
2. Jedzie na P&R Pomorzany (15 min)
3. **Parking PEŁNY** (zjazd do 8:00)
4. Musi szukać innego P&R (kolejne 20 min stracone)
5. **Spóźnienie do pracy** 😡

**Z API parking (gdyby istniało):**
1. Ania sprawdza aplikację o 7:40
2. **Widzi: P&R Pomorzany 95% zajęte (142/150)**
3. Aplikacja sugeruje: "P&R Kijewo - 30% zajęte (60/200)"
4. Jedzie tam od razu
5. **Na czas w pracy** ✅

---

### 2.5 Przykłady miast, które MAJĄ takie API

#### Transport for NSW (Sydney, Australia)

**API Endpoint:**
```
GET https://api.transport.nsw.gov.au/v1/carpark
```

**Odpowiedź:**
```json
{
  "spots": [
    {
      "carpark": "P&R Macquarie Park",
      "occupancy": {
        "total": 500,
        "occupied": 324,
        "available": 176,
        "percentage": 64.8
      },
      "lastUpdate": "2024-10-25T20:32:00Z"
    }
  ]
}
```

**Dostępne od:** 2019
**Źródło:** [NSW Open Data Hub](https://opendata.transport.nsw.gov.au/dataset/car-park-api)

---

#### Parkopedia (global commercial)

**API:**
```
GET https://api.parkopedia.com/v1/parking/availability
```

**Cena:** od $500/miesiąc (komercyjne)

**Dane:**
- Real-time occupancy (71 krajów)
- Pricing
- Accessibility
- Predictions (AI-based)

---

#### Smart City System - Rzeszów, Polska 🇵🇱

**Implementacja:** 2,200 miejsc parkingowych
**Technologia:**
- 338 kamer
- 305 czujników magnetyczno-radarowych
- Real-time dashboard
- Aplikacja mobilna e-Parking

**Czy mają API?** Nieznane (projekt zamknięty dla miasta)

**Źródło:** [Smart City System - Rzeszów](https://square.dksr.city/en/data/parking-space-occupancy-data-smart-city-system)

---

### 2.6 Dlaczego ZDiTM nie udostępnia API parking?

#### Możliwe przyczyny (spekulacja oparta na analizie):

1. **Priorytet dla transportu publicznego**
   - ZDiTM = Zarząd Dróg i **Transportu Miejskiego**
   - Parkingi to "bonus", nie core business
   - API developerów fokus: autobusy, tramwaje, rozkłady

2. **Koszty infrastruktury**
   - Tablice na parkingach działają lokalnie (prosty system)
   - Centralna platforma API wymaga:
     - Serwery
     - Bazy danych
     - Monitoring 24/7
     - Wsparcie dla developerów

3. **Prywatność / bezpieczeństwo?**
   - Dane o obłożeniu parkingów mogą być wrażliwe?
   - (mało prawdopodobne - inne miasta udostępniają)

4. **Po prostu nikt nie poprosił**
   - Może ZDiTM nie wie że deweloperzy chcą takich danych
   - Warto **napisać do nich** i zapytać!

---

### 2.7 Co możemy zrobić?

#### Opcja A: Mock Data (aktualne rozwiązanie) ✅

```python
# utils/mock_parking.py

def generate_parking_data():
    """
    Symuluje realistyczne dane obłożenia parkingów
    Gotowe do podmiany na prawdziwe API gdy się pojawi
    """
    current_hour = datetime.now().hour
    is_rush_hour = (7 <= current_hour <= 9) or (16 <= current_hour <= 18)

    base_occupancy = 0.75 if is_rush_hour else 0.40

    # ... (patrz IMPLEMENTATION.md)
```

**Zalety:**
- Działa od razu ✅
- Realistyczne dane (godziny szczytu, wariancja)
- Struktura gotowa pod prawdziwe API

**Wady:**
- Nie są to prawdziwe dane ❌
- Użytkownik może podjąć złą decyzję

**Rozwiązanie:**
```
⚠️ Disclaimer w aplikacji:
"Dane parkingów są symulowane.
Real-time data niedostępne z API ZDiTM."
```

---

#### Opcja B: Web Scraping tablic na miejscu 🤔

```python
# Teoretycznie możliwe (ale NIE REKOMENDOWANE):

import requests
from bs4 import BeautifulSoup

def scrape_parking_board(parking_url):
    """
    Próba pobrania danych z tablicy elektronicznej
    (jeśli jest dostępna przez internet)
    """
    # ⚠️ Problemy:
    # 1. Tablice mogą być offline (tylko na miejscu)
    # 2. Brak oficjalnego API = łamanie ToS?
    # 3. Niestabilne (ZDiTM może zmienić układ strony)
    # 4. Etyczne obawy
```

**Decyzja:** ❌ NIE ROBIMY (nie warto ryzyka)

---

#### Opcja C: Napisać do ZDiTM z prośbą o API 📧

**Email draft:**

```
Do: programisci@zditm.szczecin.pl (lub podobny adres)

Temat: Prośba o API dla danych Park & Ride

Szanowni Państwo,

Jesteśmy zespołem deweloperskim tworzącym demonstrację aplikacji
smart city dla Szczecina (integracja transportu publicznego + usługi miejskie).

Używamy Państwa doskonałego API dla transportu publicznego:
- /api/v1/vehicles (live tracking) ✅
- /api/v1/stops (przystanki) ✅
- GTFS (rozkłady jazdy) ✅

Czy planują Państwo udostępnienie API dla danych Park & Ride,
zawierającego:
- Obłożenie parkingów w czasie rzeczywistym
- Liczba wolnych/zajętych miejsc
- Timestamp ostatniej aktualizacji

Fizyczne tablice na parkingach już pokazują te dane, więc
infrastruktura istnieje. Byłoby wspaniale gdyby programiści
mogli z nich korzystać przez API!

Przykłady z innych miast:
- Sydney (Transport NSW): https://opendata.transport.nsw.gov.au/dataset/car-park-api
- Rzeszów Smart City System

Czy moglibyśmy współpracować przy udostępnieniu tych danych?

Pozdrawiam,
[Imię i nazwisko]
[Link do projektu GitHub]
```

**Szansa powodzenia:** 30-50%
**Czas oczekiwania na odpowiedź:** 2-4 tygodnie
**Warto spróbować?** ✅ TAK!

---

#### Opcja D: Manualny update przez obserwację 📸

```python
# Last resort (tylko dla demo):

PARKING_DATA_MANUAL = {
    "last_observation": "2025-10-25 08:00",
    "observer": "Team member",
    "parking_lots": [
        {
            "name": "P&R Pomorzany",
            "observed_occupancy": 0.80,  # Wizualna ocena: ~80% zajęte
            "notes": "Godzina szczytu, prawie pełny"
        }
    ]
}
```

**Użycie:** Tylko dla demo/pitch
**Production:** ❌ Nieakceptowalne

---

### 2.8 Podsumowanie: Park & Ride API

```
┌──────────────────────────────────────────────────────────┐
│  PARK & RIDE API - Status w Szczecinie                  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ✅ CO ISTNIEJE:                                         │
│  • Fizyczne tablice na parkingach (live data)            │
│  • Pole park_and_ride: true/false w /stops API           │
│  • Infrastruktura sensorów (kamery, indukcja)           │
│                                                           │
│  ❌ CZEGO BRAKUJE:                                       │
│  • API endpoint dla real-time occupancy                  │
│  • Dostęp programistyczny do danych tablic               │
│  • Historyczne dane (do predykcji)                       │
│  • Powiadomienia (parking się zapełnia)                  │
│                                                           │
│  🎯 NASZE ROZWIĄZANIE:                                   │
│  1. Mock data (symulacja realistyczna)                   │
│  2. Struktura gotowa pod prawdziwe API                   │
│  3. Disclaimer w UI: "Dane symulowane"                   │
│  4. Email do ZDiTM z prośbą o API                        │
│                                                           │
│  📅 TIMELINE:                                            │
│  • v1.0 (teraz): Mock data                               │
│  • v2.0 (gdy API będzie): Prawdziwe dane                 │
│  • Podmiana: 1 plik (mock_parking.py → parking_api.py)   │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Porównanie alternatyw

### 3.1 Routing: Mapbox vs Leaflet vs Google Maps

| Kryterium | Mapbox GL JS | Leaflet.js + OSM | Google Maps |
|-----------|--------------|------------------|-------------|
| **GTFS routing** | ❌ Brak | ✅ Pełne (custom) | ✅ Wbudowane |
| **Koszt (miesięcznie)** | $50-100 | **$0** | $0-200 (limity) |
| **Real-time ZDiTM** | ⚠️ Custom | ✅ Natywnie | ⚠️ Custom |
| **Map styling** | 🌟🌟🌟🌟🌟 | 🌟🌟🌟 | 🌟🌟🌟🌟 |
| **3D buildings** | ✅ | ❌ | ✅ |
| **Offline mode** | ⚠️ Ograniczone | ✅ Możliwe | ❌ |
| **Vendor lock-in** | ⚠️ Tak | ✅ Nie | ⚠️ Tak (silny!) |
| **Customization** | 🌟🌟🌟🌟 | 🌟🌟🌟🌟🌟 | 🌟🌟 |
| **Mobile performance** | 🌟🌟🌟🌟 | 🌟🌟🌟🌟🌟 | 🌟🌟🌟 |
| **Learning curve** | Średni | Łatwy | Łatwy |
| **Community** | Średnia | Ogromna | Ogromna |

**Zwycięzca dla naszego projektu:** 🏆 **Leaflet.js + OpenStreetMap**

---

### 3.2 Parking Data: Dostępne opcje

| Opcja | Koszt | Real-time | Coverage Szczecin |
|-------|-------|-----------|-------------------|
| **ZDiTM API** | Darmowe | ❌ Brak | N/A |
| **Parkopedia API** | $500/mc | ✅ Tak | ⚠️ Częściowe |
| **Google Maps Parking** | Wliczone w Maps API | ⚠️ Crowd-sourced | ⚠️ Niepewne |
| **Smart City Systems** | Custom | ✅ Tak | ❌ Nie (tylko Rzeszów) |
| **Mock Data (nasze)** | **Darmowe** | ⚠️ Symulowane | ✅ Pełne |

**Wybór dla MVP:** 🏆 **Mock Data** (gotowe pod upgrade)

---

## 4. Rekomendacje dla projektu

### 4.1 Decyzje architektoniczne

```
┌─────────────────────────────────────────────┐
│  STACK TECHNOLOGICZNY - FINAL               │
├─────────────────────────────────────────────┤
│                                              │
│  🗺️ MAPA:                                   │
│  → Leaflet.js + OpenStreetMap               │
│     Uzasadnienie:                            │
│     • Darmowe ($0 vs $50-100 Mapbox)        │
│     • Pełna kontrola GTFS                   │
│     • Dedykowane dla transit                │
│                                              │
│  🚌 TRANSPORT (live):                       │
│  → ZDiTM API                                 │
│     • /vehicles (real-time)                 │
│     • /trajectories (GeoJSON)               │
│     • GTFS + GTFS-RT                        │
│                                              │
│  🅿️ PARKINGI:                               │
│  → Mock Data (v1.0)                         │
│  → Prawdziwe API (v2.0 - gdy dostępne)      │
│     Migracja: 1 plik Python                 │
│                                              │
│  📍 POI:                                     │
│  → Statyczny JSON                            │
│     data/poi_locations.json                 │
│                                              │
└─────────────────────────────────────────────┘
```

### 4.2 Action Items

1. **Teraz (v1.0):**
   - ✅ Implementuj Leaflet.js + Folium
   - ✅ Integruj ZDiTM API (vehicles, stops)
   - ✅ Użyj mock data dla parkingów
   - ✅ Dodaj disclaimer: "Parking data symulowane"

2. **Krótkoterminowo (1-2 miesiące):**
   - 📧 Email do ZDiTM z prośbą o parking API
   - 📊 Zbierz feedback użytkowników (czy brak real-time parking to problem?)

3. **Długoterminowo (v2.0):**
   - 🔄 Jeśli ZDiTM udostępni API: podmień mock_parking.py
   - 🎨 Rozważ upgrade do smooth animations (Leaflet plugins)
   - 📱 PWA (Progressive Web App) z offline mode

---

## 5. Potencjalne rozwiązania przyszłościowe

### 5.1 Współpraca z ZDiTM

#### Propozycja partnerstwa

```
┌───────────────────────────────────────────────────────┐
│  PITCH DO ZDiTM                                       │
├───────────────────────────────────────────────────────┤
│                                                        │
│  My oferujemy:                                         │
│  • Gotową aplikację demo (proof of concept)           │
│  • Dokumentację techniczną (TECH_SPEC.md)             │
│  • Open source code (transparency)                    │
│  • Feedback od użytkowników (analytics)               │
│                                                        │
│  ZDiTM zyskuje:                                        │
│  • Lepszy UX dla pasażerów (więcej użytkowników MPK) │
│  • Marketing: "Szczecin smart city #1 w PL"           │
│  • Dane o zachowaniach użytkowników (analytics)       │
│  • Ekosystem developerski wokół ZDiTM API             │
│                                                        │
│  Potrzebujemy:                                         │
│  • Parking API endpoint (real-time occupancy)         │
│  • Zwiększenie rate limit (100→500 req/min?)          │
│  • Oficjalny status "partnera technologicznego"       │
│                                                        │
└───────────────────────────────────────────────────────┘
```

---

### 5.2 Crowdsourced parking data

#### Waze-style approach

```python
# Użytkownicy raportują:
# "Parking P&R Pomorzany - PEŁNY" (10:15)
# "Parking P&R Kijewo - Dużo miejsc" (10:16)

# Agregacja:
def calculate_occupancy_from_reports(reports):
    recent = [r for r in reports if r.timestamp > now() - 15min]

    if "PEŁNY" in recent_reports:
        occupancy = 0.95  # Assume 95%
    elif "Dużo miejsc" in recent_reports:
        occupancy = 0.30  # Assume 30%

    return occupancy
```

**Wady:**
- Wymaga dużej liczby użytkowników
- Nieprecyzyjne
- Spam / abuse możliwe

**Nie dla v1.0, może dla v3.0**

---

### 5.3 Computer Vision (kamerki na parkingach)

#### Teoretyczna implementacja

```
1. Montaż kamery IP na P&R parkingach
2. AI model (YOLO, COCO) liczy pojazdy
3. API zwraca: 142/150 zajętych

Koszty:
• Kamera IP: ~$200/szt × 4 parkingi = $800
• Edge computing (Raspberry Pi): $100/szt = $400
• Model AI: darmowy (YOLO open source)
• Cloud hosting: $20/mc

Total: ~$1200 initial + $20/mc
```

**Problem:** Potrzebna zgoda ZDiTM (kamery na ich terenie)

---

## 6. Podsumowanie Wykonawcze

### TL;DR

#### Mapbox ❌
- **Brak GTFS routing** = dealbreaker
- **Koszt $50-100/mc** = marnowanie pieniędzy
- **Rozwiązanie:** Leaflet.js + OSM ($0, pełna kontrola)

#### Park & Ride API ❌
- **ZDiTM nie udostępnia** danych obłożenia
- **Fizyczne tablice działają**, ale brak endpoint
- **Rozwiązanie v1.0:** Mock data + disclaimer
- **Rozwiązanie v2.0:** Email do ZDiTM → prawdziwe API

---

### Kluczowe wnioski

1. **Nie wszystko co wygląda premium, jest lepsze**
   - Mapbox wygląda fancy, ale nie rozwiązuje naszych problemów
   - Leaflet to "boring technology that works" ✅

2. **Braki w API to normalne**
   - Nawet duże miasta (Szczecin #1 w 15-min city!) mają luki
   - Rozwiązanie: mock data + struktura gotowa na upgrade

3. **Open source wygrywa dla smart city**
   - Leaflet, OSM, GTFS - wszystko darmowe i sprawdzone
   - Vendor lock-in (Mapbox, Google) to ryzyko

---

### Next Steps

1. ✅ Implementuj Leaflet.js (nie Mapbox)
2. ✅ Użyj mock parking data
3. 📧 Napisz do ZDiTM o parking API
4. 🚀 Ship v1.0 jako proof of concept

---

**Data ostatniej aktualizacji:** 2025-10-25
**Autorzy:** Tech Analysis Team
**Status:** ✅ KOMPLETNE
