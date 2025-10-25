"""
ZDiTM API Client
================

Fetches live vehicle data from Szczecin public transport API.

API Documentation: https://www.zditm.szczecin.pl/en/zditm/for-developers
Rate Limit: 100 requests/minute per IP
"""

import requests
from typing import Optional, List, Dict
import time
from datetime import datetime

# API Configuration
API_BASE_URL = "https://www.zditm.szczecin.pl/api/v1"
VEHICLES_ENDPOINT = f"{API_BASE_URL}/vehicles"
TIMEOUT = 10  # seconds
MAX_RETRIES = 2

# Cache configuration
_cache = {
    'data': None,
    'timestamp': None,
    'ttl': 30  # Cache for 30 seconds
}


def fetch_vehicles(use_cache: bool = True) -> Optional[List[Dict]]:
    """
    Fetch live vehicle positions from ZDiTM API.

    Args:
        use_cache: If True, return cached data if available and fresh

    Returns:
        List of vehicle dictionaries or None on error

    Example:
        >>> vehicles = fetch_vehicles()
        >>> print(f"Found {len(vehicles)} vehicles")
        >>> delayed = [v for v in vehicles if v['punctuality'] < 0]
        >>> print(f"{len(delayed)} are delayed")
    """
    # Check cache
    if use_cache and _cache['data'] is not None:
        age = time.time() - _cache['timestamp']
        if age < _cache['ttl']:
            return _cache['data']

    # Fetch fresh data
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(VEHICLES_ENDPOINT, timeout=TIMEOUT)
            response.raise_for_status()

            data = response.json()
            vehicles = data.get('data', [])

            # Update cache
            _cache['data'] = vehicles
            _cache['timestamp'] = time.time()

            return vehicles

        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)  # Wait 1 second before retry
                continue
            else:
                print(f"⚠️ API timeout after {MAX_RETRIES} attempts")
                return _get_cached_data()

        except requests.exceptions.RequestException as e:
            print(f"⚠️ API error: {e}")
            return _get_cached_data()

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None

    return None


def _get_cached_data() -> Optional[List[Dict]]:
    """
    Return cached data if available, regardless of age.
    Used as fallback when API is unavailable.
    """
    if _cache['data'] is not None:
        age = time.time() - _cache['timestamp']
        print(f"ℹ️ Using cached data (age: {int(age)}s)")
        return _cache['data']
    return None


def filter_delayed_vehicles(vehicles: List[Dict]) -> List[Dict]:
    """
    Filter vehicles that are delayed (punctuality < 0).

    Args:
        vehicles: List of vehicle dictionaries

    Returns:
        List of delayed vehicles only

    Example:
        >>> all_vehicles = fetch_vehicles()
        >>> delayed = filter_delayed_vehicles(all_vehicles)
        >>> for v in delayed:
        ...     print(f"Line {v['line_number']}: {calculate_delay_minutes(v)} min late")
    """
    return [v for v in vehicles if v.get('punctuality', 0) < 0]


def calculate_delay_minutes(vehicle: Dict) -> int:
    """
    Convert punctuality value to delay in minutes.

    Args:
        vehicle: Vehicle dictionary with 'punctuality' field

    Returns:
        Delay in minutes (always positive, or 0 if on time)

    Examples:
        >>> vehicle = {'punctuality': -5}
        >>> calculate_delay_minutes(vehicle)
        5
        >>> vehicle = {'punctuality': 0}
        >>> calculate_delay_minutes(vehicle)
        0
        >>> vehicle = {'punctuality': 2}  # 2 min early
        >>> calculate_delay_minutes(vehicle)
        0
    """
    punctuality = vehicle.get('punctuality', 0)
    return abs(punctuality) if punctuality < 0 else 0


def get_vehicle_status(vehicle: Dict) -> Dict[str, any]:
    """
    Get comprehensive status information for a vehicle.

    Args:
        vehicle: Vehicle dictionary from API

    Returns:
        Dictionary with status information:
        - is_delayed: bool
        - delay_minutes: int
        - status_text: str ('On time', 'Delayed', 'Early')
        - status_emoji: str

    Example:
        >>> vehicle = fetch_vehicles()[0]
        >>> status = get_vehicle_status(vehicle)
        >>> print(f"{status['status_emoji']} {status['status_text']}")
    """
    punctuality = vehicle.get('punctuality', 0)

    if punctuality < 0:
        status = 'Delayed'
        emoji = '⚠️'
        is_delayed = True
    elif punctuality > 0:
        status = 'Early'
        emoji = '✅'
        is_delayed = False
    else:
        status = 'On time'
        emoji = '✅'
        is_delayed = False

    return {
        'is_delayed': is_delayed,
        'delay_minutes': calculate_delay_minutes(vehicle),
        'status_text': status,
        'status_emoji': emoji
    }


def format_vehicle_info(vehicle: Dict) -> str:
    """
    Format vehicle information for display.

    Args:
        vehicle: Vehicle dictionary from API

    Returns:
        Formatted string with vehicle details

    Example:
        >>> vehicle = fetch_vehicles()[0]
        >>> print(format_vehicle_info(vehicle))
        Line 75 → Osiedle Zawadzkiego
        ⚠️ Delayed: 2 min
        Speed: 15 km/h
    """
    status = get_vehicle_status(vehicle)

    lines = [
        f"Line {vehicle.get('line_number', 'N/A')} → {vehicle.get('direction', 'Unknown')}",
    ]

    if status['is_delayed']:
        lines.append(f"{status['status_emoji']} {status['status_text']}: {status['delay_minutes']} min")
    else:
        lines.append(f"{status['status_emoji']} {status['status_text']}")

    velocity = vehicle.get('velocity', 0)
    lines.append(f"Speed: {velocity} km/h")

    return '\n'.join(lines)


def get_api_stats(vehicles: List[Dict]) -> Dict[str, any]:
    """
    Calculate statistics about fetched vehicles.

    Args:
        vehicles: List of vehicle dictionaries

    Returns:
        Dictionary with statistics:
        - total: int - total vehicles
        - delayed: int - number of delayed vehicles
        - on_time: int - vehicles on time
        - buses: int - number of buses
        - trams: int - number of trams
        - avg_delay: float - average delay in minutes (for delayed vehicles)

    Example:
        >>> vehicles = fetch_vehicles()
        >>> stats = get_api_stats(vehicles)
        >>> print(f"Total: {stats['total']}, Delayed: {stats['delayed']}")
    """
    if not vehicles:
        return {
            'total': 0,
            'delayed': 0,
            'on_time': 0,
            'buses': 0,
            'trams': 0,
            'avg_delay': 0.0
        }

    delayed_vehicles = filter_delayed_vehicles(vehicles)

    # Calculate average delay
    avg_delay = 0.0
    if delayed_vehicles:
        total_delay = sum(calculate_delay_minutes(v) for v in delayed_vehicles)
        avg_delay = total_delay / len(delayed_vehicles)

    return {
        'total': len(vehicles),
        'delayed': len(delayed_vehicles),
        'on_time': len(vehicles) - len(delayed_vehicles),
        'buses': len([v for v in vehicles if v.get('vehicle_type') == 'bus']),
        'trams': len([v for v in vehicles if v.get('vehicle_type') == 'tram']),
        'avg_delay': round(avg_delay, 1)
    }


# Example usage / testing
if __name__ == "__main__":
    print("🚌 ZDiTM API Client - Test")
    print("=" * 50)

    # Fetch vehicles
    print("\n📡 Fetching vehicle data...")
    vehicles = fetch_vehicles()

    if vehicles:
        print(f"✅ Received {len(vehicles)} vehicles")

        # Show statistics
        stats = get_api_stats(vehicles)
        print(f"\n📊 Statistics:")
        print(f"  Total vehicles: {stats['total']}")
        print(f"  Buses: {stats['buses']}")
        print(f"  Trams: {stats['trams']}")
        print(f"  On time: {stats['on_time']}")
        print(f"  Delayed: {stats['delayed']}")
        if stats['delayed'] > 0:
            print(f"  Avg delay: {stats['avg_delay']} min")

        # Show first delayed vehicle
        delayed = filter_delayed_vehicles(vehicles)
        if delayed:
            print(f"\n⚠️ First delayed vehicle:")
            print(format_vehicle_info(delayed[0]))
        else:
            print(f"\n✅ No delays! All vehicles on time.")

        # Show first vehicle on map
        if vehicles:
            v = vehicles[0]
            print(f"\n🗺️ First vehicle location:")
            print(f"  {v.get('line_number')} - {v.get('vehicle_type')}")
            print(f"  Coordinates: {v.get('latitude')}, {v.get('longitude')}")
    else:
        print("❌ Failed to fetch vehicles")
