"""
Szczecin Live Map - Transport Publiczny Real-Time
==================================================

Interaktywna mapa pokazująca:
- 🚌 Live tracking pojazdów ZDiTM (autobusy, tramwaje)
- 🅿️ Stan parkingów Park & Ride
- 📍 Punkty POI (baseny, kultura) z możliwością zakupu biletów

Tech Stack: Streamlit + Folium + ZDiTM API + OpenStreetMap
"""

import streamlit as st
from streamlit_folium import st_folium
import json
import time
from datetime import datetime

# Import our utilities
from utils.zditm_api import fetch_vehicles, get_api_stats
from utils.mock_parking import generate_parking_data, get_parking_stats
from utils.map_builder import build_complete_map

# Page configuration
st.set_page_config(
    page_title="Szczecin Live Map | Transport Real-Time",
    page_icon="🚊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Szczecin branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0A2740 0%, #00AEEF 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    .stats-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #00AEEF;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)


def load_poi_data():
    """Load POI data from JSON file."""
    try:
        with open('data/poi_locations.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('poi', [])
    except FileNotFoundError:
        st.error("❌ Plik poi_locations.json nie został znaleziony!")
        return []
    except json.JSONDecodeError:
        st.error("❌ Błąd w pliku poi_locations.json (nieprawidłowy JSON)")
        return []


def render_sidebar():
    """Render sidebar with controls and settings."""
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/0A2740/00AEEF?text=Szczecin+Live",
                 width=300)

        st.markdown("---")

        st.header("⚙️ Ustawienia")

        # Layer toggles
        st.subheader("Warstwy mapy")
        show_transport = st.checkbox("🚌 Transport publiczny", value=True)
        show_parking = st.checkbox("🅿️ Parkingi P+R", value=True)
        show_poi = st.checkbox("📍 Punkty POI", value=True)

        # Additional options
        st.subheader("Opcje transportu")
        show_delayed_only = st.checkbox("⚠️ Tylko opóźnione pojazdy", value=False)

        # Refresh interval
        st.subheader("Odświeżanie")
        refresh_interval = st.slider(
            "Interwał (sekundy)",
            min_value=10,
            max_value=60,
            value=15,
            step=5,
            help="Częstotliwość pobierania danych z API ZDiTM"
        )

        # Auto-refresh toggle
        auto_refresh = st.checkbox("🔄 Auto-odświeżanie", value=True)

        st.markdown("---")

        # Info section
        st.subheader("ℹ️ Informacje")
        st.info("""
        **Szczecin #1 w Polsce!**

        40,6% mieszkańców ma usługi w zasięgu 15 minut
        (15-Minute City Index 2025)
        """)

        st.markdown("---")
        st.caption("v1.0.0 | Made with ❤️ for Szczecin")

    return {
        'show_transport': show_transport,
        'show_parking': show_parking,
        'show_poi': show_poi,
        'show_delayed_only': show_delayed_only,
        'refresh_interval': refresh_interval,
        'auto_refresh': auto_refresh
    }


def render_header():
    """Render main header."""
    st.markdown("""
    <div class="main-header">
        <h1>🗺️ Szczecin Live Map</h1>
        <p style="margin: 0; font-size: 1.1em;">
            Transport Publiczny Real-Time | Park & Ride | Punkty POI
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_stats(vehicles_data, parking_data):
    """Render statistics section."""
    col1, col2, col3, col4 = st.columns(4)

    # Vehicle stats
    v_stats = get_api_stats(vehicles_data) if vehicles_data else {}

    with col1:
        st.metric(
            label="🚌 Pojazdy Total",
            value=v_stats.get('total', 0),
            delta=None
        )

    with col2:
        delayed = v_stats.get('delayed', 0)
        st.metric(
            label="⚠️ Opóźnione",
            value=delayed,
            delta=f"-{delayed}" if delayed > 0 else None,
            delta_color="inverse"
        )

    # Parking stats
    p_stats = get_parking_stats(parking_data) if parking_data else {}

    with col3:
        st.metric(
            label="🅿️ Wolne miejsca",
            value=p_stats.get('total_available', 0),
            delta=None
        )

    with col4:
        avg_occ = p_stats.get('avg_occupancy', 0)
        st.metric(
            label="📊 Średnie obłożenie",
            value=f"{avg_occ:.1f}%",
            delta=None
        )


def render_disclaimers():
    """Render important disclaimers."""
    with st.expander("⚠️ Ważne informacje o danych", expanded=False):
        st.markdown("""
        ### Źródła danych:

        **✅ Transport publiczny (LIVE):**
        - Dane real-time z API ZDiTM Szczecin
        - Aktualizacja: ~10 sekund
        - Endpoint: `/api/v1/vehicles`
        - [Dokumentacja API](https://www.zditm.szczecin.pl/en/zditm/for-developers)

        **⚠️ Parkingi P+R (SYMULOWANE):**
        - Dane obłożenia są symulowane (brak API od ZDiTM)
        - Lokalizacje: **potwierdzone** z API ZDiTM
        - 4 parkingi: Głębokie, Hangarowa, Turkusowa, SKM Podjuchy
        - Struktura gotowa do podmiany na prawdziwe API

        **📍 Punkty POI (STATYCZNE):**
        - Dane zebrane ręcznie z oficjalnych źródeł
        - Współrzędne zweryfikowane
        - Linki do stron biletowych aktualne

        ---

        **Projekt demonstracyjny** - proof of concept dla Szczecin Smart City

        Więcej info: [GitHub](https://github.com/...)
        """)


def main():
    """Main application logic."""

    # Render UI components
    render_header()
    settings = render_sidebar()

    # Statistics section
    st.subheader("📊 Statystyki Real-Time")

    # Fetch data
    with st.spinner("📡 Pobieranie danych..."):
        # Vehicles (live)
        vehicles_data = None
        if settings['show_transport']:
            vehicles_data = fetch_vehicles()

        # Parking (mock)
        parking_data = None
        if settings['show_parking']:
            parking_data = generate_parking_data()

        # POI (static)
        poi_data = None
        if settings['show_poi']:
            poi_data = load_poi_data()

    # Show stats
    if vehicles_data or parking_data:
        render_stats(vehicles_data, parking_data)
    else:
        st.info("ℹ️ Włącz warstwy w sidebar aby zobaczyć statystyki")

    st.markdown("---")

    # Map section
    st.subheader("🗺️ Mapa Interaktywna")

    # Check if we have any data
    if not (vehicles_data or parking_data or poi_data):
        st.warning("⚠️ Włącz przynajmniej jedną warstwę w sidebar aby zobaczyć mapę")
    else:
        # Build map
        with st.spinner("🗺️ Budowanie mapy..."):
            map_obj = build_complete_map(
                vehicles=vehicles_data if settings['show_transport'] else [],
                parking=parking_data if settings['show_parking'] else [],
                poi=poi_data if settings['show_poi'] else [],
                show_delayed_only=settings['show_delayed_only']
            )

        # Display map
        st_folium(
            map_obj,
            width=1400,
            height=700,
            returned_objects=[]
        )

    # Disclaimers
    st.markdown("---")
    render_disclaimers()

    # Last update info
    st.caption(f"🕐 Ostatnia aktualizacja: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Auto-refresh logic
    if settings['auto_refresh']:
        time.sleep(settings['refresh_interval'])
        st.rerun()


if __name__ == "__main__":
    main()
