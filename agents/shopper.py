"""
Agente Comprador: Coordina el proceso de compra.
Tipo: Agente Basado en Objetivos (Orquestador)
"""

import time
from .planner import PlannerAgent
from .optimizer import OptimizerAgent
from .cashier import CashierAgent
from data.map_data import MapData
from data.products import PRODUCTS

class ShopperAgent:
    def __init__(self, log_callback=None):
        self.map_data = MapData()
        self.planner = PlannerAgent(self.map_data)
        self.optimizer = OptimizerAgent(PRODUCTS)
        self.cashier = CashierAgent()
        self.log_callback = log_callback # Función para enviar logs a la UI

    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def run_simulation(self, start_coords, target_name, voucher_amount, move_callback=None):
        """
        Flujo completo de simulación.
        start_coords: tupla (lat, lon)
        target_name: str (Clave en map_data.locations)
        """
        target_coords = self.map_data.get_coordinates(target_name)
        if not target_coords:
            self.log(f"Error: Target {target_name} not found.")
            return None, False

        self.log(f"--- Simulation Started ---")
        self.log(f"Start: {start_coords[0]:.4f}, {start_coords[1]:.4f}")
        self.log(f"Goal: {target_name} ({voucher_amount} Bs)")

        # 1. Fase de Planificación (OSRM)
        self.log("Shopper: Requesting real street route from OSRM... (Please Wait)")
        path = self.planner.find_path(start_coords, target_coords)
        
        if not path or len(path) < 2:
            self.log("Shopper: Could not calculate path.")
            return None, False

        self.log(f"Planner: Real street path found with {len(path)} waypoints.")
        
        # 2. Fase de Movimiento
        self.log("Shopper: Moving along the route...")
        
        # Control de velocidad de animación - saltar puntos para acelerar si la ruta es muy larga
        step = 1
        if len(path) > 100: step = 5
        elif len(path) > 50: step = 2

        for i in range(0, len(path), step):
            node = path[i]
            if move_callback:
                move_callback(node) # Actualización UI: mover marcador
            
            # Actualización rápida para animación fluida
            time.sleep(0.05) 
        
        # Asegurar que llegamos al punto final
        if move_callback: move_callback(path[-1])
        
        self.log(f"Shopper: Arrived at {target_name}")
        self.log("Shopper: Selecting products...")

        # 3. Fase de Optimización
        # Simular tiempo de pensamiento
        time.sleep(1.0)
        cart = self.optimizer.optimize_cart(voucher_amount)

        if not cart:
            self.log("Optimizer: Failed to find exact match for voucher amount.")
            return None, False
        
        self.log("Optimizer: Cart filled!")
        for item in cart:
            self.log(f"  + Added: {item['name']} ({item['price']} Bs)")

        # 4. Fase de Pago (Caja)
        self.log("Shopper: Paying at Cashier...")
        success, total = self.cashier.checkout(cart, voucher_amount)

        if success:
            self.log(f"Cashier: Payment Accepted! Total: {total:.2f}")
            return cart, True
        else:
            self.log(f"Cashier: Payment Rejected. Total {total:.2f} != Voucher {voucher_amount}")
            return cart, False
