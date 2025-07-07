# reservaCitaGym

## Descripción

Este es un proyecto sencillo para la gestión de reservas de clases en un gimnasio, con enfoque principal en la base de datos. El sistema cuenta con tres tipos de usuarios:

- **Administrador:** Usuario especial con acceso a la ruta `/admin`.  
  - Usuario: `adminp2024`  
  - Contraseña: `123456`  
- **Empleados:** Añaden usuarios y clases (junto con sus cupos).  
- **Usuarios:** Pueden iniciar sesión, ver las clases disponibles por fecha y reservar su espacio en una clase, siempre y cuando haya cupos disponibles.

> **Nota:** Este proyecto no cuenta con protocolos avanzados de seguridad, pues se enfoca en la base de datos. Se agregarán medidas de seguridad en caso de que se decida vender el programa.

---

## Instalación y configuración

### Clonar el repositorio

```bash
git clone https://github.com/davdavcr/reservaCitaGym.git
cd reservaCitaGym

Crear y activar entorno virtual (Python)
Este proyecto usa Python, y el entorno virtual está nombrado como venv.

En Windows:
python -m venv venv
.\venv\Scripts\activate

En Linux/macOS:
python3 -m venv venv
source venv/bin/activate

Instalar dependencias
Si existe un archivo requirements.txt, instalar las dependencias con:
pip install -r requirements.txt

Importante: En caso de que el proyecto use Django o un framework web similar, cambiar las extensiones .django a .html o adecuar las rutas en el front-end para que funcionen correctamente.

Configuración de la base de datos
Este proyecto está pensado para usar SQL Server. Para que funcione correctamente, en el archivo data_access.py se debe modificar la cadena de conexión con los datos específicos de tu computadora:

class DataAccess:
    def __init__(self):
        self.connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=TU_SERVIDOR;'  # Cambiar 'TU_SERVIDOR' por el nombre o IP de tu servidor SQL
            'DATABASE=proyecto_gym;'
            'UID=TU_USUARIO;'      # Cambiar 'TU_USUARIO' por tu usuario de SQL Server
            'PWD=TU_CONTRASEÑA;'   # Cambiar 'TU_CONTRASEÑA' por tu contraseña de SQL Server
        )

Estructura del proyecto
__init__.py: Inicializa el paquete o módulo principal de la aplicación.

routes.py: Define las rutas o endpoints de la aplicación, controlando el flujo entre las vistas y la lógica de negocio.

business.py: Contiene la lógica de negocio, procesando datos y coordinando las operaciones entre la base de datos y la interfaz.

data_access.py: Maneja las funciones relacionadas con la conexión y consultas a la base de datos SQL Server, usando procedimientos almacenados, triggers y validaciones.

entities.py: Define las entidades o modelos de datos en Python que representan las tablas de la base de datos.

run.py: Archivo principal para iniciar la aplicación.

static/: Carpeta que contiene los recursos estáticos:

css/: Archivos de estilos.

js/: Archivos de JavaScript.

Base de datos
El sistema usa una base de datos SQL Server llamada proyecto_gym que contiene tablas para gimnasios, usuarios, clases y las inscripciones a clases.

Características importantes
Uso de procedimientos almacenados para operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en todas las entidades.

Implementación de triggers para mantener integridad referencial y validar datos (ejemplo: evitar usuarios duplicados, controlar cupos de clases, eliminar en cascada datos relacionados).

Validaciones como:

Formato específico para los nombres de usuario.

Prevención de duplicados en gimnasios, usuarios y cédulas.

Control de cupos en clases y control de inscripciones duplicadas.

El script completo de la base de datos está incluido en la documentación del proyecto o en el archivo script_bd.sql.

Uso
Iniciar la base de datos ejecutando el script SQL para crear las tablas, procedimientos y triggers.

Configurar la cadena de conexión en data_access.py.

Ejecutar la aplicación con:
python run.py

Acceder a la aplicación en el navegador.

Para acceder al panel administrativo, usar la ruta /admin con el usuario y contraseña indicados arriba.

Autores
David Arturo Brenes Angulo

Andrés Solano Contreras

Andrey Aguilar Aguirre



