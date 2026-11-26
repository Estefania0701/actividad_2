# Pruebas del sistema NEXUS Metro

## 1. Objetivo

Verificar el funcionamiento del sistema inteligente de búsqueda
de rutas, comprobando que pueda encontrar recorridos de menor
tiempo, considerar transbordos y validar las estaciones ingresadas.

## 2. Casos de prueba

### Prueba 1. Ruta directa

- Origen: Aurora
- Destino: Puerto Norte
- Resultado esperado: 21 minutos.
- Transbordos: 0.
- Estado: Aprobada.

### Prueba 2. Ruta con transbordos

- Origen: Aurora
- Destino: Colinas
- Resultado esperado: 38 minutos.
- Transbordos: 2.
- Estado: Aprobada.

Recorrido esperado:

Aurora -> Central Park -> Distrito Financiero ->
Plaza Mayor -> Museo -> Aeropuerto -> Colinas.

### Prueba 3. Mismo origen y destino

- Origen: Universidad
- Destino: Universidad
- Resultado esperado: 0 minutos.
- Transbordos: 0.
- Estado: Aprobada.

### Prueba 4. Estación inexistente

- Origen: Unknown Station
- Destino: Aurora
- Resultado esperado: Mensaje de error indicando
  que la estación no existe.
- Estado: Aprobada.

## 3. Conclusión

Las pruebas permiten verificar que el sistema utiliza
la base de conocimiento para identificar conexiones
entre estaciones y seleccionar recorridos según el
menor tiempo total de desplazamiento.

El algoritmo considera tanto los tiempos entre estaciones
como los costos adicionales de los transbordos.
