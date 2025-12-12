"""
Cashier Agent: Validates the transaction.
Type: Simple Reflex Agent
"""

class CashierAgent:
    """
    Simple agent that checks if the cart total matches the voucher.
    """
    def checkout(self, cart, voucher_amount):
        """
        Returns True if transaction is successful, else False.
        """
        total = sum(item['price'] for item in cart)
        # Float comparison tolerance
        if abs(total - voucher_amount) < 0.01:
            return True, total
        return False, total
