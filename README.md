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

### Script de la Base de Datos (SSMS se usa el usuario sa)

```sql
create database proyecto_gym

use proyecto_gym

CREATE TABLE gyms (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    password NVARCHAR(255) NOT NULL
);

CREATE TRIGGER trg_PreventDuplicateGymName
ON gyms
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    
    IF EXISTS (
        SELECT 1 
        FROM gyms 
        WHERE name = (SELECT name FROM inserted)
    )
    BEGIN
        
        RAISERROR('El gimnasio con este nombre ya existe.', 16, 1);
        RETURN;
    END

    INSERT INTO gyms (name, password)
    SELECT name, password
    FROM inserted;
END;
GO


CREATE PROCEDURE SaveGym
    @Name NVARCHAR(255),
    @Password NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO gyms (name, password)
    VALUES (@Name, @Password);
    SELECT SCOPE_IDENTITY() AS gym_id;
END;
GO


CREATE PROCEDURE GetAllGyms
AS
BEGIN
    SET NOCOUNT ON;

    SELECT id, name, password
    FROM gyms;
END;
GO


CREATE PROCEDURE GetGymById
    @GymId INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT id, name, password
    FROM gyms
    WHERE id = @GymId;
END;
GO


CREATE PROCEDURE UpdateGym
    @GymId INT,
    @Name NVARCHAR(255),
    @Password NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE gyms
    SET name = @Name, password = @Password
    WHERE id = @GymId;
END;
GO


CREATE PROCEDURE DeleteGym
    @GymId INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM gyms
    WHERE id = @GymId;
END;
GO


CREATE PROCEDURE GetGymByName
    @Name NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT id, name, password
    FROM gyms
    WHERE name = @Name;
END;
GO


__________________________________________________________________________________________________________________________________________________________________________

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(255) NOT NULL,
    password NVARCHAR(255) NOT NULL,
    cedula VARCHAR(50) NOT NULL,
    gym_id INT NOT NULL
);


CREATE TRIGGER TR_DeleteUsersOnGymDelete
ON gyms
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM users
    WHERE gym_id IN (SELECT id FROM DELETED);
END;
GO




CREATE TRIGGER trg_ValidateUsernameFormat
ON users
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Validar formato del username
    IF EXISTS (
        SELECT 1
        FROM inserted i
        INNER JOIN gyms g ON i.gym_id = g.id
        WHERE i.username NOT LIKE LOWER(g.name) + '%[0-9]%'
    )
    BEGIN
        RAISERROR('El formato del username no es válido. Debe ser: nombre del gimnasio (en minúsculas) seguido de un número.', 16, 1);
        RETURN;
    END

    -- Validar que no se repita el username
    IF EXISTS (
        SELECT 1
        FROM users u
        INNER JOIN inserted i ON u.username = i.username
    )
    BEGIN
        RAISERROR('El username ya existe en el sistema. Por favor, elija uno diferente.', 16, 1);
        RETURN;
    END

    -- Validar que no se repita la cédula
    IF EXISTS (
        SELECT 1
        FROM users u
        INNER JOIN inserted i ON u.cedula = i.cedula
    )
    BEGIN
        RAISERROR('La cédula ya está registrada en el sistema. Por favor, verifique.', 16, 1);
        RETURN;
    END

    -- Si todas las validaciones pasan, proceder con la inserción
    INSERT INTO users (username, password, cedula, gym_id)
    SELECT username, password, cedula, gym_id
    FROM inserted;
END;
GO




CREATE TRIGGER trg_ValidateUserUpdate
ON users
INSTEAD OF UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Validar que el username cumple el formato
    IF EXISTS (
        SELECT 1
        FROM inserted i
        INNER JOIN gyms g ON i.gym_id = g.id
        WHERE i.username NOT LIKE LOWER(g.name) + '%[0-9]%'
    )
    BEGIN
        RAISERROR('El formato del username no es válido. Debe ser: nombre del gimnasio (en minúsculas) seguido de un número.', 16, 1);
        RETURN;
    END

    -- Validar que el username no se repita
    IF EXISTS (
        SELECT 1
        FROM inserted i
        WHERE EXISTS (
            SELECT 1
            FROM users u
            WHERE u.username = i.username
            AND u.id != i.id  -- Excluir el registro que se está actualizando
        )
    )
    BEGIN
        RAISERROR('El username ya existe. Debe ser único.', 16, 1);
        RETURN;
    END

    -- Validar que la cédula no se repita
    IF EXISTS (
        SELECT 1
        FROM inserted i
        WHERE EXISTS (
            SELECT 1
            FROM users u
            WHERE u.cedula = i.cedula
            AND u.id != i.id  -- Excluir el registro que se está actualizando
        )
    )
    BEGIN
        RAISERROR('La cédula ya existe. Debe ser única.', 16, 1);
        RETURN;
    END

    -- Si todas las validaciones pasan, proceder con la actualización
    UPDATE users
    SET 
        username = i.username,
        password = i.password,
        cedula = i.cedula,
        gym_id = i.gym_id
    FROM inserted i
    WHERE users.id = i.id;
END;
GO




CREATE PROCEDURE SaveUser
    @Username NVARCHAR(255),
    @Password NVARCHAR(255),
    @Cedula VARCHAR(50),
    @GymID INT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO users (username, password, cedula, gym_id)
    VALUES (@Username, @Password, @Cedula, @GymID);

    SELECT SCOPE_IDENTITY() AS user_id; 
END;
GO


CREATE PROCEDURE GetAllUsers
    @GymId INT
AS
BEGIN
    SELECT id, username, password, cedula
    FROM users
    WHERE gym_id = @GymId;
END;
GO


CREATE PROCEDURE GetUserByUsername
    @Username NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT id, username, password, cedula, gym_id
    FROM users
    WHERE username = @Username;
END;
GO


CREATE PROCEDURE GetUserById
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT id, username, password, cedula, gym_id
    FROM users
    WHERE id = @UserID;
END;
GO


CREATE PROCEDURE UpdateUser
    @UserID INT,
    @Username NVARCHAR(255),
    @Password NVARCHAR(255),
    @Cedula VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE users
    SET username = @Username,
        password = @Password,
        cedula = @Cedula
    WHERE id = @UserID;
END;
GO


CREATE PROCEDURE DeleteUser
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM users
    WHERE id = @UserID;
END;
GO


_________________________________________________________________________________________________________________________________________________________________________


CREATE TABLE classes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    schedule DATETIME NOT NULL,
    capacity INT NOT NULL,
    current_participants INT DEFAULT 0,
    gym_id INT NOT NULL
);


CREATE TRIGGER TR_DeleteClassesOnGymDelete
ON gyms
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM classes
    WHERE gym_id IN (SELECT id FROM DELETED);
END;
GO


CREATE PROCEDURE SaveClass
    @Name NVARCHAR(255),
    @Schedule DATETIME,
    @Capacity INT,
    @CurrentParticipants INT = 0, -- Valor predeterminado de 0
    @GymID INT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO classes (name, schedule, capacity, current_participants, gym_id)
    VALUES (@Name, @Schedule, @Capacity, @CurrentParticipants, @GymID);

    SELECT SCOPE_IDENTITY() AS class_id;
END;
GO



CREATE PROCEDURE GetAllClasses
    @GymID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Seleccionar todas las clases asociadas a un gimnasio
    SELECT id, name, schedule, capacity, current_participants
    FROM classes
    WHERE gym_id = @GymID;
END;
GO


CREATE PROCEDURE GetClassById
    @ID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Seleccionar una clase por su ID
    SELECT id, name, schedule, capacity, current_participants, gym_id
    FROM classes
    WHERE id = @ID;
END;
GO


CREATE PROCEDURE UpdateClass
    @ID INT,
    @Name NVARCHAR(255),
    @Schedule DATETIME,
    @Capacity INT,
    @CurrentParticipants INT=0
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE classes
    SET 
        name = @Name,
        schedule = @Schedule,
        capacity = @Capacity,
        current_participants = @CurrentParticipants
    WHERE id = @ID;
END;
GO


CREATE PROCEDURE DeleteClass
    @ID INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM classes
    WHERE id = @ID;
END;
GO



_____________________________________________________________________________________________________________________________________________________________________



CREATE TABLE class_enrollments (
    id INT PRIMARY KEY IDENTITY(1,1),
    class_id INT NOT NULL,
    user_id INT NOT NULL,
    enrollment_date DATETIME DEFAULT GETDATE()
);


CREATE TRIGGER TR_DeleteEnrollmentsOnClassDelete
ON classes
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM class_enrollments
    WHERE class_id IN (SELECT id FROM DELETED);
END;
GO


CREATE TRIGGER TR_DeleteEnrollmentsOnUserDelete
ON users
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM class_enrollments
    WHERE user_id IN (SELECT id FROM DELETED);
END;
GO



CREATE TRIGGER trg_HandleClassEnrollment
ON class_enrollments
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Prevenir inscripciones duplicadas
    IF EXISTS (
        SELECT 1
        FROM class_enrollments ce
        INNER JOIN inserted i ON ce.user_id = i.user_id AND ce.class_id = i.class_id
    )
    BEGIN
        RAISERROR('El usuario ya está inscrito en esta clase.', 16, 1);
        RETURN;
    END

    -- Prevenir inscripción si la clase está llena
    IF EXISTS (
        SELECT 1
        FROM classes c
        INNER JOIN inserted i ON c.id = i.class_id
        WHERE c.capacity <= c.current_participants
    )
    BEGIN
        RAISERROR('La clase está llena. No se pueden inscribir más participantes.', 16, 1);
        RETURN;
    END

    -- Insertar la inscripción
    INSERT INTO class_enrollments (user_id, class_id, enrollment_date)
    SELECT user_id, class_id, enrollment_date
    FROM inserted;

    -- Incrementar el número de participantes actuales en la clase
    UPDATE classes
    SET current_participants = current_participants + 1
    WHERE id IN (SELECT class_id FROM inserted);
END;
GO


CREATE TRIGGER trg_HandleClassDelete
ON classes
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Aumentar el número de participantes restantes en las clases eliminadas
    UPDATE classes
    SET current_participants = current_participants + (
        SELECT COUNT(*)
        FROM class_enrollments
        WHERE class_enrollments.class_id = classes.id
    )
    WHERE id IN (SELECT id FROM DELETED);

    -- Eliminar inscripciones asociadas a las clases eliminadas
    DELETE FROM class_enrollments
    WHERE class_id IN (SELECT id FROM DELETED);
END;
GO

CREATE TRIGGER trg_UpdateParticipantsOnDelete
ON class_enrollments
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Actualizar el número de participantes actuales de la clase al eliminar una inscripción
    UPDATE classes
    SET current_participants = current_participants - 1
    FROM classes
    INNER JOIN deleted AS d ON classes.id = d.class_id;
END;



CREATE PROCEDURE GetClassesByDateNotEnrolled
    @Date DATE,
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT c.id, c.name, c.schedule, c.capacity, c.current_participants
    FROM classes c
    LEFT JOIN class_enrollments ce ON c.id = ce.class_id AND ce.user_id = @UserID
    WHERE 
        CAST(c.schedule AS DATE) = @Date
        AND ce.user_id IS NULL -- Excluir las clases en las que ya está inscrito
        AND c.gym_id = (SELECT gym_id FROM users WHERE id = @UserID); -- Asegurar que el gimnasio coincida
END;
GO



CREATE PROCEDURE EnrollUserToClass
    @UserId INT,
    @ClassId INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Verificar si el usuario ya está inscrito en la clase
    IF EXISTS (SELECT 1 FROM class_enrollments WHERE user_id = @UserId AND class_id = @ClassId)
    BEGIN
        THROW 50000, 'El usuario ya está inscrito en esta clase.', 1;
    END

    -- Verificar si hay espacio disponible en la clase
    IF NOT EXISTS (SELECT 1 FROM classes WHERE id = @ClassId AND capacity > current_participants)
    BEGIN
        THROW 50000, 'La clase está llena.', 1;
    END

    -- Insertar la inscripción
    INSERT INTO class_enrollments (user_id, class_id) VALUES (@UserId, @ClassId);
END;
GO



CREATE PROCEDURE GetClassesEnrolledByUser
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        c.id AS class_id,
        c.name AS class_name,
        c.schedule,
        c.capacity,
        c.current_participants
    FROM 
        class_enrollments ce
    INNER JOIN 
        classes c ON ce.class_id = c.id
    WHERE 
        ce.user_id = @UserID;
END;
GO


CREATE PROCEDURE DeleteEnrollment
    @UserID INT,
    @ClassID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Verificar si existe la inscripción antes de intentar eliminarla
    IF EXISTS (
        SELECT 1 FROM class_enrollments
        WHERE user_id = @UserID AND class_id = @ClassID
    )
    BEGIN
        DELETE FROM class_enrollments
        WHERE user_id = @UserID AND class_id = @ClassID;
    END
END;
GO
```

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
