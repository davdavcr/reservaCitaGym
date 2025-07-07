## reservaCitaGym: Sistema de Reservas de Clases de Gimnasio

**Descripción**

Este es un proyecto sencillo diseñado para la gestión de reservas de clases en un gimnasio, con un enfoque principal en la base de datos.

### Tipos de Usuarios y Acceso

El sistema cuenta con tres tipos de usuarios:

  * **Administrador**: Usuario especial con acceso a la ruta `/admin`.
      * **Usuario**: `adminp2024`
      * **Contraseña**: `123456`
  * **Empleados**: Pueden añadir usuarios y clases (junto con sus cupos).
  * **Usuarios**: Pueden iniciar sesión, ver las clases disponibles por fecha y reservar su espacio en una clase, siempre y cuando haya cupos disponibles.

**Nota**: Este proyecto no cuenta con protocolos avanzados de seguridad, pues se enfoca en la base de datos. Se agregarán medidas de seguridad en caso de que se decida vender el programa.

### Instalación y Configuración

#### 1\. Clonar el Repositorio

```bash
git clone https://github.com/davdavcr/reservaCitaGym.git
cd reservaCitaGym
```

#### 2\. Crear y Activar Entorno Virtual (Python)

Este proyecto usa Python, y el entorno virtual está nombrado como `venv`.

  * **En Windows**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
  * **En Linux/macOS**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

#### 3\. Instalar Dependencias

Si existe un archivo `requirements.txt`, instalar las dependencias con:

```bash
pip install -r requirements.txt
```

**Importante**: En caso de que el proyecto use Django o un framework web similar, cambiar las extensiones `.django` a `.html` o adecuar las rutas en el front-end para que funcionen correctamente.

#### 4\. Configuración de la Base de Datos

Este proyecto está pensado para usar **SQL Server**. Para que funcione correctamente, en el archivo `data_access.py` se debe modificar la cadena de conexión con los datos específicos de tu computadora:

```python
class DataAccess:
    def __init__(self):
        self.connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=TU_SERVIDOR;'  # Cambiar 'TU_SERVIDOR' por el nombre o IP de tu servidor SQL
            'DATABASE=proyecto_gym;'
            'UID=TU_USUARIO;'      # Cambiar 'TU_USUARIO' por tu usuario de SQL Server
            'PWD=TU_CONTRASEÑA;'   # Cambiar 'TU_CONTRASEÑA' por tu contraseña de SQL Server
        )
```

### Estructura del Proyecto

  * `__init__.py`: Inicializa el paquete o módulo principal de la aplicación.
  * `routes.py`: Define las rutas o *endpoints* de la aplicación, controlando el flujo entre las vistas y la lógica de negocio.
  * `business.py`: Contiene la lógica de negocio, procesando datos y coordinando las operaciones entre la base de datos y la interfaz.
  * `data_access.py`: Maneja las funciones relacionadas con la conexión y consultas a la base de datos SQL Server, usando procedimientos almacenados, *triggers* y validaciones.
  * `entities.py`: Define las entidades o modelos de datos en Python que representan las tablas de la base de datos.
  * `run.py`: Archivo principal para iniciar la aplicación.
  * `static/`: Carpeta que contiene los recursos estáticos:
      * `css/`: Archivos de estilos.
      * `js/`: Archivos de JavaScript.

### Base de Datos

El sistema usa una base de datos SQL Server llamada `proyecto_gym` que contiene tablas para gimnasios, usuarios, clases y las inscripciones a clases.

#### Características Importantes

  * **Uso de procedimientos almacenados**: Para operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en todas las entidades.
  * **Implementación de *triggers***: Para mantener integridad referencial y validar datos (ejemplo: evitar usuarios duplicados, controlar cupos de clases, eliminar en cascada datos relacionados).
  * **Validaciones como**:
      * Formato específico para los nombres de usuario.
      * Prevención de duplicados en gimnasios, usuarios y cédulas.
      * Control de cupos en clases y control de inscripciones duplicadas.

El script completo de la base de datos está incluido en la documentación del proyecto o en el archivo `script_bd.sql`.

### Uso

1.  **Iniciar la base de datos**: Ejecutando el script SQL para crear las tablas, procedimientos y *triggers*.
2.  **Configurar la cadena de conexión**: En `data_access.py`.
3.  **Ejecutar la aplicación**:
    ```bash
    python run.py
    ```
4.  **Acceder a la aplicación**: En el navegador.
5.  **Acceder al panel administrativo**: Usar la ruta `/admin` con el usuario y contraseña indicados arriba.

### Autores

  * David Arturo Brenes Angulo
  * Andrés Solano Contreras
  * Andrey Aguilar Aguirre
