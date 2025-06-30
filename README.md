# Simulador de Gravedad N-Cuerpos

Un simulador de física N-cuerpos programado en Python, diseñado para modelar y visualizar sistemas gravitacionales complejos en tiempo real. Este proyecto utiliza `matplotlib` para la renderización gráfica y `Decimal` para cálculos de alta precisión, permitiendo la creación de escenarios cósmicos estables o caóticos con un gran número de objetos.


## Características Principales

  * **Motor de Física N-Cuerpos:** Calcula la interacción gravitatoria entre todos los cuerpos del sistema en cada paso de tiempo, actualizando sus velocidades y posiciones.
  * **Visualización en Tiempo Real:** Renderiza las órbitas y posiciones de los cuerpos celestes mediante `matplotlib`, permitiendo observar la evolución del sistema al instante.
  * **Alta Precisión Numérica:** Utiliza la librería `Decimal` de Python para minimizar los errores de redondeo en los cálculos, lo que es crucial para la estabilidad de las simulaciones a largo plazo.
  * **Optimización de Rendimiento:** Implementa una `Grid` de partición espacial para agrupar objetos distantes, reduciendo la complejidad de los cálculos y permitiendo simular eficientemente un gran número de cuerpos como asteroides.
  * **CLI Interactiva:** Incluye una interfaz de línea de comandos para configurar la simulación de forma detallada antes de ejecutarla.
  * **Configuración por Escenarios:** Permite cargar y guardar sistemas completos desde y hacia archivos `JSON`, facilitando la experimentación con diferentes condiciones iniciales.
  * **Generación Procedural:** Capacidad para generar cuerpos celestes de forma procedural, incluyendo cinturones de asteroides y de Kuiper con un número personalizable de objetos.

## Arquitectura del Proyecto

El simulador está organizado en varios módulos que separan las responsabilidades:

  * **`gravedad.py`**: El motor principal del proyecto. Contiene el bucle de simulación, la lógica de la física (clases `Universo`, `Fisica`, `Cuerpo`), la interfaz de comandos (CLI) y la gestión de la visualización con `matplotlib`.
  * **`vectores.py`**: Define las estructuras de datos fundamentales. Incluye la clase `Vector2` para operaciones matemáticas y la clase `Grid` para la optimización espacial.
  * **`funciones_extra.py`**: Un módulo de utilidades con funciones auxiliares para la validación de datos, la creación de archivos JSON y la estilización de la salida en consola.
  * **Archivos `.json`**: Archivos de datos que definen escenarios específicos, como nuestro sistema solar (`solar_sistem.json`), un sistema de tres estrellas (`sistema_3soles.json`) o cualquier otro sistema personalizado.

## Instalación

Para poder ejecutar el simulador, necesitas tener Python 3 y las siguientes librerías instaladas.

1.  Asegúrate de tener **Python 3.x** en tu sistema.
2.  Instala las dependencias necesarias usando pip:
    ```bash
    pip install numpy matplotlib
    ```

## Uso

1.  Navega a la carpeta del proyecto en tu terminal.
2.  Ejecuta el script principal:
    ```bash
    python gravedad.py
    ```
3.  Una vez iniciado, el programa te mostrará una interfaz de comandos (`>>>`). Usa los siguientes comandos para configurar tu simulación:

| Comando               | Descripción                                                                               | Ejemplo                                    |
| --------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------ |
| `load [archivo]`      | Carga un sistema desde un archivo JSON.                               | `load solar_sistem.json`                   |
| `save [archivo]`      | Guarda la configuración actual de los cuerpos en un archivo JSON.       | `save mi_sistema.json`                     |
| `add`                 | Inicia un asistente para añadir un nuevo cuerpo celeste manualmente.    | `add`                                      |
| `cuerpos see/delete`  | Muestra los cuerpos actuales o elimina uno por su tag.                  | `cuerpos delete qjnd9`                     |
| `G =/? [valor]`       | Modifica o consulta la constante de gravitación universal.              | `G = 6.6743e-11`                           |
| `size view/dots`      | Ajusta la escala de la vista o el tamaño de los puntos.                 | `size view 100e11;100e11`                  |
| `time.mode ...`       | Define el modo de tiempo (variable o uniforme).                         | `time.mode uniform 50000`                  |
| `solar_sistem ...`    | Añade cinturones de asteroides o de Kuiper.                             | `solar_sistem kuiper_belt 300`             |
| `active_save [ruta]`  | Activa el guardado de las posiciones en cada ciclo de la simulación.     | `active_save sim_data.json`                |
| `run`                 | Inicia la simulación con la configuración actual.                       | `run`                                      |
| `help`                | Muestra la lista de comandos disponibles.                               | `help`                                     |

4.  Una vez configurado, escribe `run` y presiona Enter para iniciar la visualización.

## Posibles Mejoras

Este proyecto tiene una base sólida con gran potencial de expansión. Algunas ideas para el futuro:

  * **Implementar la clase `Evento`:** Activar la clase `Evento` (actualmente sin uso) para simular sucesos programados como la aparición de cometas o supernovas.
  * **Detección de Colisiones:** Añadir lógica para detectar colisiones entre cuerpos, con posibles resultados como fusión o fragmentación.
  * **Interfaz Gráfica (GUI):** Reemplazar la CLI con una interfaz gráfica completa usando librerías como Tkinter, PyQt o Kivy para una experiencia más interactiva.
  * **Mejoras de Optimización:** Implementar un algoritmo Barnes-Hut más completo para mejorar aún más el rendimiento con una gran cantidad de cuerpos.

## Licencia

Este proyecto está distribuido bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
