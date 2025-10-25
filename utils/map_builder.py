"""
Folium Map Builder
==================

Constructs interactive maps with Leaflet.js (via Folium) for Szczecin transport visualization.

Layers:
- Base map (OpenStreetMap)
- Live vehicles (buses, trams) with delay visualization
- Park & Ride parking lots with occupancy status
- Points of Interest (POI) with ticket purchase links
"""

import folium
from folium import Icon, Marker, Popup, Tooltip, DivIcon
import json
from typing import List, Dict, Optional

# Map Configuration
SZCZECIN_CENTER = [53.4285, 14.5528]  # City center coordinates
DEFAULT_ZOOM = 13
MIN_ZOOM = 11
MAX_ZOOM = 18

# Szczecin branding colors
SZCZECIN_COLORS = {
    'navy': '#0A2740',
    'blue': '#00AEEF',
    'gold': '#FFD700'
}


def create_base_map(center: List[float] = None, zoom: int = None) -> folium.Map:
    """
    Create base Folium map with OpenStreetMap tiles.

    Args:
        center: [lat, lon] coordinates for map center (default: Szczecin center)
        zoom: Initial zoom level (default: 13)

    Returns:
        Folium Map object

    Example:
        >>> map_obj = create_base_map()
        >>> map_obj.save('szczecin_map.html')
    """
    if center is None:
        center = SZCZECIN_CENTER
    if zoom is None:
        zoom = DEFAULT_ZOOM

    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles='OpenStreetMap',
        min_zoom=MIN_ZOOM,
        max_zoom=MAX_ZOOM,
        control_scale=True,
        prefer_canvas=True  # Better performance for many markers
    )

    return m


def add_vehicle_markers(
    map_obj: folium.Map,
    vehicles: List[Dict],
    show_delayed_only: bool = False
) -> folium.Map:
    """
    Add vehicle markers to the map with delay visualization.

    Args:
        map_obj: Folium Map object
        vehicles: List of vehicle dictionaries from ZDiTM API
        show_delayed_only: If True, only show delayed vehicles

    Returns:
        Updated Folium Map object

    Example:
        >>> from utils.zditm_api import fetch_vehicles
        >>> vehicles = fetch_vehicles()
        >>> map_obj = create_base_map()
        >>> add_vehicle_markers(map_obj, vehicles)
    """
    for vehicle in vehicles:
        lat = vehicle.get('latitude')
        lon = vehicle.get('longitude')

        if not (lat and lon):
            continue  # Skip vehicles without GPS

        punctuality = vehicle.get('punctuality', 0)
        is_delayed = punctuality < 0
        delay_minutes = abs(punctuality) if is_delayed else 0

        # Filter if needed
        if show_delayed_only and not is_delayed:
            continue

        # Determine icon
        vehicle_type = vehicle.get('vehicle_type', 'bus')
        line_number = vehicle.get('line_number', '?')

        # Icon name (Font Awesome)
        if vehicle_type == 'tram':
            icon_name = 'train'
        else:
            icon_name = 'bus'

        # Color based on delay
        color = 'red' if is_delayed else 'blue'

        # Tooltip text
        tooltip_html = f"""
        <div style="font-family: Arial; font-size: 12px;">
            <b>Linia {line_number}</b><br>
            Kierunek: {vehicle.get('direction', 'N/A')}<br>
            {'⚠️ Opóźnienie: ' + str(delay_minutes) + ' min' if is_delayed else '✅ Na czas'}<br>
            Prędkość: {vehicle.get('velocity', 0)} km/h
        </div>
        """

        # Create marker
        if is_delayed:
            # Pulsing marker for delayed vehicles
            marker = _create_pulsing_marker(
                lat, lon,
                line_number,
                icon_name,
                tooltip_html
            )
        else:
            # Standard marker
            marker = folium.Marker(
                location=[lat, lon],
                icon=folium.Icon(
                    color=color,
                    icon=icon_name,
                    prefix='fa'
                ),
                tooltip=Tooltip(tooltip_html, sticky=False)
            )

        marker.add_to(map_obj)

    return map_obj


def _create_pulsing_marker(
    lat: float,
    lon: float,
    line_number: str,
    icon_name: str,
    tooltip_html: str
) -> folium.Marker:
    """
    Create a pulsing marker for delayed vehicles.

    Args:
        lat: Latitude
        lon: Longitude
        line_number: Line number to display
        icon_name: Font Awesome icon name
        tooltip_html: HTML for tooltip

    Returns:
        Folium Marker with pulsing animation
    """
    html = f"""
    <div class="pulsing-marker" style="
        position: relative;
        width: 30px;
        height: 30px;
    ">
        <div style="
            position: absolute;
            width: 100%;
            height: 100%;
            background-color: #dc3545;
            border-radius: 50%;
            opacity: 0.6;
            animation: pulse 2s infinite;
        "></div>
        <div style="
            position: absolute;
            width: 100%;
            height: 100%;
            background-color: #dc3545;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 10px;
        ">
            {line_number}
        </div>
    </div>

    <style>
        @keyframes pulse {{
            0%, 100% {{
                transform: scale(1);
                opacity: 0.6;
            }}
            50% {{
                transform: scale(1.3);
                opacity: 0.3;
            }}
        }}
    </style>
    """

    return folium.Marker(
        location=[lat, lon],
        icon=DivIcon(html=html),
        tooltip=Tooltip(tooltip_html, sticky=False)
    )


def add_parking_markers(
    map_obj: folium.Map,
    parking_lots: List[Dict]
) -> folium.Map:
    """
    Add Park & Ride parking markers to the map.

    Args:
        map_obj: Folium Map object
        parking_lots: List of parking lot dictionaries

    Returns:
        Updated Folium Map object

    Example:
        >>> from utils.mock_parking import generate_parking_data
        >>> parking = generate_parking_data()
        >>> map_obj = create_base_map()
        >>> add_parking_markers(map_obj, parking)
    """
    for lot in parking_lots:
        lat = lot.get('latitude')
        lon = lot.get('longitude')

        if not (lat and lon):
            continue

        # Color based on occupancy
        occupancy = lot.get('occupancy_percent', 0)
        if occupancy < 50:
            color = 'green'
            status_emoji = '🟢'
        elif occupancy < 80:
            color = 'orange'
            status_emoji = '🟡'
        else:
            color = 'red'
            status_emoji = '🔴'

        # Tooltip
        tooltip_html = f"""
        <div style="font-family: Arial; font-size: 12px;">
            <b>{lot['name']}</b><br>
            {status_emoji} Zajęte: {lot['occupied_spaces']}/{lot['total_spaces']}<br>
            Obłożenie: {lot['occupancy_percent']:.1f}%<br>
            <small>{lot['location']}</small>
        </div>
        """

        # Popup with more details
        popup_html = f"""
        <div style="font-family: Arial; min-width: 200px;">
            <h4 style="margin: 0 0 10px 0;">{lot['name']}</h4>
            <p style="margin: 5px 0;">
                <b>Wolne miejsca:</b> {lot['available_spaces']}/{lot['total_spaces']}<br>
                <b>Obłożenie:</b> {lot['occupancy_percent']:.1f}%<br>
                <b>Lokalizacja:</b> {lot['location']}<br>
                <b>Obszar:</b> {lot.get('area', 'N/A')}
            </p>
            <p style="margin: 5px 0; font-size: 11px; color: #666;">
                ⚠️ Dane symulowane (brak API)<br>
                Ostatnia aktualizacja: {lot.get('last_updated', 'N/A')[:16]}
            </p>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(
                color=color,
                icon='car',
                prefix='fa'
            ),
            tooltip=Tooltip(tooltip_html, sticky=False),
            popup=Popup(popup_html, max_width=300)
        ).add_to(map_obj)

    return map_obj


def add_poi_markers(
    map_obj: folium.Map,
    poi_list: List[Dict]
) -> folium.Map:
    """
    Add Points of Interest markers to the map.

    Args:
        map_obj: Folium Map object
        poi_list: List of POI dictionaries

    Returns:
        Updated Folium Map object

    Example:
        >>> import json
        >>> with open('data/poi_locations.json') as f:
        ...     poi_data = json.load(f)
        >>> map_obj = create_base_map()
        >>> add_poi_markers(map_obj, poi_data['poi'])
    """
    # Icon and color mapping
    icon_map = {
        'aquapark': 'swimmer',
        'culture': 'theater-masks',
        'heritage': 'monument'
    }

    color_map = {
        'aquapark': 'blue',
        'culture': 'purple',
        'heritage': 'darkred'
    }

    for poi in poi_list:
        lat = poi.get('latitude')
        lon = poi.get('longitude')

        if not (lat and lon):
            continue

        category = poi.get('category', 'culture')
        icon_name = icon_map.get(category, 'info-circle')
        color = color_map.get(category, 'gray')

        # Tooltip
        tooltip_text = poi['name']

        # Popup with details
        ticket_button = ''
        if poi.get('ticket_url'):
            ticket_button = f"""
            <a href="{poi['ticket_url']}" target="_blank"
               style="display: inline-block; margin-top: 10px;
                      padding: 8px 16px; background-color: {SZCZECIN_COLORS['blue']};
                      color: white; text-decoration: none; border-radius: 4px;
                      font-weight: bold;">
                🎫 Kup bilet
            </a>
            """

        # Transport info
        transport_info = ''
        if poi.get('accessibility', {}).get('public_transport'):
            transport = poi['accessibility']['public_transport']
            if isinstance(transport, list):
                transport_info = f"<b>Transport:</b> {', '.join(transport)}<br>"
            else:
                transport_info = f"<b>Transport:</b> {transport}<br>"

        popup_html = f"""
        <div style="font-family: Arial; min-width: 250px;">
            <h3 style="margin: 0 0 10px 0; color: {SZCZECIN_COLORS['navy']};">
                {poi['name']}
            </h3>
            <p style="margin: 5px 0;">
                {poi.get('description', '')}<br>
                <br>
                <b>Adres:</b> {poi.get('address', 'N/A')}<br>
                {transport_info}
                {f"<b>Telefon:</b> {poi['phone']}<br>" if poi.get('phone') else ''}
            </p>
            {ticket_button}
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(
                color=color,
                icon=icon_name,
                prefix='fa'
            ),
            tooltip=tooltip_text,
            popup=Popup(popup_html, max_width=350)
        ).add_to(map_obj)

    return map_obj


def add_legend(map_obj: folium.Map) -> folium.Map:
    """
    Add a legend to the map explaining markers.

    Args:
        map_obj: Folium Map object

    Returns:
        Updated Folium Map object
    """
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 50px; right: 50px; width: 220px;
        background-color: white; border: 2px solid {SZCZECIN_COLORS['navy']};
        z-index: 9999; font-size: 12px; padding: 10px;
        border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.3);
    ">
        <h4 style="margin: 0 0 10px 0; color: {SZCZECIN_COLORS['navy']};">Legenda</h4>

        <b>Transport publiczny:</b><br>
        <span style="color: blue;">●</span> Na czas<br>
        <span style="color: red;">●</span> Opóźnienie (pulsujące)<br>
        <br>

        <b>Parkingi P+R:</b><br>
        <span style="color: green;">●</span> Dużo miejsc (&lt;50%)<br>
        <span style="color: orange;">●</span> Umiarkowane (50-80%)<br>
        <span style="color: red;">●</span> Prawie pełne (&gt;80%)<br>
        <br>

        <b>Punkty POI:</b><br>
        <span style="color: blue;">●</span> Baseny/Aquaparki<br>
        <span style="color: purple;">●</span> Kultura<br>
        <span style="color: darkred;">●</span> Dziedzictwo<br>
    </div>
    """

    map_obj.get_root().html.add_child(folium.Element(legend_html))
    return map_obj


def build_complete_map(
    vehicles: List[Dict],
    parking: List[Dict],
    poi: List[Dict],
    show_delayed_only: bool = False,
    add_legend_flag: bool = True
) -> folium.Map:
    """
    Build a complete map with all layers.

    Args:
        vehicles: List of vehicle dictionaries
        parking: List of parking lot dictionaries
        poi: List of POI dictionaries
        show_delayed_only: If True, only show delayed vehicles
        add_legend_flag: If True, add legend to map

    Returns:
        Complete Folium Map object

    Example:
        >>> from utils.zditm_api import fetch_vehicles
        >>> from utils.mock_parking import generate_parking_data
        >>> import json
        >>>
        >>> vehicles = fetch_vehicles()
        >>> parking = generate_parking_data()
        >>> with open('data/poi_locations.json') as f:
        ...     poi_data = json.load(f)
        >>>
        >>> map_obj = build_complete_map(vehicles, parking, poi_data['poi'])
        >>> map_obj.save('szczecin_live_map.html')
    """
    # Create base map
    m = create_base_map()

    # Add layers
    if vehicles:
        add_vehicle_markers(m, vehicles, show_delayed_only)
    if parking:
        add_parking_markers(m, parking)
    if poi:
        add_poi_markers(m, poi)

    # Add legend
    if add_legend_flag:
        add_legend(m)

    return m


# Example usage / testing
if __name__ == "__main__":
    print("🗺️ Folium Map Builder - Test")
    print("=" * 50)

    # This would normally be in the main app, but for testing:
    try:
        from zditm_api import fetch_vehicles
        from mock_parking import generate_parking_data

        print("\n📡 Fetching data...")
        vehicles = fetch_vehicles()
        parking = generate_parking_data()

        print(f"✅ Vehicles: {len(vehicles) if vehicles else 0}")
        print(f"✅ Parking: {len(parking)}")

        print("\n🗺️ Building map...")
        m = create_base_map()

        if vehicles:
            add_vehicle_markers(m, vehicles)
        add_parking_markers(m, parking)

        # Try to load POI
        try:
            with open('../data/poi_locations.json') as f:
                poi_data = json.load(f)
            add_poi_markers(m, poi_data['poi'])
            print(f"✅ POI: {len(poi_data['poi'])}")
        except FileNotFoundError:
            print("⚠️ POI data not found (skip)")

        add_legend(m)

        # Save
        output_file = 'test_map.html'
        m.save(output_file)
        print(f"\n✅ Map saved to: {output_file}")
        print("   Open in browser to view!")

    except ImportError as e:
        print(f"⚠️ Import error: {e}")
        print("   Run from utils/ directory or adjust imports")
