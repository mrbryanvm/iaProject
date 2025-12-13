"""
Agente Optimizador: Selecciona productos para igualar el monto exacto del vale.
Tipo: Agente Basado en Objetivos (Híbrido: Codicioso Aleatorio + Cambio de Moneda)
"""

import random
from collections import Counter

class OptimizerAgent:
    def __init__(self, products):
        self.products = products
        # Pre-proceso: Separar artículos "Principales" vs "Relleno"
        self.fillers = [p for p in products if p['price'] <= 2.0]
        self.main_items = [p for p in products if p['price'] > 2.0]
        
        # Ordenar rellenos por precio descendente (Estrategia codiciosa para cambio pequeño)
        self.fillers.sort(key=lambda x: x['price'], reverse=True)

    def optimize_cart(self, target_amount, max_attempts=1000):
        """
        Intenta encontrar una coincidencia EXACTA usando un enfoque codicioso aleatorizado.
        Permite múltiples unidades del mismo artículo.
        """
        best_cart = None
        min_diff = float('inf')

        for _ in range(max_attempts):
            cart = []
            current_sum = 0.0
            
            # Fase 1: Llenar gran parte con Artículos Principales aleatoriamente
            # Barajar permite diversidad en resultados
            random.shuffle(self.main_items)
            
            for item in self.main_items:
                # Agregar cantidad aleatoria (0-3) de este artículo principal, si cabe
                if current_sum + item['price'] <= target_amount:
                     # Chequeo codicioso simple: Agregar 1 unidad
                     cart.append(item)
                     current_sum += item['price']
                     
                     # Optimización: Si está muy lejos del objetivo, agregar más del mismo artículo
                     if target_amount - current_sum > 1000: # ¿Brecha enorme? Agregar múltiples
                         qty = int((target_amount - current_sum) / item['price'])
                         qty = min(qty, 10) # Limitar a 10 máx por iteración para mantener variedad
                         for _ in range(qty):
                             cart.append(item)
                             current_sum += item['price']

            # Fase 2: Relleno Perfecto (Cambio de Moneda)
            # Intentar llenar la brecha restante EXACTAMENTE usando artículos de relleno
            remaining = round(target_amount - current_sum, 2)
            
            fillers_added, filled_success = self._fill_exact_gap(remaining)
            
            if filled_success:
                full_cart = cart + fillers_added
                return full_cart # ¡COINCIDENCIA EXACTA ENCONTRADA!
            
            # Rastrea el mejor fallo por si acaso (aunque apuntamos al éxito)
            diff = remaining - sum(f['price'] for f in fillers_added)
            if diff < min_diff:
                min_diff = diff
                best_cart = cart + fillers_added
        
        # Si salimos del bucle, fallamos en encontrar diferencia exacta 0.00, retornar mejor aprox
        return best_cart

    def _fill_exact_gap(self, gap):
        """
        Cambio de Moneda Codicioso usando rellenos.
        Retorna: (lista_de_artículos, bool_éxito)
        """
        if gap <= 0.001: return [], True
        
        added = []
        current_gap = gap
        
        # Estrategia codiciosa en rellenos (ordenado Alto -> Bajo)
        for item in self.fillers:
            while current_gap >= item['price']:
                # Chequeo seguro de punto flotante
                if item['price'] <= current_gap + 0.001:
                    added.append(item)
                    current_gap -= item['price']
                    current_gap = round(current_gap, 2)
                else:
                    break
        
        # Verificar éxito
        if current_gap <= 0.001:
            return added, True
        else:
            return added, False
