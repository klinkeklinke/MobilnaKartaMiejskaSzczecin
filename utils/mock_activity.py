"""
Mock User Activity Data Generator
===============================

Generates simulated user activity data for heatmap visualization.
Activity points are concentrated around key locations in Szczecin.
"""

import random
from typing import List, Dict
from datetime import datetime, timedelta

# Key locations in Szczecin where user activity is likely to be higher
HOT_SPOTS = [
    # City Center
    {'name': 'Centrum Galaxy', 'lat': 53.4285, 'lon': 14.5528, 'weight': 1.0},
    {'name': 'Plac Rodła', 'lat': 53.4308, 'lon': 14.5517, 'weight': 0.8},
    {'name': 'Plac Grunwaldzki', 'lat': 53.4269, 'lon': 14.5524, 'weight': 0.7},
    
    # Transportation Hubs
    {'name': 'Dworzec Główny', 'lat': 53.4147, 'lon': 14.5654, 'weight': 0.9},
    {'name': 'Plac Kościuszki', 'lat': 53.4254, 'lon': 14.5495, 'weight': 0.6},
    
    # Shopping & Entertainment
    {'name': 'Galeria Kaskada', 'lat': 53.4292, 'lon': 14.5530, 'weight': 0.85},
    {'name': 'Deptak Bogusława', 'lat': 53.4274, 'lon': 14.5558, 'weight': 0.7},
    
    # Parks & Recreation
    {'name': 'Park Kasprowicza', 'lat': 53.4400, 'lon': 14.5372, 'weight': 0.5},
    {'name': 'Wały Chrobrego', 'lat': 53.4289, 'lon': 14.5603, 'weight': 0.75},
    
    # Educational
    {'name': 'Uniwersytet Szczeciński', 'lat': 53.4340, 'lon': 14.5478, 'weight': 0.6},
    {'name': 'ZUT', 'lat': 53.4277, 'lon': 14.5360, 'weight': 0.55}
]

def generate_activity_points(
    num_points: int = 1000,
    time_window_hours: int = 24
) -> List[Dict]:
    """
    Generate simulated user activity data points.
    
    Args:
        num_points: Number of activity points to generate
        time_window_hours: Time window for activity data in hours
    
    Returns:
        List of dictionaries with activity data points
    """
    activity_points = []
    current_time = datetime.now()
    
    for _ in range(num_points):
        # Select a random hot spot with weighted probability
        weights = [spot['weight'] for spot in HOT_SPOTS]
        hot_spot = random.choices(HOT_SPOTS, weights=weights)[0]
        
        # Add random variation around the hot spot
        # More variation for spots with lower weights
        variation = (1.0 - hot_spot['weight']) * 0.002  # Max ~200m for lowest weight
        lat = hot_spot['lat'] + random.uniform(-variation, variation)
        lon = hot_spot['lon'] + random.uniform(-variation, variation)
        
        # Generate random timestamp within the time window
        random_hours = random.uniform(0, time_window_hours)
        timestamp = current_time - timedelta(hours=random_hours)
        
        # Generate random activity type
        activity_type = random.choice([
            'map_view',
            'route_search',
            'ticket_purchase',
            'schedule_check',
            'parking_check'
        ])
        
        activity_points.append({
            'latitude': lat,
            'longitude': lon,
            'timestamp': timestamp.isoformat(),
            'activity_type': activity_type,
            'location_name': hot_spot['name']
        })
    
    return activity_points

def get_activity_stats(activity_points: List[Dict]) -> Dict:
    """
    Calculate statistics from activity data.
    
    Args:
        activity_points: List of activity data points
    
    Returns:
        Dictionary with activity statistics
    """
    if not activity_points:
        return {}
    
    # Count activities by type
    activity_counts = {}
    location_counts = {}
    
    for point in activity_points:
        # Count by activity type
        activity_type = point['activity_type']
        activity_counts[activity_type] = activity_counts.get(activity_type, 0) + 1
        
        # Count by location
        location = point['location_name']
        location_counts[location] = location_counts.get(location, 0) + 1
    
    # Find most active locations
    top_locations = sorted(
        location_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    return {
        'total_activities': len(activity_points),
        'activity_counts': activity_counts,
        'top_locations': top_locations,
        'unique_locations': len(location_counts)
    }

if __name__ == "__main__":
    # Test data generation
    print("🎯 Generating mock activity data...")
    
    activity_data = generate_activity_points(1000, 24)
    stats = get_activity_stats(activity_data)
    
    print(f"\n✅ Generated {len(activity_data)} activity points")
    print("\n📊 Activity Statistics:")
    print(f"Total activities: {stats['total_activities']}")
    print("\nActivity types:")
    for activity, count in stats['activity_counts'].items():
        print(f"- {activity}: {count}")
    
    print("\nTop 5 active locations:")
    for location, count in stats['top_locations']:
        print(f"- {location}: {count} activities")
