"""
Modern GUI for the Multi-Agent System using ttkbootstrap and tkintermapview.
Interactive Real Map of Cochabamba with Street Routing (OSRM).
Includes Fix for Marker Trails and Robust Input Validation.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import tkintermapview
from agents.shopper import ShopperAgent
from data.map_data import MapData
from collections import Counter

class AgentUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly") 
        self.title("Vale Navideño")
        self.geometry("1400x900")
        
        self.map_data = MapData()
        self.shopper = ShopperAgent(log_callback=self.log_message)
        
        # State
        self.start_coords = (-17.3938, -66.1570)
        self.current_agent_marker = None
        self.start_marker = None
        self.path_line = None
        
        self._init_ui()

    def _init_ui(self):
        # Header 
        header = ttk.Frame(self, bootstyle="primary", padding=15)
        header.pack(fill=X)
        ttk.Label(header, text="🎄 Vale Navideño 🎄", 
                 font=("Segoe UI", 20, "bold"), bootstyle="inverse-primary").pack()

        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # --- LEFT PANEL ---
        left_panel = ttk.Labelframe(main_frame, text="Panel de Control", padding=15)
        left_panel.pack(side=LEFT, fill=Y, padx=10, ipadx=5)
        
        # Config
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

        # Start Selection
        ttk.Label(config_frame, text="Punto de Partida:", font=("Segoe UI", 10, "bold"), bootstyle="primary").pack(anchor=W)
        self.start_info_label = ttk.Label(config_frame, text="📍 Haz CLICK en el mapa para elegir", font=("Segoe UI", 9, "italic"), bootstyle="secondary")
        self.start_info_label.pack(anchor=W, pady=(5, 15))

        self.start_btn = ttk.Button(config_frame, text="▶ INICIAR SIMULACIÓN", command=self.start_simulation, bootstyle="success")
        self.start_btn.pack(fill=X, pady=10, ipady=5)

        # Logs
        log_frame = ttk.Labelframe(left_panel, text="Registro (Logs)", padding=10)
        log_frame.pack(fill=BOTH, expand=YES, pady=5)
        
        self.log_text = ttk.Text(log_frame, height=20, width=35, font=("Consolas", 9), relief="flat")
        self.log_text.pack(fill=BOTH, expand=YES)


        # --- CENTER PANEL: REAL MAP ---
        center_panel = ttk.Frame(main_frame)
        center_panel.pack(side=LEFT, fill=BOTH, expand=YES, padx=10)
        
        # TkinterMapView
        self.map_widget = tkintermapview.TkinterMapView(center_panel, corner_radius=15, width=800, height=600)
        self.map_widget.pack(fill=BOTH, expand=YES)
        
        # USE GOOGLE MAPS STANDARD TILES
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=es&x={x}&y={y}&z={z}")

        self.map_widget.set_position(-17.3938, -66.1570)
        self.map_widget.set_zoom(14)
        
        self.map_widget.add_left_click_map_command(self.set_start_on_click)

        # Draw Markers
        self.draw_destinations()
        self.update_start_marker()


        # --- RIGHT PANEL ---
        right_panel = ttk.Labelframe(main_frame, text="Factura / Recibo", padding=15)
        right_panel.pack(side=LEFT, fill=Y, padx=10, ipadx=5)
        
        columns = ("qty", "prod", "price")
        self.receipt_tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=20)
        
        self.receipt_tree.heading("qty", text="#")
        self.receipt_tree.column("qty", width=30, anchor=CENTER)
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
        # Hipermaxi Branches (Red Pins)
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
        # FIX: Update existing marker position instead of deleting/creating
        if self.current_agent_marker:
            self.current_agent_marker.set_position(coords[0], coords[1])
        else:
            self.current_agent_marker = self.map_widget.set_marker(
                coords[0], coords[1], 
                text="Shopper", 
                marker_color_outside="#FBC02D" 
            )

    def start_simulation(self):
        # 1. Input Validation and Logic Checks
        MAX_AMOUNT = 20000.00
        
        try:
            amount_str = self.amount_entry.get().replace(',', '.') # Robustness
            amount = float(amount_str)
            
            # CASE: Negative Amount
            if amount < 0:
                self.log_message("❌ Error: El monto no puede ser NEGATIVO.")
                self.status_label.configure(text="MONTO NEGATIVO", bootstyle="danger")
                return

            # CASE: Zero Amount
            if amount == 0:
                self.log_message("⚠️ Error: El monto debe ser MAYOR a 0.")
                self.status_label.configure(text="MONTO CERO", bootstyle="warning")
                return
            
            # CASE: Excessive Amount
            if amount > MAX_AMOUNT:
                self.log_message(f"❌ Error: El monto excede el límite permitido ({MAX_AMOUNT} Bs).")
                self.status_label.configure(text="MONTO EXCESIVO", bootstyle="danger")
                return

            # CASE: Fractional Pennies (Less than 0.01)
            # Check if there are more than 2 decimal places
            # Multiply by 100, round, subtract -> should be near 0
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

        # 2. Start Logic if Validation Passed
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
            self.log_message(f"Critical Error: {e}")
            self.after(0, lambda: self._reset_ui_state())

    def _reset_ui_state(self):
        self.start_btn.configure(state=NORMAL, text="▶ INICIAR SIMULACIÓN")
        self.status_label.configure(text="ERROR", bootstyle="danger")

    def _finalize_ui(self, cart, success):
        self.start_btn.configure(state=NORMAL, text="▶ INICIAR SIMULACIÓN")
        if cart:
            total = 0
            # Group items by name
            cart_counter = Counter([item['name'] for item in cart])
            cart_prices = {item['name']: item['price'] for item in cart}
            
            for name, qty in cart_counter.items():
                unit_price = cart_prices[name]
                subtotal = unit_price * qty
                self.receipt_tree.insert("", END, values=(f"{qty}", name, f"{subtotal:.2f}"))
                total += subtotal
                
            self.receipt_tree.insert("", END, values=("", "TOTAL", f"{total:.2f}"))

        if success:
            self.status_label.configure(text="¡ÉXITO!", bootstyle="success")
        else:
            self.status_label.configure(text="FALLÓ", bootstyle="danger")

if __name__ == "__main__":
    app = AgentUI()
    app.mainloop()
