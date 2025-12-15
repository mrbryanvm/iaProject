# Arquitectura Actualizada del Sistema Multi-Agente

```mermaid
graph TD
    %% Roles y Actores
    User(Usuario)
    UI[Interfaz Gráfica - AgentUI]
    
    %% Agentes
    subgraph "Sistema Multi-Agente"
        Shopper[ShopperAgent - Orquestador]
        Planner[PlannerAgent - Utilidad OSRM]
        Optimizer[OptimizerAgent - Objetivos Greedy]
        Recolector[RecolectorAgent - Objetivos BFS]
        Cashier[CashierAgent - Reactivo Simple]
    end

    %% Datos y Servicios
    subgraph "Datos y Servicios"
        MapData[(Datos Mapa Geográfico)]
        InternalMaps[(Mapas Internos Supermercados)]
        Products[(Catálogo Productos + Stock)]
        OSRM(API OSRM)
    end

    %% Relaciones - Flujo Principal
    User -->|Define Monto y Destino| UI
    UI -->|Inicia Simulación| Shopper
    
    %% Fase 1: Planificación y Movimiento
    Shopper -->|Solicita Ruta Real| Planner
    Planner -->|Consulta HTTP| OSRM
    Planner -->|Retorna Ruta| Shopper
    Shopper -->|Se Mueve| MapData
    
    %% Fase 2: Optimización y Selección
    Shopper -->|Solicita Opciones de Compra| Optimizer
    Optimizer -->|Lee Datos| Products
    Optimizer -->|Retorna 3 Opciones| Shopper
    Shopper -->|Presenta Opciones| UI
    User -->|Selecciona Opción| UI
    
    %% Fase 3: Recolección
    UI -->|Confirma Selección| Shopper
    Shopper -->|Delega Recolección| Recolector
    Recolector -->|Lee Layout| InternalMaps
    Recolector -->|Planifica Ruta Interna BFS| Recolector
    Recolector -->|Recolecta Productos| Products
    Recolector -->|Retorna Carrito Físico| Shopper
    
    %% Fase 4: Pago
    Shopper -->|Valida Compra| Cashier
    Cashier -->|Retorna Recibo Final| Shopper
    Shopper -->|Actualiza UI| UI

    %% Estilos
    style Shopper fill:#ffecb3,stroke:#fbc02d,stroke-width:2px
    style Recolector fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style Optimizer fill:#e1bee7,stroke:#8e24aa,stroke-width:2px
    style Planner fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style Cashier fill:#ffccbc,stroke:#f4511e,stroke-width:2px
```

## Cambios Clave en la Arquitectura

1.  **Nuevo Agente (Recolector)**: Se encarga exclusivamente de la navegación interna y recolección física de productos, separando esta responsabilidad del Shopper o el Optimizador.
2.  **Interacción Humana (Selección)**: El flujo ya no es 100% automático; incluye una pausa para que el usuario elija entre opciones optimizadas, añadiendo un nivel de simulación de "preferencia humana".
3.  **Datos de Mapas Internos**: Nueva fuente de datos estructurada (`InternalMaps`) que permite la navegación BFS detallada sección por sección.
4.  **Optimización Diferida**: El Optimizador ahora genera múltiples escenarios potenciales en lugar de decidir uno solo, dando más poder de decisión al usuario (o simulando indecisión).
