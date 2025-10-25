"""
Mock Parking Data Generator
============================

Generates realistic parking occupancy data for Park & Ride facilities in Szczecin.

⚠️ IMPORTANT: This data is SIMULATED as ZDiTM does not provide real-time parking API.
   Structure is ready for migration to real API when available.

Verified P+R Locations (from ZDiTM API, 2025-10-25):
- P+R Głębokie (7 stops in API)
- P+R Hangarowa (4 stops in API)
- P+R Turkusowa (10 stops in API - largest!)
- P+R SKM Podjuchy (5 stops in API)

Source: https://www.zditm.szczecin.pl/api/v1/stops (park_and_ride: true)
"""

import random
from datetime import datetime
from typing import List, Dict

# ONLY 4 VERIFIED OPERATIONAL PARKING LOTS
# Source: ZDiTM API stops with park_and_ride: true (verified 2025-10-25)
PARKING_LOTS = [
    {
        "id": 1,
        "name": "P+R Głębokie",
        "location": "Skrzyżowanie ulic Miodowej i Kupczyka",
        "latitude": 53.471,
        "longitude": 14.487,
        "total_spaces": 150,  # Estimated (no official capacity data)
        "api_stops": 7,  # Number of stops with park_and_ride flag
        "area": "Północ"  # North
    },
    {
        "id": 2,
        "name": "P+R Hangarowa",
        "location": "Skrzyżowanie ulic Eskadrowej, Leszczynowej i Hangarowej",
        "latitude": 53.388,
        "longitude": 14.625,
        "total_spaces": 120,  # Estimated
        "api_stops": 4,
        "area": "Wschód"  # East (airport area)
    },
    {
        "id": 3,
        "name": "P+R Turkusowa",
        "location": "Przy pętli tramwajowo-autobusowej Turkusowa",
        "latitude": 53.380,
        "longitude": 14.643,
        "total_spaces": 200,  # Estimated (largest - 10 stops!)
        "api_stops": 10,
        "area": "Wschód"  # East
    },
    {
        "id": 4,
        "name": "P+R SKM Podjuchy",
        "location": "Ulica Metalowa (przy stacji SKM)",
        "latitude": 53.360,
        "longitude": 14.587,
        "total_spaces": 100,  # Estimated
        "api_stops": 5,
        "area": "Południe"  # South (SKM station integration)
    }
]


def generate_parking_data() -> List[Dict]:
    """
    Generate realistic mock parking data based on time of day and day of week.

    Returns:
        List of parking lot dictionaries with simulated occupancy

    Example:
        >>> parking = generate_parking_data()
        >>> for lot in parking:
        ...     print(f"{lot['name']}: {lot['occupancy_percent']}% full")
        P+R Głębokie: 67.3% full
        P+R Hangarowa: 45.8% full
        ...
    """
    current_time = datetime.now()
    hour = current_time.hour
    weekday = current_time.weekday()  # 0 = Monday, 6 = Sunday

    # Base occupancy depends on time and day
    is_weekend = weekday >= 5  # Saturday or Sunday
    is_rush_hour = (7 <= hour <= 9) or (16 <= hour <= 18)
    is_work_hours = 9 <= hour <= 17

    if is_weekend:
        base_occupancy = 0.25  # 25% on weekends (less commuters)
    elif is_rush_hour:
        base_occupancy = 0.75  # 75% during rush hour
    elif is_work_hours:
        base_occupancy = 0.60  # 60% during work hours
    else:
        base_occupancy = 0.30  # 30% off-peak

    parking_data = []

    for lot in PARKING_LOTS:
        # Add realistic variance ±20%
        variance = random.uniform(-0.2, 0.2)
        occupancy = max(0.0, min(1.0, base_occupancy + variance))

        # Larger parkings tend to fill slower (more capacity = less % full)
        if lot["total_spaces"] >= 150:
            occupancy *= 0.9  # -10% for large parkings

        # SKM parking higher occupancy (train integration)
        if "SKM" in lot["name"]:
            occupancy *= 1.15  # +15% for SKM integration

        occupied = int(lot["total_spaces"] * occupancy)
        available = lot["total_spaces"] - occupied
        occupancy_percent = (occupied / lot["total_spaces"]) * 100

        # Determine status
        if occupancy_percent < 50:
            status = "available"
        elif occupancy_percent < 80:
            status = "moderate"
        else:
            status = "almost_full"

        parking_data.append({
            **lot,  # Include all original fields
            "occupied_spaces": occupied,
            "available_spaces": available,
            "occupancy_percent": round(occupancy_percent, 1),
            "status": status,
            "last_updated": current_time.isoformat(),
            "simulated": True,  # Flag for UI disclaimer
        })

    return parking_data


def get_parking_status_color(occupancy_percent: float) -> str:
    """
    Get color code for parking status based on occupancy.

    Args:
        occupancy_percent: Percentage of occupied spaces (0-100)

    Returns:
        Color name for Folium marker ('green', 'orange', 'red')

    Example:
        >>> get_parking_status_color(30)
        'green'
        >>> get_parking_status_color(65)
        'orange'
        >>> get_parking_status_color(90)
        'red'
    """
    if occupancy_percent < 50:
        return 'green'
    elif occupancy_percent < 80:
        return 'orange'
    else:
        return 'red'


def get_parking_emoji(status: str) -> str:
    """
    Get emoji representation of parking status.

    Args:
        status: Status string ('available', 'moderate', 'almost_full')

    Returns:
        Emoji string

    Example:
        >>> get_parking_emoji('available')
        '🟢'
        >>> get_parking_emoji('almost_full')
        '🔴'
    """
    emoji_map = {
        'available': '🟢',
        'moderate': '🟡',
        'almost_full': '🔴'
    }
    return emoji_map.get(status, '⚪')


def format_parking_info(parking: Dict) -> str:
    """
    Format parking information for display.

    Args:
        parking: Parking lot dictionary

    Returns:
        Formatted string with parking details

    Example:
        >>> parking = generate_parking_data()[0]
        >>> print(format_parking_info(parking))
        P+R Głębokie
        🟢 Available: 67/150 occupied (44.7%)
        Location: Skrzyżowanie ulic Miodowej i Kupczyka
    """
    emoji = get_parking_emoji(parking['status'])

    lines = [
        parking['name'],
        f"{emoji} {parking['status'].replace('_', ' ').title()}: "
        f"{parking['occupied_spaces']}/{parking['total_spaces']} occupied "
        f"({parking['occupancy_percent']}%)",
        f"Location: {parking['location']}"
    ]

    return '\n'.join(lines)


def get_parking_stats(parking_data: List[Dict]) -> Dict[str, any]:
    """
    Calculate statistics about parking availability.

    Args:
        parking_data: List of parking lot dictionaries

    Returns:
        Dictionary with statistics:
        - total_spaces: int - total capacity across all lots
        - total_occupied: int - total occupied spaces
        - total_available: int - total available spaces
        - avg_occupancy: float - average occupancy percentage
        - most_full: dict - parking lot with highest occupancy
        - most_empty: dict - parking lot with lowest occupancy

    Example:
        >>> parking = generate_parking_data()
        >>> stats = get_parking_stats(parking)
        >>> print(f"City-wide availability: {stats['total_available']} spaces")
    """
    if not parking_data:
        return {
            'total_spaces': 0,
            'total_occupied': 0,
            'total_available': 0,
            'avg_occupancy': 0.0,
            'most_full': None,
            'most_empty': None
        }

    total_spaces = sum(p['total_spaces'] for p in parking_data)
    total_occupied = sum(p['occupied_spaces'] for p in parking_data)
    total_available = total_spaces - total_occupied
    avg_occupancy = (total_occupied / total_spaces * 100) if total_spaces > 0 else 0

    # Find extremes
    most_full = max(parking_data, key=lambda p: p['occupancy_percent'])
    most_empty = min(parking_data, key=lambda p: p['occupancy_percent'])

    return {
        'total_spaces': total_spaces,
        'total_occupied': total_occupied,
        'total_available': total_available,
        'avg_occupancy': round(avg_occupancy, 1),
        'most_full': most_full,
        'most_empty': most_empty
    }


def get_parking_by_id(parking_id: int) -> Dict:
    """
    Get static information about a parking lot by ID.

    Args:
        parking_id: Parking lot ID (1-4)

    Returns:
        Parking lot dictionary or None if not found

    Example:
        >>> info = get_parking_by_id(1)
        >>> print(info['name'])
        P+R Głębokie
    """
    for lot in PARKING_LOTS:
        if lot['id'] == parking_id:
            return lot.copy()
    return None


def get_parking_by_name(name: str) -> Dict:
    """
    Get static information about a parking lot by name.

    Args:
        name: Parking lot name (case-insensitive partial match)

    Returns:
        Parking lot dictionary or None if not found

    Example:
        >>> info = get_parking_by_name("Głębokie")
        >>> print(info['location'])
        Skrzyżowanie ulic Miodowej i Kupczyka
    """
    name_lower = name.lower()
    for lot in PARKING_LOTS:
        if name_lower in lot['name'].lower():
            return lot.copy()
    return None


# Example usage / testing
if __name__ == "__main__":
    print("🅿️ Mock Parking Data Generator - Test")
    print("=" * 50)

    # Generate parking data
    print("\n📊 Generating parking data...")
    parking = generate_parking_data()

    print(f"✅ Generated data for {len(parking)} parking lots\n")

    # Show each parking lot
    for lot in parking:
        print(format_parking_info(lot))
        print(f"   Area: {lot['area']}")
        print(f"   API stops: {lot['api_stops']}")
        print()

    # Show statistics
    stats = get_parking_stats(parking)
    print("📈 City-wide Statistics:")
    print(f"  Total capacity: {stats['total_spaces']} spaces")
    print(f"  Occupied: {stats['total_occupied']} spaces")
    print(f"  Available: {stats['total_available']} spaces")
    print(f"  Average occupancy: {stats['avg_occupancy']}%")
    print(f"\n  Most full: {stats['most_full']['name']} ({stats['most_full']['occupancy_percent']}%)")
    print(f"  Most empty: {stats['most_empty']['name']} ({stats['most_empty']['occupancy_percent']}%)")

    print(f"\n⚠️ Note: Data is SIMULATED (ZDiTM parking API not available)")
    print(f"   Verified locations from ZDiTM API (park_and_ride: true)")
    print(f"   Ready for migration to real API when available")
