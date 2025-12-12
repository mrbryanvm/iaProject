"""
Planner Agent: Responsible for finding the optimal path using OSRM.
Type: Utility-Based Agent (consumes External Routing Service)
"""

import requests
import json

class PlannerAgent:
    """
    Agent that calculates the real street route using the OSRM API.
    """
    def __init__(self, map_data):
        self.map_data = map_data
        self.osrm_url = "http://router.project-osrm.org/route/v1/driving/"

    def find_path(self, start_coords, goal_coords):
        """
        Fetches the path from OSRM.
        Args:
            start_coords: tuple (lat, lon)
            goal_coords: tuple (lat, lon)
        Returns:
            list of (lat, lon) tuples representing the path geometry.
        """
        # OSRM expects: {lon},{lat};{lon},{lat}
        url = f"{self.osrm_url}{start_coords[1]},{start_coords[0]};{goal_coords[1]},{goal_coords[0]}?overview=full&geometries=geojson"
        
        try:
            # Add user-agent to respect OSM usage policy
            headers = {'User-Agent': 'IAProject-StudentDemo/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 'Ok':
                    # Extract coordinates [lon, lat] and convert to (lat, lon)
                    geometry = data['routes'][0]['geometry']['coordinates']
                    path = [(p[1], p[0]) for p in geometry]
                    return path
                
        except Exception as e:
            print(f"Error fetching OSRM path: {e}")
            
        # Fallback: Straight line if API fails
        return [start_coords, goal_coords]
