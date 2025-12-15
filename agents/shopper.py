"""
Agente Comprador: Coordina el proceso de compra.
Tipo: Agente Basado en Objetivos (Orquestador)
"""

import time
from .planner import PlannerAgent
from .optimizer import OptimizerAgent
from .cashier import CashierAgent
from .recolector import RecolectorAgent
from data.map_data import MapData
from data.products import PRODUCTS

class ShopperAgent:
    def __init__(self, log_callback=None):
        self.map_data = MapData()
        self.planner = PlannerAgent(self.map_data)
        self.optimizer = OptimizerAgent(PRODUCTS)
        self.cashier = CashierAgent()
        self.recolector = RecolectorAgent()
        self.log_callback = log_callback # Función para enviar logs a la UI
        self.supermarket_name = ""  # Variable para almacenar el nombre del supermercado

    def request_purchase_options(self, voucher_amount):
        return self.optimizer.generate_options(voucher_amount)
    
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
            self.log(f"Error: Destino {target_name} no encontrado.")
            return None, False

        self.supermarket_name = target_name # Guardar el nombre del supermercado
        self.log(f"--- Simulación Iniciada ---")
        self.log(f"Inicio: {start_coords[0]:.4f}, {start_coords[1]:.4f}")
        self.log(f"Meta: {target_name} ({voucher_amount} Bs)")

        # 1. Fase de Planificación (OSRM)
        self.log("Comprador: Solicitando ruta real a OSRM... (Por favor espere)")
        path = self.planner.find_path(start_coords, target_coords)
        
        if not path or len(path) < 2:
            self.log("Comprador: No se pudo calcular la ruta.")
            return None, False

        self.log(f"Planificador: Ruta real encontrada con {len(path)} puntos de paso.")
        
        # 2. Fase de Movimiento
        self.log("Comprador: Moviéndose a lo largo de la ruta...")
        
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
        
        self.log(f"Comprador: Llegada a {target_name}")
        self.log("Comprador: Seleccionando productos...")

        # 🔹 OPTIMIZADOR SOLO GENERA OPCIONES
        options = self.optimizer.generate_options(voucher_amount, self.supermarket_name)

        if not options:
            self.log("Optimizador: No se pudieron generar opciones.")
            return None, False
        
        # ⛔ AQUÍ SE DETIENE EL FLUJO
        # La UI ahora debe mostrar las opciones
        return options, "WAITING_SELECTION"
        
    def finalize_purchase(self, option, voucher_amount, move_callback=None):
        self.log("Comprador: Opción confirmada.")
        self.log("Recolector: Iniciando recorrido interno...")

        cart = self.recolector.collect(
            option,
            self.supermarket_name,
            log_callback=self.log,
            move_callback=move_callback  
        )


        self.log("Comprador: Pagando en caja...")
        success, total = self.cashier.checkout(cart, voucher_amount)

        if success:
            self.log(f"Cajero: ¡Pago Aceptado! Total: {total:.2f}")
            return cart, True
        else:
            self.log(f"Cajero: Pago Rechazado ({total:.2f})")
            return cart, False

