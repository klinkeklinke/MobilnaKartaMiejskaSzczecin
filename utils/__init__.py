"""
Utils package for Szczecin Live Map application.

This package contains utility modules for:
- ZDiTM API integration (live vehicle data)
- Mock parking data generation
- Folium map building and visualization
"""

__version__ = "1.0.0"

# Make key functions available at package level
from .zditm_api import fetch_vehicles, filter_delayed_vehicles, calculate_delay_minutes
from .mock_parking import generate_parking_data, get_parking_status_color
from .map_builder import create_base_map, add_vehicle_markers, add_parking_markers, add_poi_markers

__all__ = [
    'fetch_vehicles',
    'filter_delayed_vehicles',
    'calculate_delay_minutes',
    'generate_parking_data',
    'get_parking_status_color',
    'create_base_map',
    'add_vehicle_markers',
    'add_parking_markers',
    'add_poi_markers',
]
