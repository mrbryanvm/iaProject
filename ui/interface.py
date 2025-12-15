"""
GUI moderno para el Sistema Multi-Agente usando ttkbootstrap y tkintermapview.
Mapa Real Interactivo de Cochabamba con Enrutamiento de Calles (OSRM).
Incluye Corrección para Rastros de Marcadores y Validación de Entrada Robusta.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import tkintermapview
from agents.shopper import ShopperAgent
from data.map_data import MapData
from data.products import PRODUCTS
from data.supermarket_maps import SUPERMARKET_MAPS
from collections import Counter

class AgentUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly") 
        self.title("Vale Navideño")
        self.geometry("1400x900")
        
        self.map_data = MapData()
        self.shopper = ShopperAgent(log_callback=self.log_message)
        
        # Estado
        self.start_coords = (-17.3938, -66.1570)
        self.current_agent_marker = None
        self.start_marker = None
        self.path_line = None

        # Estado visual interno
        self.internal_map_visible = False
        self.internal_nodes = []
        self.internal_paths = []
        self.current_supermarket = None
        
        # Guardar stock inicial para reset
        self.initial_stock = {p['name']: p.get('stock', 0) for p in PRODUCTS}
        
        # Estado de última compra (para resaltar en inventario)
        self.last_purchase_counts = {}
        self.refresh_inventory_callback = None

        # 🔥 NUEVO ESTADO: Opcion seleccionada por el usuario
        self.selected_option = None

        self._init_ui()

    def _init_ui(self):
        # Encabezado
        header = ttk.Frame(self, bootstyle="primary", padding=15)
        header.pack(fill=X)
        ttk.Label(
            header,
            text="🎄 Vale Navideño 🎄",
            font=("Segoe UI", 20, "bold"),
            bootstyle="inverse-primary"
        ).pack()

        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=BOTH, expand=YES)

        # --- PANEL IZQUIERDO ---
        left_panel = ttk.Labelframe(main_frame, text="Panel de Control", padding=15)
        left_panel.pack(side=LEFT, fill=Y, padx=10, ipadx=5)

        config_frame = ttk.Labelframe(left_panel, text="Configuración", padding=15)
        config_frame.pack(fill=X, pady=10)

        ttk.Label(config_frame, text="Monto del Vale (Bs):", font=("Segoe UI", 10)).pack(anchor=W)
        self.amount_entry = ttk.Entry(config_frame)
        self.amount_entry.insert(0, "50.0")
        self.amount_entry.pack(fill=X, pady=(5, 15))

        ttk.Label(config_frame, text="Sucursal Destino (Meta):", font=("Segoe UI", 10)).pack(anchor=W)
        self.target_var = ttk.StringVar()
        branches = [k for k in self.map_data.locations.keys() if "Hipermaxi" in k]
        self.target_combo = ttk.Combobox(
            config_frame,
            textvariable=self.target_var,
            values=branches,
            state="readonly"
        )
        if branches:
            self.target_combo.current(0)
        self.target_combo.pack(fill=X, pady=(5, 15))

        ttk.Label(
            config_frame,
            text="Punto de Partida:",
            font=("Segoe UI", 10, "bold"),
            bootstyle="primary"
        ).pack(anchor=W)

        self.start_info_label = ttk.Label(
            config_frame,
            text="📍 Haz CLICK en el mapa para elegir",
            font=("Segoe UI", 9, "italic"),
            bootstyle="secondary"
        )
        self.start_info_label.pack(anchor=W, pady=(5, 15))

        self.start_btn = ttk.Button(
            config_frame,
            text="▶ INICIAR SIMULACIÓN",
            command=self.start_simulation,
            bootstyle="success"
        )
        self.start_btn.pack(fill=X, pady=5, ipady=5)

        self.inv_btn = ttk.Button(
            config_frame,
            text="📦 Ver Inventario",
            command=self.open_inventory_window,
            bootstyle="info-outline"
        )
        self.inv_btn.pack(fill=X, pady=(0, 10))

        log_frame = ttk.Labelframe(left_panel, text="Registro (Logs)", padding=10)
        log_frame.pack(fill=BOTH, expand=YES, pady=5)

        self.log_text = ttk.Text(
            log_frame,
            height=20,
            width=35,
            font=("Consolas", 9),
            relief="flat"
        )
        self.log_text.pack(fill=BOTH, expand=YES)

        # --- PANEL CENTRAL: MAPA REAL ---
        center_panel = ttk.Frame(main_frame)
        center_panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=10)

        # Mapa real (SIN CAMBIOS)
        self.map_widget = tkintermapview.TkinterMapView(
            center_panel,
            corner_radius=15,
            width=800,
            height=600
        )
        self.map_widget.pack(fill=BOTH, expand=YES)

        self.map_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=m&hl=es&x={x}&y={y}&z={z}"
        )
        self.map_widget.set_position(-17.3938, -66.1570)
        self.map_widget.set_zoom(14)
        self.map_widget.add_left_click_map_command(self.set_start_on_click)

        # 🔧 MAPA INTERNO (MISMO PANEL, ENCIMA DEL MAPA)
        self.internal_canvas = ttk.Canvas(
            center_panel,
            bg="#f5f5f5",
            highlightthickness=0
        )

        self.internal_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ⬅️ oculto por defecto (FORMA CORRECTA)
        self.internal_canvas.place_forget()

        # --- BOTÓN MAPEO INTERNO ---
        self.internal_map_btn = ttk.Button(
            center_panel,
            text="🗺 Ver Mapeo Interno",
            bootstyle="info-outline",
            command=self.toggle_internal_map
        )
        self.internal_map_btn.place(relx=0.98, rely=0.02, anchor=NE)

        self.draw_destinations()
        self.update_start_marker()

        # --- PANEL DERECHO ---
        right_panel = ttk.Labelframe(
            main_frame,
            text="Acciones dentro el supermercado: Opciones/Recoleccion/Factura",
            padding=10
        )
        right_panel.pack(side=LEFT, fill=Y, padx=10, ipadx=5)

        content_frame = ttk.Frame(right_panel)
        content_frame.pack(fill=BOTH, expand=YES)

        canvas = ttk.Canvas(content_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.options_frame = ttk.Frame(scrollable_frame)
        self.options_frame.pack(fill=BOTH, expand=YES)

        ttk.Label(
            self.options_frame,
            text="Esperando cálculo de opciones...",
            font=("Segoe UI", 12, "italic"),
            bootstyle="secondary"
        ).pack(pady=20)

        self.old_receipt_frame = ttk.Frame(scrollable_frame)
        self.receipt_tree = self._create_receipt_tree(self.old_receipt_frame)
        self.receipt_tree.pack(fill=BOTH, expand=YES, pady=10)

        self.cashier_receipt_frame = ttk.Labelframe(
            scrollable_frame,
            text="🧾 Factura del Cajero (Opción Elegida)",
            padding=10
        )
        self.cashier_receipt_tree = self._create_receipt_tree(
            self.cashier_receipt_frame,
            height=8
        )
        self.cashier_receipt_tree.pack(fill=BOTH, expand=YES)

        self.collection_list_frame = ttk.Labelframe(
            scrollable_frame,
            text="🛒 Lista de Recolección del Agente (Orden de Recorrido)",
            padding=10
        )

        cols = ("qty", "prod", "unit_price")
        self.collection_tree = ttk.Treeview(
            self.collection_list_frame,
            columns=cols,
            show="headings",
            height=10
        )

        self.collection_tree.heading("qty", text="Nro.")
        self.collection_tree.column("qty", width=40, anchor=CENTER)

        self.collection_tree.heading("prod", text="Producto Recolectado")
        self.collection_tree.column("prod", width=260, anchor=W)

        self.collection_tree.heading("unit_price", text="PU (Bs)")
        self.collection_tree.column("unit_price", width=80, anchor=E)
        self.collection_tree.pack(fill=BOTH, expand=YES)

        self.status_frame = ttk.Frame(right_panel, padding=10, bootstyle="light")
        self.status_frame.pack(fill=X, side=BOTTOM)

        self.status_label = ttk.Label(
            self.status_frame,
            text="LISTO",
            font=("Segoe UI", 14, "bold"),
            bootstyle="secondary",
            anchor=CENTER
        )
        self.status_label.pack(fill=X)

    def _create_receipt_tree(self, parent_frame, height=18):
        """Función auxiliar para crear un Treeview de recibo estándar."""
        columns = ("qty", "unit_price", "prod", "price")
        tree = ttk.Treeview(
            parent_frame,
            columns=columns,
            show="headings",
            height=height
        )

        tree.heading("qty", text="#")
        tree.column("qty", width=30, anchor=CENTER)
        tree.heading("unit_price", text="PU")
        tree.column("unit_price", width=60, anchor=E)
        tree.heading("prod", text="Producto")
        tree.column("prod", width=180, anchor=W)
        tree.heading("price", text="Bs")
        tree.column("price", width=80, anchor=E)
        return tree
    
    def reset_right_panel(self):
        # 🔹 Limpiar y mostrar opciones por defecto
        for w in self.options_frame.winfo_children():
            w.destroy()

        ttk.Label(
            self.options_frame,
            text="Esperando cálculo de opciones...",
            font=("Segoe UI", 12, "italic"),
            bootstyle="secondary"
        ).pack(pady=20)

        # 🔹 Mostrar opciones / Ocultar resultados finales
        self.options_frame.pack(fill=BOTH, expand=YES)
        self.old_receipt_frame.pack_forget()
        self.cashier_receipt_frame.pack_forget()
        self.collection_list_frame.pack_forget()

        # 🔹 Limpiar arboles
        self.receipt_tree.delete(*self.receipt_tree.get_children())
        self.cashier_receipt_tree.delete(*self.cashier_receipt_tree.get_children())
        self.collection_tree.delete(*self.collection_tree.get_children())
        
        # 🔹 Resetear estado
        self.selected_option = None

    def update_internal_position(self, section_name):
        if not self.internal_map_visible:
            return

        if not hasattr(self, "internal_positions"):
            return

        if section_name not in self.internal_positions:
            return

        px, py = self.internal_positions[section_name]

        def draw():
            # Borrar marcador anterior
            self.internal_canvas.delete("agent")

            # Dibujar agente
            self.internal_canvas.create_oval(
                px - 8, py - 8,
                px + 8, py + 8,
                fill="#fbc02d",
                outline="#f57f17",
                width=2,
                tags="agent"
            )

        self.after(0, draw)
        
    def _start_pan(self, event):
        self.internal_canvas.scan_mark(event.x, event.y)

    def _do_pan(self, event):
        self.internal_canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_mousewheel(self, event):
        # Windows / Linux
        self.internal_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mousewheel(self, event):
        # Scroll horizontal con Shift
        self.internal_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def show_internal_map_fullscreen(self, supermarket_name):

        # Ocultar mapa real
        self.map_widget.place_forget()

        # Mostrar canvas interno
        self.internal_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.internal_canvas.delete("all")
        self.internal_map_visible = True

        # 🎮 Habilitar PAN con mouse
        self.internal_canvas.bind("<ButtonPress-1>", self._start_pan)
        self.internal_canvas.bind("<B1-Motion>", self._do_pan)

        self.internal_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.internal_canvas.bind("<Shift-MouseWheel>", self._on_shift_mousewheel)

        # 🎨 Fondo tipo supermercado
        self.internal_canvas.configure(bg="#f2efe9")

        market = SUPERMARKET_MAPS[supermarket_name]
        sections = market["sections"]
        connections = market["connections"]

        # 📐 Layout visual (más separación)
        CELL = 220
        OFFSET_X = 300
        OFFSET_Y = 220
        NODE_R = 16

        self.internal_positions = {}

        # 🔗 Dibujar conexiones (pasillos)
        for src, targets in connections.items():
            x1, y1 = sections[src]
            px1 = OFFSET_X + x1 * CELL
            py1 = OFFSET_Y + y1 * CELL

            for dst in targets:
                x2, y2 = sections[dst]
                px2 = OFFSET_X + x2 * CELL
                py2 = OFFSET_Y + y2 * CELL

                self.internal_canvas.create_line(
                    px1, py1, px2, py2,
                    fill="#b0bec5",
                    width=4,
                    smooth=True
                )

        # 🟢 Dibujar nodos
        for name, (x, y) in sections.items():
            px = OFFSET_X + x * CELL
            py = OFFSET_Y + y * CELL
            self.internal_positions[name] = (px, py)

            # Color especial
            if name.lower() == "entrada":
                color = "#2ecc71"
            elif name.lower() == "caja":
                color = "#e74c3c"
            else:
                color = "white"

            # Nodo
            self.internal_canvas.create_oval(
                px - NODE_R, py - NODE_R,
                px + NODE_R, py + NODE_R,
                fill=color,
                outline="#37474f",
                width=2
            )

            # Texto
            text_id = self.internal_canvas.create_text(
                px, py + 36,
                text=name,
                font=("Segoe UI", 9, "bold"),
                fill="#263238",
                anchor="n"
            )

            # Fondo del texto
            x1, y1, x2, y2 = self.internal_canvas.bbox(text_id)
            rect = self.internal_canvas.create_rectangle(
                x1 - 6, y1 - 3, x2 + 6, y2 + 3,
                fill="white",
                outline=""
            )
            self.internal_canvas.tag_raise(text_id)

        # 🧭 IMPORTANTE: permitir desplazamiento
        self.internal_canvas.configure(
            scrollregion=self.internal_canvas.bbox("all")
        )

    def hide_internal_map(self):
        self.internal_canvas.place_forget()
        self.map_widget.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.internal_map_visible = False

    def toggle_internal_map(self):
        if not self.current_supermarket:
            self.log_message("⚠ El agente aún no llegó al supermercado.")
            return

        if self.internal_map_visible:
            self.hide_internal_map()
        else:
            self.show_internal_map_fullscreen(self.current_supermarket)

    def clear_internal_map(self):
        for m in self.internal_nodes:
            m.delete()
        for p in self.internal_paths:
            p.delete()

        self.internal_nodes.clear()
        self.internal_paths.clear()

    def show_internal_map(self, supermarket_name):
        self.clear_internal_map()

        market = SUPERMARKET_MAPS[supermarket_name]
        sections = market["sections"]
        connections = market["connections"]

        # Escala visual simple (para que se vea grande)
        SCALE = 0.0003
        BASE_LAT, BASE_LON = self.map_data.get_coordinates(supermarket_name)

        # Dibujar nodos (secciones)
        for name, (x, y) in sections.items():
            lat = BASE_LAT + y * SCALE
            lon = BASE_LON + x * SCALE

            marker = self.map_widget.set_marker(
                lat, lon,
                text=name,
                marker_color_outside="#455a64",
                marker_color_circle="white"
            )
            self.internal_nodes.append(marker)

        # Dibujar conexiones
        for src, targets in connections.items():
            for dst in targets:
                x1, y1 = sections[src]
                x2, y2 = sections[dst]

                lat1 = BASE_LAT + y1 * SCALE
                lon1 = BASE_LON + x1 * SCALE
                lat2 = BASE_LAT + y2 * SCALE
                lon2 = BASE_LON + x2 * SCALE

                path = self.map_widget.set_path(
                    [(lat1, lon1), (lat2, lon2)],
                    width=2
                )
                self.internal_paths.append(path)

    def _finalize_collection_ui(self, cart, success):
        self.show_final_results(cart, self.selected_option)

        from collections import Counter
        self.last_purchase_counts = Counter([p["name"] for p in cart])

        if success:
            self.status_label.configure(
                text="¡COMPRA FINALIZADA!",
                bootstyle="success"
            )
        else:
            self.status_label.configure(
                text="ERROR EN COMPRA",
                bootstyle="danger"
            )

        self.start_btn.configure(
            state=NORMAL,
            text="▶ INICIAR SIMULACIÓN"
        )

    def _run_collection_logic(self, recolector_option, voucher_amount):
        try:
            cart, success = self.shopper.finalize_purchase(
                recolector_option,
                voucher_amount,
                move_callback=self.update_internal_position
            )

            # 🔁 Volver al hilo UI
            self.after(
                0,
                lambda: self._finalize_collection_ui(cart, success)
            )

        except Exception as e:
            self.after(0, lambda: self.log_message(f"Error en recolección: {e}"))

    def select_option(self, option):
        self.log_message("Usuario eligió una opción de compra.")
        self.selected_option = option

        self.options_frame.pack_forget()
        voucher_amount = float(self.amount_entry.get())

        recolector_option = [
            {
                "name": item["name"],
                "qty": item["qty"],
                "price": item["unit_price"]
            }
            for item in option["items"]
        ]

        self.status_label.configure(
            text="RECOLECTANDO PRODUCTOS...",
            bootstyle="warning"
        )

        # 🔥 EJECUTAR EN HILO
        thread = threading.Thread(
            target=self._run_collection_logic,
            args=(recolector_option, voucher_amount)
        )
        thread.daemon = True
        thread.start()
    
    # 🔥 NUEVAS FUNCIONES DE VISUALIZACIÓN
    def show_final_results(self, cart, original_option):
        """Muestra los dos paneles de resultados finales."""
        # 1. Asegurar que los contenedores estén visibles y los otros ocultos
        self.options_frame.pack_forget()
        self.old_receipt_frame.pack_forget() # Ocultar el recibo viejo
        
        self.cashier_receipt_frame.pack(fill=X, pady=10)
        self.collection_list_frame.pack(fill=X, pady=10)
        
        # 2. Renderizar cada tabla
        self.render_cashier_receipt(original_option)
        self.render_collection_list(cart)
        
        # 3. Llamar al show_receipt original para compatibilidad con el código subyacente
        # (Aunque ya no es visible, podríamos usarlo para el estado interno si fuera necesario)
        # Lo omitimos ya que estamos reemplazándolo.

    def render_cashier_receipt(self, option):
        """Muestra la factura (opción seleccionada) en el formato agrupado/alfabético."""
        self.cashier_receipt_tree.delete(*self.cashier_receipt_tree.get_children())
        total = 0

        # Agrupar y ordenar para la presentación "oficial" de la factura
        item_counts = Counter()
        item_prices = {}

        for item in option["items"]:
            item_counts[item["name"]] += item["qty"]
            item_prices[item["name"]] = item["unit_price"] # Precio unitario

        sorted_names = sorted(item_counts.keys())

        for name in sorted_names:
            qty = item_counts[name]
            unit_price = item_prices[name]
            subtotal = unit_price * qty
            total += subtotal

            self.cashier_receipt_tree.insert(
                "",
                END,
                values=(qty, f"{unit_price:.2f}", name, f"{subtotal:.2f}")
            )

        self.cashier_receipt_tree.insert(
            "", 
            END, 
            values=("", "", "TOTAL", f"{total:.2f}"), 
            tags=("total_row",)
        )
        self.cashier_receipt_tree.tag_configure("total_row", font=("Segoe UI", 10, "bold"))


    def render_collection_list(self, cart):
        """Lista de recolección con Nro ascendente, PU y TOTAL final."""
        self.collection_tree.delete(*self.collection_tree.get_children())

        total = 0.0

        for idx, item in enumerate(cart, start=1):
            name = item.get("name", "Producto Desconocido")
            price = float(item.get("price", 0.0))
            total += price

            self.collection_tree.insert(
                "",
                END,
                values=(idx, name, f"{price:.2f}"),
                tags=("collected",)
            )

        # Fila TOTAL
        self.collection_tree.insert(
            "",
            END,
            values=("", "TOTAL", f"{total:.2f}"),
            tags=("total_row",)
        )

        self.collection_tree.tag_configure("collected", foreground="#00796b")
        self.collection_tree.tag_configure("total_row", font=("Segoe UI", 10, "bold"))

    # ... [El resto del código es el mismo, pero lo dejo por si el _finalize_ui original necesita adaptarse] ...

    # Adaptación de show_receipt original (se mantiene para compatibilidad, aunque no se usa para mostrar)
    def show_receipt(self, cart):
        # Esta función ya no necesita empaquetar el frame, solo llenar el treeview (si fuera necesario).
        # Para el propósito del usuario, reemplazamos esta presentación con show_final_results.
        pass

    def _finalize_ui(self, cart, success):
        """Función que se llama al finalizar la simulación asíncrona (si no hay opciones)."""
        self.start_btn.configure(state=NORMAL, text="▶ INICIAR SIMULACIÓN")
        
        # Si 'finalize_purchase' se ejecutó en un hilo y no a través de 'select_option' (flujo original),
        # también debemos mostrar los dos paneles aquí.
        if cart:
            # Recrear la 'opcion' original para la Factura del Cajero
            item_counts = Counter([item['name'] for item in cart])
            item_prices = {item['name']: item['price'] for item in cart}
            
            reconstructed_option = {
                "items": [
                    {"name": name, "qty": qty, "unit_price": item_prices[name], "total_price": qty * item_prices[name]}
                    for name, qty in item_counts.items()
                ],
                "total": sum(qty * item_prices[name] for name, qty in item_counts.items())
            }
            
            self.show_final_results(cart, reconstructed_option)
            
            # Actualizar estado de última compra
            self.last_purchase_counts = item_counts
            
            # Auto-refrescar ventana de inventario si está abierta
            if self.refresh_inventory_callback:
                try:
                    self.refresh_inventory_callback()
                except Exception:
                    self.refresh_inventory_callback = None # Ventana cerrada probablemente

        if success:
            self.status_label.configure(text="¡ÉXITO!", bootstyle="success")
        else:
            self.status_label.configure(text="FALLÓ", bootstyle="danger")

    # ... [El resto de las funciones (refresh_options, show_optimizer_options, draw_destinations, etc.) son las mismas] ...
    def refresh_options(self):
        self.log_message("Refrescando opciones del optimizador...")
        options = self.shopper.request_purchase_options(
            float(self.amount_entry.get())
        )
        self.show_optimizer_options(options)

    def show_optimizer_options(self, options):
        # Limpiar frame
        for w in self.options_frame.winfo_children():
            w.destroy()

        ttk.Label(
            self.options_frame,
            text="Opciones de Compra",
            font=("Segoe UI", 14, "bold"),
            bootstyle="primary"
        ).pack(pady=10)

        for idx, option in enumerate(options, start=1):
            box = ttk.Labelframe(
                self.options_frame,
                text=f"Opción {idx}",
                padding=10
            )
            box.pack(fill=X, pady=8)

            # Mostrar productos ORDENADOS alfabéticamente
            for item in sorted(option["items"], key=lambda x: x["name"]):
                ttk.Label(
                    box,
                    text=f"- {item['name']}  x{item['qty']}  "
                         f"(Bs {item['unit_price']:.2f} c/u → Bs {item['total_price']:.2f})",
                    font=("Segoe UI", 9)
                ).pack(anchor=W)

            ttk.Label(
                box,
                text=f"Total: Bs {option['total']:.2f}",
                font=("Segoe UI", 10, "bold")
            ).pack(anchor=E, pady=5)

            ttk.Button(
                box,
                text="Elegir esta opción",
                bootstyle="success",
                command=lambda opt=option: self.select_option(opt)
            ).pack(fill=X, pady=5)

        ttk.Button(
            self.options_frame,
            text="🔄 Refrescar Opciones",
            bootstyle="info",
            command=self.refresh_options
        ).pack(fill=X, pady=10)

    def draw_destinations(self):
        self.map_widget.delete_all_marker()
        # Sucursales Hipermaxi (Pines Rojos)
        for name, coords in self.map_data.locations.items():
            if "Hipermaxi" in name:
                display_name = name.replace("Hipermaxi ", "HM ")
                self.map_widget.set_marker(coords[0], coords[1], text=display_name, marker_color_circle="white", marker_color_outside="#d32f2f")
        
        self.update_start_marker()

    def set_start_on_click(self, coords):
        self.start_coords = coords
        self.update_start_marker()
        self.start_info_label.configure(text=f"Lat: {coords[0]:.4f}, Lon: {coords[1]:.4f}", bootstyle="primary")
        self.log_message(f"Sistema: Inicio fijado en {coords[0]:.4f}, {coords[1]:.4f}")

    def update_start_marker(self):
        if self.start_marker:
            self.start_marker.delete()
        
        self.start_marker = self.map_widget.set_marker(
            self.start_coords[0], self.start_coords[1], 
            text="INICIO", 
            marker_color_outside="#1976D2" 
        )

    def log_message(self, message):
        self.after(0, lambda: self._append_log(message))

    def _append_log(self, message):
        self.log_text.insert(END, message + "\n")
        self.log_text.see(END)

    def draw_path_on_map(self, path_coords):
        if self.path_line:
            self.path_line.delete()
        
        if path_coords and len(path_coords) > 1:
            self.path_line = self.map_widget.set_path(path_coords, color="#4285F4", width=5)

    def update_agent_position(self, coords):
        self.after(0, lambda: self._move_marker_thread_safe(coords))

    def _move_marker_thread_safe(self, coords):
        # ARREGLO: Actualizar posición de marcador existente en lugar de borrar/crear
        if self.current_agent_marker:
            self.current_agent_marker.set_position(coords[0], coords[1])
        else:
            self.current_agent_marker = self.map_widget.set_marker(
                coords[0], coords[1], 
                text="Comprador", 
                marker_color_outside="#FBC02D" 
            )

    def start_simulation(self):
        self.clear_internal_map()
        self.internal_map_visible = False
        self.current_supermarket = None

        self.reset_right_panel()

        self.status_label.configure(
            text="CALCULANDO RUTA...",
            bootstyle="warning"
        )

        # 1. Validación de Entrada y Chequeos Lógicos
        MAX_AMOUNT = 20000.00
        
        try:
            amount_str = self.amount_entry.get().replace(',', '.') # Robustness
            amount = float(amount_str)
            
            # CASO: Monto Negativo
            if amount < 0:
                self.log_message("❌ Error: El monto no puede ser NEGATIVO.")
                self.status_label.configure(text="MONTO NEGATIVO", bootstyle="danger")
                return

            # CASO: Monto Cero
            if amount == 0:
                self.log_message("⚠️ Error: El monto debe ser MAYOR a 0.")
                self.status_label.configure(text="MONTO CERO", bootstyle="warning")
                return
            
            # CASO: Monto Excesivo
            if amount > MAX_AMOUNT:
                self.log_message(f"❌ Error: El monto excede el límite permitido ({MAX_AMOUNT} Bs).")
                self.status_label.configure(text="MONTO EXCESIVO", bootstyle="danger")
                return

            # CASO: Centavos Fraccionarios (Menos de 0.01)
            # Verificar si hay más de 2 decimales
            # Multiplicar por 100, redondear, restar -> debería ser cercano a 0
            if abs(amount * 100 - round(amount * 100)) > 0.001:
                self.log_message("⚠️ Error: Ingrese un monto con máximo 2 decimales (ej: 50.10).")
                self.status_label.configure(text="DECIMALES INVÁLIDOS", bootstyle="warning")
                return
            
            target = self.target_var.get()
            target_coords = self.map_data.get_coordinates(target)
            if not target_coords:
                self.log_message(f"Error: Coordenadas no encontradas para {target}")
                return

        except ValueError:
            self.log_message("❌ Error: Ingrese un número válido.")
            self.status_label.configure(text="MONTO INVÁLIDO", bootstyle="danger")
            return

        # 2. Iniciar Lógica si Validación Pasó
        self.start_btn.configure(state=DISABLED, text="Simulando...")
        self.log_text.delete(1.0, END)
        self.status_label.configure(text="CALCULANDO RUTA...", bootstyle="warning")
        
        if self.path_line: self.path_line.delete()
        
        if self.current_agent_marker: 
            self.current_agent_marker.delete()
            self.current_agent_marker = None

        thread = threading.Thread(target=self._run_logic, args=(self.start_coords, target, amount))
        thread.daemon = True
        thread.start()

    def _run_logic(self, start_coords, target_name, amount):
        try:
            self.current_supermarket = target_name

            target_coords = self.map_data.get_coordinates(target_name)
            
            path = self.shopper.planner.find_path(start_coords, target_coords)
            if path:
                self.after(0, lambda: self.draw_path_on_map(path))
            
            result, state = self.shopper.run_simulation(
                start_coords, target_name, amount,
                move_callback=self.update_agent_position
            )

            if state == "WAITING_SELECTION":
                self.after(0, lambda: self.show_optimizer_options(result))
                self.after(0, lambda: self.show_internal_map_fullscreen(target_name)) 
                return

            self.after(0, lambda: self._finalize_ui(result, state))
        
        except Exception as e:
            print(f"Logic Error: {e}")
            self.log_message(f"Error Crítico: {e}")
            self.after(0, lambda: self._reset_ui_state())

    def _reset_ui_state(self):
        self.start_btn.configure(state=NORMAL, text="▶ INICIAR SIMULACIÓN")
        self.status_label.configure(text="ERROR", bootstyle="danger")

    def open_inventory_window(self):
        inv_window = ttk.Toplevel(self)
        inv_window.title("Inventario de Productos")
        inv_window.geometry("700x600") # Un poco más ancho para la nueva columna
        
        # Título
        ttk.Label(inv_window, text="Estado de Stock", font=("Segoe UI", 14, "bold"), bootstyle="primary").pack(pady=10)
        
        # Tabla
        cols = ("prod", "price", "stock", "last_qty")
        tree = ttk.Treeview(inv_window, columns=cols, show="headings", height=20)
        
        tree.heading("prod", text="Producto")
        tree.column("prod", width=280, anchor=W)
        
        tree.heading("price", text="Precio")
        tree.column("price", width=80, anchor=E)
        
        tree.heading("stock", text="Stock")
        tree.column("stock", width=80, anchor=CENTER)

        tree.heading("last_qty", text="Últ. Compra")
        tree.column("last_qty", width=100, anchor=CENTER)
        
        # Scrollbar
        scroll = ttk.Scrollbar(inv_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        
        tree.pack(side=TOP, fill=BOTH, expand=YES, padx=10)
        scroll.place(relx=0.95, rely=0.1, relheight=0.8, anchor=NE)
        
        # Llenar datos con lógica mejorada
        def load_data():
            if not tree.winfo_exists(): return

            tree.delete(*tree.get_children())
            
            # Refinamiento: Productos comprados arriba (ordenados por cantidad desc), resto abajo (alfabético)
            purchased = [p for p in PRODUCTS if self.last_purchase_counts.get(p['name'], 0) > 0]
            others = [p for p in PRODUCTS if self.last_purchase_counts.get(p['name'], 0) == 0]
            
            purchased.sort(key=lambda x: self.last_purchase_counts.get(x['name'], 0), reverse=True)
            others.sort(key=lambda x: x['name'])
            
            final_list = purchased + others

            for p in final_list:
                name = p['name']
                price = p['price']
                stock = p.get('stock', 0)
                last_qty = self.last_purchase_counts.get(name, 0)
                
                last_qty_str = str(last_qty) if last_qty > 0 else "-"
                
                # Tags
                tags = []
                if last_qty > 0: tags.append("purchased")
                
                if stock == 0: tags.append("critical")
                elif stock < 10: tags.append("low")
                else: tags.append("normal") # default
                
                tree.insert("", END, values=(name, f"{price:.2f}", stock, last_qty_str), tags=tuple(tags))
            
            # Configuración de Colores
            tree.tag_configure("critical", foreground="#d32f2f") # Texto Rojo (Agotado)
            tree.tag_configure("low", foreground="#ef6c00") # Texto Naranja (Bajo)
            tree.tag_configure("normal", foreground="black")
            
            # Resaltado de compra (Fondo)
            tree.tag_configure("purchased", background="#c8e6c9") # Verde suave estilo Excel

        load_data()
        
        # Registrar callback para auto-refresh
        self.refresh_inventory_callback = load_data
        
        # Limpiar callback al cerrar
        def on_close():
            self.refresh_inventory_callback = None
            inv_window.destroy()
            
        inv_window.protocol("WM_DELETE_WINDOW", on_close)
        
        # Botones
        btn_frame = ttk.Frame(inv_window, padding=10)
        btn_frame.pack(fill=X, side=BOTTOM)
        
        def reset_stock_action():
            for p in PRODUCTS:
                p['stock'] = self.initial_stock.get(p['name'], 0)
            
            load_data()
            self.log_message("Sistema: Stock reseteado a valores originales.")
            
        ttk.Button(btn_frame, text="🔄 Refrescar", bootstyle="info", command=load_data).pack(side=LEFT, fill=X, expand=YES, padx=5)
        ttk.Button(btn_frame, text="⚙️ Resetear Stock", bootstyle="warning", command=reset_stock_action).pack(side=LEFT, fill=X, expand=YES, padx=5)
        ttk.Button(btn_frame, text="Cerrar", bootstyle="secondary", command=on_close).pack(side=RIGHT, fill=X, expand=YES, padx=5)


if __name__ == "__main__":
    app = AgentUI()
    app.mainloop()