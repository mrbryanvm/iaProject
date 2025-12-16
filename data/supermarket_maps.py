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
    },

    # ==================== MAPEO INTERNO - HIPERMAXI EL PRADO ====================
    "Hipermaxi El Prado": {
        "geo_location": (-17.381920, -66.163870),
        "entry": "Entrada",
        "exit": "Caja",

        "sections": {
            "Entrada": (0, 0),

            "Frutas": (1, 0),
            "Verduras": (2, 0),
            "Panadería y Repostería": (3, 0),

            "Carnes y Embutidos": (0, 1),
            "Pescados y Mariscos": (1, 1),
            "Lácteos": (2, 1),
            "Congelados": (3, 1),

            "Despensa Básica": (0, 2),
            "Legumbres y Granos": (1, 2),
            "Enlatados y Conservas": (2, 2),
            "Cereales y Desayuno": (3, 2),

            "Snacks y Golosinas": (0, 3),
            "Café, Té e Infusiones": (1, 3),
            "Condimentos y Especias": (2, 3),
            "Misceláneos": (3, 3),

            "Productos de Limpieza": (0, 4),
            "Papel y Desechables": (1, 4),
            "Cuidado Personal": (2, 4),
            "Cuidado Bebé": (3, 4),

            "Cuidado Femenino": (0, 5),
            "Bebidas": (1, 5),
            "Bebidas Alcohólicas": (2, 5),
            "Adicionales": (3, 5),

            "Navideños": (1, 6),
            "Caja": (2, 6),
        },

        # Grafo de conectividad
        "connections": {
            "Entrada": ["Frutas", "Carnes y Embutidos"],

            "Frutas": ["Entrada", "Verduras"],
            "Verduras": ["Frutas", "Panadería y Repostería"],
            "Panadería y Repostería": ["Verduras", "Congelados"],

            "Carnes y Embutidos": ["Entrada", "Pescados y Mariscos"],
            "Pescados y Mariscos": ["Carnes y Embutidos", "Lácteos"],
            "Lácteos": ["Pescados y Mariscos", "Congelados"],
            "Congelados": ["Lácteos", "Panadería y Repostería", "Cereales y Desayuno"],

            "Despensa Básica": ["Legumbres y Granos", "Snacks y Golosinas"],
            "Legumbres y Granos": ["Despensa Básica", "Enlatados y Conservas"],
            "Enlatados y Conservas": ["Legumbres y Granos", "Cereales y Desayuno"],
            "Cereales y Desayuno": ["Enlatados y Conservas", "Congelados"],

            "Snacks y Golosinas": ["Despensa Básica", "Café, Té e Infusiones"],
            "Café, Té e Infusiones": ["Snacks y Golosinas", "Condimentos y Especias"],
            "Condimentos y Especias": ["Café, Té e Infusiones", "Misceláneos"],
            "Misceláneos": ["Condimentos y Especias", "Cuidado Personal"],

            "Productos de Limpieza": ["Papel y Desechables"],
            "Papel y Desechables": ["Productos de Limpieza", "Cuidado Personal"],
            "Cuidado Personal": ["Papel y Desechables", "Misceláneos", "Cuidado Bebé"],
            "Cuidado Bebé": ["Cuidado Personal", "Adicionales"],

            "Cuidado Femenino": ["Bebidas"],
            "Bebidas": ["Cuidado Femenino", "Bebidas Alcohólicas", "Navideños"],
            "Bebidas Alcohólicas": ["Bebidas", "Adicionales"],
            "Adicionales": ["Bebidas Alcohólicas", "Cuidado Bebé", "Caja"],

            "Navideños": ["Bebidas", "Caja"],
            "Caja": [],
        },
    },
    # ==================== MAPEO INTERNO - HIPERMAXI JUAN DE LA ROSA ====================
    "Hipermaxi Juan de la Rosa": {
        "geo_location": (-17.3767, -66.1725),
        "entry": "Entrada",
        "exit": "Caja",

        "sections": {
            "Entrada": (2, 0),

            "Bebidas": (0, 1),
            "Bebidas Alcohólicas": (1, 1),
            "Adicionales": (2, 1),
            "Navideños": (3, 1),

            "Panadería y Repostería": (0, 2),
            "Frutas": (1, 2),
            "Verduras": (2, 2),
            "Congelados": (3, 2),

            "Carnes y Embutidos": (0, 3),
            "Pescados y Mariscos": (1, 3),
            "Lácteos": (2, 3),
            "Cereales y Desayuno": (3, 3),

            "Despensa Básica": (0, 4),
            "Legumbres y Granos": (1, 4),
            "Enlatados y Conservas": (2, 4),
            "Snacks y Golosinas": (3, 4),

            "Café, Té e Infusiones": (0, 5),
            "Condimentos y Especias": (1, 5),
            "Misceláneos": (2, 5),
            "Productos de Limpieza": (3, 5),

            "Papel y Desechables": (0, 6),
            "Cuidado Personal": (1, 6),
            "Cuidado Femenino": (2, 6),
            "Cuidado Bebé": (3, 6),

            "Caja": (2, 7),
        },

        # ==================== CONECTIVIDAD ====================
        "connections": {
            "Entrada": ["Adicionales", "Verduras"],

            "Bebidas": ["Bebidas Alcohólicas", "Panadería y Repostería"],
            "Bebidas Alcohólicas": ["Bebidas", "Adicionales"],
            "Adicionales": ["Bebidas Alcohólicas", "Navideños", "Entrada"],
            "Navideños": ["Adicionales", "Congelados"],

            "Panadería y Repostería": ["Bebidas", "Frutas"],
            "Frutas": ["Panadería y Repostería", "Verduras"],
            "Verduras": ["Frutas", "Congelados", "Entrada"],
            "Congelados": ["Verduras", "Navideños", "Cereales y Desayuno"],

            "Carnes y Embutidos": ["Pescados y Mariscos", "Despensa Básica"],
            "Pescados y Mariscos": ["Carnes y Embutidos", "Lácteos"],
            "Lácteos": ["Pescados y Mariscos", "Cereales y Desayuno"],
            "Cereales y Desayuno": ["Lácteos", "Congelados", "Snacks y Golosinas"],

            "Despensa Básica": ["Carnes y Embutidos", "Legumbres y Granos", "Misceláneos"],
            "Legumbres y Granos": ["Despensa Básica", "Enlatados y Conservas", "Condimentos y Especias"],
            "Enlatados y Conservas": ["Legumbres y Granos", "Snacks y Golosinas", "Misceláneos"],
            "Snacks y Golosinas": ["Enlatados y Conservas", "Cereales y Desayuno", "Condimentos y Especias"],

            "Café, Té e Infusiones": ["Condimentos y Especias", "Papel y Desechables"],
            "Condimentos y Especias": ["Café, Té e Infusiones", "Misceláneos", "Legumbres y Granos",  "Snacks y Golosinas"],
            "Misceláneos": ["Condimentos y Especias", "Productos de Limpieza", "Despensa Básica", "Enlatados y Conservas"],
            "Productos de Limpieza": ["Misceláneos", "Cuidado Bebé"],

            "Papel y Desechables": ["Café, Té e Infusiones", "Cuidado Personal"],
            "Cuidado Personal": ["Papel y Desechables", "Cuidado Femenino"],
            "Cuidado Femenino": ["Cuidado Personal", "Cuidado Bebé"],
            "Cuidado Bebé": ["Cuidado Femenino", "Productos de Limpieza", "Caja"],

            "Caja": [],
        },
    },

    # ==================== MAPEO INTERNO - HIPERMAXI CIRCUNVALACIÓN (DISPOSICIÓN ALTERNATIVA) ====================
    "Hipermaxi Circunvalación": {
        "geo_location": (-17.3638, -66.1659),
        "entry": "Entrada",
        "exit": "Caja",

        "sections": {
            # --- Inicio y Productos Frescos (Cerca de la Entrada) ---
            "Entrada": (0, 0),

            "Frutas": (1, 1),
            "Verduras": (1, 2),
            "Panadería y Repostería": (2, 3), # Moviéndola un poco
            "Carnes y Embutidos": (0, 3),
            "Pescados y Mariscos": (0, 4),
            "Lácteos": (1, 5),
            "Congelados": (2, 5),

            # --- Pasillo Central de Despensa ---
            "Despensa Básica": (4, 1),
            "Legumbres y Granos": (4, 2),
            "Enlatados y Conservas": (4, 3),
            "Cereales y Desayuno": (4, 4),

            # --- Pasillo de Golosinas y Misceláneos ---
            "Snacks y Golosinas": (6, 1),
            "Café, Té e Infusiones": (6, 2),
            "Condimentos y Especias": (6, 3),
            "Misceláneos": (6, 4),

            # --- Pasillo de No Comestibles (Limpieza y Cuidado) ---
            "Productos de Limpieza": (8, 1),
            "Papel y Desechables": (8, 2),
            "Cuidado Personal": (8, 3),
            "Cuidado Bebé": (8, 4),
            "Cuidado Femenino": (8, 5),

            # --- Zona de Bebidas y Salida ---
            "Bebidas": (6, 6),
            "Bebidas Alcohólicas": (7, 6),
            "Adicionales": (8, 6), # Cerca del final

            "Navideños": (5, 7), # Una sección temporal
            "Caja": (10, 8), # La salida bien lejos para maximizar el recorrido
        },

        # ==================== CONECTIVIDAD (SIN CAMBIOS) ====================
        "connections": {
            "Entrada": ["Frutas", "Carnes y Embutidos"],

            "Frutas": ["Entrada", "Verduras"],
            "Verduras": ["Frutas", "Panadería y Repostería"],
            "Panadería y Repostería": ["Verduras", "Congelados"],

            "Carnes y Embutidos": ["Entrada", "Pescados y Mariscos"],
            "Pescados y Mariscos": ["Carnes y Embutidos", "Lácteos"],
            "Lácteos": ["Pescados y Mariscos", "Congelados"],
            "Congelados": ["Lácteos", "Panadería y Repostería", "Cereales y Desayuno"],

            "Despensa Básica": ["Legumbres y Granos", "Snacks y Golosinas"],
            "Legumbres y Granos": ["Despensa Básica", "Enlatados y Conservas"],
            "Enlatados y Conservas": ["Legumbres y Granos", "Cereales y Desayuno"],
            "Cereales y Desayuno": ["Enlatados y Conservas", "Congelados"],

            "Snacks y Golosinas": ["Despensa Básica", "Café, Té e Infusiones"],
            "Café, Té e Infusiones": ["Snacks y Golosinas", "Condimentos y Especias"],
            "Condimentos y Especias": ["Café, Té e Infusiones", "Misceláneos"],
            "Misceláneos": ["Condimentos y Especias", "Cuidado Personal"],

            "Productos de Limpieza": ["Papel y Desechables"],
            "Papel y Desechables": ["Productos de Limpieza", "Cuidado Personal"],
            "Cuidado Personal": ["Papel y Desechables", "Misceláneos", "Cuidado Bebé"],
            "Cuidado Bebé": ["Cuidado Personal", "Adicionales"],

            "Cuidado Femenino": ["Bebidas"],
            "Bebidas": ["Cuidado Femenino", "Bebidas Alcohólicas", "Navideños"],
            "Bebidas Alcohólicas": ["Bebidas", "Adicionales"],
            "Adicionales": ["Bebidas Alcohólicas", "Cuidado Bebé", "Caja"],

            "Navideños": ["Bebidas", "Caja"],
            "Caja": [],
        },
    },

    # ==================== MAPEO INTERNO - HIPERMAXI SACABA ====================
    "Hipermaxi Sacaba": {
        "geo_location": (-17.3819, -66.1190),
        "entry": "Entrada",
        "exit": "Caja",

        "sections": {
            "Entrada": (2, 0),

            "Panadería y Repostería": (1, 1),
            "Frutas": (2, 1),
            "Verduras": (3, 1),

            "Lácteos": (0, 2),
            "Carnes y Embutidos": (1, 2),
            "Pescados y Mariscos": (2, 2),
            "Congelados": (3, 2),

            "Despensa Básica": (0, 3),
            "Legumbres y Granos": (1, 3),
            "Enlatados y Conservas": (2, 3),
            "Cereales y Desayuno": (3, 3),

            "Snacks y Golosinas": (0, 4),
            "Café, Té e Infusiones": (1, 4),
            "Condimentos y Especias": (2, 4),
            "Misceláneos": (3, 4),

            "Productos de Limpieza": (0, 5),
            "Papel y Desechables": (1, 5),
            "Cuidado Personal": (2, 5),
            "Cuidado Bebé": (3, 5),

            "Cuidado Femenino": (1, 6),
            "Bebidas": (2, 6),
            "Bebidas Alcohólicas": (3, 6),

            "Navideños": (0, 7),
            "Adicionales": (1, 7),
            "Caja": (2, 7),
        },

        # ==================== CONECTIVIDAD ====================
        "connections": {
            "Entrada": ["Frutas", "Panadería y Repostería"],

            "Panadería y Repostería": ["Entrada", "Frutas", "Carnes y Embutidos"],
            "Frutas": ["Entrada", "Panadería y Repostería", "Verduras"],
            "Verduras": ["Frutas", "Pescados y Mariscos"],

            "Lácteos": ["Carnes y Embutidos", "Despensa Básica"],
            "Carnes y Embutidos": ["Panadería y Repostería", "Lácteos", "Pescados y Mariscos"],
            "Pescados y Mariscos": ["Carnes y Embutidos", "Verduras", "Congelados"],
            "Congelados": ["Pescados y Mariscos", "Cereales y Desayuno"],

            "Despensa Básica": ["Lácteos", "Legumbres y Granos", "Snacks y Golosinas"],
            "Legumbres y Granos": ["Despensa Básica", "Enlatados y Conservas"],
            "Enlatados y Conservas": ["Legumbres y Granos", "Cereales y Desayuno"],
            "Cereales y Desayuno": ["Enlatados y Conservas", "Congelados"],

            "Snacks y Golosinas": ["Despensa Básica", "Café, Té e Infusiones"],
            "Café, Té e Infusiones": ["Snacks y Golosinas", "Condimentos y Especias"],
            "Condimentos y Especias": ["Café, Té e Infusiones", "Misceláneos"],
            "Misceláneos": ["Condimentos y Especias", "Cuidado Personal"],

            "Productos de Limpieza": ["Papel y Desechables", "Navideños"],
            "Papel y Desechables": ["Productos de Limpieza", "Cuidado Personal"],
            "Cuidado Personal": ["Papel y Desechables", "Misceláneos", "Cuidado Bebé"],
            "Cuidado Bebé": ["Cuidado Personal", "Bebidas"],

            "Cuidado Femenino": ["Bebidas"],
            "Bebidas": ["Cuidado Femenino", "Cuidado Bebé", "Bebidas Alcohólicas"],
            "Bebidas Alcohólicas": ["Bebidas", "Adicionales"],

            "Navideños": ["Productos de Limpieza", "Adicionales"],
            "Adicionales": ["Navideños", "Bebidas Alcohólicas", "Caja"],

            "Caja": [],
        },
    },

    # ==================== MAPEO INTERNO - HIPERMAXI BLANCO GALINDO ====================
    "Hipermaxi Blanco Galindo": {
        "geo_location": (-17.393820, -66.182200),
        "entry": "Entrada",
        "exit": "Caja",

        "sections": {
            # 🔹 ENTRADA Y CAJA (lado izquierdo, juntas)
            "Entrada": (0, 0),
            "Caja": (0, 1),

            # 🔹 FILA SUPERIOR
            "Despensa Básica": (1, 0),
            "Legumbres y Granos": (2, 0),
            "Enlatados y Conservas": (3, 0),

            # 🔹 SEGUNDA FILA
            "Snacks y Golosinas": (1, 1),
            "Cereales y Desayuno": (2, 1),
            "Café, Té e Infusiones": (3, 1),

            # 🔹 TERCERA FILA
            "Condimentos y Especias": (1, 2),
            "Productos de Limpieza": (2, 2),
            "Papel y Desechables": (3, 2),

            # 🔹 CUARTA FILA
            "Cuidado Personal": (1, 3),
            "Cuidado Femenino": (2, 3),
            "Cuidado Bebé": (3, 3),

            # 🔹 QUINTA FILA
            "Frutas": (1, 4),
            "Verduras": (2, 4),
            "Lácteos": (3, 4),

            # 🔹 SEXTA FILA
            "Carnes y Embutidos": (1, 5),
            "Pescados y Mariscos": (2, 5),
            "Congelados": (3, 5),

            # 🔹 SÉPTIMA FILA
            "Panadería y Repostería": (1, 6),
            "Misceláneos": (2, 6),
            "Navideños": (3, 6),

            # 🔹 ÚLTIMA FILA
            "Bebidas": (1, 7),
            "Bebidas Alcohólicas": (2, 7),
            "Adicionales": (3, 7),
        },

        # ==================== CONECTIVIDAD ====================
        "connections": {
            # Entrada / Caja
            "Entrada": ["Despensa Básica", "Snacks y Golosinas"],
            "Caja": ["Snacks y Golosinas", "Cuidado Personal"],

            # Fila 1
            "Despensa Básica": ["Entrada", "Legumbres y Granos", "Snacks y Golosinas"],
            "Legumbres y Granos": ["Despensa Básica", "Enlatados y Conservas"],
            "Enlatados y Conservas": ["Legumbres y Granos", "Café, Té e Infusiones"],

            # Fila 2
            "Snacks y Golosinas": ["Despensa Básica", "Cereales y Desayuno", "Caja"],
            "Cereales y Desayuno": ["Snacks y Golosinas", "Café, Té e Infusiones"],
            "Café, Té e Infusiones": ["Cereales y Desayuno", "Condimentos y Especias"],

            # Fila 3
            "Condimentos y Especias": ["Café, Té e Infusiones", "Productos de Limpieza"],
            "Productos de Limpieza": ["Condimentos y Especias", "Papel y Desechables"],
            "Papel y Desechables": ["Productos de Limpieza", "Cuidado Personal"],

            # Fila 4
            "Cuidado Personal": ["Papel y Desechables", "Cuidado Femenino", "Caja"],
            "Cuidado Femenino": ["Cuidado Personal", "Cuidado Bebé"],
            "Cuidado Bebé": ["Cuidado Femenino", "Lácteos"],

            # Fila 5
            "Frutas": ["Verduras", "Panadería y Repostería"],
            "Verduras": ["Frutas", "Lácteos"],
            "Lácteos": ["Verduras", "Cuidado Bebé", "Carnes y Embutidos"],

            # Fila 6
            "Carnes y Embutidos": ["Lácteos", "Pescados y Mariscos"],
            "Pescados y Mariscos": ["Carnes y Embutidos", "Congelados"],
            "Congelados": ["Pescados y Mariscos", "Misceláneos"],

            # Fila 7
            "Panadería y Repostería": ["Frutas", "Misceláneos"],
            "Misceláneos": ["Panadería y Repostería", "Navideños"],
            "Navideños": ["Misceláneos", "Bebidas"],

            # Fila 8
            "Bebidas": ["Navideños", "Bebidas Alcohólicas"],
            "Bebidas Alcohólicas": ["Bebidas", "Adicionales"],
            "Adicionales": ["Bebidas Alcohólicas"],
        },
    },

    # ==================== MAPEO INTERNO - HIPERMAXI PANAMERICANA ====================
    "Hipermaxi Panamericana": {
        "geo_location": (-17.4192, -66.1582),
        "entry": "Entrada",
        "exit": "Caja",

        "sections": {
            # 🔹 ENTRADA Y CAJA (abajo, juntas)
            "Entrada": (1, 8),
            "Caja": (2, 8),

            # 🔹 FILA INFERIOR
            "Bebidas": (0, 7),
            "Bebidas Alcohólicas": (1, 7),
            "Adicionales": (2, 7),
            "Navideños": (3, 7),

            # 🔹 FILA 6
            "Cuidado Personal": (0, 6),
            "Cuidado Femenino": (1, 6),
            "Cuidado Bebé": (2, 6),
            "Misceláneos": (3, 6),

            # 🔹 FILA 5
            "Productos de Limpieza": (0, 5),
            "Papel y Desechables": (1, 5),
            "Condimentos y Especias": (2, 5),
            "Café, Té e Infusiones": (3, 5),

            # 🔹 FILA 4
            "Snacks y Golosinas": (0, 4),
            "Cereales y Desayuno": (1, 4),
            "Enlatados y Conservas": (2, 4),
            "Legumbres y Granos": (3, 4),

            # 🔹 FILA 3
            "Despensa Básica": (0, 3),
            "Congelados": (1, 3),
            "Lácteos": (2, 3),
            "Pescados y Mariscos": (3, 3),

            # 🔹 FILA 2
            "Carnes y Embutidos": (0, 2),
            "Verduras": (1, 2),
            "Frutas": (2, 2),
            "Panadería y Repostería": (3, 2),
        },

        # ==================== CONECTIVIDAD ====================
        "connections": {
            # Entrada / Caja
            "Entrada": ["Bebidas Alcohólicas", "Adicionales"],
            "Caja": ["Adicionales", "Navideños"],

            # Fila 7
            "Bebidas": ["Bebidas Alcohólicas", "Cuidado Personal"],
            "Bebidas Alcohólicas": ["Bebidas", "Adicionales", "Entrada"],
            "Adicionales": ["Bebidas Alcohólicas", "Navideños", "Entrada", "Caja"],
            "Navideños": ["Adicionales", "Misceláneos", "Caja"],

            # Fila 6
            "Cuidado Personal": ["Bebidas", "Cuidado Femenino", "Productos de Limpieza"],
            "Cuidado Femenino": ["Cuidado Personal", "Cuidado Bebé"],
            "Cuidado Bebé": ["Cuidado Femenino", "Misceláneos"],
            "Misceláneos": ["Cuidado Bebé", "Navideños", "Café, Té e Infusiones"],

            # Fila 5
            "Productos de Limpieza": ["Cuidado Personal", "Papel y Desechables", "Snacks y Golosinas"],
            "Papel y Desechables": ["Productos de Limpieza", "Condimentos y Especias"],
            "Condimentos y Especias": ["Papel y Desechables", "Café, Té e Infusiones", "Cereales y Desayuno"],
            "Café, Té e Infusiones": ["Condimentos y Especias", "Misceláneos", "Enlatados y Conservas"],

            # Fila 4
            "Snacks y Golosinas": ["Cereales y Desayuno", "Despensa Básica", "Productos de Limpieza"],
            "Cereales y Desayuno": ["Snacks y Golosinas", "Enlatados y Conservas", "Condimentos y Especias"],
            "Enlatados y Conservas": ["Cereales y Desayuno", "Legumbres y Granos", "Café, Té e Infusiones"],
            "Legumbres y Granos": ["Enlatados y Conservas", "Congelados"],

            # Fila 3
            "Despensa Básica": ["Snacks y Golosinas", "Congelados"],
            "Congelados": ["Despensa Básica", "Lácteos", "Legumbres y Granos"],
            "Lácteos": ["Congelados", "Pescados y Mariscos"],
            "Pescados y Mariscos": ["Lácteos", "Carnes y Embutidos"],

            # Fila 2
            "Carnes y Embutidos": ["Pescados y Mariscos", "Verduras"],
            "Verduras": ["Carnes y Embutidos", "Frutas"],
            "Frutas": ["Verduras", "Panadería y Repostería"],
            "Panadería y Repostería": ["Frutas"],
        },
    }
}