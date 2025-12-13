"""
Agente Planificador: Responsable de encontrar la ruta óptima usando OSRM.
Tipo: Agente Basado en Utilidad (consume Servicio de Enrutamiento Externo)
"""

import requests
import json

class PlannerAgent:
    """
    Agente que calcula la ruta real por calles usando la API de OSRM.
    """
    def __init__(self, map_data):
        self.map_data = map_data
        self.osrm_url = "http://router.project-osrm.org/route/v1/driving/"

    def find_path(self, start_coords, goal_coords):
        """
        Obtiene la ruta desde OSRM.
        Args:
            start_coords: tupla (lat, lon)
            goal_coords: tupla (lat, lon)
        Returns:
            lista de tuplas (lat, lon) representando la geometría de la ruta.
        """
        # OSRM espera: {lon},{lat};{lon},{lat}
        url = f"{self.osrm_url}{start_coords[1]},{start_coords[0]};{goal_coords[1]},{goal_coords[0]}?overview=full&geometries=geojson"
        
        try:
            # Agregar user-agent para respetar la política de uso de OSM
            headers = {'User-Agent': 'IAProject-StudentDemo/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 'Ok':
                    # Extraer coordenadas [lon, lat] y convertir a (lat, lon)
                    geometry = data['routes'][0]['geometry']['coordinates']
                    path = [(p[1], p[0]) for p in geometry]
                    return path
                
        except Exception as e:
            print(f"Error fetching OSRM path: {e}")
            
        # Alternativa: Línea recta si falla la API
        return [start_coords, goal_coords]
