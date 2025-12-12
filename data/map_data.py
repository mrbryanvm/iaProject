"""
Data module for map representation of Cochabamba.
Includes specific GPS coordinates provided by USER (Corrected Set).
"""

import math

class MapData:
    def __init__(self):
        # Nodes: Name -> (Latitude, Longitude)
        self.locations = {
            # --- HIPERMAXI BRANCHES (USER CORRECTED COORDINATES) ---
            
            # 1. Torres Sofer (Av. Oquendo 630) - Unchanged from previous user input
            'Hipermaxi Torres Sofer': (-17.384523, -66.150682), 

            # 2. El Prado (CORRECTED)
            'Hipermaxi El Prado': (-17.3841, -66.1589),

            # 3. Juan de la Rosa (CORRECTED)
            'Hipermaxi Juan de la Rosa': (-17.3767, -66.1725),

            # 4. Circunvalación (CORRECTED)
            'Hipermaxi Circunvalación': (-17.3638, -66.1659),

            # 5. Av. Villazón – Sacaba (CORRECTED)
            'Hipermaxi Sacaba': (-17.3819, -66.1190),

            # 6. Blanco Galindo (Av. Blanco Galindo 2029) - Unchanged from previous user input
            'Hipermaxi Blanco Galindo': (-17.393820, -66.182200),

            # 7. Panamericana (CORRECTED)
            'Hipermaxi Panamericana': (-17.4192, -66.1582),


            # --- NAVIGATION HUBS ---
            'Plaza 14 de Septiembre': (-17.3938, -66.1570), 
        }

        self.graph = {} 

    def get_coordinates(self, node_name):
        return self.locations.get(node_name)

    def find_nearest_node(self, lat, lon):
        min_dist = float('inf')
        nearest = None
        for name, coords in self.locations.items():
            dist = self.haversine_distance((lat, lon), coords)
            if dist < min_dist:
                min_dist = dist
                nearest = name
        return nearest, min_dist

    def haversine_distance(self, node_a, node_b):
        if isinstance(node_a, str): node_a = self.locations.get(node_a, (0,0))
        if isinstance(node_b, str): node_b = self.locations.get(node_b, (0,0))
        
        lat1, lon1 = node_a
        lat2, lon2 = node_b

        R = 6371  
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
