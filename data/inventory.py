
import random
from data.products import PRODUCTS
from data.supermarket_maps import SUPERMARKET_MAPS

# ==================== STOCK INDEPENDIENTE POR SUCURSAL ====================

def _initialize_stock():
    """
    Genera un inventario inicial para cada sucursal basado en los valores base de products.py.
    Retorna un diccionario: { 'Nombre Sucursal': { 'Nombre Producto': Cantidad } }
    """
    stock_db = {}
    
    # Obtener nombres de sucursales desde el mapa
    branch_names = list(SUPERMARKET_MAPS.keys())
    
    for branch in branch_names:
        branch_stock = {}
        for product in PRODUCTS:
            # Usar el stock definido en products.py como base
            # Si no existe, usar 0 por defecto
            qty = product.get('stock', 0)
            branch_stock[product['name']] = qty
            
        stock_db[branch] = branch_stock
        
    return stock_db

# Inicializar inventario global al importar
STOCK_BY_SUPERMARKET = _initialize_stock()

def get_stock(supermarket_name, product_name):
    """Retorna el stock actual de un producto en una sucursal específica."""
    if supermarket_name not in STOCK_BY_SUPERMARKET:
        return 0
    return STOCK_BY_SUPERMARKET[supermarket_name].get(product_name, 0)

def reduce_stock(supermarket_name, product_name, quantity):
    """Reduce el stock de un producto en una sucursal específica."""
    if supermarket_name in STOCK_BY_SUPERMARKET:
        current = STOCK_BY_SUPERMARKET[supermarket_name].get(product_name, 0)
        if current >= quantity:
            STOCK_BY_SUPERMARKET[supermarket_name][product_name] = current - quantity
            return True
    return False

def reset_stock_for_branch(supermarket_name):
    """Resetea el stock de una sucursal específica a los valores originales de products.py."""
    if supermarket_name in STOCK_BY_SUPERMARKET:
        for product in PRODUCTS:
            # Restaurar valor original
            qty = product.get('stock', 0)
            STOCK_BY_SUPERMARKET[supermarket_name][product['name']] = qty
