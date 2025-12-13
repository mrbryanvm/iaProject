# MANUAL DE USUARIO: SISTEMA DE SIMULACIÓN "VALE NAVIDEÑO"

**Materia**: Inteligencia Artificial I  
**Versión del Documento**: 1.0  

---

## 1. Introducción

Este manual proporciona una guía detallada y minuciosa para la instalación, configuración y ejecución del **Sistema Multi-Agente de Simulación de Compras**. El software ha sido diseñado en lenguaje Python y utiliza tecnologías de mapeo en tiempo real para simular el comportamiento de agentes inteligentes en un entorno comercial realista (Supermercados Hipermaxi en Cochabamba).

El objetivo de este manual es permitir que cualquier usuario, con o sin experiencia previa profunda en Python, pueda replicar el entorno de desarrollo y ejecutar la simulación exitosamente.

---

## 2. Requisitos Previos del Sistema

Antes de iniciar la instalación, asegúrese de que su equipo cumpla con los siguientes requisitos mínimos:

### 2.1. Software Base
*   **Sistema Operativo**: Windows 10/11, macOS (Catalina o superior), o Linux (Ubuntu 20.04+).
*   **Python**: Versión 3.8 o superior (Se recomienda Python 3.12 para compatibilidad óptima).
*   **Git**: Herramienta de control de versiones para clonar el repositorio.

### 2.2. Hardware y Red
*   **Conexión a Internet**: **OBLIGATORIA** y estable. El sistema consume servicios de mapas (Google Maps Tiles) y enrutamiento (API OSRM) en tiempo real. Sin internet, la simulación no podrá calcular rutas.
*   **Memoria RAM**: Mínimo 4 GB (Recomendado 8 GB).

---

## 3. Instalación Paso a Paso

Siga estos pasos rigurosamente para preparar su entorno.

### Paso 1: Obtención del Código Fuente
Abra su terminal o consola de comandos (CMD/PowerShell en Windows) y ejecute el siguiente comando para descargar el proyecto:

```bash
git clone https://github.com/mrbryanvm/iaProject.git
```

Una vez finalizada la descarga, ingrese al directorio del proyecto:

```bash
cd iaProject
```

### Paso 2: Instalación de Dependencias
El proyecto depende de librerías externas para la interfaz gráfica y el manejo de mapas. Hemos facilitado un archivo `requirements.txt` que contiene todas las bibliotecas necesarias.

Ejecute el siguiente comando para instalar todo automáticamente:

```bash
pip install -r requirements.txt
```

**Desglose de lo que se instalará:**
*   `ttkbootstrap`: Proporciona una interfaz gráfica moderna y estilizada (Tema "Flatly").
*   `tkintermapview`: Módulo crucial para visualizar el mapa interactivo de Cochabamba.
*   `requests`: Permite al Agente Planificador comunicarse con el servidor de rutas OSRM.
*   `geocoder`: Utilidad para manejo de coordenadas geográficas.

---

## 4. Guía de Ejecución

Una vez instalado todo, está listo para iniciar el sistema.

### 4.1. Iniciar el Programa
En la terminal, dentro de la carpeta `iaProject`, ejecute:

```bash
python main.py
```

Debería abrirse una ventana titulada **"Vale Navideño"** con un mapa centrado en Cochabamba.

### 4.2. Interfaz de Usuario (Explicación Detallada)

La interfaz se divide en tres secciones principales:

#### A. Panel de Control (Izquierda)
*   **Monto del Vale (Bs)**: Campo de texto donde debe ingresar el valor exacto del vale (Ej: `50.0`, `100.0`, `2000.0`).
    *   *Nota*: El sistema valida que sea un número positivo y con máximo 2 decimales.
*   **Sucursal Destino**: Menú desplegable para elegir a qué supermercado Hipermaxi debe ir el agente.
    *   Opciones disponibles: El Prado, Juan de la Rosa, Circunvalación, Sacaba, Blanco Galindo, Panamericana, Torres Sofer.
*   **Botón INICIAR SIMULACIÓN**: Activa a los agentes. Se bloquea durante la simulación.
*   **Registro (Logs)**: Consola de texto que muestra en tiempo real "pensamientos" y acciones de los agentes (Traducidos al español).

#### B. Mapa Interactivo (Centro)
*   Muestra el entorno real.
*   **Pines Rojos**: Indican las sucursales de Hipermaxi disponibles.
*   **Pin Azul (INICIO)**: Usted debe hacer **CLIC IZQUIERDO** en cualquier lugar del mapa (calle o avenida) para definir dónde empieza el agente.
*   **Ruta Azul**: Trazo del camino real que seguirá el agente.
*   **Agente (Amarillo)**: Marcador móvil que simula el viaje del comprador.

#### C. Recibo / Factura (Derecha)
*   Tabla que se llenará automáticamente al final de la simulación con los productos comprados.
*   Columnas: Cantidad (`#`), Producto, Precio (`Bs`).
*   **Total**: Muestra la suma final, que debe coincidir exactamente con su vale.

---

## 5. Descripción de los Agentes (Para el Usuario)

Para entender qué sucede "tras bambalinas", aquí explicamos los roles de la Inteligencia Artificial:

### 🤖 El Comprador (Shopper)
Es el "jefe" de la misión. Recibe sus órdenes (monto y destino) y se encarga de llamar a los especialistas (Planificador y Optimizador) para cumplir la tarea. Es quien reporta el progreso en la consola de registros.

### 🗺️ El Planificador (Planner)
Es el experto en navegación. Cuando usted elige un punto de partida, este agente consulta satélites y mapas digitales (OSRM) para trazar la ruta más inteligente por las calles reales de Cochabamba, evitando atravesar edificios o volar en línea recta.

### 🧠 El Optimizador (Optimizer)
Es el genio matemático. Su trabajo es el más difícil: tomar el catálogo de más de 400 productos y encontrar una combinación única que sume **EXACTAMENTE** el monto de su vale.
*   *Curiosidad*: Si el monto es muy alto (ej. 20,000 Bs), verá que este agente decide comprar packs grandes de productos (ej. 11 botellas de Whisky o Electrodomésticos) para llenar el cupo rápidamente.

### 🏪 El Cajero (Cashier)
Es el auditor. Al final, verifica centavo por centavo. Si sobra o falta dinero del vale, rechazará la compra (aunque nuestros agentes están diseñados para nunca fallar).

---

## 6. Solución de Problemas Comunes

*   **Error: "Coordenadas no encontradas"**: Asegúrese de seleccionar una sucursal válida del menú.
*   **El mapa no carga**: Verifique su conexión a internet. El mapa necesita descargar imágenes en vivo.
*   **El agente no se mueve**: Si la ruta es extremadamente larga o compleja, el servicio OSRM puede tardar unos segundos en responder. Observe el registro de logs.

---
**Desarrollado por**: Grupo de IA I - Gestión 2-2025
*UMSS - Cochabamba, Bolivia*
