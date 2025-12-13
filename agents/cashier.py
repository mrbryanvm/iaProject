"""
Agente Cajero: Valida la transacción.
Tipo: Agente Reactivo Simple
"""

class CashierAgent:
    """
    Agente simple que verifica si el total del carrito coincide con el vale.
    """
    def checkout(self, cart, voucher_amount):
        """
        Retorna True si la transacción es exitosa, sino False.
        """
        total = sum(item['price'] for item in cart)
        # Tolerancia de comparación de flotantes
        if abs(total - voucher_amount) < 0.01:
            return True, total
        return False, total
