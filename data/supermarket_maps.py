# ==================== SECCIONES OFICIALES ====================
SECTIONS = [
    "Panadería y Repostería",
    "Bebidas",
    "Bebidas Alcohólicas",
    "Lácteos",
    "Carnes y Embutidos",
    "Pescados y Mariscos",
    "Despensa Básica",
    "Legumbres y Granos",
    "Enlatados y Conservas",
    "Snacks y Golosinas",
    "Cereales y Desayuno",
    "Café, Té e Infusiones",
    "Condimentos y Especias",
    "Productos de Limpieza",
    "Papel y Desechables",
    "Cuidado Personal",
    "Cuidado Femenino",
    "Cuidado Bebé",
    "Frutas",
    "Verduras",
    "Congelados",
    "Misceláneos",
    "Navideños",
    "Adicionales",
]


# ==================== MAPEO INTERNO - HIPERMAXI TORRES SOFER ====================
SUPERMARKET_MAPS = {
    "Hipermaxi Torres Sofer": {
        "geo_location": (-17.384523, -66.150682),
        "entry": "Entrada",
        "exit": "Caja",

        "sections": {
            "Entrada": (1, 0),

            "Panadería y Repostería": (0, 1),
            "Frutas": (1, 1),
            "Verduras": (2, 1),

            "Lácteos": (0, 2),
            "Carnes y Embutidos": (1, 2),
            "Pescados y Mariscos": (2, 2),

            "Despensa Básica": (0, 3),
            "Legumbres y Granos": (1, 3),
            "Enlatados y Conservas": (2, 3),

            "Snacks y Golosinas": (0, 4),
            "Cereales y Desayuno": (1, 4),
            "Café, Té e Infusiones": (2, 4),

            "Condimentos y Especias": (0, 5),
            "Productos de Limpieza": (1, 5),
            "Papel y Desechables": (2, 5),

            "Cuidado Personal": (0, 6),
            "Cuidado Femenino": (1, 6),
            "Cuidado Bebé": (2, 6),

            "Congelados": (0, 7),
            "Misceláneos": (1, 7),
            "Navideños": (2, 7),

            "Bebidas": (0, 8),
            "Bebidas Alcohólicas": (1, 8),
            "Adicionales": (2, 8),

            "Caja": (1, 9),
        },

        # Grafo de conectividad (movimiento permitido entre secciones)
        "connections": {
            "Entrada": ["Panadería y Repostería", "Frutas"],

            "Panadería y Repostería": ["Entrada", "Frutas", "Lácteos"],
            "Frutas": ["Panadería y Repostería", "Verduras", "Carnes y Embutidos"],
            "Verduras": ["Frutas", "Lácteos"],

            "Lácteos": ["Panadería y Repostería", "Verduras", "Carnes y Embutidos"],
            "Carnes y Embutidos": ["Lácteos", "Pescados y Mariscos", "Despensa Básica"],
            "Pescados y Mariscos": ["Carnes y Embutidos", "Despensa Básica"],

            "Despensa Básica": ["Carnes y Embutidos", "Legumbres y Granos", "Snacks y Golosinas"],
            "Legumbres y Granos": ["Despensa Básica", "Enlatados y Conservas"],
            "Enlatados y Conservas": ["Legumbres y Granos", "Cereales y Desayuno"],

            "Snacks y Golosinas": ["Despensa Básica", "Cereales y Desayuno"],
            "Cereales y Desayuno": ["Snacks y Golosinas", "Café, Té e Infusiones"],
            "Café, Té e Infusiones": ["Cereales y Desayuno", "Condimentos y Especias"],

            "Condimentos y Especias": ["Café, Té e Infusiones", "Productos de Limpieza"],
            "Productos de Limpieza": ["Condimentos y Especias", "Papel y Desechables"],
            "Papel y Desechables": ["Productos de Limpieza", "Cuidado Personal"],

            "Cuidado Personal": ["Papel y Desechables", "Cuidado Femenino"],
            "Cuidado Femenino": ["Cuidado Personal", "Cuidado Bebé"],
            "Cuidado Bebé": ["Cuidado Femenino", "Congelados"],

            "Congelados": ["Cuidado Bebé", "Misceláneos"],
            "Misceláneos": ["Congelados", "Navideños"],
            "Navideños": ["Misceláneos", "Bebidas"],

            "Bebidas": ["Navideños", "Bebidas Alcohólicas"],
            "Bebidas Alcohólicas": ["Bebidas", "Adicionales"],
            "Adicionales": ["Bebidas Alcohólicas", "Caja"],

            "Caja": [],
        },
    }
}