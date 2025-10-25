🚌 Transport publiczny i infrastruktura

ZDiTM – Przystanki

Opis: Dane o przystankach komunikacji miejskiej w Szczecinie.

Endpoint: GET https://www.zditm.szczecin.pl/api/v1/stops

Format: JSON

Dokumentacja:
ZDiTM Szczecin https://www.zditm.szczecin.pl/en/zditm/for-developers/api-stops?utm_source=chatgpt.com

ZDiTM – Linie

Opis: Informacje o liniach komunikacji miejskiej.

Endpoint: GET https://www.zditm.szczecin.pl/api/v1/lines

Format: JSON

Dokumentacja:
ZDiTM Szczecin https://www.zditm.szczecin.pl/en/zditm/for-developers/api-lines?utm_source=chatgpt.com

ZDiTM – Trajektorie linii

Opis: Geograficzny przebieg tras linii komunikacyjnych.

Endpoint: GET https://www.zditm.szczecin.pl/api/v1/trajectories/{lineId}

Format: GeoJSON

Dokumentacja:
ZDiTM Szczecin https://www.zditm.szczecin.pl/en/zditm/for-developers/api-line-trajectories?utm_source=chatgpt.com

ZDiTM – Pojazdy

Opis: Bieżąca lokalizacja pojazdów komunikacji miejskiej.

Endpoint: GET https://www.zditm.szczecin.pl/api/v1/vehicles

Format: JSON

Dokumentacja:
ZDiTM Szczecin https://www.zditm.szczecin.pl/en/zditm/for-developers/api-vehicles?utm_source=chatgpt.com

ZDiTM – Tablice odjazdów

Opis: Informacje o nadchodzących odjazdach z przystanku.

Endpoint: GET https://www.zditm.szczecin.pl/api/v1/displays/{stopNumber}

Format: JSON

Dokumentacja:
ZDiTM Szczecin https://www.zditm.szczecin.pl/en/zditm/for-developers/api-departure-boards?utm_source=chatgpt.com

ZDiTM – GTFS

Opis: Statyczny rozkład jazdy oraz dane w czasie rzeczywistym w formacie GTFS.

Dostęp:

Statyczny: https://www.zditm.szczecin.pl/storage/gtfs/gtfs.zip

Realtime: https://www.zditm.szczecin.pl/storage/gtfs-rt/gtfs-rt.pb

Dokumentacja:
ZDiTM Szczecin https://www.zditm.szczecin.pl/en/zditm/for-developers/gtfs?utm_source=chatgpt.com

ZDiTM – Park & Ride

Opis: System parkingów typu Park & Ride dla osób korzystających z transportu publicznego.

Strona:
ZDiTM Szczecin https://www.zditm.szczecin.pl/en/passenger/park-ride?utm_source=chatgpt.com

🌍 Dane przestrzenne i administracyjne

Geoportal Szczecin

Opis: Dane przestrzenne miasta Szczecin, w tym granice administracyjne, osiedla, ulice.

Strona:
Data.europa.eu https://data.europa.eu/en/news-events/news/open-data-portals-around-europe-poland?utm_source=chatgpt.com

GUS – API REGON

Opis: Dostęp do danych o jednostkach gospodarczych w Polsce.

Strona:
GUS API https://api.stat.gov.pl/Home/Index?lang=en&utm_source=chatgpt.com

📅 Wydarzenia i konferencje

Dev.Events – Meetupy Data Science w Szczecinie

Opis: Kalendarz spotkań i wydarzeń związanych z Data Science w Szczecinie.

Strona:
dev.events https://dev.events/meetups/EU/PL/Szczecin/datascience?utm_source=chatgpt.com

AllConferenceAlert – Konferencje w Szczecinie

Opis: Baza nadchodzących konferencji i wydarzeń naukowych w Szczecinie.

Strona:
All Conference Alert https://www.allconferencealert.com/szczecin.html?utm_source=chatgpt.com

ConferenceInEurope – Konferencje w Szczecinie

Opis: Lista międzynarodowych konferencji odbywających się w Szczecinie.

Strona:
Konferencje w Europie https://www.conferenceineurope.org/szczecin?utm_source=chatgpt.com

🅿️ Parkowanie

Unguarded Paid Parking Lots (UPPL)

Opis: Informacje o lokalizacji i zasadach korzystania z niepilnowanych płatnych parkingów w Szczecinie.

Strona:
Strefa Płatnego Parkowania

Parkopedia – Globalne dane o parkingach https://spp.szczecin.pl/lokalizacja/trasa-zamkowa-unguarded-paid-parking-lot?utm_source=chatgpt.com

Opis: Baza danych o parkingach na całym świecie, w tym dostępność miejsc.

Strona:
Parkopedia Business https://spp.szczecin.pl/lokalizacja/trasa-zamkowa-unguarded-paid-parking-lot?utm_source=chatgpt.com

🌱 Środowisko i zrównoważony rozwój

Copernicus – Sentinel-2

Opis: Dane satelitarne dotyczące środowiska, w tym monitorowanie zielonych obszarów w Szczecinie.

Strona:
ScienceDirect https://www.sciencedirect.com/science/article/pii/S1569843224002371?utm_source=chatgpt.com

SDG API – Cele Zrównoważonego Rozwoju

Opis: Dostęp do danych monitorujących realizację Celów Zrównoważonego Rozwoju w Polsce.

Strona:
SDG https://sdg.gov.pl/en/api/custodian/?utm_source=chatgpt.com

---

## 📍 Implementacja Mapy - Rekomendacje Techniczne

### Przegląd rozwiązań mapowych

Poniżej przedstawiamy analizę dostępnych technologii do wizualizacji danych ZDiTM na interaktywnej mapie.

---

### 🗺️ Opcja 1: Leaflet.js + OpenStreetMap (⭐ REKOMENDOWANE)

#### Zalety
✅ **Darmowe i open source** (bez kosztów licencji)
✅ **Doskonała integracja z GTFS** - dedykowane narzędzia do wizualizacji transportu
✅ **Leaflet.js** - najpopularniejsza biblioteka map (dojrzała, stabilna)
✅ **OpenStreetMap** - darmowe tile'y, dokładne mapy Polski
✅ **Real-time updates** - łatwa aktualizacja pozycji pojazdów
✅ **Lekkość** - szybko ładuje się na mobile

#### Wady
⚠️ **Podstawowy styling** - mniej "wow factor" niż Mapbox
⚠️ **Wymaga więcej kodu** dla zaawansowanych animacji

#### Stack technologiczny
**Dla aplikacji webowej (React/Next.js):**
```javascript
npm install leaflet react-leaflet
```

**Dla Python/Streamlit:**
```bash
pip install folium streamlit-folium
```

#### Przykład integracji z ZDiTM API

```javascript
// React + Leaflet
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

function TransitMap() {
  const [vehicles, setVehicles] = useState([]);

  useEffect(() => {
    // Fetch co 15 sekund
    const interval = setInterval(async () => {
      const response = await fetch('https://www.zditm.szczecin.pl/api/v1/vehicles');
      const data = await response.json();
      setVehicles(data.data);
    }, 15000);

    return () => clearInterval(interval);
  }, []);

  return (
    <MapContainer center={[53.4285, 14.5528]} zoom={13}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {vehicles.map(vehicle => (
        <Marker
          key={vehicle.vehicle_id}
          position={[vehicle.latitude, vehicle.longitude]}
          icon={vehicle.punctuality < 0 ? delayedIcon : normalIcon}
        >
          <Popup>
            Linia {vehicle.line_number}<br/>
            {vehicle.punctuality < 0 && `Opóźnienie: ${Math.abs(vehicle.punctuality)} min`}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
```

#### Wizualizacja trajektorii linii (GTFS)
```javascript
// Wykorzystaj endpoint /api/v1/trajectories/{lineId}
fetch('https://www.zditm.szczecin.pl/api/v1/trajectories/22')
  .then(res => res.json())
  .then(geojson => {
    L.geoJSON(geojson, {
      style: { color: '#00AEEF', weight: 3 }
    }).addTo(map);
  });
```

#### Hosting map tiles
- **OpenStreetMap Standard:** Darmowy, nieograniczony (fair use)
- **Thunderforest Transport:** Dedykowany styl dla transportu publicznego (15k req/miesiąc darmowo)

---

### 🌐 Opcja 2: Mapbox GL JS

#### Zalety
✅ **Piękny design** - premium styling out of the box
✅ **Smooth animations** - hardware-accelerated (WebGL)
✅ **3D buildings** - dodatkowy "wow factor"
✅ **Oficjalne React bindings** (react-map-gl)

#### Wady
❌ **Płatne** (free tier: 50k map loads/miesiąc, potem $5/$1k loads)
❌ **Brak wsparcia dla routingu transportu publicznego** (tylko car/bike/walk)
❌ **Wymaga dodatkowej usługi** dla GTFS routing (np. Transitland API)

#### Kiedy wybrać?
- Gdy budżet pozwala
- Gdy priorytetem jest visual appeal
- Gdy potrzebujesz 3D wizualizacji

#### Integracja
```javascript
npm install mapbox-gl react-map-gl
```

**Uwaga:** Dla danych transportu publicznego musisz:
1. Użyć Mapbox dla **mapy** (wizualizacja)
2. Dodać **Transitland API** lub podobny dla routingu GTFS
3. Nałożyć warstwy ręcznie (więcej kodu)

---

### 📱 Opcja 3: Google Maps API

#### Zalety
✅ **Znana użytkownikom** - intuicyjny UX
✅ **Dokładne dane** - szczególnie dla Polski
✅ **Directions API** - routing samochodowy/pieszy

#### Wady
❌ **Płatne** (free tier: $200 credit/miesiąc)
❌ **Brak GTFS support** - trzeba nakładać dane ręcznie
❌ **Vendor lock-in** - trudniejsza migracja

#### Kiedy wybrać?
- Gdy już używasz innych usług Google (Firebase, Cloud)
- Gdy potrzebujesz Places API (POI, reviews)

---

### 🏆 Nasze Rekomendacje

#### Dla MVP / Proof of Concept
**→ Leaflet.js + OpenStreetMap + Folium (Python)**

**Dlaczego?**
- ✅ Darmowe (zero kosztów)
- ✅ Najszybsze time-to-market
- ✅ Świetna integracja z ZDiTM API (GTFS, GeoJSON)
- ✅ Python end-to-end (Streamlit + Folium) = 2-3 dni robocze

#### Dla Production App
**→ Leaflet.js + OpenStreetMap (React/Next.js)**

**Dlaczego?**
- ✅ Darmowe, skalowalne
- ✅ Pełna kontrola nad UX
- ✅ Multi-user ready
- ✅ PWA capable (offline mode)

#### Jeśli budżet pozwala i priorytetem jest design
**→ Mapbox GL JS + Transitland API**

**Koszty (szacunkowe):**
- Mapbox: ~$50-100/miesiąc (przy średnim ruchu)
- Transitland: darmowe (open data)

---

### 🛠️ Implementacja End-to-End

#### Architektura rekomendowana (Streamlit + Folium)

```
┌─────────────────────────────────────┐
│     Streamlit App (app.py)          │
│  ┌──────────────────────────────┐   │
│  │  Folium Map (OSM tiles)      │   │
│  │  • Vehicle markers (live)    │   │
│  │  • Parking status (mock)     │   │
│  │  • POI (static)              │   │
│  └──────────┬───────────────────┘   │
│             │                        │
│  ┌──────────▼───────────────────┐   │
│  │  ZDiTM API Client            │   │
│  │  • GET /vehicles (15s)       │   │
│  │  • GET /trajectories         │   │
│  │  • Caching (30s)             │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

#### Przykład kompletny (Python + Folium)

```python
import folium
import requests
import streamlit as st
from streamlit_folium import st_folium

# Fetch live data
def get_vehicles():
    response = requests.get('https://www.zditm.szczecin.pl/api/v1/vehicles')
    return response.json()['data']

# Create map
def create_map(vehicles):
    m = folium.Map(
        location=[53.4285, 14.5528],
        zoom_start=13,
        tiles='OpenStreetMap'
    )

    for v in vehicles:
        color = 'red' if v['punctuality'] < 0 else 'blue'
        folium.Marker(
            [v['latitude'], v['longitude']],
            popup=f"Linia {v['line_number']}<br>Opóźnienie: {abs(v['punctuality'])} min",
            icon=folium.Icon(color=color, icon='bus', prefix='fa')
        ).add_to(m)

    return m

# Streamlit app
st.title('🚌 Szczecin Live Transit Map')
vehicles = get_vehicles()
map_obj = create_map(vehicles)
st_folium(map_obj, width=1400, height=800)
```

**Efekt:** Działająca mapa w **<100 linii kodu**, gotowa w 1 dzień!

---

### 📚 Zasoby i dokumentacja

#### Leaflet.js
- **Docs:** https://leafletjs.com/
- **React Leaflet:** https://react-leaflet.js.org/
- **Przykłady:** https://leafletjs.com/examples.html

#### Folium (Python wrapper Leaflet)
- **Docs:** https://python-visualization.github.io/folium/
- **Streamlit-Folium:** https://folium.streamlit.app/

#### GTFS Tools
- **GTFS to GeoJSON:** https://github.com/node-geojson/gtfs-to-geojson
- **Transitland API:** https://www.transit.land/documentation

#### ZDiTM API
- **Dokumentacja:** https://www.zditm.szczecin.pl/en/zditm/for-developers
- **Rate limit:** 100 req/min per IP

---

### ⚡ Quick Start Commands

#### React + Leaflet
```bash
npx create-react-app szczecin-map
cd szczecin-map
npm install leaflet react-leaflet
npm start
```

#### Python + Streamlit + Folium
```bash
pip install streamlit folium streamlit-folium requests
streamlit run app.py
```

---

**Ostatnia aktualizacja:** 2025-10-25
**Status:** ✅ READY FOR IMPLEMENTATION
**Rekomendacja:** Leaflet.js + OpenStreetMap (darmowe, szybkie, skuteczne)
