"""
Optimizer Agent: Selects products to match the exact voucher amount.
Type: Goal-Based Agent
"""

class OptimizerAgent:
    """
    Agent that uses Recursive Backtracking to solve the Subset Sum Problem.
    """
    def __init__(self, products):
        self.products = products
        self.memo = {}

    def optimize_cart(self, target_amount):
        """
        Finds a combination of products that sums exactly to target_amount.
        Returns a list of product dictionaries or None if no solution.
        """
        self.memo = {}
        # Sort products by price descending to potentially hit target faster or prune
        sorted_products = sorted(self.products, key=lambda x: x['price'], reverse=True)
        return self._backtrack(sorted_products, target_amount, 0, [])

    def _backtrack(self, products, target, index, current_cart):
        """
        Recursive backtracking with pruning.
        """
        # Base Case: Exact match found
        # Using a small epsilon for float comparison safety
        if abs(target - 0) < 0.01:
            return current_cart
        
        # Base Case: Exceeded target or no more items
        if target < 0 or index >= len(products):
            return None

        # Optimization: Pruning with basic memoization state (index, approximate_target)
        # Not perfect for float keys due to precision, but helps for discrete-like currency
        state = (index, round(target, 2))
        if state in self.memo:
            return None # Already visited this state and it failed

        # Option 1: Include current item
        item = products[index]
        result_with = self._backtrack(products, target - item['price'], index + 1, current_cart + [item])
        if result_with:
            return result_with

        # Option 2: Exclude current item
        result_without = self._backtrack(products, target, index + 1, current_cart)
        if result_without:
            return result_without
        
        # If neither worked, mark state as failed
        self.memo[state] = False
        return None
