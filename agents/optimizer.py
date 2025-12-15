"""
Agente Optimizador: Selecciona productos para igualar el monto exacto del vale.
"""

import random
from collections import Counter
from data.inventory import get_stock

class OptimizerAgent:
    def __init__(self, products):
        self.products = products
        # Separar artículos "Principales" vs "Relleno"
        self.fillers = [p for p in products if p['price'] <= 2.0]
        self.main_items = [p for p in products if p['price'] > 2.0]
        
        # Ordenar rellenos por precio descendente
        self.fillers.sort(key=lambda x: x['price'], reverse=True)

    def optimize_cart(self, target_amount, supermarket_name, max_attempts=1000):
        """
        Intenta encontrar una coincidencia EXACTA usando un enfoque codicioso aleatorizado.
        """
        best_cart = None
        min_diff = float('inf')

        for _ in range(max_attempts):
            cart = []
            current_sum = 0.0
            
            # Inventario temporal
            temp_stock = {p['name']: get_stock(supermarket_name, p['name']) for p in self.products}
            
            # Fase 1: Artículos Principales
            random.shuffle(self.main_items)
            
            for item in self.main_items:
                if temp_stock[item['name']] <= 0:
                    continue

                remaining = target_amount - current_sum
                if remaining <= 0: break

                max_qty_budget = int(remaining / item['price'])
                max_qty_stock = temp_stock[item['name']]
                
                max_qty = min(max_qty_budget, max_qty_stock)

                if max_qty <= 0:
                    continue

                if target_amount - current_sum > 1000:
                    # Modo Acelerado
                    qty = random.randint(1, min(max_qty, 10))
                else:
                    # Modo Normal
                    qty = random.randint(1, min(max_qty, 5))

                for _ in range(qty):
                    cart.append(item)
                    current_sum += item['price']
                    temp_stock[item['name']] -= 1

            # Fase 2: Relleno (Cambio)
            remaining = round(target_amount - current_sum, 2)
            fillers_added, filled_success = self._fill_exact_gap(remaining, temp_stock)
            
            if filled_success:
                full_cart = cart + fillers_added
                return full_cart # Coincidencia exacta encontrada
            
            diff = remaining - sum(f['price'] for f in fillers_added)
            if diff < min_diff:
                min_diff = diff
                best_cart = cart + fillers_added
        
        return best_cart

    def _fill_exact_gap(self, gap, temp_stock):
        """
        Intenta llenar la diferencia exacta con productos de relleno.
        """
        if gap <= 0.001: return [], True
        
        added = []
        current_gap = gap
        
        for item in self.fillers:
            while current_gap >= item['price'] and temp_stock[item['name']] > 0:
                if item['price'] <= current_gap + 0.001:
                    added.append(item)
                    current_gap -= item['price']
                    current_gap = round(current_gap, 2)
                    temp_stock[item['name']] -= 1
                else:
                    break
        
        if current_gap <= 0.001:
            return added, True
        else:
            return added, False

    def generate_options(self, voucher_amount, supermarket_name, num_options=3):
        options = []
        attempts = 0

        while len(options) < num_options and attempts < 20:
            raw_cart = self.optimize_cart(voucher_amount, supermarket_name)
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

            if packaged_option not in options:
                options.append(packaged_option)

        return options