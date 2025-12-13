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
        
        # Guardar stock inicial para reset
        self.initial_stock = {p['name']: p.get('stock', 0) for p in PRODUCTS}
        
        # Estado de última compra (para resaltar en inventario)
        self.last_purchase_counts = {}
        self.refresh_inventory_callback = None

        self._init_ui()

    def _init_ui(self):
        # Encabezado
        header = ttk.Frame(self, bootstyle="primary", padding=15)
        header.pack(fill=X)
        ttk.Label(header, text="🎄 Vale Navideño 🎄", 
                 font=("Segoe UI", 20, "bold"), bootstyle="inverse-primary").pack()

        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # --- PANEL IZQUIERDO ---
        left_panel = ttk.Labelframe(main_frame, text="Panel de Control", padding=15)
        left_panel.pack(side=LEFT, fill=Y, padx=10, ipadx=5)
        
        # Configuración
        config_frame = ttk.Labelframe(left_panel, text="Configuración", padding=15)
        config_frame.pack(fill=X, pady=10)

        ttk.Label(config_frame, text="Monto del Vale (Bs):", font=("Segoe UI", 10)).pack(anchor=W)
        self.amount_entry = ttk.Entry(config_frame)
        self.amount_entry.insert(0, "50.0")
        self.amount_entry.pack(fill=X, pady=(5, 15))
        
        ttk.Label(config_frame, text="Sucursal Destino (Meta):", font=("Segoe UI", 10)).pack(anchor=W)
        self.target_var = ttk.StringVar()
        branches = [k for k in self.map_data.locations.keys() if "Hipermaxi" in k]
        self.target_combo = ttk.Combobox(config_frame, textvariable=self.target_var, values=branches, state="readonly")
        if branches: self.target_combo.current(0)
        self.target_combo.pack(fill=X, pady=(5, 15))

        # Selección de Inicio
        ttk.Label(config_frame, text="Punto de Partida:", font=("Segoe UI", 10, "bold"), bootstyle="primary").pack(anchor=W)
        self.start_info_label = ttk.Label(config_frame, text="📍 Haz CLICK en el mapa para elegir", font=("Segoe UI", 9, "italic"), bootstyle="secondary")
        self.start_info_label.pack(anchor=W, pady=(5, 15))

        self.start_btn = ttk.Button(config_frame, text="▶ INICIAR SIMULACIÓN", command=self.start_simulation, bootstyle="success")
        self.start_btn.pack(fill=X, pady=5, ipady=5)

        self.inv_btn = ttk.Button(config_frame, text="📦 Ver Inventario", command=self.open_inventory_window, bootstyle="info-outline")
        self.inv_btn.pack(fill=X, pady=(0, 10))

        # Registros
        log_frame = ttk.Labelframe(left_panel, text="Registro (Logs)", padding=10)
        log_frame.pack(fill=BOTH, expand=YES, pady=5)
        
        self.log_text = ttk.Text(log_frame, height=20, width=35, font=("Consolas", 9), relief="flat")
        self.log_text.pack(fill=BOTH, expand=YES)


        # --- PANEL CENTRAL: MAPA REAL ---
        center_panel = ttk.Frame(main_frame)
        center_panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=10)
        
        # Vista de Mapa Tkinter
        self.map_widget = tkintermapview.TkinterMapView(center_panel, corner_radius=15, width=800, height=600)
        self.map_widget.pack(fill=BOTH, expand=YES)
        
        # USAR MOSAICOS ESTÁNDAR DE GOOGLE MAPS
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=es&x={x}&y={y}&z={z}")

        self.map_widget.set_position(-17.3938, -66.1570)
        self.map_widget.set_zoom(14)
        
        self.map_widget.add_left_click_map_command(self.set_start_on_click)

        # Dibujar Marcadores
        self.draw_destinations()
        self.update_start_marker()


        # --- PANEL DERECHO ---
        right_panel = ttk.Labelframe(main_frame, text="Factura / Recibo", padding=15)
        right_panel.pack(side=LEFT, fill=Y, padx=10, ipadx=5)
        
        columns = ("qty", "unit_price", "prod", "price")
        self.receipt_tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=20)
        
        self.receipt_tree.heading("qty", text="#")
        self.receipt_tree.column("qty", width=30, anchor=CENTER)

        self.receipt_tree.heading("unit_price", text="PU")
        self.receipt_tree.column("unit_price", width=60, anchor=E)

        self.receipt_tree.heading("prod", text="Producto")
        self.receipt_tree.column("prod", width=180, anchor=W)

        self.receipt_tree.heading("price", text="Bs")
        self.receipt_tree.column("price", width=80, anchor=E)
        
        self.receipt_tree.pack(fill=BOTH, expand=YES, pady=10)
        
        self.status_frame = ttk.Frame(right_panel, padding=10, bootstyle="light")
        self.status_frame.pack(fill=X, pady=10)
        self.status_label = ttk.Label(self.status_frame, text="ESPERANDO...", font=("Segoe UI", 14, "bold"), bootstyle="secondary", anchor=CENTER)
        self.status_label.pack(fill=X)

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
        self.receipt_tree.delete(*self.receipt_tree.get_children())
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
            target_coords = self.map_data.get_coordinates(target_name)
            
            path = self.shopper.planner.find_path(start_coords, target_coords)
            if path:
                self.after(0, lambda: self.draw_path_on_map(path))
            
            cart, success = self.shopper.run_simulation(start_coords, target_name, amount, move_callback=self.update_agent_position)
            
            self.after(0, lambda: self._finalize_ui(cart, success))
        except Exception as e:
            print(f"Logic Error: {e}")
            self.log_message(f"Error Crítico: {e}")
            self.after(0, lambda: self._reset_ui_state())

    def _reset_ui_state(self):
        self.start_btn.configure(state=NORMAL, text="▶ INICIAR SIMULACIÓN")
        self.status_label.configure(text="ERROR", bootstyle="danger")

    def _finalize_ui(self, cart, success):
        self.start_btn.configure(state=NORMAL, text="▶ INICIAR SIMULACIÓN")
        if cart:
            total = 0
            # Agrupar artículos por nombre
            cart_counter = Counter([item['name'] for item in cart])
            cart_prices = {item['name']: item['price'] for item in cart}
            
            for name, qty in cart_counter.items():
                unit_price = cart_prices[name]
                subtotal = unit_price * qty

                self.receipt_tree.insert(
                    "",
                    END,
                    values=(
                        f"{qty}",
                        f"{unit_price:.2f}",
                        name,
                        f"{subtotal:.2f}"
                    )
                )
                total += subtotal
                
            self.receipt_tree.insert("", END, values=("","", "TOTAL", f"{total:.2f}"))

            # Actualizar estado de última compra
            self.last_purchase_counts = cart_counter
            
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
            
            # Criterio de Ordenamiento:
            # 1. Productos comprados en la última vez (last_qty > 0) -> PRIMERO
            # 2. Stock agotado (stock == 0) -> DESPUÉS (para llamar la atención)
            # 3. Nombre alfabético
            
            def sort_key(p):
                name = p['name']
                last_qty = self.last_purchase_counts.get(name, 0)
                stock = p.get('stock', 0)
                
                # Tupla de ordenamiento (Mayor prioridad = menor valor de tupla para sort ascendente? No, queremos descendente en importancia)
                # Queremos: Comprados primero.
                # Python sort es estable.
                # Usaremos valores negativos para invertir el orden natural en campos numéricos si queremos descendente
                
                is_purchased = last_qty > 0
                is_out_of_stock = stock == 0
                
                # Prioridad 1: Comprado (True > False). Queremos True primero -> -1
                p1 = -1 if is_purchased else 0
                
                # Prioridad 2: Si NO comprado, agotados primero? O simplemente alfabético.
                # El usuario pidió "ordenarlos por orden" de lo comprado.
                
                return (p1, name) # Simple: Comprados arriba, luego alfabético

            sorted_products = sorted(PRODUCTS, key=sort_key)
            
            # También podemos hacer sort manual más específico si queremos que dentro de comprados se ordenen por cantidad
            # sorted_products.sort(key=lambda x: self.last_purchase_counts.get(x['name'], 0), reverse=True) 
            # Pero eso mezclaría nombres. Mejor mantenerlos agrupados arriba.
            
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
            # Prioridad de colores: Treeview usa la última configuración o la jerarquía? 
            # En Tkinter, el orden en tags define. "purchased" debe prevalecer si queremos que se vea verde.
            
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
            
            # Limpiar historial de "última compra" al resetear stock para evitar confusión?
            # O mantenerlo? Mejor mantenerlo, solo reseteamos stock.
            load_data()
            self.log_message("Sistema: Stock reseteado a valores originales.")
            
        ttk.Button(btn_frame, text="🔄 Refrescar", bootstyle="info", command=load_data).pack(side=LEFT, fill=X, expand=YES, padx=5)
        ttk.Button(btn_frame, text="⚙️ Resetear Stock", bootstyle="warning", command=reset_stock_action).pack(side=LEFT, fill=X, expand=YES, padx=5)
        ttk.Button(btn_frame, text="Cerrar", bootstyle="secondary", command=on_close).pack(side=RIGHT, fill=X, expand=YES, padx=5)

if __name__ == "__main__":
    app = AgentUI()
    app.mainloop()
