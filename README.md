# NEXUS Metro - Buscador Inteligente de Rutas

## Descripción

NEXUS Metro es un sistema ficticio de transporte masivo ubicado en Nova City.

Este proyecto implementa un buscador inteligente de rutas utilizando una base de conocimiento basada en reglas lógicas y el algoritmo de Dijkstra para encontrar el camino más corto.

El sistema encuentra la ruta con el menor tiempo estimado de viaje, considerando las conexiones entre estaciones y el costo de tiempo asociado a los transbordos.

## Características

- Tres líneas de metro ficticias.
- Cuatro estaciones de transbordo.
- Representación mediante grafo ponderado.
- Reglas lógicas para las conexiones entre estaciones.
- Algoritmo de Dijkstra para la ruta más corta.
- Cálculo de tiempos de viaje y transbordo.
- Pruebas automatizadas con pytest.

## Requisitos

- Python 3.10 o superior.
- pip.

## Instalación

Clonar el repositorio:

    git clone <repository-url>

Ingresar al directorio del proyecto:

    cd actividad_2

Crear un entorno virtual:

    python -m venv .venv

Activarlo en Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

Instalar dependencias:

    python -m pip install -r requirements.txt

## Ejecución

Ejecutar la aplicación desde la raíz del proyecto:

    python -m src.main

Ingrese las estaciones de origen y destino cuando el sistema se lo solicite.

## Ejecución de pruebas

Ejecutar:

    python -m pytest -v

## Estructura del proyecto

- map/nexus_metro_map.py: Generación de imagen con mapa del sistema de transporte.
- src/knowledge_base.py: Base de conocimiento y reglas lógicas.
- src/route_engine.py: Construcción del grafo y algoritmo de búsqueda de rutas.
- src/main.py: Interfaz de usuario por consola.
- tests/test_routes.py: Pruebas automatizadas.
- docs/: Documentación del proyecto.
- assets/: Mapa del sistema de transporte.

## Algoritmo

El proyecto utiliza el algoritmo de Dijkstra para encontrar la ruta de menor costo.

El costo total incluye el tiempo de viaje entre estaciones consecutivas y el tiempo adicional correspondiente a los transbordos.
