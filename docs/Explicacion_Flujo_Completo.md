# Explicación del Flujo de Ejecución - Sistema Multi-Agente "Vale Navideño"

## Resumen Ejecutivo
El sistema simula el proceso completo de compra utilizando 5 agentes especializados que trabajan en secuencia. Cada agente tiene un rol específico y utiliza algoritmos de Inteligencia Artificial para resolver su tarea.

---

## Flujo Cronológico Detallado

### **FASE 1: INICIALIZACIÓN Y PLANIFICACIÓN DE RUTA**

#### 🤖 **Agente: ShopperAgent (Orquestador)**
**Momento en el log:**
```
--- Simulación Iniciada ---
Inicio: -17.3938, -66.1570
Meta: Hipermaxi Torres Sofer (5.0 Bs)
```

**Función:**
- Coordina todo el proceso (es el "jefe").
- Recibe la configuración del usuario: punto de partida, destino y monto del vale.
- Delega tareas a los demás agentes según sea necesario.

**Tipo:** Agente Basado en Objetivos  
**Algoritmo:** Ninguno (coordinación pura)

---

#### 🗺️ **Agente: PlannerAgent (Planificador de Rutas)**
**Momento en el log:**
```
Comprador: Solicitando ruta real a OSRM... (Por favor espere)
Planificador: Ruta real encontrada con 83 puntos de paso.
```

**Función:**
- Calcula la ruta más corta desde el punto de partida hasta el supermercado.
- Usa coordenadas GPS reales y calles de Cochabamba.

**Tipo:** Agente Basado en Utilidad  
**Algoritmo:** **Dijkstra/A*** (ejecutado externamente por OSRM API)

**Explicación técnica:**
- OSRM (Open Source Routing Machine) es un servicio web especializado en cálculo de rutas.
- El agente envía una petición HTTP con las coordenadas de origen y destino.
- OSRM retorna una lista de 83 puntos GPS que forman la ruta óptima.

---

### **FASE 2: MOVIMIENTO Y LLEGADA AL SUPERMERCADO**

#### 🤖 **Agente: ShopperAgent (Visualización del Movimiento)**
**Momento en el log:**
```
Comprador: Moviéndose a lo largo de la ruta...
Comprador: Llegada a Hipermaxi Torres Sofer
```

**Función:**
- Simula el movimiento del agente por la ciudad.
- Actualiza el marcador en el mapa de la UI punto por punto.

**Nota:** No hay algoritmo aquí, solo animación visual.

---

### **FASE 3: OPTIMIZACIÓN Y SELECCIÓN DE PRODUCTOS**

#### 🧠 **Agente: OptimizerAgent (Optimizador)**
**Momento en el log:**
```
Comprador: Seleccionando productos...
```

**Función:**
- Genera **3 opciones diferentes** de carritos de compra.
- Cada opción suma exactamente el monto del vale (5.0 Bs en este caso).
- Combina productos de forma inteligente para evitar desperdiciar dinero.

**Tipo:** Agente Basado en Objetivos  
**Algoritmo:** **Greedy Aleatorizado + Change Making (Cambio de Moneda)**

**Explicación técnica:**
1. **Fase Greedy**: Selecciona productos caros aleatoriamente para llenar la mayor parte del vale.
2. **Fase Change Making**: Llena la brecha final con productos baratos (≤2 Bs) usando un algoritmo codicioso similar al problema clásico de dar cambio con monedas.

**Ejemplo de la opción elegida:**
- Chicle Doble: 1.0 Bs
- Chocolate Snickers: 4.0 Bs
- **Total: 5.0 Bs** ✅

---

#### 👤 **Interacción Humana (Usuario)**
**Momento en el log:**
```
Usuario eligió una opción de compra.
```

**Función:**
- El sistema presenta 3 opciones en la interfaz gráfica.
- El usuario selecciona cuál prefiere (simulando preferencias humanas).
- **Esto NO es un agente**, es el criterio de pausa donde el humano toma la decisión.

---

### **FASE 4: RECOLECCIÓN FÍSICA DE PRODUCTOS**

#### 🛒 **Agente: RecolectorAgent (Recolector)**
**Momento en el log:**
```
Comprador: Opción confirmada.
Recolector: Iniciando recorrido interno...
Recolector: Recolectando productos en Hipermaxi Torres Sofer
Secciones objetivo: {'Snacks y Golosinas'}
Ruta planificada: ['Entrada', 'Frutas', 'Carnes y Embutidos', ...]
```

**Función:**
- Navega por el interior del supermercado sección por sección.
- Planifica la ruta más corta para visitar todas las secciones necesarias.
- Recolecta los productos físicamente.

**Tipo:** Agente Basado en Objetivos  
**Algoritmo:** **BFS (Breadth-First Search - Búsqueda en Anchura)**

**Explicación técnica:**

1. **Agrupación Inteligente:**
   - Analiza qué productos necesita (Chicle y Chocolate).
   - Detecta que ambos están en la sección "Snacks y Golosinas".
   - Agrupa: "Debo ir a esta sección y recoger ambos ahí".

2. **Planificación de Ruta con BFS:**
   - El supermercado es un **grafo** donde:
     - **Nodos** = Secciones (Entrada, Frutas, Lácteos, Caja, etc.)
     - **Aristas** = Conexiones permitidas entre secciones (pasillos).
   - BFS calcula el camino más corto desde "Entrada" → "Snacks y Golosinas" → "Caja".
   - La ruta tiene 20 pasos totales.

3. **Ejecución del Recorrido:**
   - Se mueve de sección en sección.
   - Al llegar a "Snacks y Golosinas", recolecta:
     ```
     Recolectado: Chicle Doble (1.0 Bs)
     Recolectado: Chocolate Snickers (4.0 Bs)
     ```
   - Continúa hasta la Caja.

**¿Por qué pasa por 20 secciones si solo necesita 1?**
- BFS garantiza el camino **más corto**, pero el grafo del supermercado tiene una topología lineal (tipo "serpiente").
- No puede "teletransportarse" a Snacks y Golosinas; debe recorrer secciones intermedias.

---

### **FASE 5: VALIDACIÓN Y PAGO**

#### 💵 **Agente: CashierAgent (Cajero)**
**Momento en el log:**
```
Comprador: Pagando en caja...
Cajero: ¡Pago Aceptado! Total: 5.00
```

**Función:**
- Valida que el total del carrito coincida exactamente con el monto del vale.
- Simula al cajero humano que verifica el pago.

**Tipo:** Agente Reactivo Simple  
**Algoritmo:** Ninguno (regla simple: `if total == vale: aprobar`)

**Lógica:**
```python
if total == voucher_amount:
    return True, total  # ✅ Pago aceptado
else:
    return False, total  # ❌ Pago rechazado
```

---

## Resumen Visual del Flujo

```
┌─────────────────────────────────────────────────────────┐
│  USUARIO define: Origen, Destino, Monto               │
└────────────────┬────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────┐
│  🤖 SHOPPER coordina todo el proceso                   │
└────────────────┬────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────┐
│  🗺️ PLANNER calcula ruta con Dijkstra (OSRM)          │
│  Resultado: 83 puntos GPS                              │
└────────────────┬────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────┐
│  🚶 SHOPPER se mueve por la ciudad (animación)          │
└────────────────┬────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────┐
│  🧠 OPTIMIZER genera 3 opciones (Greedy + Change)      │
│  Opción 1: [Chicle 1Bs + Snickers 4Bs]                │
│  Opción 2: [Pan 0.5Bs + Leche 2Bs + Jabón 2.5Bs]      │
│  Opción 3: [Arroz 3Bs + Sal 0.5Bs + Azúcar 1.5Bs]     │
└────────────────┬────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────┐
│  👤 USUARIO elige una opción (Opción 1)                │
└────────────────┬────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────┐
│  🛒 RECOLECTOR navega con BFS                          │
│  Entrada → Snacks → Caja (20 secciones)               │
│  Recolecta: Chicle y Snickers                          │
└────────────────┬────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────┐
│  💵 CAJERO valida total = vale                         │
│  5.0 Bs = 5.0 Bs ✅ APROBADO                           │
└─────────────────────────────────────────────────────────┘
```

---

## Algoritmos de IA Aplicados (Resumen)

| Agente | Algoritmo | Tipo de Búsqueda | Complejidad |
|--------|-----------|------------------|-------------|
| PlannerAgent | Dijkstra/A* | Informada | O(E + V log V) |
| OptimizerAgent | Greedy + Change Making | No informada | O(n × m) |
| RecolectorAgent | BFS | No informada | O(V + E) |

**Leyenda:**
- V = Nodos (vértices)
- E = Aristas (conexiones)
- n = Número de productos
- m = Cantidad de intentos

---

## Conclusión para el Informe

Este sistema demuestra:
1. **Coordinación Multi-Agente**: Cada agente tiene una responsabilidad específica y bien definida.
2. **Aplicación Práctica de Algoritmos de IA**: Dijkstra para rutas urbanas, BFS para navegación interna, Greedy para optimización.
3. **Integración Humano-Agente**: El sistema permite intervención humana en el proceso de decisión (selección de opciones).
4. **Simulación Realista**: No solo calcula matemáticamente, sino que simula el movimiento físico y la recolección de productos.

**Énfasis en Planificación:**
- El sistema tiene **2 niveles de planificación**:
  1. **Macro**: Ruta urbana (PlannerAgent con Dijkstra).
  2. **Micro**: Ruta interna del supermercado (RecolectorAgent con BFS).
- Ambos usan algoritmos de búsqueda de caminos óptimos, cumpliendo con el requisito académico de "énfasis en la planificación".
