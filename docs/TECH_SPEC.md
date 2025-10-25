# Technical Specification
## Interaktywna Mapa Real-Time Szczecin

### Wersja dokumentu: 1.0
**Data utworzenia:** 2025-10-25
**Autor:** Tech Demo Team

---

## 1. Przegląd projektu

### 1.1 Cel
Stworzenie działającej demonstracji technologicznej (proof of concept) pokazującej możliwości integracji API transportu publicznego Szczecina z interaktywną mapą w czasie rzeczywistym.

### 1.2 Zakres funkcjonalny
- **Live tracking** pojazdów komunikacji miejskiej (autobusy, tramwaje)
- Wizualizacja **opóźnień** w transporcie publicznym
- Prezentacja **dostępności parkingów** Park & Ride (mock data)
- Wyświetlanie **punktów POI** (baseny, kultura) z możliwością zakupu biletów

### 1.3 Stack technologiczny
- **Python 3.9+**
- **Streamlit** - framework aplikacji webowej
- **Folium** - biblioteka map (wrapper Leaflet.js)
- **Requests** - komunikacja z API
- **OpenStreetMap** - podkład mapowy

---

## 2. Źródła danych

### 2.1 ZDiTM Vehicles API (LIVE DATA)

#### Endpoint
```
GET https://www.zditm.szczecin.pl/api/v1/vehicles
```

#### Charakterystyka
- **Format:** JSON
- **Częstotliwość aktualizacji:** ~10 sekund
- **Rate limit:** 100 żądań/minutę na IP
- **Autoryzacja:** Brak (public API)

#### Przykładowa odpowiedź
```json
{
  "data": [
    {
      "line_id": 22,
      "line_number": "60",
      "line_type": "day",
      "line_subtype": "normal",
      "vehicle_type": "bus",
      "vehicle_id": 5,
      "vehicle_number": "1052",
      "vehicle_model": "Solaris Urbino 18",
      "vehicle_low_floor": true,
      "vehicle_ticket_machine": {
        "cards": true,
        "coins": false
      },
      "vehicle_operator": "SPA Klonowica",
      "route_variant_number": 12,
      "service": "060-02",
      "direction": "Stocznia Szczecińska",
      "previous_stop": "Stocznia Szczecińska",
      "next_stop": null,
      "latitude": 53.4420013428,
      "longitude": 14.5742998123,
      "bearing": null,
      "velocity": 0,
      "punctuality": 0,
      "updated_at": "2025-10-25T20:06:21.000000Z"
    },
    {
      "line_id": 37,
      "line_number": "75",
      "vehicle_type": "bus",
      "latitude": 53.4571685791,
      "longitude": 14.4967002869,
      "bearing": 270,
      "velocity": 15,
      "punctuality": -2,
      "updated_at": "2025-10-25T20:06:27.000000Z"
    }
  ]
}
```

#### Kluczowe pola

| Pole | Typ | Opis | Przykład |
|------|-----|------|----------|
| `line_number` | string | Numer linii | "60", "75", "3" |
| `vehicle_type` | string | Typ pojazdu | "bus", "tram" |
| `vehicle_number` | string | Numer boczny pojazdu | "1052" |
| `vehicle_model` | string | Model pojazdu | "Solaris Urbino 18" |
| `direction` | string | Kierunek jazdy | "Stocznia Szczecińska" |
| `latitude` | float | Szerokość geograficzna | 53.4420013428 |
| `longitude` | float | Długość geograficzna | 14.5742998123 |
| `bearing` | int/null | Azymut (kierunek jazdy w stopniach) | 270 |
| `velocity` | int | Prędkość w km/h | 15 |
| **`punctuality`** | **int** | **Punktualność w minutach** | **-2 = 2 min opóźnienia** |
| `updated_at` | string | Timestamp ostatniej aktualizacji | "2025-10-25T20:06:27.000000Z" |

#### Logika opóźnień
- `punctuality >= 0` → pojazd **NA CZAS** lub wcześniej
- `punctuality < 0` → pojazd **OPÓŹNIONY** (wartość bezwzględna = minuty opóźnienia)

**Przykłady:**
- `punctuality: 0` → bez opóźnienia
- `punctuality: -2` → **2 minuty opóźnienia** ⚠️
- `punctuality: -5` → **5 minut opóźnienia** 🔴
- `punctuality: 1` → 1 minuta przed czasem

---

### 2.2 Park & Ride Parking (MOCK DATA)

#### Status API
⚠️ **Brak publicznego API z danymi real-time o obłożeniu parkingów**

#### Źródło informacji
- Strona ZDiTM: https://www.zditm.szczecin.pl/en/passenger/park-ride
- Fizyczne tablice na parkingach pokazują wolne miejsca
- API nie jest udostępnione publicznie

#### Mock Data - struktura
Przygotowana struktura danych gotowa do podmiany na prawdziwe API w przyszłości:

```json
{
  "parking_lots": [
    {
      "id": 1,
      "name": "P&R Pomorzany",
      "latitude": 53.4284,
      "longitude": 14.4833,
      "total_spaces": 150,
      "occupied_spaces": 45,
      "occupancy_percent": 30,
      "status": "available",
      "last_updated": "2025-10-25T20:00:00Z"
    },
    {
      "id": 2,
      "name": "P&R Kijewo",
      "latitude": 53.4012,
      "longitude": 14.5289,
      "total_spaces": 200,
      "occupied_spaces": 165,
      "occupancy_percent": 82.5,
      "status": "almost_full",
      "last_updated": "2025-10-25T20:00:00Z"
    }
  ]
}
```

#### Kategorie obłożenia
| Procent | Status | Kolor markera | Opis |
|---------|--------|---------------|------|
| 0-50% | `available` | 🟢 Zielony | Dużo wolnych miejsc |
| 50-80% | `moderate` | 🟡 Żółty | Umiarkowane obłożenie |
| 80-100% | `almost_full` | 🔴 Czerwony | Prawie pełny |

#### Lokalizacje P&R w Szczecinie
Dane ze strony ZDiTM (do weryfikacji współrzędnych):
1. P&R Pomorzany (przybliżone współrzędne)
2. P&R Kijewo (przybliżone współrzędne)
3. P&R Turkusowa (do dodania)
4. P&R Dąbie (do dodania)

---

### 2.3 Points of Interest (POI) - STATIC DATA

#### Format przechowywania
Plik JSON: `data/poi_locations.json`

#### Kategorie POI

##### A. Baseny / Aquaparki 🏊

| Nazwa | Adres | Latitude | Longitude | Opis |
|-------|-------|----------|-----------|------|
| **Arkonka** | ul. Arkońska 30a, 71-470 Szczecin | 53.4528 | 14.4833 | Kompleks basenowo-rekreacyjny w Lesie Arkońskim |
| **Fabryka Wody** | ul. 1 Maja 41, Szczecin | 53.4456 | 14.5012 | Nowoczesny aquapark (otwarty 2024) |

##### B. Kultura i rozrywka 🎭

| Nazwa | Adres | Latitude | Longitude | Opis |
|-------|-------|----------|-----------|------|
| **Filharmonia im. M. Karłowicza** | ul. Małopolska 48, Szczecin | 53.4289 | 14.5531 | Ikona architektury, nowa siedziba (2014) |
| **Teatr Współczesny** | Wały Chrobrego 3, 70-500 Szczecin | 53.4294 | 14.5606 | W budynku Muzeum Narodowego |
| **Cmentarz Centralny** | Al. Wojska Polskiego, Szczecin | 53.4186 | 14.5328 | Historyczny cmentarz komunalny |

#### Struktura JSON
```json
{
  "poi": [
    {
      "id": 1,
      "name": "Arkonka",
      "category": "aquapark",
      "address": "ul. Arkońska 30a, 71-470 Szczecin",
      "latitude": 53.4528,
      "longitude": 14.4833,
      "ticket_url": "https://arkonka.szczecin.eu/",
      "description": "Kompleks basenowo-rekreacyjny w Lesie Arkońskim",
      "icon": "swimmer"
    },
    {
      "id": 2,
      "name": "Fabryka Wody",
      "category": "aquapark",
      "address": "ul. 1 Maja 41, Szczecin",
      "latitude": 53.4456,
      "longitude": 14.5012,
      "ticket_url": "https://fabrykawody.eu/",
      "description": "Nowoczesny aquapark otwarty w 2024 roku",
      "icon": "swimmer"
    },
    {
      "id": 3,
      "name": "Filharmonia im. Mieczysława Karłowicza",
      "category": "culture",
      "address": "ul. Małopolska 48, Szczecin",
      "latitude": 53.4289,
      "longitude": 14.5531,
      "ticket_url": "https://filharmonia.szczecin.pl/",
      "description": "Ikona architektury współczesnej Szczecina",
      "icon": "music"
    },
    {
      "id": 4,
      "name": "Teatr Współczesny",
      "category": "culture",
      "address": "Wały Chrobrego 3, 70-500 Szczecin",
      "latitude": 53.4294,
      "longitude": 14.5606,
      "ticket_url": "https://wspolczesny.szczecin.pl/",
      "description": "Teatr w zabytkowym budynku nad Odrą",
      "icon": "theater"
    },
    {
      "id": 5,
      "name": "Cmentarz Centralny",
      "category": "heritage",
      "address": "Al. Wojska Polskiego, Szczecin",
      "latitude": 53.4186,
      "longitude": 14.5328,
      "ticket_url": null,
      "description": "Historyczny cmentarz komunalny",
      "icon": "landmark"
    }
  ]
}
```

---

## 3. Wymagania techniczne

### 3.1 Rate Limiting i wydajność

#### ZDiTM API
- **Limit:** 100 requests/min per IP
- **Interwał odświeżania:** 15-20 sekund (bezpieczny margines)
- **Timeout:** 10 sekund na request
- **Retry logic:** 2 próby przy błędzie, exponential backoff

#### Obliczenia
- 60 sekund / 15 sekund = **4 requests/min** ✅ (daleko poniżej limitu 100)
- Nawet przy 10s interwale: 6 requests/min ✅

### 3.2 Obsługa błędów

#### Scenariusze błędów
1. **API niedostępne** → pokaż cached dane + komunikat
2. **Timeout** → retry z exponential backoff
3. **Rate limit exceeded** → zwiększ interwał automatycznie
4. **Nieprawidłowy JSON** → log error, użyj cached data
5. **Brak danych GPS** → pomiń pojazd w wizualizacji

### 3.3 Caching
- **Ostatnia odpowiedź API** → cache na 30 sekund
- **POI data** → load raz przy starcie
- **Mock parking data** → refresh co 60 sekund (symulacja)

---

## 4. Mapa i wizualizacja

### 4.1 Parametry mapy
- **Centrum początkowe:** `[53.4285, 14.5528]` (centrum Szczecina)
- **Zoom początkowy:** 13
- **Tile layer:** OpenStreetMap Standard
- **Max zoom:** 18
- **Min zoom:** 11

### 4.2 Ikony i markery

#### Transport publiczny (live)
| Typ | Warunek | Ikona | Kolor | Efekt |
|-----|---------|-------|-------|-------|
| Autobus OK | `punctuality >= 0` | 🚌 | Niebieski | Statyczna |
| Autobus opóźniony | `punctuality < 0` | 🚌 | Czerwony | **Pulsująca** |
| Tramwaj OK | `punctuality >= 0` | 🚊 | Niebieski | Statyczna |
| Tramwaj opóźniony | `punctuality < 0` | 🚊 | Czerwony | **Pulsująca** |

#### Tooltip transport
```
Linia: 75
Kierunek: Osiedle Zawadzkiego
Opóźnienie: 2 min
Prędkość: 15 km/h
```

#### Parkingi P&R
| Obłożenie | Ikona | Kolor | Tooltip |
|-----------|-------|-------|---------|
| 0-50% | 🅿️ | Zielony | "45/150 zajętych (30%)" |
| 50-80% | 🅿️ | Żółty | "120/200 zajętych (60%)" |
| 80-100% | 🅿️ | Czerwony | "165/200 zajętych (82%)" |

#### POI
| Kategoria | Ikona | Kolor | Popup |
|-----------|-------|-------|-------|
| Aquapark | 🏊 | Niebieski | Nazwa + "Kup bilet" button |
| Kultura | 🎭 | Fioletowy | Nazwa + "Kup bilet" button |
| Dziedzictwo | 🏛️ | Brązowy | Nazwa + opis |

---

## 5. Bezpieczeństwo i zgodność

### 5.1 CORS i API security
- ZDiTM API: publiczne, brak CORS restrictions
- Brak wrażliwych danych osobowych
- Brak uwierzytelniania

### 5.2 RODO
- **Nie gromadzimy** danych użytkowników
- **Nie zapisujemy** historii przeglądania
- **Nie trackujemy** lokalizacji użytkownika
- Dane pojazdów: anonimowe, publiczne

### 5.3 Licencje
- **OpenStreetMap:** © OpenStreetMap contributors (ODbL)
- **Folium:** BSD-3-Clause
- **Streamlit:** Apache 2.0

---

## 6. Ograniczenia i known issues

### 6.1 Ograniczenia techniczne
1. **Brak prawdziwych danych parkingowych** (mock data)
2. **Basic animation** - tramwaje "skaczą" zamiast smooth transitions
3. **Brak trasowania** - tylko pozycje, bez planowania podróży
4. **Brak offline mode** - wymaga połączenia z internetem

### 6.2 Skalowanie
- Demo dla **celów prezentacyjnych**
- **Nie production-ready** (brak autentykacji, monitoring, logging)
- Single-user oriented (Streamlit nie jest multi-user friendly bez deployment)

### 6.3 Browser compatibility
- **Rekomendowane:** Chrome 90+, Firefox 88+, Safari 14+
- **Mobile:** Responsive design, ale desktop preferred

---

## 7. Przyszłe rozszerzenia (out of scope)

### Możliwe upgrade'y (wersja 2.0)
1. ✨ **Smooth animation** tramwajów (interpolacja pozycji)
2. 📊 **Dashboard analytics** (statystyki opóźnień, heatmapy)
3. 🔔 **Push notifications** o opóźnieniach na ulubionych liniach
4. 🗺️ **Routing** - planowanie podróży multimodalne
5. 🅿️ **Prawdziwe API parkingowe** (gdy ZDiTM udostępni)
6. 📱 **Progressive Web App** (offline, instalacja)
7. 🌍 **i18n** - wielojęzyczność (PL/EN/DE)

---

## 8. Kontakt i wsparcie

### API ZDiTM
- **Dokumentacja:** https://www.zditm.szczecin.pl/en/zditm/for-developers
- **Email:** (do wypełnienia przez ZDiTM)

### Projekt
- **Repozytorium:** GitHub (link TBD)
- **Issues:** GitHub Issues
- **Wersja:** 1.0.0 (Tech Demo)

---

**Ostatnia aktualizacja:** 2025-10-25
**Status dokumentu:** ✅ FINAL (wersja demonstracyjna)
