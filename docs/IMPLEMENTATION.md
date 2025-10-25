# Implementation Guide
## Interaktywna Mapa Real-Time Szczecin - Architektura i Implementacja

### Wersja dokumentu: 1.0
**Data utworzenia:** 2025-10-25

---

## 1. Wybór technologii

### 1.1 Dlaczego Streamlit + Folium?

#### Rozważane opcje

| Rozwiązanie | Zalety | Wady | Decyzja |
|-------------|--------|------|---------|
| **Streamlit + Folium** ✅ | • Szybki rozwój<br>• Python end-to-end<br>• Świetna integracja z OSM<br>• Brak potrzeby frontend skills<br>• Auto-refresh built-in | • Ograniczona customizacja<br>• Single-user oriented<br>• Wolniejsze niż pure JS | **WYBRANE** |
| Streamlit + PyDeck | • 3D wizualizacje<br>• WebGL performance | • Gorsze wsparcie OSM<br>• Trudniejsza custom markers<br>• Overkill dla 2D | ❌ Odrzucone |
| React + Leaflet.js | • Pełna kontrola<br>• Production-ready<br>• Multi-user | • Wymaga frontend skills<br>• Dłuższy rozwój<br>• Potrzebny backend | ❌ Zbyt skomplikowane dla PoC |
| React + Mapbox GL | • Piękne mapy<br>• Smooth animations | • Brak wsparcia transport<br>• Płatne (free tier limity)<br>• Wymaga dodatkowego API | ❌ Koszty + complexity |

#### Ostateczny wybór: **Streamlit + Folium**

**Uzasadnienie:**
- ✅ **Time-to-market:** Prototyp w 1-2 dni zamiast tygodni
- ✅ **Python stack:** Jeden język dla całej aplikacji
- ✅ **Leaflet.js under the hood:** Dojrzała biblioteka map
- ✅ **OSM friendly:** Natywne wsparcie dla OpenStreetMap
- ✅ **Demo-perfect:** Idealne dla proof of concept

**Trade-offs zaakceptowane:**
- ⚠️ Brak smooth animations (basic refresh) - akceptowalne dla demo
- ⚠️ Single-user focus - to tylko demonstracja technologii
- ⚠️ Ograniczona customizacja UI - wystarczające dla celów prezentacyjnych

---

## 2. Architektura aplikacji

### 2.1 Diagram architektury

```
┌─────────────────────────────────────────────────────────────┐
│                     STREAMLIT APP (app.py)                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  UI LAYER                              │  │
│  │  • Sidebar controls (toggles, refresh interval)       │  │
│  │  • Main map display (st_folium)                       │  │
│  │  • Status indicators                                  │  │
│  └─────────────────┬─────────────────────────────────────┘  │
│                    │                                         │
│  ┌─────────────────▼─────────────────────────────────────┐  │
│  │              MAP BUILDER (map_builder.py)             │  │
│  │  • Folium map initialization                          │  │
│  │  • Layer management                                   │  │
│  │  • Marker creation & styling                          │  │
│  │  • Tooltips & popups                                  │  │
│  └──┬────────────────┬────────────────┬─────────────────┘  │
│     │                │                │                     │
└─────┼────────────────┼────────────────┼─────────────────────┘
      │                │                │
      ▼                ▼                ▼
┌──────────┐   ┌──────────────┐   ┌──────────────┐
│ ZDiTM API│   │Mock Parking  │   │POI Data      │
│(Live)    │   │(Simulated)   │   │(Static JSON) │
│          │   │              │   │              │
│vehicles  │   │mock_parking  │   │poi_locations │
│endpoint  │   │.py           │   │.json         │
└──────────┘   └──────────────┘   └──────────────┘
     │                │                │
     ▼                ▼                ▼
┌────────────────────────────────────────────┐
│         DATA PROCESSING LAYER              │
│  • zditm_api.py (fetch & parse vehicles)  │
│  • mock_parking.py (generate P&R data)    │
│  • JSON loader (POI data)                 │
└────────────────────────────────────────────┘
```

### 2.2 Struktura projektu

```
MobilnaKartaMiejskaSzczecin/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Quick start guide
│
├── docs/                           # Dokumentacja
│   ├── TECH_SPEC.md               # Specyfikacja techniczna
│   ├── IMPLEMENTATION.md          # Ten dokument
│   └── USER_GUIDE.md              # Instrukcja użytkownika
│
├── data/                           # Statyczne dane
│   └── poi_locations.json         # Points of Interest
│
├── utils/                          # Moduły pomocnicze
│   ├── __init__.py
│   ├── zditm_api.py               # ZDiTM API client
│   ├── mock_parking.py            # Mock parking data generator
│   └── map_builder.py             # Folium map construction
│
├── assets/                         # (opcjonalnie) Custom icons
│   └── icons/
│       ├── bus_on_time.png
│       ├── bus_delayed.png
│       └── ...
│
└── .streamlit/                     # Streamlit config
    └── config.toml                # App configuration
```

---

## 3. Moduły i komponenty

### 3.1 app.py - Main Application

#### Odpowiedzialności
- Inicjalizacja Streamlit UI
- Zarządzanie session state
- Obsługa user input (sidebar controls)
- Wywołanie refresh logic
- Wyświetlanie mapy (st_folium)

#### Kluczowe funkcje

```python
def main():
    """Main application entry point"""
    # 1. Page config
    st.set_page_config(
        page_title="Szczecin Live Map",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Sidebar controls
    render_sidebar()

    # 3. Fetch data
    vehicles_data = fetch_vehicles_data()
    parking_data = generate_parking_data()
    poi_data = load_poi_data()

    # 4. Build map
    map_obj = build_map(vehicles_data, parking_data, poi_data)

    # 5. Display map
    st_folium(map_obj, width=1400, height=800)

    # 6. Auto-refresh logic
    time.sleep(refresh_interval)
    st.rerun()
```

#### Session State Management

```python
# Przechowywane w st.session_state:
{
    "refresh_interval": 15,          # sekund
    "show_transport": True,          # toggle warstwa transport
    "show_parking": True,            # toggle warstwa parkingi
    "show_poi": True,                # toggle warstwa POI
    "last_update": "2025-10-25 20:00:00",
    "cached_vehicles": [...],        # cache ostatnich danych
    "error_count": 0                 # licznik błędów API
}
```

---

### 3.2 utils/zditm_api.py - ZDiTM API Client

#### Funkcjonalność
- Pobieranie live danych pojazdów
- Retry logic z exponential backoff
- Caching odpowiedzi
- Error handling

#### Główne funkcje

```python
import requests
from typing import Optional, Dict, List
import time

API_URL = "https://www.zditm.szczecin.pl/api/v1/vehicles"
TIMEOUT = 10  # seconds
MAX_RETRIES = 2

def fetch_vehicles(cache_time: int = 30) -> Optional[List[Dict]]:
    """
    Fetch live vehicle positions from ZDiTM API

    Args:
        cache_time: Cache duration in seconds

    Returns:
        List of vehicle dictionaries or None on error
    """
    try:
        response = requests.get(API_URL, timeout=TIMEOUT)
        response.raise_for_status()

        data = response.json()
        return data.get("data", [])

    except requests.exceptions.Timeout:
        # Retry logic
        return retry_fetch()

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return get_cached_data()  # Fallback to cache

def filter_delayed_vehicles(vehicles: List[Dict]) -> List[Dict]:
    """Filter vehicles with delays (punctuality < 0)"""
    return [v for v in vehicles if v.get("punctuality", 0) < 0]

def calculate_delay_minutes(punctuality: int) -> int:
    """Convert punctuality to delay in minutes"""
    return abs(punctuality) if punctuality < 0 else 0
```

---

### 3.3 utils/mock_parking.py - Parking Data Generator

#### Funkcjonalność
- Generowanie realistycznych danych parkingowych
- Symulacja zmian obłożenia w czasie
- Przygotowanie struktury gotowej pod prawdziwe API

#### Przykładowa implementacja

```python
import random
from datetime import datetime
from typing import List, Dict

PARKING_LOTS = [
    {
        "id": 1,
        "name": "P&R Pomorzany",
        "latitude": 53.4284,
        "longitude": 14.4833,
        "total_spaces": 150
    },
    {
        "id": 2,
        "name": "P&R Kijewo",
        "latitude": 53.4012,
        "longitude": 14.5289,
        "total_spaces": 200
    },
    {
        "id": 3,
        "name": "P&R Turkusowa",
        "latitude": 53.4456,
        "longitude": 14.5123,
        "total_spaces": 180
    }
]

def generate_parking_data() -> List[Dict]:
    """
    Generate mock parking data with realistic occupancy

    Returns:
        List of parking lot dictionaries with occupancy info
    """
    current_time = datetime.now()
    hour = current_time.hour

    # Symulacja: więcej zajętych miejsc w godzinach szczytu
    is_rush_hour = (7 <= hour <= 9) or (16 <= hour <= 18)
    base_occupancy = 0.7 if is_rush_hour else 0.4

    parking_data = []
    for lot in PARKING_LOTS:
        # Losowa wariancja ±20%
        variance = random.uniform(-0.2, 0.2)
        occupancy = max(0.0, min(1.0, base_occupancy + variance))

        occupied = int(lot["total_spaces"] * occupancy)
        occupancy_percent = (occupied / lot["total_spaces"]) * 100

        # Determine status
        if occupancy_percent < 50:
            status = "available"
        elif occupancy_percent < 80:
            status = "moderate"
        else:
            status = "almost_full"

        parking_data.append({
            **lot,
            "occupied_spaces": occupied,
            "occupancy_percent": round(occupancy_percent, 1),
            "status": status,
            "last_updated": current_time.isoformat()
        })

    return parking_data
```

#### Gotowość na prawdziwe API

```python
# W przyszłości wystarczy podmienić na:
def fetch_real_parking_data() -> List[Dict]:
    """Fetch real parking data when API becomes available"""
    response = requests.get("https://api.szczecin.pl/parking/realtime")
    return response.json()["parking_lots"]
```

---

### 3.4 utils/map_builder.py - Folium Map Builder

#### Funkcjonalność
- Tworzenie obiektu mapy Folium
- Dodawanie warstw (transport, parkingi, POI)
- Stylizacja markerów
- Tooltips i popups

#### Główne funkcje

```python
import folium
from folium import Icon, Marker, Popup, Tooltip
from typing import List, Dict

SZCZECIN_CENTER = [53.4285, 14.5528]
DEFAULT_ZOOM = 13

def create_base_map() -> folium.Map:
    """Create base Folium map with OSM tiles"""
    return folium.Map(
        location=SZCZECIN_CENTER,
        zoom_start=DEFAULT_ZOOM,
        tiles="OpenStreetMap",
        max_zoom=18,
        min_zoom=11,
        control_scale=True
    )

def add_vehicle_markers(map_obj: folium.Map, vehicles: List[Dict]):
    """Add vehicle markers with delay visualization"""

    for vehicle in vehicles:
        lat = vehicle.get("latitude")
        lon = vehicle.get("longitude")

        if not (lat and lon):
            continue

        punctuality = vehicle.get("punctuality", 0)
        is_delayed = punctuality < 0
        delay_minutes = abs(punctuality) if is_delayed else 0

        # Icon selection
        if vehicle["vehicle_type"] == "bus":
            icon_name = "bus"
        else:  # tram
            icon_name = "subway"

        # Color based on delay
        color = "red" if is_delayed else "blue"

        # Create tooltip
        tooltip_text = f"""
        <b>Linia {vehicle['line_number']}</b><br>
        Kierunek: {vehicle.get('direction', 'N/A')}<br>
        {'⚠️ Opóźnienie: ' + str(delay_minutes) + ' min' if is_delayed else '✅ Na czas'}<br>
        Prędkość: {vehicle.get('velocity', 0)} km/h
        """

        # Create marker
        marker = folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(
                color=color,
                icon=icon_name,
                prefix="fa"
            ),
            tooltip=Tooltip(tooltip_text, sticky=True)
        )

        # Add pulsing effect for delayed vehicles
        if is_delayed:
            # Custom CSS class for pulsing (via DivIcon)
            marker = create_pulsing_marker(lat, lon, vehicle)

        marker.add_to(map_obj)

def create_pulsing_marker(lat, lon, vehicle):
    """Create pulsing marker for delayed vehicles"""
    html = f"""
    <div style="
        animation: pulse 2s infinite;
        background-color: red;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        opacity: 0.8;
    ">
        <i class="fa fa-{vehicle['vehicle_type']}"></i>
    </div>

    <style>
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.2); opacity: 1; }}
        }}
    </style>
    """

    return folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(html=html)
    )

def add_parking_markers(map_obj: folium.Map, parking_lots: List[Dict]):
    """Add parking lot markers with occupancy colors"""

    for lot in parking_lots:
        status = lot["status"]

        # Color mapping
        color_map = {
            "available": "green",
            "moderate": "orange",
            "almost_full": "red"
        }
        color = color_map.get(status, "gray")

        # Tooltip
        tooltip_text = f"""
        <b>{lot['name']}</b><br>
        Zajęte: {lot['occupied_spaces']}/{lot['total_spaces']}<br>
        Obłożenie: {lot['occupancy_percent']:.1f}%
        """

        folium.Marker(
            location=[lot["latitude"], lot["longitude"]],
            icon=folium.Icon(
                color=color,
                icon="parking",
                prefix="fa"
            ),
            tooltip=Tooltip(tooltip_text, sticky=True)
        ).add_to(map_obj)

def add_poi_markers(map_obj: folium.Map, poi_list: List[Dict]):
    """Add POI markers with ticket purchase option"""

    icon_map = {
        "aquapark": "swimmer",
        "culture": "theater-masks",
        "heritage": "landmark"
    }

    color_map = {
        "aquapark": "blue",
        "culture": "purple",
        "heritage": "darkred"
    }

    for poi in poi_list:
        category = poi["category"]

        # Popup with ticket button
        popup_html = f"""
        <div style="min-width: 200px;">
            <h4>{poi['name']}</h4>
            <p>{poi['description']}</p>
            <p><b>Adres:</b> {poi['address']}</p>
            {"<a href='" + poi['ticket_url'] + "' target='_blank'><button>🎫 Kup bilet</button></a>" if poi.get('ticket_url') else ""}
        </div>
        """

        folium.Marker(
            location=[poi["latitude"], poi["longitude"]],
            icon=folium.Icon(
                color=color_map.get(category, "gray"),
                icon=icon_map.get(category, "info-sign"),
                prefix="fa"
            ),
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=poi["name"]
        ).add_to(map_obj)
```

---

## 4. Real-time Update Mechanism (Basic Version)

### 4.1 Strategia odświeżania

#### Opcja wybrana: **Periodic Full Refresh**

```python
def main():
    # ... inicjalizacja ...

    # Get refresh interval from sidebar
    refresh_interval = st.sidebar.slider(
        "Odświeżanie (sekundy)",
        min_value=10,
        max_value=60,
        value=15
    )

    # Fetch fresh data
    vehicles = fetch_vehicles()

    # Build map
    map_obj = build_map(vehicles, ...)

    # Display
    st_folium(map_obj, width=1400, height=800)

    # Wait and refresh
    time.sleep(refresh_interval)
    st.rerun()  # Rerun entire app
```

#### Charakterystyka
- ✅ **Prosty w implementacji**
- ✅ **Działa out-of-the-box w Streamlit**
- ⚠️ **Cała mapa mruga** przy odświeżeniu
- ⚠️ **Brak smooth transitions** (tramwaje "skaczą")

### 4.2 Future: Smooth Animation (v2.0)

Dla wersji 2.0 można zaimplementować:

```python
# Wymaga custom JavaScript component
import streamlit.components.v1 as components

def smooth_update_vehicles(old_positions, new_positions):
    """Interpolate between old and new positions"""

    js_code = f"""
    <script>
        // Leaflet marker update with animation
        markers.forEach((marker, id) => {{
            const newPos = newPositions[id];
            const duration = 1000; // 1 second

            marker.slideTo(newPos, {{
                duration: duration,
                keepAtCenter: false
            }});
        }});
    </script>
    """

    components.html(js_code, height=0)
```

**Trade-off:** Znacznie więcej kodu, wymaga custom Streamlit component.
**Decyzja:** Pozostawiamy dla v2.0, jeśli demo spotka się z pozytywnym odzewem.

---

## 5. UI/UX Design

### 5.1 Layout

```
┌────────────────────────────────────────────────────────┐
│  SZCZECIN LIVE MAP                          [Legend]   │
├──────────┬─────────────────────────────────────────────┤
│ SIDEBAR  │                                             │
│          │                                             │
│ ☑ Transport│               MAPA                        │
│ ☑ Parkingi│            (Folium/OSM)                    │
│ ☑ POI     │                                             │
│          │                                             │
│ Refresh: │                                             │
│  [15s▼]  │                                             │
│          │                                             │
│ Status:  │                                             │
│ 🟢 Live  │                                             │
│          │                                             │
│ Last:    │                                             │
│ 20:06:35 │                                             │
└──────────┴─────────────────────────────────────────────┘
```

### 5.2 Kolory i styl

#### Paleta
- **Szczecin branding:**
  - Granat: `#0A2740`
  - Błękit: `#00AEEF`
  - Złoto: `#FFD700` (akcenty)

- **Status colors:**
  - Zielony (OK): `#28a745`
  - Żółty (warning): `#ffc107`
  - Czerwony (alert): `#dc3545`

#### Custom CSS (Streamlit)

```python
st.markdown("""
<style>
    .main-header {
        background-color: #0A2740;
        color: white;
        padding: 1rem;
        border-radius: 5px;
    }

    .status-live {
        color: #28a745;
        font-weight: bold;
    }

    .delay-warning {
        color: #dc3545;
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)
```

---

## 6. Error Handling Strategy

### 6.1 Hierarchia błędów

```python
class ZDiTMAPIError(Exception):
    """Base exception for ZDiTM API errors"""
    pass

class APITimeoutError(ZDiTMAPIError):
    """API request timeout"""
    pass

class RateLimitError(ZDiTMAPIError):
    """Rate limit exceeded"""
    pass

class InvalidDataError(ZDiTMAPIError):
    """Invalid JSON response"""
    pass
```

### 6.2 Fallback mechanisms

```python
def fetch_vehicles_with_fallback():
    """
    Fetch vehicles with graceful degradation
    """
    try:
        # 1. Try live API
        data = fetch_from_api()
        cache_data(data)  # Update cache
        return data

    except APITimeoutError:
        # 2. Retry once
        try:
            return fetch_from_api()
        except:
            # 3. Use cached data
            st.warning("⚠️ Używam cached danych (API timeout)")
            return get_cached_data()

    except RateLimitError:
        # 4. Increase refresh interval automatically
        st.error("🛑 Rate limit - zwiększam interwał")
        st.session_state.refresh_interval = 30
        return get_cached_data()

    except Exception as e:
        # 5. Last resort: empty state
        st.error(f"❌ Błąd: {e}")
        return []
```

---

## 7. Performance Optimization

### 7.1 Data fetching
- ✅ Connection pooling (requests.Session)
- ✅ Timeout limits (10s)
- ✅ Caching responses (30s)
- ✅ Gzip compression (automatic)

### 7.2 Map rendering
- ✅ Max 200 markers jednocześnie (limit dla czytelności)
- ✅ Cluster markers przy > 100 pojazdów (future)
- ✅ Disable animations w trybie debug

### 7.3 Streamlit specific
```python
@st.cache_data(ttl=60)
def load_poi_data():
    """Cache POI data for 60 seconds"""
    with open("data/poi_locations.json") as f:
        return json.load(f)

@st.cache_resource
def get_api_session():
    """Reuse HTTP session across reruns"""
    return requests.Session()
```

---

## 8. Testing Strategy

### 8.1 Unit tests

```python
# tests/test_zditm_api.py
def test_fetch_vehicles_success():
    mock_response = {...}
    vehicles = fetch_vehicles()
    assert len(vehicles) > 0
    assert all("latitude" in v for v in vehicles)

def test_filter_delayed():
    vehicles = [
        {"punctuality": 0},
        {"punctuality": -2},
        {"punctuality": -5}
    ]
    delayed = filter_delayed_vehicles(vehicles)
    assert len(delayed) == 2
```

### 8.2 Integration tests

```python
# tests/test_integration.py
def test_full_map_render():
    """Test całego flow: API -> Map -> Display"""
    vehicles = fetch_vehicles()
    parking = generate_parking_data()
    poi = load_poi_data()

    map_obj = build_map(vehicles, parking, poi)

    assert map_obj is not None
    assert len(map_obj._children) > 0  # Ma markery
```

### 8.3 Manual testing checklist
- [ ] Mapa się ładuje poprawnie
- [ ] Tramwaje pojawiają się na mapie
- [ ] Opóźnione pojazdy mają czerwone ikony
- [ ] Parkingi pokazują poprawne obłożenie
- [ ] POI tooltips działają
- [ ] "Kup bilet" otwiera właściwy link
- [ ] Sidebar toggles działają
- [ ] Auto-refresh działa
- [ ] Graceful degradation przy błędzie API

---

## 9. Deployment (opcjonalnie)

### 9.1 Streamlit Cloud (darmowe)

```bash
# Wystarczy push na GitHub i deploy via Streamlit Cloud
streamlit run app.py
```

### 9.2 Docker (dla production)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

### 9.3 Heroku / AWS / GCP
- Możliwe, ale out of scope dla demo
- Wymaga dodatkowych configów (Procfile, app.yaml)

---

## 10. Timeline i Milestones

### Phase 1: Dokumentacja ✅ (DONE)
- [x] TECH_SPEC.md
- [x] IMPLEMENTATION.md
- [ ] USER_GUIDE.md

### Phase 2: Core Development (1 dzień)
- [ ] Setup projektu + dependencies
- [ ] ZDiTM API integration
- [ ] Mock parking data
- [ ] POI JSON data

### Phase 3: Map & UI (1 dzień)
- [ ] Folium map builder
- [ ] Marker styling
- [ ] Streamlit sidebar
- [ ] Auto-refresh logic

### Phase 4: Testing & Polish (0.5 dnia)
- [ ] Manual testing
- [ ] Bug fixes
- [ ] README dokumentacja

**Total estimate:** 2-3 dni robocze

---

## 11. Known Limitations & Future Work

### Limitations (v1.0)
1. ❌ Brak prawdziwych danych parkingowych
2. ❌ Basic animation (nie smooth)
3. ❌ Single-user (Streamlit limitation)
4. ❌ Brak historii opóźnień
5. ❌ Brak routing/planowania tras

### Roadmap v2.0
1. ✨ Smooth animations (custom JS component)
2. 📊 Dashboard z analytics (heatmapy opóźnień)
3. 🗺️ Routing multimodalny (GTFS + OSM)
4. 🔔 Notifications (email/push o opóźnieniach)
5. 🌍 Multi-language (PL/EN/DE)
6. 🅿️ Prawdziwe API parkingowe (gdy dostępne)

---

## 12. Lessons Learned

### Co zadziałało dobrze
✅ **Streamlit** - szybki prototyping
✅ **Folium** - łatwa integracja z OSM
✅ **Python end-to-end** - jeden język, prostsza architektura

### Challenges encountered
⚠️ **Brak API parkingowego** - musieliśmy mocować
⚠️ **Streamlit reruns** - trudność z smooth animations
⚠️ **Rate limits** - trzeba było zaimplementować caching

### Rekomendacje dla przyszłych projektów
1. **Zweryfikuj dostępność API** przed projektem
2. **Zacznij od MVP** - smooth animations mogą poczekać
3. **Dokumentuj wcześnie** - TECH_SPEC przed kodem
4. **Cache agressively** - respect rate limits

---

**Ostatnia aktualizacja:** 2025-10-25
**Status:** ✅ READY FOR IMPLEMENTATION
**Next step:** USER_GUIDE.md + kod aplikacji
