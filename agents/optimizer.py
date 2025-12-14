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
            
            # Crear inventario temporal para esta simulación
            # Usamos get con valor alto por defecto por seguridad, aunque todos deberían tener stock ahora
            temp_stock = {p['name']: p.get('stock', 9999) for p in self.products}
            
            # Fase 1: Llenar gran parte con Artículos Principales aleatoriamente
            # Barajar permite diversidad en resultados
            random.shuffle(self.main_items)
            
            for item in self.main_items:
                # Verificar stock antes de procesar
                if temp_stock[item['name']] <= 0:
                    continue

                remaining = target_amount - current_sum
                if remaining <= 0: break

                # Máximo de unidades posibles de este producto
                max_qty_budget = int(remaining / item['price'])
                max_qty_stock = temp_stock[item['name']]
                
                max_qty = min(max_qty_budget, max_qty_stock)

                if max_qty <= 0:
                    continue

                if target_amount - current_sum > 1000:
                    # Modo Acelerado: Brecha grande, agregar más unidades pero aleatoriamente (1-10)
                    qty = random.randint(1, min(max_qty, 10))
                else:
                    # Modo Normal: Variedad, agregar pocas unidades (1-5)
                    qty = random.randint(1, min(max_qty, 5))

                for _ in range(qty):
                    cart.append(item)
                    current_sum += item['price']
                    temp_stock[item['name']] -= 1

                
        

            # Fase 2: Relleno Perfecto (Cambio de Moneda)
            # Intentar llenar la brecha restante EXACTAMENTE usando artículos de relleno
            remaining = round(target_amount - current_sum, 2)
            
            # Pasar temp_stock a la función de relleno
            fillers_added, filled_success = self._fill_exact_gap(remaining, temp_stock)
            
            if filled_success:
                full_cart = cart + fillers_added
                
                # ACTUALIZACIÓN DE STOCK REAL
                # Si encontramos una solución, debemos confirmar la reducción de stock global
                for item in full_cart:
                    # Encontrar el objeto original en self.products y reducir su stock
                    # Nota: self.products es una lista de dicts. 
                    # item es una referencia al dict en self.products? 
                    # Sí, porque cart.append(item) guarda la referencia.
                    # PERO, si modificamos item['stock'] aquí, afectamos a la próxima iteración del loop principal
                    # si fallamos y reintentamos.
                    # ESPERA. Si modificamos item['stock'] aquí, es permanente.
                    # Solo debemos hacerlo si RETORNAMOS (éxito o mejor esfuerzo final).
                    pass 
                    
                # Como optimize_cart devuelve una lista de items, quien llame al optimizador
                # o el propio optimizador antes de retornar debe "commit" los cambios.
                # PERO, optimize_cart se llama muchas veces en simulaciones fallidas internas?
                # No, el loop es interno.
                
                # Correcto: Aquí confirmamos la transacción.
                
                #for item in full_cart:
                #    item['stock'] -= 1
                
                    
                return full_cart # ¡COINCIDENCIA EXACTA ENCONTRADA!
            
            # Rastrea el mejor fallo por si acaso (aunque apuntamos al éxito)
            diff = remaining - sum(f['price'] for f in fillers_added)
            if diff < min_diff:
                min_diff = diff
                best_cart = cart + fillers_added
        
        # Si salimos del bucle, fallamos en encontrar diferencia exacta 0.00, retornar mejor aprox
        # También debemos reducir stock del best_cart
        
        #if best_cart:
        #    for item in best_cart:
        #        item['stock'] -= 1        
        #return best_cart
        

    def commit_stock(self, cart):
        for item in cart:
            item['stock'] -= 1

    def _fill_exact_gap(self, gap, temp_stock):
        """
        Cambio de Moneda Codicioso usando rellenos.
        Retorna: (lista_de_artículos, bool_éxito)
        """
        if gap <= 0.001: return [], True
        
        added = []
        current_gap = gap
        
        # Estrategia codiciosa en rellenos (ordenado Alto -> Bajo)
        for item in self.fillers:
            while current_gap >= item['price'] and temp_stock[item['name']] > 0:
                # Chequeo seguro de punto flotante
                if item['price'] <= current_gap + 0.001:
                    added.append(item)
                    current_gap -= item['price']
                    current_gap = round(current_gap, 2)
                    temp_stock[item['name']] -= 1
                else:
                    break
        
        # Verificar éxito
        if current_gap <= 0.001:
            return added, True
        else:
            return added, False
        

    def generate_options(self, voucher_amount, num_options=3):
        options = []
        attempts = 0

        while len(options) < num_options and attempts < 20:
            raw_cart = self.optimize_cart(voucher_amount)
            attempts += 1

            if not raw_cart:
                continue

            counter = Counter([p["name"] for p in raw_cart])
            option = []
            total_option = 0.0

            for name, qty in counter.items():
                product = next(p for p in self.products if p["name"] == name)
                unit_price = product["price"]
                subtotal = round(unit_price * qty, 2)

                option.append({
                    "name": name,
                    "unit_price": unit_price,
                    "qty": qty,
                    "total_price": subtotal
                })

                total_option += subtotal

            total_option = round(total_option, 2)

            option.sort(key=lambda x: x["name"])

            packaged_option = {
                "items": option,
                "total": total_option
            }

            # Evitar duplicados
            if packaged_option not in options:
                options.append(packaged_option)

        return options