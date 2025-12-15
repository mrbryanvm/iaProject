import time
from collections import deque
from data.products import PRODUCTS
from data.supermarket_maps import SUPERMARKET_MAPS


class RecolectorAgent:
    """
    Agente Recolector basado en objetivos.
    Recorre el supermercado recolectando productos según un mapa interno (grafo).
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
        positions = supermarket["sections"]

        current_section = supermarket["entry"]
        exit_section = supermarket["exit"]

        # Determinar secciones objetivo
        target_sections = self._extract_required_sections(option)
        log_callback(f"Secciones objetivo: {target_sections}")

        cart = []

        # POSICIÓN INICIAL
        if move_callback:
            move_callback(current_section)

        # Recorrido por objetivos
        while target_sections:
            next_section = self._nearest_section(
                current_section, target_sections, positions
            )

            path = self._bfs_path(current_section, next_section, connections)

            for section in path[1:]:
                log_callback(f"Moviéndose a sección: {section}")

                # 🔥 AVISAR A LA UI
                if move_callback:
                    move_callback(section)

                time.sleep(0.15)
                current_section = section

                if section in target_sections:
                    self._collect_products_from_section(
                        section, option, cart, log_callback
                    )
                    target_sections.remove(section)

        # 3️⃣ Ir a Caja
        path_to_exit = self._bfs_path(current_section, exit_section, connections)
        for section in path_to_exit[1:]:
            log_callback(f"Moviéndose a sección: {section}")

            if move_callback:
                move_callback(section)

            time.sleep(0.15)

        log_callback("Recolección finalizada. Llegó a Caja.")
        return cart

    # ================= AUX =================

    def _extract_required_sections(self, option):
        sections = set()
        for item in option:
            product = next(p for p in PRODUCTS if p["name"] == item["name"])
            sections.add(product["section"])
        return sections

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

    def _nearest_section(self, current, targets, positions):
        cx, cy = positions[current]

        def distance(section):
            sx, sy = positions[section]
            return abs(cx - sx) + abs(cy - sy)

        return min(targets, key=distance)

    def _collect_products_from_section(self, section, option, cart, log_callback):
        for item in option:
            product = next(p for p in PRODUCTS if p["name"] == item["name"])
            if product["section"] == section:
                for _ in range(item["qty"]):
                    log_callback(
                        f"  Recolectado: {product['name']} ({product['price']} Bs)"
                    )
                    cart.append(product)
                    time.sleep(0.1)
