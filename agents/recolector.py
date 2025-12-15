"""
Agente Recolector: Inicia el recorrido del supermercado, y recolecta los productos.
Tipo: Agente Basado en Objetivos 
"""
import time
from collections import deque, defaultdict
from data.products import PRODUCTS
from data.supermarket_maps import SUPERMARKET_MAPS


class RecolectorAgent:
    """
    Agente Recolector basado en objetivos.
    Planifica primero el recorrido y luego recolecta por sección.
    """

    def collect(
        self,
        option,
        supermarket_name,
        log_callback=print,
        move_callback=None
    ):
        log_callback(f"Recolector: Recolectando productos en {supermarket_name}")

        supermarket = SUPERMARKET_MAPS[supermarket_name]
        connections = supermarket["connections"]

        entry_section = supermarket["entry"]
        exit_section = supermarket["exit"]

        # 🔥 1️⃣ PREPROCESAR PRODUCTOS POR SECCIÓN (CLAVE)
        products_by_section = self._group_products_by_section(option)

        target_sections = set(products_by_section.keys())
        remaining_sections = set(target_sections)

        log_callback(f"Secciones objetivo: {remaining_sections}")

        # 2️⃣ PLANIFICAR RECORRIDO COMPLETO
        planned_route = self._plan_route(
            entry_section,
            remaining_sections,
            exit_section,
            connections
        )

        log_callback(f"Ruta planificada: {planned_route}")

        cart = []

        # 3️⃣ EJECUTAR RECORRIDO PLANIFICADO
        current_section = planned_route[0]

        if move_callback:
            move_callback(current_section)

        for section in planned_route[1:]:
            log_callback(f"Moviéndose a sección: {section}")

            if move_callback:
                move_callback(section)

            time.sleep(0.3)
            current_section = section

            # 🔥 Recolectar TODO lo que corresponde a esa sección
            if section in remaining_sections:
                self._collect_section_products(
                    section,
                    products_by_section,
                    cart,
                    log_callback
                )
                remaining_sections.remove(section)

        # 4️⃣ 🔒 GARANTIZAR LLEGADA REAL A CAJA (FIX)
        if current_section != exit_section:
            log_callback("⚠️ No se llegó a Caja. Recalculando ruta final...")

            path_to_exit = self._bfs_path(
                current_section,
                exit_section,
                connections
            )

            if path_to_exit:
                for section in path_to_exit[1:]:
                    log_callback(f"Moviéndose a sección: {section}")

                    if move_callback:
                        move_callback(section)

                    time.sleep(0.3)
                    current_section = section
            else:
                log_callback(
                    "❌ ERROR CRÍTICO: No existe camino a Caja desde la posición actual"
                )

        log_callback("Recolección finalizada. Llegó a Caja.")
        return cart
    
    def _bfs_distances(self, start, connections):
        queue = deque([(start, 0)])
        distances = {start: 0}
        visited = {start}

        graph = {}
        for k, v in connections.items():
            graph.setdefault(k, set()).update(v)
            for n in v:
                graph.setdefault(n, set()).add(k)

        while queue:
            node, dist = queue.popleft()
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    distances[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))

        return distances

    # ================= PLANIFICACIÓN =================

    def _plan_route(self, entry, targets, exit, connections):
        route = [entry]
        current = entry

        # 🔹 Distancia global desde entrada
        distances = self._bfs_distances(entry, connections)

        # 🔹 Ordenar secciones por profundidad (no greedy)
        ordered_targets = sorted(
            targets,
            key=lambda s: distances.get(s, float("inf"))
        )

        for section in ordered_targets:
            path = self._bfs_path(current, section, connections)
            if path:
                route.extend(path[1:])
                current = section

        # 🔹 Ir a caja
        path_to_exit = self._bfs_path(current, exit, connections)
        if path_to_exit:
            route.extend(path_to_exit[1:])

        return route


    # ================= PREPROCESAMIENTO =================

    def _group_products_by_section(self, option):
        """
        Agrupa TODOS los productos por sección ANTES del recorrido.
        """
        grouped = defaultdict(list)

        for item in option:
            product = next(p for p in PRODUCTS if p["name"] == item["name"])
            grouped[product["section"]].append({
                "product": product,
                "qty": item["qty"]
            })

        return grouped

    # ================= AUX =================

    def _bfs_path(self, start, goal, connections):
        queue = deque([[start]])
        visited = set()

        graph = {}
        for k, v in connections.items():
            graph.setdefault(k, set()).update(v)
            for n in v:
                graph.setdefault(n, set()).add(k)

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == goal:
                return path

            if node not in visited:
                visited.add(node)
                for neighbor in graph.get(node, []):
                    queue.append(path + [neighbor])

        return []

    def _nearest_section_graph(self, current, targets, connections):
        best_section = None
        best_distance = float("inf")

        for section in targets:
            path = self._bfs_path(current, section, connections)
            if path and len(path) < best_distance:
                best_distance = len(path)
                best_section = section

        return best_section

    def _collect_section_products(
        self,
        section,
        products_by_section,
        cart,
        log_callback
    ):
        """
        Recolecta TODO lo que pertenece a una sección.
        """
        for entry in products_by_section.get(section, []):
            product = entry["product"]
            qty = entry["qty"]

            for _ in range(qty):
                log_callback(
                    f"  Recolectado: {product['name']} ({product['price']} Bs)"
                )
                cart.append(product)
                time.sleep(0.2)