import time
from data.products import PRODUCTS

class RecolectorAgent:
    def collect(self, option, log_callback=print):
        cart = []
        for item in option:
            for _ in range(item["qty"]):
                log_callback(f"  + Agente Recolecto: {item['name']} ({item['price']} Bs)")
                product = next(p for p in PRODUCTS if p["name"] == item["name"])
                cart.append(product)
                time.sleep(0.1)
        return cart
