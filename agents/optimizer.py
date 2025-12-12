"""
Optimizer Agent: Selects products to match the exact voucher amount.
Type: Goal-Based Agent (Hybrid: Random Greedy + Change Making)
"""

import random
from collections import Counter

class OptimizerAgent:
    def __init__(self, products):
        self.products = products
        # Pre-process: Separate "Main" items vs "Filler" items
        self.fillers = [p for p in products if p['price'] <= 2.0]
        self.main_items = [p for p in products if p['price'] > 2.0]
        
        # Sort fillers by price descending (Greedy strategy for small change)
        self.fillers.sort(key=lambda x: x['price'], reverse=True)

    def optimize_cart(self, target_amount, max_attempts=1000):
        """
        Tries to find an EXACT match using a randomized greedy approach.
        Allows multiple units of the same item.
        """
        best_cart = None
        min_diff = float('inf')

        for _ in range(max_attempts):
            cart = []
            current_sum = 0.0
            
            # Phase 1: Fill big chunk with Main Items randomly
            # Shuffle allows diversity in results
            random.shuffle(self.main_items)
            
            for item in self.main_items:
                # Add random quantity (0-3) of this main item, if it fits
                if current_sum + item['price'] <= target_amount:
                     # Simple greedy check: Add 1 unit
                     cart.append(item)
                     current_sum += item['price']
                     
                     # Optimization: If very far from target, add more of same item
                     if target_amount - current_sum > 1000: # Huge gap? Add multiple
                         qty = int((target_amount - current_sum) / item['price'])
                         qty = min(qty, 10) # Limit to 10 max per iteration to keep variety
                         for _ in range(qty):
                             cart.append(item)
                             current_sum += item['price']

            # Phase 2: Perfect Filling (Change Making)
            # Try to fill the remaining gap EXACTLY using filler items
            remaining = round(target_amount - current_sum, 2)
            
            fillers_added, filled_success = self._fill_exact_gap(remaining)
            
            if filled_success:
                full_cart = cart + fillers_added
                return full_cart # EXACT MATCH FOUND!
            
            # Track best failure just in case (though we aim for success)
            diff = remaining - sum(f['price'] for f in fillers_added)
            if diff < min_diff:
                min_diff = diff
                best_cart = cart + fillers_added
        
        # If we exit loop, we failed to find exact 0.00 difference, return best approx
        return best_cart

    def _fill_exact_gap(self, gap):
        """
        Greedy Change-Making using fillers.
        Returns: (list_of_items, success_bool)
        """
        if gap <= 0.001: return [], True
        
        added = []
        current_gap = gap
        
        # Greedy strategy on fillers (sorted High -> Low)
        for item in self.fillers:
            while current_gap >= item['price']:
                # Floating point safe check
                if item['price'] <= current_gap + 0.001:
                    added.append(item)
                    current_gap -= item['price']
                    current_gap = round(current_gap, 2)
                else:
                    break
        
        # Check success
        if current_gap <= 0.001:
            return added, True
        else:
            return added, False
